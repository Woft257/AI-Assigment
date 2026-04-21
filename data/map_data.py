import pandas as pd
import os
import sys

# Thêm đường dẫn để có thể import từ thư mục modules ở ngoài
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.search import Node, Edge, Graph

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NODES_PATH = os.path.join(CURRENT_DIR, 'nodes.csv')
DEFAULT_SEGMENTS_PATH = os.path.join(CURRENT_DIR, 'segments.csv')
DEFAULT_UDS_PATH = os.path.join(CURRENT_DIR, 'uds-orders-aug2024.csv')

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

print("\n-- Test do thi --")
print(f"Tong so nga tu (nodes): {len(graph.adj_list)}")
print(f"So nga tu co duong di: {sum(1 for edges in graph.adj_list.values() if edges)}")
print(f"So canh (edges) tong cong: {sum(len(edges) for edges in graph.adj_list.values())}")

# ============================================
# ĐỌC TỌA ĐỘ TỪ XE DÙ
# ============================================
def load_uds_coordinates(uds_path=DEFAULT_UDS_PATH):
    """
    Đọc tọa độ từ Xe dù (sender và receiver)

    Returns:
        List of dict với sender_lat, sender_lng, receiver_lat, receiver_lng
    """
    import csv

    uds_df = pd.read_csv(uds_path)

    coordinates = []
    for _, row in uds_df.iterrows():
        try:
            sender_lat = float(row['senderLat'])
            sender_lng = float(row['senderLng'])
            receiver_lat = float(row['receiverLat'])
            receiver_lng = float(row['receiverLng'])

            coordinates.append({
                'sender_lat': sender_lat,
                'sender_lng': sender_lng,
                'receiver_lat': receiver_lat,
                'receiver_lng': receiver_lng
            })
        except (ValueError, TypeError):
            continue

    return coordinates

if __name__ == "__main__":
    coords = load_uds_coordinates()
    print(f"\n-- Test toa do Xe du --")
    print(f"Da doc {len(coords)} toa do")
    if coords:
        print(f"Vi du: {coords[0]}")