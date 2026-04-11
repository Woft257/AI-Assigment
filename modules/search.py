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
        self.nodes = {} 

    def add_node(self, node: Node):
        # TODO: Code thêm node vào đồ thị
        if node.node_id not in self.adj_list:
            self.adj_list[node.node_id] = []
            self.nodes[node.node_id] = node

    def add_edge(self, from_node: str, edge: Edge):
        # TODO: Code thêm cạnh vào node tương ứng
        if from_node in self.adj_list:
            self.adj_list[from_node].append(edge)

# ==========================================
# CÁC HÀM PHỤ TRỢ & THUẬT TOÁN (CHƯA CODE LOGIC)
# ==========================================

def get_euclidean_distance(node_a: Node, node_b: Node) -> float:
    # TODO: Tính khoảng cách đường chim bay
    return math.sqrt((node_a.point_x - node_b.point_x)**2 + (node_a.point_y - node_b.point_y)**2)

def calculate_travel_time(distance: float, speed: float) -> float:
    # TODO: Tính thời gian di chuyển
    if speed <= 0:
        return float('inf')
    return distance / speed

def calculate_heuristic(current_node: Node, goal_node: Node, max_global_speed: float) -> float:
    # TODO: Hàm ước lượng heuristic
    distance = get_euclidean_distance(current_node, goal_node)
    return calculate_travel_time(distance, max_global_speed)

def a_star_search(graph: Graph, start_id: str, goal_id: str, max_global_speed: float) -> list:
    # TODO: Thuật toán A* (để lại pass, tuần sau code)
    if start_id not in graph.nodes or goal_id not in graph.nodes:
        return []

    open_set = []
    heapq.heappush(open_set, (0.0, start_id))

    came_from = {}
    
    g_score = {node_id: float('inf') for node_id in graph.nodes}
    g_score[start_id] = 0.0

    f_score = {node_id: float('inf') for node_id in graph.nodes}
    f_score[start_id] = calculate_heuristic(graph.nodes[start_id], graph.nodes[goal_id], max_global_speed)

    while open_set:
        current_f, current_id = heapq.heappop(open_set)

        if current_id == goal_id:
            return reconstruct_path(came_from, current_id)

        if current_f > f_score[current_id]:
            continue

        # Duyệt qua các node láng giềng
        for edge in graph.adj_list.get(current_id, []):
            neighbor_id = edge.target_node
            
            if neighbor_id not in graph.nodes:
                continue

            travel_time = calculate_travel_time(edge.distance, edge.max_speed)
            tentative_g_score = g_score[current_id] + travel_time

            if tentative_g_score < g_score[neighbor_id]:
                came_from[neighbor_id] = current_id
                g_score[neighbor_id] = tentative_g_score
                
                h = calculate_heuristic(graph.nodes[neighbor_id], graph.nodes[goal_id], max_global_speed)
                f_score[neighbor_id] = g_score[neighbor_id] + h
                
                heapq.heappush(open_set, (f_score[neighbor_id], neighbor_id))

    return []

def reconstruct_path(came_from: dict, current_node_id: str) -> list:
    # TODO: Truy vết đường đi
    path = [current_node_id]
    while current_node_id in came_from:
        current_node_id = came_from[current_node_id]
        path.append(current_node_id)
    path.reverse()
    return path