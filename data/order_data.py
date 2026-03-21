import csv
import ast
from datetime import datetime

class OrderDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data_for_csp(self):
        orders = []
        shippers_dict = {}

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
            
            print(f"[OK] Da xu ly thanh cong {len(orders)} don hang va {len(shippers)} shipper.")
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