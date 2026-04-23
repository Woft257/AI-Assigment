"""
CSP Solver - Phần B
Phân công đơn hàng cho shipper bằng Backtracking + Branch & Bound
Không sử dụng thư viện ngoài - chỉ dùng Python standard library
"""

import os
import sys
import time

# ============================================
# CLASS CHÍNH: DeliveryCSP
# ============================================
class DeliveryCSP:
    def __init__(self, orders, shippers):
        """
        Khởi tạo bài toán CSP cho hệ thống giao hàng.

        Mô hình:
            - Variables: assignment[i] = j  (đơn hàng i gán cho shipper j)
            - Domain: mỗi đơn hàng có thể được gán cho bất kỳ shipper nào
            - Ma trận nhị phân X[i][j] ∈ {0, 1}

        Args:
            orders: List[Dict] - Danh sách đơn hàng, mỗi dict có:
                    {'id', 'weight' (kg), 'real_time' (phút)}
            shippers: List[Dict] - Danh sách shipper, mỗi dict có:
                    {'id', 'max_weight' (kg), 'max_time' (phút)}
        """
        self.orders = orders
        self.shippers = shippers
        self.N = len(orders)    # Số đơn hàng
        self.M = len(shippers)  # Số shipper

        # ĐỊNH NGHĨA VARIABLES (Biến quyết định)
        # assignment[i] = j nghĩa là đơn hàng i được gán cho shipper j
        # -1 = chưa gán
        self.assignment = [-1] * self.N

        # Theo dõi tải hiện tại của mỗi shipper (tăng dần khi gán)
        self.current_weight = [0.0] * self.M  # Tổng weight mỗi shipper
        self.current_time = [0.0] * self.M    # Tổng time mỗi shipper

        # Branch & Bound: lưu nghiệm tốt nhất
        self.best_assignment = None
        self.best_cost = float('inf')

        # Thống kê
        self.nodes_explored = 0

    # ============================================
    # ĐỊNH NGHĨA CONSTRAINTS (Các ràng buộc)
    # ============================================
    def check_weight_constraint(self, shipper_idx, new_weight):
        """
        Ràng buộc: Tổng khối lượng không vượt quá sức chứa của xe
        Σ w_i * X[i][j] <= W_max cho mỗi shipper j
        """
        return self.current_weight[shipper_idx] + new_weight <= self.shippers[shipper_idx]['max_weight']

    def check_time_constraint(self, shipper_idx, new_time):
        """
        Ràng buộc: Tổng thời gian không vượt quá ca làm việc
        Σ t_i * X[i][j] <= T_max cho mỗi shipper j
        """
        return self.current_time[shipper_idx] + new_time <= self.shippers[shipper_idx]['max_time']

    def is_consistent(self, order_idx, shipper_idx):
        """
        Kiểm tra tất cả ràng buộc khi gán đơn hàng order_idx cho shipper shipper_idx.

        Ràng buộc 1 (N<=50, M<=10): đã đảm bảo qua batching trước khi gọi solve()
        Ràng buộc 2 (mỗi đơn chỉ 1 shipper): đảm bảo bởi cấu trúc assignment[i] = j
        Ràng buộc 3: Tổng weight <= W_max
        Ràng buộc 4: Tổng time <= T_max
        """
        order = self.orders[order_idx]
        w = order['weight']
        t = order['real_time']

        # Ràng buộc 3: trọng lượng
        if not self.check_weight_constraint(shipper_idx, w):
            return False

        # Ràng buộc 4: thời gian
        if not self.check_time_constraint(shipper_idx, t):
            return False

        return True

    # ============================================
    # HÀM MỤC TIÊU
    # ============================================
    def get_total_cost(self):
        """
        Hàm mục tiêu: Cực tiểu hoá tổng chi phí thời gian vận hành
        Cost = Σ_j (Σ_i X[i][j] * t_i)
        Tức là tổng thời gian của tất cả shipper.
        """
        return sum(self.current_time)

    def get_lower_bound(self, next_order_idx):
        """
        Tính lower bound cho Branch & Bound.
        Chi phí hiện tại + chi phí tối thiểu của các đơn chưa gán
        (ước lượng: mỗi đơn chưa gán ít nhất tốn thời gian t_i của nó)
        """
        current_cost = self.get_total_cost()

        # Đơn chưa gán: thời gian tối thiểu vẫn phải tốn
        remaining_time = sum(
            self.orders[i]['real_time']
            for i in range(next_order_idx, self.N)
        )

        return current_cost + remaining_time

    # ============================================
    # HEURISTICS
    # ============================================
    def get_ordered_shippers(self, order_idx):
        """
        LCV (Least Constraining Value): Sắp xếp shipper theo capacity còn lại
        giảm dần → thử shipper còn nhiều chỗ nhất trước.
        Giúp tăng khả năng tìm nghiệm khả thi nhanh hơn.
        """
        order = self.orders[order_idx]
        w = order['weight']
        t = order['real_time']

        shipper_scores = []
        for j in range(self.M):
            if self.is_consistent(order_idx, j):
                # Score = capacity còn lại (càng nhiều càng tốt)
                remaining_weight = self.shippers[j]['max_weight'] - self.current_weight[j] - w
                remaining_time = self.shippers[j]['max_time'] - self.current_time[j] - t
                score = remaining_weight + remaining_time
                shipper_scores.append((j, score))

        # Sắp xếp giảm dần theo score (shipper rộng rãi nhất trước)
        shipper_scores.sort(key=lambda x: x[1], reverse=True)
        return [j for j, _ in shipper_scores]

    def select_next_order(self, unassigned):
        """
        MRV (Minimum Remaining Values): Chọn đơn hàng có ít shipper khả dụng nhất.
        Giúp phát hiện dead-end sớm → pruning hiệu quả hơn.
        """
        best_order = None
        min_options = float('inf')

        for order_idx in unassigned:
            # Đếm số shipper khả dụng cho đơn này
            count = sum(
                1 for j in range(self.M) 
                if self.is_consistent(order_idx, j)
            )
            if count < min_options:
                min_options = count
                best_order = order_idx

        return best_order, min_options

    # ============================================
    # THUẬT TOÁN BACKTRACKING + BRANCH & BOUND
    # ============================================
    def _backtrack(self, unassigned):
        """
        Thuật toán Backtracking đệ quy với Branch & Bound.

        Quy trình:
        1. Chọn đơn hàng tiếp theo (MRV heuristic)
        2. Thử gán cho từng shipper (LCV heuristic)
        3. Kiểm tra ràng buộc (is_consistent)
        4. Kiểm tra Branch & Bound (lower_bound < best_cost?)
        5. Đệ quy hoặc Backtrack
        """
        self.nodes_explored += 1
        
        # Thêm giới hạn số nodes để tránh treo máy trên các batch quá khó/vô nghiệm
        if self.nodes_explored > 10000:
            return

        # Base case: tất cả đơn đã được gán
        if not unassigned:
            cost = self.get_total_cost()
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_assignment = self.assignment[:]
            return

        # MRV: chọn đơn có ít lựa chọn nhất
        order_idx, num_options = self.select_next_order(unassigned)

        # Nếu không có shipper nào khả dụng → dead-end
        if num_options == 0:
            return

        # Tạo danh sách unassigned mới (bỏ order đang xét)
        remaining = [i for i in unassigned if i != order_idx]
        order = self.orders[order_idx]

        # LCV: thử các shipper theo thứ tự capacity giảm dần
        for shipper_idx in self.get_ordered_shippers(order_idx):
            # Branch & Bound: kiểm tra lower bound
            # Nếu chi phí tối thiểu có thể đạt đã >= best_cost → prune
            if self.get_lower_bound(0) >= self.best_cost and self.best_assignment is not None:
                break

            # GÁN: đơn hàng order_idx cho shipper shipper_idx
            self.assignment[order_idx] = shipper_idx
            self.current_weight[shipper_idx] += order['weight']
            self.current_time[shipper_idx] += order['real_time']

            # Đệ quy
            self._backtrack(remaining)

            # HỦY GÁN (Backtrack)
            self.assignment[order_idx] = -1
            self.current_weight[shipper_idx] -= order['weight']
            self.current_time[shipper_idx] -= order['real_time']

    def solve(self):
        """
        Entry point: Giải bài toán CSP.

        Returns:
            Dict hoặc None:
                {
                    'assignment': {order_id: shipper_id},
                    'cost': float (tổng thời gian),
                    'shipper_loads': {shipper_id: {'weight': .., 'time': .., 'orders': [..]}},
                    'nodes_explored': int
                }
        """
        print(f"\n{'='*50}")
        print(f"  CSP SOLVER - Backtracking + Branch & Bound")
        print(f"{'='*50}")
        print(f"  Số đơn hàng (N): {self.N}")
        print(f"  Số shipper  (M): {self.M}")
        print(f"{'='*50}")

        # Reset
        self.assignment = [-1] * self.N
        self.current_weight = [0.0] * self.M
        self.current_time = [0.0] * self.M
        self.best_assignment = None
        self.best_cost = float('inf')
        self.nodes_explored = 0

        # Danh sách index các đơn hàng chưa gán
        unassigned = list(range(self.N))

        start_time = time.time()
        self._backtrack(unassigned)
        elapsed = time.time() - start_time

        if self.best_assignment is None:
            print("\n  [FAIL] Không tìm thấy nghiệm khả thi!")
            print(f"  Nodes explored: {self.nodes_explored}")
            print(f"  Thời gian chạy: {elapsed:.3f}s")
            return None

        print(f"\n  [OK] Tìm thấy nghiệm tối ưu!")
        print(f"  Tổng chi phí (tổng thời gian): {self.best_cost:.2f} phút")
        print(f"  Nodes explored: {self.nodes_explored}")
        print(f"  Thời gian chạy: {elapsed:.3f}s")

        # Xây dựng kết quả chi tiết
        result = self._build_result()
        return result

    def _build_result(self):
        """Xây dựng dict kết quả từ best_assignment."""
        assignment_map = {}
        shipper_loads = {}

        # Khởi tạo shipper_loads
        for j in range(self.M):
            sid = self.shippers[j]['id']
            shipper_loads[sid] = {
                'weight': 0.0,
                'time': 0.0,
                'max_weight': self.shippers[j]['max_weight'],
                'max_time': self.shippers[j]['max_time'],
                'orders': []
            }

        # Điền dữ liệu
        for i in range(self.N):
            j = self.best_assignment[i]
            oid = self.orders[i]['id']
            sid = self.shippers[j]['id']

            assignment_map[oid] = sid
            shipper_loads[sid]['weight'] += self.orders[i]['weight']
            shipper_loads[sid]['time'] += self.orders[i]['real_time']
            shipper_loads[sid]['orders'].append(self.orders[i])

        return {
            'assignment': assignment_map,
            'cost': self.best_cost,
            'shipper_loads': shipper_loads,
            'nodes_explored': self.nodes_explored
        }

    # ============================================
    # IN KẾT QUẢ
    # ============================================
    def print_solution(self, result):
        """In lịch phân công chi tiết."""
        if result is None:
            print("Không có nghiệm để in.")
            return

        print(f"\n{'='*60}")
        print(f"  KẾT QUẢ PHÂN CÔNG ĐƠN HÀNG")
        print(f"{'='*60}")

        shipper_loads = result['shipper_loads']

        for sid, info in shipper_loads.items():
            num_orders = len(info['orders'])
            if num_orders == 0:
                continue

            w_pct = (info['weight'] / info['max_weight']) * 100 if info['max_weight'] > 0 else 0
            t_pct = (info['time'] / info['max_time']) * 100 if info['max_time'] > 0 else 0

            # Rút gọn shipper ID cho dễ đọc
            display_id = sid[:12] + "..." if len(sid) > 15 else sid

            print(f"\n  Shipper [{display_id}]: {num_orders} đơn")
            print(f"    Trọng lượng: {info['weight']:.1f} / {info['max_weight']:.0f} kg ({w_pct:.0f}%)")
            print(f"    Thời gian:   {info['time']:.1f} / {info['max_time']:.0f} phút ({t_pct:.0f}%)")
            print(f"    Đơn hàng:")

            for order in info['orders']:
                print(f"      - {order['id']} ({order['weight']:.1f}kg, {order['real_time']:.1f} phút)")

        print(f"\n{'='*60}")
        print(f"  TỔNG CHI PHÍ: {result['cost']:.2f} phút")
        print(f"  Nodes explored: {result['nodes_explored']}")
        print(f"{'='*60}\n")


# ============================================
# BATCHING: CHIA ĐỂ TRỊ
# ============================================
def solve_all_batches(orders, shippers, batch_size=20, max_shippers=5):
    """
    Chia N đơn hàng thành các batch nhỏ rồi giải từng batch.

    Kiến trúc Chia để trị (theo idea.md):
    - Mỗi batch (zone) có N <= 50 đơn, M <= 10 shipper
    - CSP giải từng batch độc lập
    - Kết quả được gộp lại

    Args:
        orders: List[Dict] - Tất cả đơn hàng
        shippers: List[Dict] - Tất cả shipper
        batch_size: int - Số đơn hàng mỗi batch (default: 20)
        max_shippers: int - Số shipper mỗi batch (default: 5)

    Returns:
        List[Dict] - Kết quả từng batch
    """
    print(f"\n{'#'*60}")
    print(f"  BATCHING: {len(orders)} đơn / {len(shippers)} shipper")
    print(f"  Batch size: {batch_size} đơn, {max_shippers} shipper/batch")
    print(f"{'#'*60}")

    # Giới hạn theo ràng buộc C1: N <= 50, M <= 10
    batch_size = min(batch_size, 50)
    max_shippers = min(max_shippers, 10)

    # Chia đơn hàng thành các batch
    batches = []
    for i in range(0, len(orders), batch_size):
        batches.append(orders[i:i + batch_size])

    total_batches = len(batches)
    print(f"  Tổng số batch: {total_batches}")

    all_results = []
    total_cost = 0.0
    total_assigned = 0

    # Phân bổ shipper cho các batch (round-robin)
    for batch_idx, batch_orders in enumerate(batches):
        print(f"\n--- Batch {batch_idx + 1}/{total_batches} ({len(batch_orders)} đơn) ---")

        # Chọn shipper cho batch này (round-robin để phân bổ đều)
        start_shipper = (batch_idx * max_shippers) % len(shippers)
        batch_shippers = []
        for k in range(max_shippers):
            idx = (start_shipper + k) % len(shippers)
            # Deep copy shipper để tránh ảnh hưởng giữa các batch
            batch_shippers.append(dict(shippers[idx]))

        # Giải CSP cho batch này
        csp = DeliveryCSP(batch_orders, batch_shippers)
        result = csp.solve()

        if result:
            csp.print_solution(result)
            all_results.append(result)
            total_cost += result['cost']
            total_assigned += len(result['assignment'])
        else:
            print(f"  [WARNING] Batch {batch_idx + 1} không tìm được nghiệm!")
            all_results.append(None)

    # Tổng kết
    print(f"\n{'#'*60}")
    print(f"  TỔNG KẾT BATCHING")
    print(f"{'#'*60}")
    print(f"  Tổng đơn đã phân công: {total_assigned}/{len(orders)}")
    print(f"  Tổng chi phí:          {total_cost:.2f} phút")
    successful = sum(1 for r in all_results if r is not None)
    print(f"  Batch thành công:      {successful}/{total_batches}")
    print(f"{'#'*60}\n")

    return all_results


# ============================================
# DEMO / TEST
# ============================================
if __name__ == "__main__":
    # Thêm path để import data
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from data.order_data import OrderDataLoader

    print("=" * 60)
    print("  DEMO: CSP SOLVER")
    print("=" * 60)

    # --- Test 1: Bài toán nhỏ (tự tạo) ---
    print("\n\n>>> TEST 1: Bài toán nhỏ (5 đơn, 2 shipper)")
    test_orders = [
        {'id': 'ORD001', 'weight': 5.0, 'real_time': 30.0},
        {'id': 'ORD002', 'weight': 8.0, 'real_time': 45.0},
        {'id': 'ORD003', 'weight': 3.0, 'real_time': 20.0},
        {'id': 'ORD004', 'weight': 12.0, 'real_time': 60.0},
        {'id': 'ORD005', 'weight': 6.0, 'real_time': 35.0},
    ]
    test_shippers = [
        {'id': 'SHIPPER_A', 'max_weight': 20.0, 'max_time': 120.0},
        {'id': 'SHIPPER_B', 'max_weight': 25.0, 'max_time': 150.0},
    ]

    csp = DeliveryCSP(test_orders, test_shippers)
    result = csp.solve()
    if result:
        csp.print_solution(result)

        # Verify constraints
        print("  [VERIFY] Kiểm tra ràng buộc:")
        for sid, info in result['shipper_loads'].items():
            w_ok = info['weight'] <= info['max_weight']
            t_ok = info['time'] <= info['max_time']
            print(f"    {sid}: weight {'OK' if w_ok else 'FAIL'}, time {'OK' if t_ok else 'FAIL'}")

    # --- Test 2: Data thật từ Xe dù (1 batch) ---
    print("\n\n>>> TEST 2: Data thật từ Xe dù (1 batch = 20 đơn)")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'uds-orders-aug2024.csv')

    if os.path.exists(data_path):
        loader = OrderDataLoader(data_path)
        all_orders, all_shippers = loader.load_data_for_csp()

        if all_orders and all_shippers:
            batch_orders = all_orders[:20]
            batch_shippers = all_shippers[:5]

            csp2 = DeliveryCSP(batch_orders, batch_shippers)
            result2 = csp2.solve()
            if result2:
                csp2.print_solution(result2)
    else:
        print(f"  [SKIP] Khong tim thay file data: {data_path}")

    # --- Test 3: Tich hop Bayes -> CSP ---
    print("\n\n>>> TEST 3: Tich hop Bayes -> CSP (he so phat giao thong)")
    from modules.traffic_ai import get_trained_bayes, apply_traffic_penalty, get_time_slot_from_hour

    train_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'train.csv')

    if os.path.exists(data_path) and os.path.exists(train_path):
        # Buoc 1: Train Bayes tu data giao thong
        bayes = get_trained_bayes(train_path)

        # Buoc 2: Suy luan traffic_level cho gio cao diem
        result_peak = bayes.infer_traffic_level("Peak", "Main")
        traffic_level = result_peak['prediction']
        penalty = result_peak['penalty']
        print(f"  Bayes suy luan: Traffic = {traffic_level} (penalty x{penalty})")

        # Buoc 3: Ap dung he so phat vao don hang
        loader = OrderDataLoader(data_path)
        all_orders, all_shippers = loader.load_data_for_csp()

        if all_orders and all_shippers:
            batch_orders = all_orders[:15]
            batch_shippers = all_shippers[:5]

            # Ap dung traffic penalty
            adjusted_orders = apply_traffic_penalty(batch_orders, traffic_level)

            print(f"  Vi du dieu chinh thoi gian:")
            for i in range(min(3, len(adjusted_orders))):
                orig = batch_orders[i]['real_time']
                adj = adjusted_orders[i]['real_time']
                print(f"    {adjusted_orders[i]['id']}: {orig:.1f}min -> {adj:.1f}min (x{penalty})")

            # Buoc 4: Giai CSP voi thoi gian da dieu chinh
            csp3 = DeliveryCSP(adjusted_orders, batch_shippers)
            result3 = csp3.solve()
            if result3:
                csp3.print_solution(result3)