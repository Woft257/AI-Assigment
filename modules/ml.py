"""
ML Module - Phần E
Class Order và hàm đọc data từ Xe dù (data thật)
"""

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

                # Traffic level - chưa có, default là "medium"
                # (sẽ map từ Traffic HCM sau)
                traffic_level = "medium"

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
# VÍ DỤ
# ============================================
if __name__ == "__main__":
    orders = load_ml_data_from_uds()

    print(f"Total orders loaded: {len(orders)}")
    print("\nFirst 5 orders:")
    for o in orders[:5]:
        print(f"  {o.order_id}: {o.distance_km:.2f}km, {o.eta_minutes:.1f}min, {o.eta_label}")

    # Thống kê
    fast = sum(1 for o in orders if o.eta_label == "fast")
    slow = sum(1 for o in orders if o.eta_label == "slow")
    print(f"\nFast: {fast} ({fast/len(orders)*100:.1f}%)")
    print(f"Slow: {slow} ({slow/len(orders)*100:.1f}%)")
