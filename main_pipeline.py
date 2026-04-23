import sys
import os
import random
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
    print("  XỬ LÝ DỮ LIỆU ĐƠN HÀNG (PIPELINE)")
    print("="*60)
    
    # Load 1 batch data từ file CSV (Dữ liệu đầu vào)
    print("\n[*] Nạp dữ liệu 1 Batch (15 đơn hàng, 5 Shipper)...")
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'uds-orders-aug2024.csv')
    loader = OrderDataLoader(data_path)
    all_orders, all_shippers = loader.load_data_for_csp()
    
    batch_orders = all_orders[:15]
    batch_shippers = all_shippers[:5]
    
    processed_orders = []
    
    for order in batch_orders:
        print(f"\n--- Xử lý đơn hàng: {order['id']} ---")
        
        # 1. PHẦN A (Search): Lấy distance và suy ra Road_Type (giả lập A*)
        distance_km = order['weight'] * 1.5  # mock distance based on weight for variety
        # Nếu quãng đường > 5km thì thường đi đường chính, ngược lại đi đường hẻm
        road_type = "Main" if distance_km > 5.0 else "Alley"
        print(f"  [Phần A] Quãng đường: {distance_km:.2f}km -> Lộ trình: {road_type}")
        
        # Lấy giờ tạo đơn (Mock giờ từ 7h-20h)
        time_hour = random.randint(7, 20)
        time_slot = get_time_slot_from_hour(time_hour)
        day_of_week = random.randint(0, 6)
        is_rush_hour = time_hour in [7, 8, 9, 17, 18, 19]
        
        # 2. PHẦN D (Bayes): Dự đoán giao thông
        bayes_result = bayes_model.infer_traffic_level(time_slot, road_type)
        traffic_level = bayes_result['prediction']
        traffic_penalty = bayes_result['penalty']
        print(f"  [Phần D] Giờ: {time_hour}h ({time_slot}) -> Bayes dự đoán giao thông: {traffic_level.upper()} (Phạt x{traffic_penalty})")
        
        # 3. PHẦN E (ML): Dự đoán tốc độ giao (Fast/Slow)
        if ml_model:
            traffic_map = {'low': 0, 'medium': 1, 'high': 2}
            priority_map = {'low': 0, 'normal': 1, 'urgent': 2}
            
            ml_features = {
                'distance_km': distance_km,
                'time_hour': time_hour,
                'day_of_week': day_of_week,
                'traffic_level': traffic_map.get(traffic_level.lower(), 1),
                'order_priority': 1, # normal
                'is_weekend': 1 if day_of_week in [5, 6] else 0,
                'is_rush_hour': int(is_rush_hour)
            }
            eta_pred = predict_eta(ml_model, ml_features)
            print(f"  [Phần E] ML Decision Tree dự đoán: Đơn hàng giao {eta_pred.upper()}")
            
        # 4. PHẦN C (Rules): Tính phụ phí và giới hạn thời gian
        # Tạo Order ảo cho Rule
        weather_mock = random.choice(["clear", "rain"])
        is_vip = random.choice([True, False, False])
        dist_cat = "long" if distance_km > 10 else "medium" if distance_km > 5 else "short"
        
        rule_order = RuleOrder(
            order_id=order['id'],
            order_type="electronic" if order['weight'] > 5 else "food",
            is_vip=is_vip,
            distance_category=dist_cat,
            customer_location="residential",
            order_weight=order['weight'],
            delivery_time_requested="express" if eta_pred == "slow" else "normal",
            is_rush_hour=is_rush_hour,
            weather=weather_mock
        )
        rule_result = rule_order.apply_rules()
        print(f"  [Phần C] Rule IF-THEN: Phụ phí {rule_result['estimated_surcharge']}đ | Độ ưu tiên: {rule_result['priority_level'].upper()} | Limit: {rule_result['delivery_time_limit']}p")
        
        # Cập nhật order chuẩn bị cho CSP
        # Nhân thời gian thực tế với penalty từ Bayes
        original_time = order['real_time']
        adjusted_time = original_time * traffic_penalty
        
        order['real_time'] = adjusted_time
        processed_orders.append(order)
        
    # 5. PHẦN B (CSP): Phân công tối ưu
    print("\n" + "="*60)
    print("  PHẦN B: CSP PHÂN CÔNG ĐƠN HÀNG")
    print("="*60)
    print("[*] Đang giải bài toán CSP (Backtracking + Branch & Bound)...")
    csp_solver = DeliveryCSP(processed_orders, batch_shippers)
    solution = csp_solver.solve()
    
    if solution:
        print("\n=> TÌM THẤY LỊCH PHÂN CÔNG TỐI ƯU:\n")
        csp_solver.print_solution(solution)
    else:
        print("\n=> KHÔNG THỂ PHÂN CÔNG (Vượt quá ràng buộc W_max/T_max).")

if __name__ == "__main__":
    # Để terminal in đẹp hơn với UTF-8 (dành cho Windows)
    sys.stdout.reconfigure(encoding='utf-8')
    run_pipeline()
