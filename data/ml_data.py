"""
Data ML - Phần E
Đọc data từ Xe dù (data thật)
"""

# ============================================
# DATA TỪ XE DÙ
# ============================================
# Nguồn: data/uds-orders-aug2024.csv
# Số lượng: ~1400 đơn (sau khi lọc ETA <= 180p)

# Input features (từ Xe dù):
# - distance_km: shippingDistance (m) -> km
# - time_hour: từ createdAt
# - day_of_week: từ createdAt (0=Mon, 6=Sun)
# - traffic_level: sẽ map từ Traffic HCM (low/medium/high)
# - order_priority: từ serviceType (urgent=3h, normal=5h, low=khác)
# - is_weekend: từ day_of_week
# - is_rush_hour: từ time_hour (7-9, 17-19)

# Output:
# - eta_minutes: Thời gian giao thực tế (phút)
# - eta_label: fast (<90p) / slow (>=90p)

# ============================================
# HÀM ĐỌC DATA
# ============================================
def load_ml_data():
    """
    Đọc data từ Xe dù

    Returns:
        List of dict với features và label
    """
    import csv
    from datetime import datetime

    data = []
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
                # Các đơn >3h có thể là giao qua đêm, không phản ánh giao hàng thực tế
                if eta_minutes <= 0 or eta_minutes > 180:
                    continue

                # Distance (m -> km)
                distance_km = float(row['shippingDistance']) / 1000

                # Time features
                time_hour = created.hour
                day_of_week = created.weekday()
                is_weekend = day_of_week in [5, 6]
                is_rush_hour = time_hour in [7, 8, 9, 17, 18, 19]

                # Traffic level - default
                traffic_level = "medium"

                # Order priority
                service_type = row.get('serviceType', '5h')
                if service_type == '3h':
                    order_priority = "urgent"
                elif service_type == '5h':
                    order_priority = "normal"
                else:
                    order_priority = "low"

                # Label: fast < 90p, slow >= 90p
                eta_label = "fast" if eta_minutes < 90 else "slow"

                data.append({
                    "order_id": row['id'],
                    "distance_km": distance_km,
                    "time_hour": time_hour,
                    "day_of_week": day_of_week,
                    "traffic_level": traffic_level,
                    "order_priority": order_priority,
                    "is_weekend": is_weekend,
                    "is_rush_hour": is_rush_hour,
                    "eta_minutes": eta_minutes,
                    "eta_label": eta_label
                })

            except Exception:
                continue

    return data


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    data = load_ml_data()

    print(f"Total samples: {len(data)}")
    print("\nFirst 5 samples:")
    for d in data[:5]:
        print(f"  {d['order_id']}: {d['distance_km']:.2f}km, {d['eta_minutes']:.1f}min, {d['eta_label']}")

    # Thống kê
    fast = sum(1 for d in data if d['eta_label'] == "fast")
    slow = sum(1 for d in data if d['eta_label'] == "slow")
    print(f"\nFast: {fast} ({fast/len(data)*100:.1f}%)")
    print(f"Slow: {slow} ({slow/len(data)*100:.1f}%)")
