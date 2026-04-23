import csv
import ast
from datetime import datetime

class OrderDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data_for_csp(self, max_time_filter=240.0):
        """
        Đọc data từ CSV cho bài toán CSP.

        Args:
            max_time_filter: Lọc bỏ đơn hàng có real_time > giá trị này (phút).
                             Mặc định 240 phút (4 giờ). Các đơn vượt quá thường là
                             giao qua đêm hoặc lỗi data, không phù hợp cho CSP.
        
        Returns:
            (orders, shippers): tuple of lists
        """
        orders = []
        shippers_dict = {}
        skipped = 0

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    order_id = row.get('mdh', 'UNKNOWN_ID')
                    
                    try:
                        weight = float(row['weight'])
                    except ValueError:
                        weight = 0.0
                    
                    shipper_raw = row['shipper']
                    try:
                        shipper_data = ast.literal_eval(shipper_raw)
                        shipper_id = shipper_data.get('$oid', 'UNKNOWN_SHIPPER')
                    except (ValueError, SyntaxError):
                        shipper_id = 'UNKNOWN_SHIPPER'

                    try:
                        # Cắt bỏ phần mili-giây và chữ Z ở đuôi (vd: 2023-07-22T11:00:45)
                        created_str = row['createdAt'][:19]
                        delivered_str = row['deliveredAt'][:19]
                        
                        created = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S")
                        delivered = datetime.strptime(delivered_str, "%Y-%m-%dT%H:%M:%S")
                        
                        real_time_minutes = (delivered - created).total_seconds() / 60.0
                    except (ValueError, TypeError):
                        real_time_minutes = 60.0

                    # Lọc bỏ đơn có thời gian bất hợp lý (quá lâu hoặc âm)
                    if real_time_minutes <= 0 or real_time_minutes > max_time_filter:
                        skipped += 1
                        continue

                    orders.append({
                        'id': order_id,
                        'weight': weight,
                        'shipping_distance': float(row['shippingDistance']) if row.get('shippingDistance') else 0.0,
                        'real_time': real_time_minutes
                    })

                    if shipper_id not in shippers_dict:
                        shippers_dict[shipper_id] = {
                            'id': shipper_id,
                            'max_weight': 50.0, # Giả định: xe chở tối đa 50kg
                            'max_time': 480.0   # Giả định: ca làm việc 8 tiếng (480 phút)
                        }

            shippers = list(shippers_dict.values())
            
            print(f"[OK] Da xu ly thanh cong {len(orders)} don hang va {len(shippers)} shipper. (Bo qua {skipped} don bat hop ly)")
            return orders, shippers

        except FileNotFoundError:
            print(f"[ERROR] Khong tim thay file tai: {self.file_path}")
            return [], []

if __name__ == "__main__":
    loader = OrderDataLoader('data/uds-orders-aug2024.csv')
    my_orders, my_shippers = loader.load_data_for_csp()

    if my_orders:
        print(f"\nFirst 5 orders:")
        for order in my_orders[:5]:
            print(order)