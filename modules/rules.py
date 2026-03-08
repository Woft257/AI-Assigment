"""
Rule-based System - Phần C
Hệ thống IF-THEN để xác định thời gian giao hàng tối đa và phụ phí
"""

# ============================================
# BIẾN ĐẦU VÀO
# ============================================
# 1. order_type: loại hàng hóa - str (food, document, fragile, electronic, clothing)
# 2. is_vip: khách hàng VIP hay không - bool
# 3. distance_category: phân loại khoảng cách - str (short, medium, long)
# 4. customer_location: vị trí khách hàng - str (residential, commercial, industrial)
# 5. order_weight: trọng lượng đơn hàng (kg) - float
# 6. delivery_time_requested: thời gian giao hàng yêu cầu - str (express, normal, flexible)
# 7. is_rush_hour: có phải giờ cao điểm không - bool
# 8. weather: thời tiết - str (clear, rain, storm, fog)

# ============================================
# BIẾN ĐẦU RA
# ============================================
# 1. delivery_time_limit: thời gian giao hàng tối đa (phút) - int
# 2. priority_level: mức độ ưu tiên - str (low, normal, high, urgent)
# 3. estimated_surcharge: phụ phí ước tính (VND) - int

# ============================================
# 14 RULES THIẾT KẾ
# ============================================

# ----- Rules về delivery_time_limit -----
# Rule 1: IF order_type = "food" THEN delivery_time_limit = 30
# Rule 2: IF order_type = "document" THEN delivery_time_limit = 60
# Rule 3: IF order_type = "fragile" THEN delivery_time_limit = 45
# Rule 4: IF order_type = "electronic" THEN delivery_time_limit = 90
# Rule 5: IF order_type = "clothing" THEN delivery_time_limit = 120

# ----- Rules về priority_level -----
# Rule 6: IF is_vip = True THEN priority_level = "high"
# Rule 7: IF delivery_time_requested = "express" THEN priority_level = "urgent"

# ----- Rules về estimated_surcharge -----
# Rule 8: IF is_rush_hour = True THEN estimated_surcharge + 10000
# Rule 9: IF weather = "rain" THEN estimated_surcharge + 15000
# Rule 10: IF weather = "storm" THEN estimated_surcharge + 25000
# Rule 11: IF distance_category = "long" THEN estimated_surcharge + 20000
# Rule 12: IF order_weight > 10 THEN estimated_surcharge + 15000
# Rule 13: IF order_weight > 20 THEN estimated_surcharge + 30000
# Rule 14: IF customer_location = "industrial" THEN estimated_surcharge + 10000

# ============================================
# VÍ DỤ MẪU
# ============================================
sample_rules = [
    {
        "rule_id": 1,
        "condition": 'order_type = "food"',
        "action": 'delivery_time_limit = 30'
    },
    {
        "rule_id": 2,
        "condition": 'order_type = "document"',
        "action": 'delivery_time_limit = 60'
    },
    {
        "rule_id": 3,
        "condition": 'order_type = "fragile"',
        "action": 'delivery_time_limit = 45'
    },
    {
        "rule_id": 4,
        "condition": 'order_type = "electronic"',
        "action": 'delivery_time_limit = 90'
    },
    {
        "rule_id": 5,
        "condition": 'order_type = "clothing"',
        "action": 'delivery_time_limit = 120'
    },
    {
        "rule_id": 6,
        "condition": "is_vip = True",
        "action": 'priority_level = "high"'
    },
    {
        "rule_id": 7,
        "condition": 'delivery_time_requested = "express"',
        "action": 'priority_level = "urgent"'
    },
    {
        "rule_id": 8,
        "condition": "is_rush_hour = True",
        "action": "estimated_surcharge + 10000"
    },
    {
        "rule_id": 9,
        "condition": 'weather = "rain"',
        "action": "estimated_surcharge + 15000"
    },
    {
        "rule_id": 10,
        "condition": 'weather = "storm"',
        "action": "estimated_surcharge + 25000"
    },
    {
        "rule_id": 11,
        "condition": 'distance_category = "long"',
        "action": "estimated_surcharge + 20000"
    },
    {
        "rule_id": 12,
        "condition": "order_weight > 10",
        "action": "estimated_surcharge + 15000"
    },
    {
        "rule_id": 13,
        "condition": "order_weight > 20",
        "action": "estimated_surcharge + 30000"
    },
    {
        "rule_id": 14,
        "condition": 'customer_location = "industrial"',
        "action": "estimated_surcharge + 10000"
    }
]


# ============================================
# CLASS ORDER - THIẾT KẾ
# ============================================
class Order:
    """
    Class lưu thông tin đơn hàng cho Rule-based System
    """
    # Input attributes
    order_id: str
    order_type: str  # food, document, fragile, electronic, clothing
    is_vip: bool
    distance_category: str  # short, medium, long
    customer_location: str  # residential, commercial, industrial
    order_weight: float
    delivery_time_requested: str  # express, normal, flexible
    is_rush_hour: bool
    weather: str  # clear, rain, storm, fog

    # Output attributes
    delivery_time_limit: int  # phút
    priority_level: str  # low, normal, high, urgent
    estimated_surcharge: int  # VND

    def __init__(self, order_id, order_type, is_vip, distance_category,
                 customer_location, order_weight, delivery_time_requested,
                 is_rush_hour, weather):
        self.order_id = order_id
        self.order_type = order_type
        self.is_vip = is_vip
        self.distance_category = distance_category
        self.customer_location = customer_location
        self.order_weight = order_weight
        self.delivery_time_requested = delivery_time_requested
        self.is_rush_hour = is_rush_hour
        self.weather = weather

        # Initialize outputs
        self.delivery_time_limit = None
        self.priority_level = "normal"  # default
        self.estimated_surcharge = 0  # base = 0

    def apply_rules(self):
        """
        Áp dụng 14 rules để tính toán output
        """
        # Rules 1-5: delivery_time_limit theo order_type
        if self.order_type == "food":
            self.delivery_time_limit = 30
        elif self.order_type == "document":
            self.delivery_time_limit = 60
        elif self.order_type == "fragile":
            self.delivery_time_limit = 45
        elif self.order_type == "electronic":
            self.delivery_time_limit = 90
        elif self.order_type == "clothing":
            self.delivery_time_limit = 120

        # Rules 6-7: priority_level
        if self.is_vip:
            self.priority_level = "high"
        if self.delivery_time_requested == "express":
            self.priority_level = "urgent"

        # Rules 8-14: estimated_surcharge
        if self.is_rush_hour:
            self.estimated_surcharge += 10000
        if self.weather == "rain":
            self.estimated_surcharge += 15000
        elif self.weather == "storm":
            self.estimated_surcharge += 25000
        if self.distance_category == "long":
            self.estimated_surcharge += 20000
        if self.order_weight > 10:
            self.estimated_surcharge += 15000
        if self.order_weight > 20:
            self.estimated_surcharge += 30000
        if self.customer_location == "industrial":
            self.estimated_surcharge += 10000

        return {
            "delivery_time_limit": self.delivery_time_limit,
            "priority_level": self.priority_level,
            "estimated_surcharge": self.estimated_surcharge
        }


# ============================================
# VÍ DỤ ÁP DỤNG RULES
# ============================================
sample_order = Order(
    order_id="ORD001",
    order_type="food",
    is_vip=True,
    distance_category="short",
    customer_location="residential",
    order_weight=2.5,
    delivery_time_requested="normal",
    is_rush_hour=False,
    weather="clear"
)

# Kết quả sau khi apply_rules:
# delivery_time_limit = 30 (Rule 1)
# priority_level = "high" (Rule 6)
# estimated_surcharge = 0 (no surcharge conditions met)
