class DeliveryCSP:
    def __init__(self, orders, shippers):
        """
        Khởi tạo bài toán CSP cho hệ thống giao hàng.
        orders: Danh sách đơn hàng (Dict)
        shippers: Danh sách người giao hàng (Dict)
        """
        self.orders = orders
        self.shippers = shippers
        
        # ĐỊNH NGHĨA VARIABLES (Biến quyết định)
        # assignment = {order_id: shipper_id}
        self.assignment = {} 
        
        # Thêm Kho Chờ để chứa hàng nếu quá tải (Dummy Shipper)
        self.dummy_shipper = {
            'id': 'KHO_CHO', 
            'max_weight': float('inf'), 
            'max_time': float('inf')
        }
        self.shippers.append(self.dummy_shipper)

    # ĐỊNH NGHĨA CONSTRAINTS (Các ràng buộc)
    def check_weight_constraint(self, shipper_idx, new_weight, current_load):
        """Ràng buộc 1: Tổng khối lượng không vượt quá sức chứa của xe"""
        return current_load + new_weight <= self.shippers[shipper_idx]['max_weight']

    def check_time_constraint(self, shipper_idx, new_time, current_time_spent):
        """Ràng buộc 2: Tổng thời gian không vượt quá ca làm việc"""
        return current_time_spent + new_time <= self.shippers[shipper_idx]['max_time']

    def solve(self):
        pass