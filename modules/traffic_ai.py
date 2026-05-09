"""
Bayesian Network - Phan D
Mang Bayes suy luan muc do ket xe (Traffic Level)
Su dung data that tu Traffic HCM (train.csv)
Khong dung thu vien ngoai - chi dung Python standard library
"""

import csv
import os
import sys

# ============================================
# HANG SO
# ============================================
TRAFFIC_LEVELS = ["Low", "Medium", "High"]
TIME_SLOTS = ["Peak", "Normal"]
ROAD_TYPES = ["Main", "Alley"]

# He so phat thoi gian theo muc giao thong (dung cho CSP)
TRAFFIC_PENALTY = {
    "Low": 1.0,     # Thong thoang - khong phat
    "Medium": 1.3,  # Binh thuong - tang 30%
    "High": 1.6     # Ket xe - tang 60%
}

# Gio cao diem
PEAK_HOURS = {7, 8, 12, 17, 18}


# ============================================
# CLASS CHINH: TrafficBayesNetwork
# ============================================
class TrafficBayesNetwork:
    """
    Mang Bayes don gian voi 3 bien:
        Time_Slot in {Peak, Normal}
        Road_Type in {Main, Alley}
        Traffic_Level in {Low, Medium, High}

    Cau truc DAG:
        Time_Slot -> Traffic_Level <- Road_Type

    Cong thuc:
        P(Traffic_Level | Time_Slot, Road_Type)
    """

    def __init__(self):
        # Cau truc mang
        self.nodes = ['Time_Slot', 'Road_Type', 'Traffic_Level']
        self.edges = [
            ('Time_Slot', 'Traffic_Level'),
            ('Road_Type', 'Traffic_Level')
        ]

        # Prior probabilities - P(Time_Slot), P(Road_Type)
        self.prior_time_slot = {}
        self.prior_road_type = {}

        # CPT: P(Traffic_Level | Time_Slot, Road_Type)
        # Key: (time_slot, road_type) -> {traffic_level: probability}
        self.cpt_traffic = {}

        # Trang thai
        self.trained = False
        self.total_samples = 0

    # ============================================
    # MAPPING FUNCTIONS: Data that -> Bien Bayes
    # ============================================
    @staticmethod
    def _map_period_to_time_slot(period):
        """
        Map period string tu train.csv sang Time_Slot.

        Peak hours: 7:00-9:00, 12:00-13:30, 17:00-19:00
        Cac khung gio con lai: Normal

        Args:
            period: str, vd "period_7_30", "period_17_00"
        Returns:
            "Peak" hoac "Normal"
        """
        try:
            parts = period.split('_')
            hour = int(parts[1])
            if hour in PEAK_HOURS:
                return "Peak"
            return "Normal"
        except (IndexError, ValueError):
            return "Normal"

    @staticmethod
    def _map_street_level_to_road_type(street_level):
        """
        Map street_level tu train.csv sang Road_Type.

        Level 1-2 (motorway, primary, trunk): Main
        Level 3-4 (secondary, tertiary, residential): Alley

        Args:
            street_level: str, vd "1", "2", "3", "4"
        Returns:
            "Main" hoac "Alley"
        """
        try:
            level = int(street_level)
            return "Main" if level <= 2 else "Alley"
        except (ValueError, TypeError):
            return "Alley"

    @staticmethod
    def _map_los_to_traffic_level(los):
        """
        Map LOS (Level of Service) tu train.csv sang Traffic_Level.

        A: Low (thong thoang)
        B, C: Medium (binh thuong)
        D, E, F: High (ket xe)

        Args:
            los: str, vd "A", "B", "C", "D", "E", "F"
        Returns:
            "Low", "Medium", hoac "High"
        """
        if los == 'A':
            return "Low"
        elif los in ('B', 'C'):
            return "Medium"
        else:
            return "High"

    # ============================================
    # HOC CPT TU DATA (TRAIN)
    # ============================================
    def train_probabilities(self, csv_path):
        """
        Hoc CPT (Conditional Probability Tables) tu du lieu thuc train.csv.

        Quy trinh:
        1. Doc tung dong train.csv
        2. Map cac cot sang 3 bien Bayes
        3. Dem tan suat (counting)
        4. Tinh xac suat co dieu kien voi Laplace smoothing

        Args:
            csv_path: Duong dan toi file train.csv
        """
        # Bo dem
        time_slot_counts = {ts: 0 for ts in TIME_SLOTS}
        road_type_counts = {rt: 0 for rt in ROAD_TYPES}
        joint_counts = {}       # (time_slot, road_type, traffic_level) -> count
        condition_counts = {}   # (time_slot, road_type) -> count
        total = 0

        # Doc va dem tu data
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = self._map_period_to_time_slot(row['period'])
                rt = self._map_street_level_to_road_type(row['street_level'])
                tl = self._map_los_to_traffic_level(row['LOS'])

                time_slot_counts[ts] += 1
                road_type_counts[rt] += 1

                joint_key = (ts, rt, tl)
                joint_counts[joint_key] = joint_counts.get(joint_key, 0) + 1

                cond_key = (ts, rt)
                condition_counts[cond_key] = condition_counts.get(cond_key, 0) + 1

                total += 1

        self.total_samples = total

        # Tinh Prior probabilities
        self.prior_time_slot = {k: v / total for k, v in time_slot_counts.items()}
        self.prior_road_type = {k: v / total for k, v in road_type_counts.items()}

        # Tinh CPT voi Laplace smoothing (cong 1 de tranh xac suat = 0)
        num_traffic_levels = len(TRAFFIC_LEVELS)

        for ts in TIME_SLOTS:
            for rt in ROAD_TYPES:
                cond_key = (ts, rt)
                cond_count = condition_counts.get(cond_key, 0)

                probs = {}
                for tl in TRAFFIC_LEVELS:
                    joint_key = (ts, rt, tl)
                    count = joint_counts.get(joint_key, 0) + 1  # Laplace +1
                    probs[tl] = count / (cond_count + num_traffic_levels)

                self.cpt_traffic[cond_key] = probs

        self.trained = True

    # ============================================
    # SUY LUAN (INFERENCE)
    # ============================================
    def infer_traffic_level(self, time_slot, road_type):
        """
        Suy luan MAP (Maximum A Posteriori) cho Traffic_Level.

        Cho evidence (Time_Slot, Road_Type), tra ve:
        - Traffic_Level co xac suat cao nhat
        - Phan phoi xac suat day du

        Cong thuc: P(Traffic_Level | Time_Slot, Road_Type)
        Truy van truc tiep tu CPT (Variable Elimination don gian hoa
        vi ca 2 parent deu da biet -> chi can tra bang).

        Args:
            time_slot: "Peak" hoac "Normal"
            road_type: "Main" hoac "Alley"

        Returns:
            dict: {
                'prediction': str,          # Traffic level co xac suat cao nhat
                'probabilities': dict,      # {Low: p, Medium: p, High: p}
                'penalty': float            # He so phat thoi gian
            }
        """
        if not self.trained:
            raise ValueError("Model chua duoc train! Goi train_probabilities() truoc.")

        cond_key = (time_slot, road_type)
        probs = self.cpt_traffic.get(cond_key)

        if probs is None:
            # Fallback neu khong co trong CPT
            default_probs = {tl: 1.0 / len(TRAFFIC_LEVELS) for tl in TRAFFIC_LEVELS}
            return {
                'prediction': 'Medium',
                'probabilities': default_probs,
                'penalty': TRAFFIC_PENALTY['Medium']
            }

        # MAP: chon traffic_level co xac suat cao nhat
        prediction = max(probs, key=probs.get)

        return {
            'prediction': prediction,
            'probabilities': probs,
            'penalty': TRAFFIC_PENALTY[prediction]
        }

    # ============================================
    # HIEN THI
    # ============================================
    def print_network_structure(self):
        """In cau truc mang Bayes."""
        print("\n--- Cau truc Mang Bayes ---")
        print(f"  Bien (Nodes): {self.nodes}")
        print(f"  Quan he (Edges):")
        for parent, child in self.edges:
            print(f"    {parent} -> {child}")
        print(f"  DAG: Time_Slot -> Traffic_Level <- Road_Type")

    def print_cpt(self):
        """In bang CPT (Conditional Probability Table) day du."""
        if not self.trained:
            print("  [!] Chua train. Goi train_probabilities() truoc.")
            return

        print(f"\n{'='*65}")
        print(f"  BANG XAC SUAT CO DIEU KIEN (CPT)")
        print(f"  P(Traffic_Level | Time_Slot, Road_Type)")
        print(f"  Hoc tu {self.total_samples:,} mau du lieu giao thong TP.HCM")
        print(f"{'='*65}")

        # Prior
        print(f"\n  Prior P(Time_Slot):")
        for ts, p in self.prior_time_slot.items():
            print(f"    P({ts}) = {p:.4f}")

        print(f"\n  Prior P(Road_Type):")
        for rt, p in self.prior_road_type.items():
            print(f"    P({rt}) = {p:.4f}")

        # CPT
        print(f"\n  {'Time_Slot':<12} {'Road_Type':<12} {'P(Low)':<10} {'P(Medium)':<12} {'P(High)':<10}")
        print(f"  {'-'*56}")

        for ts in TIME_SLOTS:
            for rt in ROAD_TYPES:
                probs = self.cpt_traffic.get((ts, rt), {})
                p_low = probs.get('Low', 0)
                p_med = probs.get('Medium', 0)
                p_high = probs.get('High', 0)
                print(f"  {ts:<12} {rt:<12} {p_low:<10.4f} {p_med:<12.4f} {p_high:<10.4f}")

        print(f"{'='*65}")


# ============================================
# HELPER FUNCTIONS (DUNG CHO TICH HOP)
# ============================================
def get_time_slot_from_hour(hour):
    """
    Map gio trong ngay (0-23) sang Time_Slot.
    Dung de tich hop voi CSP va ML.

    Args:
        hour: int (0-23)
    Returns:
        "Peak" hoac "Normal"
    """
    if hour in PEAK_HOURS:
        return "Peak"
    return "Normal"


def get_road_type_from_path(path, graph):
    """
    Phan tich duong di tu A* de xac dinh Road_Type chu dao.

    Dem so canh thuoc duong chinh (Main) va hem (Alley).
    Neu da so la duong chinh -> "Main", nguoc lai -> "Alley".

    Args:
        path: list of node_id (ket qua tu A*)
        graph: Graph object (tu search.py)
    Returns:
        "Main" hoac "Alley"
    """
    if not path or len(path) < 2:
        return "Main"  # Default

    main_count = 0
    alley_count = 0

    for i in range(len(path) - 1):
        current_id = path[i]
        next_id = path[i + 1]

        # Tim edge tuong ung trong graph
        for edge in graph.adj_list.get(current_id, []):
            if edge.target_node == next_id:
                # Phan loai dua tren toc do toi da
                # Duong chinh thuong co max_speed > 40 km/h
                if edge.max_speed > 40:
                    main_count += 1
                else:
                    alley_count += 1
                break

    return "Main" if main_count >= alley_count else "Alley"


def apply_traffic_penalty(orders, traffic_level):
    """
    Ap dung he so phat giao thong vao thoi gian giao hang.
    Dung de tich hop Bayes -> CSP (Phan B).

    Theo idea.md: "ket qua nay duoc dung lam he so phat (Penalty)
    de tinh toan lai thoi gian di chuyen thuc te t_i cho CSP"

    Args:
        orders: list of dict (co key 'real_time')
        traffic_level: "Low", "Medium", hoac "High"
    Returns:
        list of dict voi real_time da dieu chinh
    """
    penalty = TRAFFIC_PENALTY.get(traffic_level, 1.0)

    adjusted_orders = []
    for order in orders:
        adjusted = dict(order)  # Copy
        adjusted['real_time'] = order['real_time'] * penalty
        adjusted['traffic_penalty'] = penalty
        adjusted['traffic_level'] = traffic_level
        adjusted_orders.append(adjusted)

    return adjusted_orders


# ============================================
# TRAIN VA CACHE GLOBAL INSTANCE
# ============================================
_global_bayes = None


def get_trained_bayes(csv_path=None):
    """
    Lay instance TrafficBayesNetwork da train.
    Cache lai de khong phai train lai nhieu lan.

    Args:
        csv_path: Duong dan toi train.csv. Neu None, dung default.
    Returns:
        TrafficBayesNetwork da train
    """
    global _global_bayes

    if _global_bayes is not None and _global_bayes.trained:
        return _global_bayes

    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'train.csv')

    bayes = TrafficBayesNetwork()
    bayes.train_probabilities(csv_path)
    _global_bayes = bayes
    return bayes


# ============================================
# DEMO / TEST
# ============================================
if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    train_path = os.path.join(data_dir, 'train.csv')

    print("=" * 65)
    print("  DEMO: BAYESIAN NETWORK - Suy luan muc do giao thong")
    print("=" * 65)

    # 1. Khoi tao va train
    bayes = TrafficBayesNetwork()
    bayes.print_network_structure()
    bayes.train_probabilities(train_path)

    # 2. In CPT
    bayes.print_cpt()

    # 3. Test suy luan
    print(f"\n{'='*65}")
    print(f"  TEST SUY LUAN (INFERENCE)")
    print(f"{'='*65}")

    test_cases = [
        ("Peak", "Main",  "Gio cao diem + Duong chinh"),
        ("Peak", "Alley", "Gio cao diem + Hem"),
        ("Normal", "Main",  "Gio thuong + Duong chinh"),
        ("Normal", "Alley", "Gio thuong + Hem"),
    ]

    for ts, rt, desc in test_cases:
        result = bayes.infer_traffic_level(ts, rt)
        pred = result['prediction']
        penalty = result['penalty']
        probs = result['probabilities']

        print(f"\n  [{desc}]")
        print(f"    Evidence: Time_Slot={ts}, Road_Type={rt}")
        print(f"    => Traffic_Level = {pred} (penalty x{penalty})")
        print(f"       P(Low)={probs['Low']:.4f}, P(Medium)={probs['Medium']:.4f}, P(High)={probs['High']:.4f}")

    # 4. Test helper: hour -> time_slot
    print(f"\n\n{'='*65}")
    print(f"  TEST HELPER: get_time_slot_from_hour()")
    print(f"{'='*65}")

    for hour in [6, 7, 8, 9, 12, 14, 17, 18, 21]:
        ts = get_time_slot_from_hour(hour)
        print(f"    {hour}:00 -> {ts}")

    # 5. Test tich hop: apply_traffic_penalty
    print(f"\n\n{'='*65}")
    print(f"  TEST TICH HOP: apply_traffic_penalty()")
    print(f"{'='*65}")

    sample_orders = [
        {'id': 'ORD001', 'weight': 2.0, 'real_time': 30.0},
        {'id': 'ORD002', 'weight': 5.0, 'real_time': 60.0},
    ]

    for level in TRAFFIC_LEVELS:
        adjusted = apply_traffic_penalty(sample_orders, level)
        print(f"\n    Traffic = {level} (x{TRAFFIC_PENALTY[level]}):")
        for o in adjusted:
            print(f"      {o['id']}: {sample_orders[0]['real_time'] if o['id']=='ORD001' else sample_orders[1]['real_time']:.0f}min -> {o['real_time']:.0f}min")