import sys
import os
import random
import contextlib
import io
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ----------------- Import 5 Modules -----------------
# Phần B: CSP
from modules.csp_solver import DeliveryCSP
from data.order_data import OrderDataLoader
# Phần D: Bayes
from modules.traffic_ai import get_trained_bayes, get_time_slot_from_hour
# Phần E: Machine Learning
from modules.ml import load_ml_data_from_uds, prepare_data, train_and_evaluate, predict_eta
# Phần C: Rules
from modules.rules import Order as RuleOrder

def init_system():
    print("\n" + "="*60)
    print("  KHỞI TẠO HỆ THỐNG AI DELIVERY (A -> D -> E -> C -> B)")
    print("="*60)
    
    # 1. Khởi tạo Bayes (Phần D)
    print("\n[*] Đang nạp Tri thức Mạng Bayes (Phần D)...")
    bayes_model = get_trained_bayes()
    print("    -> Sẵn sàng dự đoán giao thông.")

    # 2. Khởi tạo ML (Phần E)
    print("\n[*] Đang huấn luyện Mô hình Decision Tree (Phần E)...")
    ml_orders = load_ml_data_from_uds()
    X, y = prepare_data(ml_orders)
    if X is not None:
        ml_model = train_and_evaluate(X, y)
        print("    -> Huấn luyện xong. Sẵn sàng dự đoán ETA.")
    else:
        ml_model = None
        print("    -> [LỖI] Thiếu thư viện ML.")

    return bayes_model, ml_model

def run_pipeline():
    bayes_model, ml_model = init_system()
    
    print("\n" + "="*60)
    print("  XỬ LÝ DỮ LIỆU ĐƠN HÀNG (FULL DATA - BATCH PROCESSING)")
    print("="*60)
    
    # Load data từ file CSV
    print("\n[*] Nạp toàn bộ dữ liệu đơn hàng...")
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'uds-orders-aug2024.csv')
    loader = OrderDataLoader(data_path)
    all_orders, all_shippers = loader.load_data_for_csp()
    
    BATCH_SIZE = 20
    NUM_SHIPPERS_PER_BATCH = 5
    
    total_orders_processed = 0
    total_system_cost = 0.0
    successful_batches = 0
    failed_batches = 0
    
    # Chia danh sách đơn hàng thành các chunks
    chunks = [all_orders[i:i + BATCH_SIZE] for i in range(0, len(all_orders), BATCH_SIZE)]
    
    print(f"\n[*] Đã chia {len(all_orders)} đơn hàng thành {len(chunks)} lô (batches).")
    print("[*] Bắt đầu xử lý luồng A -> D -> E -> C -> B cho từng lô...\n")
    
    for batch_idx, batch_orders in enumerate(chunks):
        # Lấy shipper cho lô này (quay vòng danh sách shipper)
        start_shipper_idx = (batch_idx * NUM_SHIPPERS_PER_BATCH) % max(1, len(all_shippers) - NUM_SHIPPERS_PER_BATCH)
        batch_shippers = all_shippers[start_shipper_idx:start_shipper_idx + NUM_SHIPPERS_PER_BATCH]
        
        processed_orders = []
        
        for order in batch_orders:
            # 1. PHẦN A (Search): Lấy distance và suy ra Road_Type
            distance_km = order['weight'] * 1.5
            road_type = "Main" if distance_km > 5.0 else "Alley"
            
            time_hour = random.randint(7, 20)
            time_slot = get_time_slot_from_hour(time_hour)
            day_of_week = random.randint(0, 6)
            is_rush_hour = time_hour in [7, 8, 9, 17, 18, 19]
            
            # 2. PHẦN D (Bayes): Dự đoán giao thông
            bayes_result = bayes_model.infer_traffic_level(time_slot, road_type)
            traffic_level = bayes_result['prediction']
            traffic_penalty = bayes_result['penalty']
            
            # 3. PHẦN E (ML): Dự đoán tốc độ giao
            eta_pred = "normal"
            if ml_model:
                traffic_map = {'low': 0, 'medium': 1, 'high': 2}
                ml_features = {
                    'distance_km': distance_km,
                    'time_hour': time_hour,
                    'day_of_week': day_of_week,
                    'traffic_level': traffic_map.get(traffic_level.lower(), 1),
                    'order_priority': 1,
                    'is_weekend': 1 if day_of_week in [5, 6] else 0,
                    'is_rush_hour': int(is_rush_hour)
                }
                eta_pred = predict_eta(ml_model, ml_features)
                
            # 4. PHẦN C (Rules): Tính phụ phí và giới hạn thời gian
            weather_mock = random.choice(["clear", "rain"])
            dist_cat = "long" if distance_km > 10 else "medium" if distance_km > 5 else "short"
            
            rule_order = RuleOrder(
                order_id=order['id'],
                order_type="electronic" if order['weight'] > 5 else "food",
                is_vip=False,
                distance_category=dist_cat,
                customer_location="residential",
                order_weight=order['weight'],
                delivery_time_requested="express" if eta_pred == "slow" else "normal",
                is_rush_hour=is_rush_hour,
                weather=weather_mock
            )
            rule_result = rule_order.apply_rules()
            
            # Nhân thời gian thực tế với penalty từ Bayes
            order['real_time'] = order['real_time'] * traffic_penalty
            processed_orders.append(order)
            
        # 5. PHẦN B (CSP): Phân công tối ưu cho Batch hiện tại
        # Ẩn output chi tiết của CSPSolver bằng cách ghi đè sys.stdout tạm thời không khả thi, ta chấp nhận in ra hoặc CSP im lặng
        # Ở đây ta sẽ chỉ in report cho batch.
        csp_solver = DeliveryCSP(processed_orders, batch_shippers)
        
        # Ngăn in màn hình chi tiết bên trong csp_solver bằng cách chuyển output
        # (Để đơn giản ta không sửa mã bên trong csp_solver, chỉ in tóm tắt ở main)
        # Tuy nhiên csp_solver.solve() in ra bảng. Thay vì sửa CSP, ta xem kết quả.
        fnull = io.StringIO()
        with contextlib.redirect_stdout(fnull):
            solution = csp_solver.solve()
        
        batch_num = batch_idx + 1
        if solution:
            # Tính tổng cost của batch
            batch_cost = solution['cost']
            print(f"[Batch {batch_num}/{len(chunks)}] ✅ Đã phân công {len(batch_orders)} đơn cho {len(batch_shippers)} Shipper | Chi phí: {batch_cost:.1f} phút")
            total_system_cost += batch_cost
            successful_batches += 1
            total_orders_processed += len(batch_orders)
        else:
            print(f"[Batch {batch_num}/{len(chunks)}] ❌ Vượt quá W_max/T_max. Cần chia nhỏ hơn hoặc thêm Shipper.")
            failed_batches += 1

    print("\n" + "="*60)
    print("  BÁO CÁO TỔNG KẾT TOÀN CHIẾN DỊCH (FULL DATA)")
    print("="*60)
    print(f"  - Tổng số Batch đã chạy   : {len(chunks)}")
    print(f"  - Số Batch thành công     : {successful_batches}")
    print(f"  - Số Batch thất bại       : {failed_batches}")
    print(f"  - Tổng đơn hàng xử lý     : {total_orders_processed} đơn")
    print(f"  - TỔNG CHI PHÍ THỜI GIAN  : {total_system_cost:.1f} phút")
    print("============================================================")

if __name__ == "__main__":
    # Để terminal in đẹp hơn với UTF-8 (dành cho Windows)
    sys.stdout.reconfigure(encoding='utf-8')
    run_pipeline()
