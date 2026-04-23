"""
ML Module - Phan E
Class Order va ham doc data tu Xe du (data that)
Tich hop voi Bayes Network (Phan D) de suy luan traffic_level
"""

import os
import sys

# Them path de import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.traffic_ai import get_trained_bayes, get_time_slot_from_hour

# Import thu vien ML
try:
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, export_text
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    import joblib
    HAS_ML_LIBS = True
except ImportError:
    HAS_ML_LIBS = False
    print("[WARNING] Thieu thu vien pandas hoac scikit-learn. Chay 'pip install pandas scikit-learn' de train ML.")

# ============================================
# CLASS ORDER
# ============================================
class Order:
    """
    Class lưu thông tin đơn hàng cho ML
    """
    # Input attributes (từ Xe dù)
    order_id: str
    distance_km: float          # shippingDistance (m) -> km
    time_hour: int              # từ createdAt
    day_of_week: int            # từ createdAt (0=Chủ nhật)
    traffic_level: str         # từ Traffic HCM (low/medium/high)
    order_priority: str        # từ serviceType (urgent/normal/low)
    is_weekend: bool            # từ day_of_week
    is_rush_hour: bool          # từ time_hour (7-9, 17-19)
    # weather: KHÔNG có trong Xe dù

    # Output attribute
    eta_minutes: float          # Thời gian giao thực tế (phút)
    eta_label: str              # "fast" (<20p) hoặc "slow" (>=20p)

    def __init__(self, order_id, distance_km, time_hour, day_of_week,
                 traffic_level, order_priority, is_weekend, is_rush_hour):
        self.order_id = order_id
        self.distance_km = distance_km
        self.time_hour = time_hour
        self.day_of_week = day_of_week
        self.traffic_level = traffic_level
        self.order_priority = order_priority
        self.is_weekend = is_weekend
        self.is_rush_hour = is_rush_hour
        self.eta_minutes = None
        self.eta_label = None

    def set_eta(self, eta_minutes: float):
        """
        Set ETA thực tế từ data Xe dù
        Label: fast < 90p, slow >= 90p
        """
        self.eta_minutes = eta_minutes
        self.eta_label = "fast" if eta_minutes < 90 else "slow"


# ============================================
# HÀM ĐỌC DATA TỪ XE DÙ
# ============================================
def load_ml_data_from_uds():
    """
    Đọc data từ Xe dù (uds-orders-aug2024.csv)

    Returns:
        List of Order objects
    """
    import csv
    from datetime import datetime

    orders = []
    filename = "data/uds-orders-aug2024.csv"

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Parse createdAt và deliveredAt
                created = datetime.fromisoformat(row['createdAt'].replace('Z', '+00:00'))
                delivered = datetime.fromisoformat(row['deliveredAt'].replace('Z', '+00:00'))

                # Tính ETA (phút)
                eta_minutes = (delivered - created).total_seconds() / 60

                # Skip nếu ETA quá lớn (>3h = 180p) hoặc âm
                if eta_minutes <= 0 or eta_minutes > 180:
                    continue

                # Distance (m -> km)
                distance_km = float(row['shippingDistance']) / 1000

                # Time features
                time_hour = created.hour
                day_of_week = created.weekday()  # 0=Mon, 6=Sun
                is_weekend = day_of_week in [5, 6]
                is_rush_hour = time_hour in [7, 8, 9, 17, 18, 19]

                # Traffic level - suy luan tu Bayes Network (Phan D)
                time_slot = get_time_slot_from_hour(time_hour)
                try:
                    bayes = get_trained_bayes()
                    bayes_result = bayes.infer_traffic_level(time_slot, "Main")
                    probs = bayes_result['probabilities']
                    import random
                    levels = list(probs.keys())
                    weights = list(probs.values())
                    traffic_level = random.choices(levels, weights=weights, k=1)[0].lower()
                except Exception:
                    traffic_level = "medium"  # Fallback

                # Order priority từ serviceType
                service_type = row.get('serviceType', '5h')
                if service_type == '3h':
                    order_priority = "urgent"
                elif service_type == '5h':
                    order_priority = "normal"
                else:
                    order_priority = "low"

                # Tạo Order
                order = Order(
                    order_id=row['id'],
                    distance_km=distance_km,
                    time_hour=time_hour,
                    day_of_week=day_of_week,
                    traffic_level=traffic_level,
                    order_priority=order_priority,
                    is_weekend=is_weekend,
                    is_rush_hour=is_rush_hour
                )
                order.set_eta(eta_minutes)
                orders.append(order)

            except Exception as e:
                continue

    return orders


# ============================================
# HÀM HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH (ML PIPELINE)
# ============================================
def prepare_data(orders):
    """
    Chuyển list Order thành DataFrame và mã hóa dữ liệu.
    """
    if not HAS_ML_LIBS:
        return None, None
        
    data = []
    for o in orders:
        if o.eta_label is None:
            continue
        data.append({
            'distance_km': o.distance_km,
            'time_hour': o.time_hour,
            'day_of_week': o.day_of_week,
            'traffic_level': o.traffic_level,
            'order_priority': o.order_priority,
            'is_weekend': int(o.is_weekend),
            'is_rush_hour': int(o.is_rush_hour),
            'label': 1 if o.eta_label == 'slow' else 0  # 1: slow, 0: fast
        })
    
    df = pd.DataFrame(data)
    
    # Mã hóa biến categorical bằng map
    traffic_map = {'low': 0, 'medium': 1, 'high': 2}
    priority_map = {'low': 0, 'normal': 1, 'urgent': 2}
    
    df['traffic_level'] = df['traffic_level'].map(traffic_map)
    df['order_priority'] = df['order_priority'].map(priority_map)
    
    # Fill NaN nếu có lỗi map
    df.fillna(0, inplace=True)
    
    # Tách features (X) và labels (y)
    X = df.drop(columns=['label'])
    y = df['label']
    
    return X, y

def train_and_evaluate(X, y):
    """
    Huấn luyện Decision Tree và in kết quả đánh giá.
    """
    if not HAS_ML_LIBS:
        return None
        
    # Chia train/test 80-20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"[*] Đã chia dữ liệu: {len(X_train)} train, {len(X_test)} test")
    
    # Khởi tạo và huấn luyện mô hình (max_depth=5 để tránh overfitting)
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Dự đoán trên tập test
    y_pred = model.predict(X_test)
    
    # Đánh giá
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n" + "="*50)
    print("  KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH DECISION TREE")
    print("="*50)
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f} (Dự đoán slow đúng / Tổng dự đoán slow)")
    print(f"  Recall    : {rec:.4f} (Dự đoán slow đúng / Tổng thực tế slow)")
    print(f"  F1-Score  : {f1:.4f}")
    print("\n  Confusion Matrix:")
    print(f"    TN (Đoán Fast đúng): {cm[0][0]:<5} | FP (Đoán Slow sai): {cm[0][1]}")
    print(f"    FN (Đoán Fast sai) : {cm[1][0]:<5} | TP (Đoán Slow đúng): {cm[1][1]}")
    print("="*50)
    
    # Feature Importance
    print("\n[*] Mức độ quan trọng của các đặc trưng (Feature Importances):")
    importances = model.feature_importances_
    features = X.columns
    for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
        print(f"  - {feat:<15}: {imp:.4f}")
        
    # Tùy chọn: In ra một số rules dạng text
    print("\n[*] Một số quy tắc quan trọng trên Cây Quyết Định:")
    tree_rules = export_text(model, feature_names=list(features), max_depth=2)
    print(tree_rules)
    
    # LƯU MÔ HÌNH VÀO THƯ MỤC features/ (Yêu cầu nộp bài)
    features_dir = os.path.join(os.path.dirname(__file__), '..', 'features')
    if not os.path.exists(features_dir):
        os.makedirs(features_dir)
    model_path = os.path.join(features_dir, 'decision_tree_model.pkl')
    try:
        joblib.dump(model, model_path)
        print(f"\n[OK] Đã lưu mô hình Decision Tree vào: {model_path}")
    except Exception as e:
        print(f"\n[WARNING] Lỗi khi lưu mô hình: {e}")
    
    return model

def predict_eta(model, order_features_dict):
    """
    Dự đoán nhãn cho 1 đơn hàng mới.
    order_features_dict: dictionary chứa các features đã được số hóa.
    """
    if not HAS_ML_LIBS or model is None:
        return "unknown"
    df = pd.DataFrame([order_features_dict])
    pred = model.predict(df)[0]
    return "slow" if pred == 1 else "fast"

# ============================================
# VÍ DỤ / DEMO RUN
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("  DEMO: HỌC MÁY (PHẦN E) - DỰ ĐOÁN ETA")
    print("="*50)
    
    # 1. Load data
    orders = load_ml_data_from_uds()
    print(f"\n[*] Đã tải {len(orders)} đơn hàng từ Xe dù.")
    
    # Thống kê
    fast = sum(1 for o in orders if o.eta_label == "fast")
    slow = sum(1 for o in orders if o.eta_label == "slow")
    print(f"    Nhãn Fast (< 90p): {fast} ({fast/len(orders)*100:.1f}%)")
    print(f"    Nhãn Slow (>= 90p): {slow} ({slow/len(orders)*100:.1f}%)")
    
    # 2. Huấn luyện
    if HAS_ML_LIBS:
        print("\n[*] Đang chuẩn bị dữ liệu và huấn luyện mô hình...")
        X, y = prepare_data(orders)
        if X is not None:
            model = train_and_evaluate(X, y)
            
            # 3. Thử inference 1 đơn mới
            print("\n[*] Thử suy luận (Inference) 1 đơn hàng mới:")
            sample_order = {
                'distance_km': 8.5,
                'time_hour': 18,
                'day_of_week': 4,
                'traffic_level': 2, # high
                'order_priority': 1, # normal
                'is_weekend': 0,
                'is_rush_hour': 1
            }
            pred = predict_eta(model, sample_order)
            print(f"  Đơn hàng: Khoảng cách xa (8.5km), Giờ cao điểm, Kẹt xe (high)")
            print(f"  => Mô hình dự đoán: {pred.upper()}")
    else:
        print("\n[!] Không thể huấn luyện mô hình vì thiếu thư viện.")
