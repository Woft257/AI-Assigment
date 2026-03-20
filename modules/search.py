#Search - PHẦN A

class Node:
    def __init__(self, node_id: str, point_x: float, point_y: float):
        self.node_id = node_id
        self.point_x = point_x
        self.point_y = point_y

class Edge:
    def __init__(self, target_node: str, distance: float, max_speed: float):
        self.target_node = target_node
        self.distance = distance
        self.max_speed = max_speed

class Graph:
    def __init__(self):
        # adj_list lưu trữ theo dạng Dict: { "Node_ID": [Edge1, Edge2,...] }
        self.adj_list = {} 

    def add_node(self, node_id: str):
        # TODO: Code thêm node vào đồ thị
        pass

    def add_edge(self, from_node: str, edge: Edge):
        # TODO: Code thêm cạnh vào node tương ứng
        pass

# ==========================================
# CÁC HÀM PHỤ TRỢ & THUẬT TOÁN (CHƯA CODE LOGIC)
# ==========================================

def get_euclidean_distance(node_a: Node, node_b: Node) -> float:
    # TODO: Tính khoảng cách đường chim bay
    pass

def calculate_travel_time(distance: float, speed: float) -> float:
    # TODO: Tính thời gian di chuyển
    pass

def calculate_heuristic(current_node: Node, goal_node: Node, max_global_speed: float) -> float:
    # TODO: Hàm ước lượng heuristic
    pass

def a_star_search(graph: Graph, start_id: str, goal_id: str, max_global_speed: float) -> list:
    # TODO: Thuật toán A* (để lại pass, tuần sau code)
    pass

def reconstruct_path(came_from: dict, current_node_id: str) -> list:
    # TODO: Truy vết đường đi
    pass