"""
Data huấn luyện ML - 1000 samples
Phần E: Dự đoán ETA (fast/slow)

Dataset cân bằng: ~50% fast, ~50% slow
"""

# ============================================
# CẤU TRÚC DATA
# ============================================
# Input features:
# - distance_km: khoảng cách (km)
# - time_hour: giờ trong ngày (0-23)
# - day_of_week: ngày trong tuần (0-6)
# - building_type: apartment, house, office, mall, school
# - traffic_level: low, medium, high
# - order_priority: low, normal, high, urgent
# - is_weekend: True/False
# - is_rush_hour: True/False
# - weather: clear, rain, storm, fog

# Output:
# - eta_label: fast (<20 phút) / slow (>=20 phút)

# ============================================
# CÔNG THỨC TẠO LABEL (ĐIỀU CHỈNH ĐỂ CÂN BẰNG)
# ============================================
# ETA = 2 + (distance * 1.5)    # Base: 2.75-17 phút
# + traffic: medium +5, high +10
# + weather: rain +5, storm +10, fog +3
# + rush_hour: +5
# + building: apartment +3, mall +5
# + priority: urgent -2, low +2
# fast nếu ETA < 20, else slow


# ============================================
# HÀM TẠO SAMPLES
# ============================================
def generate_ml_data(n_samples=500):
    """
    Tạo n_samples dữ liệu tổng hợp
    """
    import random

    building_types = ["apartment", "house", "office", "mall", "school"]
    traffic_levels = ["low", "medium", "high"]
    order_priorities = ["low", "normal", "high", "urgent"]
    weathers = ["clear", "rain", "storm", "fog"]

    data = []

    for i in range(n_samples):
        distance = round(random.uniform(0.5, 10.0), 2)
        hour = random.randint(0, 23)
        day = random.randint(0, 6)
        building = random.choice(building_types)
        traffic = random.choice(traffic_levels)
        priority = random.choice(order_priorities)
        weather = random.choice(weathers)
        is_weekend = day in [0, 6]
        is_rush_hour = hour in [7, 8, 9, 17, 18, 19]

        # Tính ETA (công thức cân bằng fast/slow)
        eta = 2 + (distance * 1.5)     # Base: 2.75-17 phút
        if traffic == "medium": eta += 5
        elif traffic == "high": eta += 10
        if weather == "rain": eta += 5
        elif weather == "storm": eta += 10
        elif weather == "fog": eta += 3
        if is_rush_hour: eta += 5
        if building == "apartment": eta += 3
        elif building == "mall": eta += 5
        if priority == "urgent": eta -= 2
        elif priority == "low": eta += 2

        eta_label = "fast" if eta < 20 else "slow"

        data.append({
            "order_id": f"ORD{i+1:04d}",
            "distance_km": distance,
            "time_hour": hour,
            "day_of_week": day,
            "building_type": building,
            "traffic_level": traffic,
            "order_priority": priority,
            "is_weekend": is_weekend,
            "is_rush_hour": is_rush_hour,
            "weather": weather,
            "eta_label": eta_label
        })

    return data


# ============================================
# TEST: TẠO VÀ LƯU DATA
# ============================================
if __name__ == "__main__":
    import csv

    data = generate_ml_data(1000)

    # In thống kê
    print(f"Total samples: {len(data)}")
    fast = sum(1 for d in data if d["eta_label"] == "fast")
    slow = sum(1 for d in data if d["eta_label"] == "slow")
    print(f"Fast: {fast} ({fast/len(data)*100:.1f}%)")
    print(f"Slow: {slow} ({slow/len(data)*100:.1f}%)")

    # Lưu CSV
    filename = "ml_data_1000.csv"
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nSaved to: {filename}")
