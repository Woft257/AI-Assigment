import pandas as pd
import os
import sys

# Thêm đường dẫn để có thể import từ thư mục modules ở ngoài
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.search import Node, Edge, Graph

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NODES_PATH = os.path.join(CURRENT_DIR, 'nodes.csv')
DEFAULT_SEGMENTS_PATH = os.path.join(CURRENT_DIR, 'segments.csv')

def build_map_graph(nodes_path=DEFAULT_NODES_PATH, segments_path=DEFAULT_SEGMENTS_PATH):
    # Khởi tạo đồ thị rỗng
    g = Graph()
    
    print("Đang đọc dữ liệu Nodes...")
    nodes_df = pd.read_csv(nodes_path)
    
    # Đổ data vào Đồ thị (Khởi tạo các ngã tư)
    for _, row in nodes_df.iterrows():
        node_id = str(row['_id'])
        # Ép kiểu dữ liệu theo đúng yêu cầu của Leader
        g.adj_list[node_id] = [] # Khởi tạo danh sách các đường đi rỗng cho ngã tư này

    print("Đang đọc dữ liệu Segments (Edges)...")
    segments_df = pd.read_csv(segments_path)
    
    # Xử lý các đường bị thiếu dữ liệu tốc độ (cho mặc định 40.0 km/h)
    segments_df['max_velocity'] = segments_df['max_velocity'].fillna(40.0)
    
    # Đổ data vào Đồ thị (Nối các con đường giữa các ngã tư)
    for _, row in segments_df.iterrows():
        start_node = str(row['s_node_id'])
        end_node = str(row['e_node_id'])
        distance = float(row['length'])
        max_speed = float(row['max_velocity'])
        
        # Khởi tạo đối tượng Edge (Cạnh)
        edge = Edge(target_node=end_node, distance=distance, max_speed=max_speed)
        
        # Thêm cạnh này vào danh sách của ngã tư xuất phát
        if start_node in g.adj_list:
            g.adj_list[start_node].append(edge)
            
    print("Khởi tạo Đồ thị thành công!")
    return g

#dòng để test (không test cứ # là được)
if __name__ == "__main__":
   graph = build_map_graph()