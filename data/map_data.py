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
    
    #print("Đang đọc dữ liệu Nodes...")
    nodes_df = pd.read_csv(nodes_path)
    
    # Đổ data vào Đồ thị (Khởi tạo các ngã tư)
    for _, row in nodes_df.iterrows():
        node_id = str(int(row['_id']))
        point_x = float(row['long'])
        point_y = float(row['lat'])

        node = Node(node_id=node_id, point_x=point_x, point_y=point_y)
        g.add_node(node)  

    #print("Đang đọc dữ liệu Segments (Edges)...")
    segments_df = pd.read_csv(segments_path)
    
    # Xử lý các đường bị thiếu dữ liệu tốc độ (cho mặc định 40.0 km/h)
    segments_df['max_velocity'] = segments_df['max_velocity'].fillna(40.0)
    
    # Đổ data vào Đồ thị (Nối các con đường giữa các ngã tư)
    for _, row in segments_df.iterrows():
        start_node = str(int(row['s_node_id']))
        end_node = str(int(row['e_node_id']))
        distance = float(row['length'])
        max_speed = float(row['max_velocity'])
        
        # Khởi tạo đối tượng Edge (Cạnh)
        edge = Edge(target_node=end_node, distance=distance, max_speed=max_speed)
        g.add_edge(start_node, edge)
        
            
    #print("Khởi tạo Đồ thị thành công!")
    return g

#dòng để test (không test cứ # là được)
if __name__ == "__main__":
   graph = build_map_graph()

print("\n-- Test đồ thị --")
print(f"Tổng số ngã tư (nodes): {len(graph.adj_list)}")
print(f"Số ngã tư có đường đi: {sum(1 for edges in graph.adj_list.values() if edges)}")
print(f"Số ngã tư không có đường đi: {sum(1 for edges in graph.adj_list.values() if not edges)}")
print(f"Số cạnh (edges) tổng cộng: {sum(len(edges) for edges in graph.adj_list.values())}")
test_id = '373543511'
print(f"\nCác đường đi từ node {test_id}:")
if test_id in graph.adj_list:
    for edge in graph.adj_list[test_id]:
        print(f"  -> Đi đến {edge.target_node} (Khoảng cách: {edge.distance} m, Tốc độ tối đa: {edge.max_speed} km/h)")
else:
    print(f"  -> Không tìm thấy ngã tư với ID {test_id}")