"""
ML Module - Phần E
Class Order và hàm tạo data huấn luyện
"""

# ============================================
# CLASS ORDER
# ============================================
class Order:
    """
    Class lưu thông tin đơn hàng cho ML
    """
    # Input attributes
    order_id: str
    distance_km: float
    time_hour: int
    day_of_week: int
    building_type: str      # apartment, house, office, mall, school
    traffic_level: str     # low, medium, high
    order_priority: str    # low, normal, high, urgent
    is_weekend: bool
    is_rush_hour: bool
    weather: str           # clear, rain, storm, fog

    # Output attribute
    eta_label: str         # "fast" hoặc "slow"

    def __init__(self, order_id, distance_km, time_hour, day_of_week,
                 building_type, traffic_level, order_priority,
                 is_weekend, is_rush_hour, weather):
        self.order_id = order_id
        self.distance_km = distance_km
        self.time_hour = time_hour
        self.day_of_week = day_of_week
        self.building_type = building_type
        self.traffic_level = traffic_level
        self.order_priority = order_priority
        self.is_weekend = is_weekend
        self.is_rush_hour = is_rush_hour
        self.weather = weather
        self.eta_label = None

    def calculate_eta_label(self):
        """
        Tính toán ETA label dựa trên công thức
        """
        # Bước 1: ETA cơ bản
        eta = 5 + (self.distance_km * 3)

        # Bước 2: Thêm thời gian do giao thông
        if self.traffic_level == "medium":
            eta += 5
        elif self.traffic_level == "high":
            eta += 10

        # Bước 3: Thêm thời gian do thời tiết
        if self.weather == "rain":
            eta += 5
        elif self.weather == "storm":
            eta += 10
        elif self.weather == "fog":
            eta += 3

        # Bước 4: Thêm thời gian do giờ cao điểm
        if self.is_rush_hour:
            eta += 5

        # Bước 5: Thêm thời gian do loại tòa nhà
        if self.building_type == "apartment":
            eta += 3
        elif self.building_type == "mall":
            eta += 5

        # Bước 6: Điều chỉnh do độ ưu tiên
        if self.order_priority == "urgent":
            eta -= 2
        elif self.order_priority == "low":
            eta += 2

        # Bước 7: Gán nhãn
        self.eta_label = "fast" if eta < 20 else "slow"
        return self.eta_label


# ============================================
# HÀM TẠO DATA TỔNG HỢP
# ============================================
def generate_ml_data(n_samples=500):
    """
    Hàm tạo n_samples dữ liệu tổng hợp cho ML

    Args:
        n_samples: Số lượng mẫu cần tạo (500-1000)

    Returns:
        List of Order objects đã có eta_label
    """
    import random

    building_types = ["apartment", "house", "office", "mall", "school"]
    traffic_levels = ["low", "medium", "high"]
    order_priorities = ["low", "normal", "high", "urgent"]
    weathers = ["clear", "rain", "storm", "fog"]

    orders = []

    for i in range(n_samples):
        # Random các giá trị
        distance = round(random.uniform(0.5, 10.0), 2)
        hour = random.randint(0, 23)
        day = random.randint(0, 6)
        building = random.choice(building_types)
        traffic = random.choice(traffic_levels)
        priority = random.choice(order_priorities)
        weather = random.choice(weathers)
        is_weekend = day in [0, 6]
        is_rush_hour = hour in [7, 8, 9, 17, 18, 19]

        # Tạo Order
        order = Order(
            order_id=f"ORD{i+1:04d}",
            distance_km=distance,
            time_hour=hour,
            day_of_week=day,
            building_type=building,
            traffic_level=traffic,
            order_priority=priority,
            is_weekend=is_weekend,
            is_rush_hour=is_rush_hour,
            weather=weather
        )

        # Tính ETA label
        order.calculate_eta_label()
        orders.append(order)

    return orders
