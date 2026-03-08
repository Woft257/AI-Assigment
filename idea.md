Điều phối Shipper
Tên biến:
Phần A:
Định nghĩa:
Node: định dạng là (node_id, point_x, point_y)
node_id: id định danh (str)
point_x: tọa độ x (kinh độ) (float)
point_y: tọa độ y (vĩ độ) (float)
Edge: định dạng là (target_node, distance, max_speed)
target_node: đích đến (str)
distance: khoảng cách (float)
max_speed: tốc độ tối đa được phép (float)
Graph: 
adj_list: theo cách key - value chứa node - edge.
Ví dụ cho dễ hiểu thì:
adj_list = {“A”: [ Edge("B", 5.0, 40.0), Edge("C", 2.0, 30.0) ], "B": [ Edge("A", 5.0, 40.0) ], "C": [ Edge("A", 2.0, 30.0) ] }
Hàm
def get_euclidean_distance(node_a: Node, node_b: Node): hàm tính khoảng cách giữa 2 node trả về float

def calculate_travel_time(distance: float, speed: float): hàm tính thời gian di chuyển trả về float

def calculate_heuristic(current_node: Node, goal_node: Node, max_global_speed: float): hàm ước lượng heuristic cho trường hợp này trả về float

def a_star_search(graph: Graph, start_id: str, goal_id: str, max_global_speed: float) hàm thuật toán a* trả về list. 
4 biến bắt buộc:
open_set: hàng đợi chứa các node tiếp theo, ưu tiên f_score bé nhất nằm ở đỉnh
g_score: Lưu lại thời gian di chuyển ít nhất tính từ điểm xuất phát đến một node n bất kỳ
f_score: Lưu giá trị hàm mục tiêu f(n) = g(n) + h(n). A* dùng bảng này để đánh giá xem node nào "có vẻ" sẽ dẫn đến đích nhanh nhất.
came_from: Bảng truy vết đường đi, sau khi tới đích có thể dò ngược lại thành một đường đi hoàn chỉnh.
Cách hoạt động:
Bước 1: Rút node trên cùng của open_set ra (gọi là current_node). Đây chắc chắn là node có f_score thấp nhất hiện tại.
Bước 2: Duyệt các node kề (neighbors). Nhìn vào đồ thị adj_list để lấy ra tất cả các con đường nối từ current_node đến các node neighbor.
Bước 3: Tính giá trị trung gian (Trọng tâm của A)* với mỗi con đường đi từ current_node đến một neighbor gọi là tentative_g_score (Chi phí g thử nghiệm).
Công thức: tentative_g_score = g_score[current_node] + time(current_node -> neighbor)
Bước 4: So sánh và Cập nhật Bây giờ, ta lấy cái tentative_g_score vừa tính đem so sánh với kỷ lục hiện tại đang lưu trong bảng g_score[neighbor]. Nếu tentative_g_score < g_score[neighbor]: 
Ghi đè kỷ lục mới: g_score[neighbor] = tentative_g_score
Tính lại f: f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
Ghi lại dấu vết: came_from[neighbor] = current_node (Nghĩa là: đường tốt nhất để đến neighbor tính tới lúc này là đi qua current_node).
Cuối cùng, đẩy cái neighbor này vào open_set để vòng lặp sau sẽ lấy nó ra xét tiếp.
def reconstruct_path(came_from: dict, current_node_id: str) hàm truy xuất lại đường đi khi mà tìm được đích trả về list
Ví dụ: lịch sử đi là ABCDE thì hàm này đầu tiên sẽ là EDCBA sau đó sẽ đảo thành ABCDE rồi mới trả list này
Phần B:
Mô hình hoá bài toán Điều phối giao hàng thoả mãn các ràng buộc (CSP):
Để đảm bảo hệ thống phản hồi trong thời gian thực và tránh tràn bộ nhớ, kiến trúc điều phối được thiết kế theo cơ chế Chia để trị. Thuật toán CSP đóng vai trò giải quyết các bài toán con tại từng phân vùng địa lý nhỏ (zone) trong một khung thời gian ngắn (batch).
Các dữ liệu cần có trong mô hình: 
N: Số lượng đơn hàng cần giao trong cụm hiện tại.
M: Số lượng shipper đang ở trạng thái khả dụng trong cụm
w_i: Khối lượng thực tế của đơn hàng thứ i (kg), với i in {1, 2, ..., N}
t_i: Thời gian di chuyển dự kiến để hoàn tất đơn hàng i (phút)
W_{max}: Trọng tải chuyên chở an toàn tối đa của phương tiện
T_{max}: Giới hạn thời gian tối đa cho phép của một chuyến giao hàng
Trạng thái phân công của hệ thống được biểu diễn bằng không gian ma trận nhị phân X có kích thước NxM, trong đó:
 X_{i,j} in {0, 1}
 X_{i,j} = 1: Đơn hàng thứ i được phân công cho shipper thứ j.
 X_{i,j} = 0: Đơn hàng thứ i không thuộc về shipper thứ j.
Để nghiệm của bài toán khả thi, ma trận quyết định X_{i,j} phải thỏa mãn đồng thời 4 tập ràng buộc vật lý, logic và quy mô sau:
N <= 50 và M<=10. Trong một cụm (zone) để giới hạn kích thước của bài toán con, ta quy định kích thước N và M với 1 giới hạn cụ thể.
Mỗi đơn hàng phát sinh bắt buộc phải được xử lý và chỉ do đúng một shipper đảm nhận, nhằm tránh tình trạng trùng lặp hoặc sót đơn hàng.
Tổng khối lượng các đơn hàng được gán cho bất kỳ shipper j nào cũng không được vượt quá giới hạn có thể chuyên chở.

Tổng thời gian di chuyển dự kiến để hoàn tất toàn bộ khối lượng công việc của shipper j phải nằm trong ngưỡng quy định của một ca làm cục bộ.
Khi sử dụng các bộ giải công nghiệp (như OR-Tools CP-SAT Solver) để duyệt không gian nghiệm khả thi, hệ thống sẽ hướng tới việc tìm ra nghiệm tối ưu (Optimal Solution) bằng cách cực tiểu hóa tổng chi phí thời gian vận hành của toàn bộ đội ngũ:


Phần C:
Biến đầu vào:
- order_type: loại hàng hóa (food, document, fragile, electronic, clothing)
- is_vip: khách hàng VIP hay không (True/False)
- distance_category: phân loại khoảng cách (short, medium, long)
- customer_location: vị trí khách hàng (residential, commercial, industrial)
- order_weight: trọng lượng đơn hàng (kg)
- delivery_time_requested: thời gian giao hàng yêu cầu (express, normal, flexible)
- is_rush_hour: có phải giờ cao điểm không (True/False)
- weather: thời tiết (clear, rain, storm, fog)
Biến đầu ra:
- delivery_time_limit: thời gian giao hàng tối đa (phút)
- priority_level: mức độ ưu tiên (low, normal, high, urgent)
- estimated_surcharge: phụ phí ước tính (VND)

Phần D:  Suy luận Xác suất và Quản lý Rủi ro với Mạng Bayes
Trong môi trường vận hành thực tế, khoảng cách vật lý do thuật toán tìm đường (Pathfinding) cung cấp chỉ phản ánh được thời gian di chuyển lý tưởng. Yếu tố giao thông luôn chứa đựng tính bất định (Uncertainty) và thay đổi liên tục theo thời gian, địa điểm. Để hệ thống có khả năng định lượng rủi ro này và tự động điều chỉnh thời gian giao hàng, Mạng Bayes (Bayesian Network) được ứng dụng làm động cơ suy luận xác suất.
Module Mạng Bayes hoạt động như một bộ lọc rủi ro, kết nối trực tiếp với các phần khác:
Dữ liệu đầu vào (Evidence): * Lấy biến is_rush_hour và time_hour từ cấu hình hệ thống (Phần C & E) để xác định trạng thái thời gian.
Lấy lộ trình chi tiết từ thuật toán A* (Phần A) để phân tích tỷ lệ đường di chuyển (chiếm đa số là đường lớn hay hẻm nhỏ).
Dữ liệu đầu ra (Output): Trả về biến traffic_level (mức độ kẹt xe).
Nhãn này được đẩy thẳng vào làm feature đầu vào cho mô hình Decision Tree (Phần E) để phân loại ETA.
Đồng thời, kết quả này được dùng làm hệ số phạt (Penalty) để tính toán lại thời gian di chuyển thực tế t_i cho hệ phương trình CSP (Phần B).
Mạng Bayes đơn giản hóa bài toán với 3 biến ngẫu nhiên (Random Variables) cốt lõi:
Time_Slot in {Peak, Normal}: Khung giờ (Cao điểm / Bình thường).
Road_Type in {Main, Alley}: Loại đường tuyến tính (Đường chính / Hẻm nhánh).
Traffic_Level in {Low, Medium, High}: Biến mục tiêu biểu thị mức độ giao thông.
Cấu trúc Đồ thị và Xác suất có Điều kiện (DAG & CPTs):
Mô hình được thiết lập dưới dạng Đồ thị có hướng không chu trình (DAG) dựa trên giả định nhân quả: Khung giờ và Loại đường trực tiếp gây ra Tình trạng kẹt xe.
Cấu trúc:  Time_Slot -> Traffic_Level
Road_Type ->Traffic_Level
Quy tắc suy luận: Bảng phân phối xác suất có điều kiện (CPT) được định nghĩa cho biến mục tiêu thông qua công thức Bayes:
	P(Traffic_Level|Time_Slot, Road_Type)
Tại thời điểm phân công, ngay khi thuật toán A* (Phần A) chốt được tuyến đường, Mạng Bayes sẽ tự động cập nhật các bằng chứng (Evidence) hiện tại. Bằng việc sử dụng thuật toán tính toán xác suất (ví dụ: Variable Elimination), hệ thống truy vấn và trích xuất nhãn Traffic_Level có xác suất xảy ra cao nhất (Maximum A Posteriori - MAP) để cập nhật vào pipeline dữ liệu tổng của toàn hệ thống.
Phần E:
Biến đầu vào:
(dùng chung với phần C: is_rush_hour, weather  isf_rush_hour, weather
- distance_km: khoảng cách từ cửa hàng đến khách hàng (km)
- time_hour: giờ trong ngày (0-23)
- day_of_week: ngày trong tuần (0-6, 0=Chủ nhật)
- building_type: loại tòa nhà (apartment, house, office, mall, school)
- traffic_level: mức giao thông (low, medium, high)
- order_priority: độ ưu tiên đơn hàng (low, normal, high, urgent)
- is_weekend: có phải cuối tuần không (True/False)
Biến đầu ra:
eta_label: nhãn dự đoán (fast = dưới 20 phút, slow = từ 20 phút trở lên)



(A) Biểu diễn & tìm kiếm (L.O.1)
Bài toán:
Tìm đường đi ngắn nhất từ cửa hàng → khách hàng.
State
Một node giao lộ trên bản đồ.
Action
Đi sang node kế tiếp (theo edge có sẵn).
Goal
Đến node đích (khách hàng).
Cost
Thời gian di chuyển giữa 2 node.
Thuật toán:
Dùng A*.
Heuristic:
 Khoảng cách Euclidean / vận tốc tối đa.

(B) Heuristic hoặc CSP (L.O.1)
Dùng CSP (Constraint Sastifaction Problem)
Bài toán:
Phân 20 đơn hàng cho 3 shipper.
Variables
x_{i,j} = 1 nếu shipper j giao đơn i.
Ràng buộc (ví dụ):
Mỗi đơn chỉ do 1 shipper giao.


Tổng khối lượng ≤ 20kg.


Tổng thời gian ≤ 4 giờ.


Giải bằng:
 Backtracking hoặc OR-Tools.





(C) Biễu diễn & suy luận tri thức (L.O.2.1)
Rule 1: Thời gian giao hàng theo loại hàng
IF order_type = "food" THEN delivery_time_limit = 30
IF order_type = "document" THEN delivery_time_limit = 60
IF order_type = "fragile" THEN delivery_time_limit = 45
IF order_type = "electronic" THEN delivery_time_limit = 90
IF order_type = "clothing" THEN delivery_time_limit = 120

Rule 2: Ưu tiên khách hàng VIP
IF is_vip = True THEN priority_level = "high"

Rule 3: Ưu tiên giao hàng nhanh
IF delivery_time_requested = "express" THEN priority_level = "urgent"
IF delivery_time_requested = "express" THEN delivery_time_limit = delivery_time_limit * 0.5

Rule 4: Phụ phí giờ cao điểm
IF is_rush_hour = True THEN estimated_surcharge = estimated_surcharge + 10000

Rule 5: Phụ phí thời tiết xấu
IF weather = "rain" THEN estimated_surcharge = estimated_surcharge + 15000
IF weather = "storm" THEN estimated_surcharge = estimated_surcharge + 25000

Rule 6: Phụ phí khoảng cách xa
IF distance_category = "long" THEN estimated_surcharge = estimated_surcharge + 20000

Rule 7: Phụ phí trọng lượng nặng
IF order_weight > 10 THEN estimated_surcharge = estimated_surcharge + 15000
IF order_weight > 20 THEN estimated_surcharge = estimated_surcharge + 30000

Rule 8: Phụ phí vị trí khó tiếp cận
IF customer_location = "industrial" THEN estimated_surcharge = estimated_surcharge + 10000

(D) Mạng Bayes hoặc xác suất (L.O.2.2)
Yếu tố không chắc chắn:
Mô hình hóa mức độ kẹt xe như một biến ngẫu nhiên nhằm phản ánh tính không chắc chắn của môi trường.
Xây dựng mạng Bayes đơn giản gồm 3 biến:
Traffic_Level:
Traffic_Level∈{Low,Medium,High}
Time_Slot:
		Time_Slot∈{Peak,Normal}
Road_Type:
Road_Type∈{Main,Alley}

giả định:
Time_Slot ảnh hưởng đến Traffic_Level


Road_Type ảnh hưởng đến Traffic_Level


Cấu trúc:
Time_Slot →
       Traffic_Level
 Road_Type →
Điều này có nghĩa:
P(Traffic_Level | Time_Slot, Road_Type)
(E) Học máy (L.O.3)
Bài toán: Xây dựng mô hình Decision Tree để phân loại thời gian giao hàng thành hai lớp: nhanh (dưới 20 phút) hoặc chậm (từ 20 phút trở lên).
Các bước mô hình:
Tạo 500-1000 mẫu dữ liệu tổng hợp (synthetic data). Mỗi mẫu gồm các thông tin về đơn hàng và điều kiện giao hàng. Nhãn được tạo bằng công thức tính ETA dựa trên khoảng cách, thời tiết, giao thông, loại tòa nhà và độ ưu tiên.

Mã hóa các biến phân loại (categorical) thành số bằng LabelEncoder. Chia dữ liệu thành tập huấn luyện (80%) và tập kiểm tra (20%).

Huấn luyện mô hình DecisionTreeClassifier với max_depth=5 để tránh overfitting. Đánh giá bằng các chỉ số: accuracy, precision, recall, F1-score và confusion matrix.

Thuật toán:
Decision Tree (Cây quyết định) được áp dụng vào bài toán dự đoán ETA giao hàng như sau.

Mô hình học từ dữ liệu huấn luyện để tìm ra các quy tắc quyết định. Ví dụ, cây có thể học được quy tắc: nếu khoảng cách nhỏ hơn 3 km VÀ giao thông không cao VÀ không phải giờ cao điểm thì giao hàng nhanh (fast). Ngược lại, nếu khoảng cách lớn hơn 5 km HOẶC giao thông cao HOẶC trời mưa thì giao hàng chậm (slow).

Cách mô hình học các quy tắc này như sau. Từ tập dữ liệu huấn luyện, thuật toán tìm điểm chia đầu tiên tại nút gốc bằng cách thử tất cả các biến. Ví dụ, thử chia theo khoảng cách với các ngưỡng khác nhau (1km, 2km, 3km...). Hoặc thử chia theo mức giao thông (low/medium/high). Hoặc thử chia theo thời tiết (clear/rain/storm). Mỗi lần chia, tính Gini impurity hoặc Entropy để đo lường mức độ thuần nhất của các nhóm con. Chọn điểm chia cho Gini thấp nhất hoặc Information Gain (giảm Entropy) cao nhất.

Sau khi chia, mỗi nhóm con lại tiếp tục được chia nhỏ hơn. Ví dụ, nhóm khoảng cách dưới 3km được chia tiếp theo giao thông. Nhóm giao thông low lại được chia tiếp theo thời tiết. Quá trình tiếp tục cho đến khi đạt độ sâu tối đa (max_depth=5) hoặc các nút lá đã đủ thuần nhất.

Kết quả là một cây quyết định có thể được diễn giải bằng ngôn ngữ tự nhiên. Nút gốc có thể là khoảng cách với ngưỡng 3km. Nhánh trái (dưới 3km) được chia theo giao thông. Nhánh phải (trên 3km) được chia theo thời tiết. Mỗi đường đi từ gốc đến lá tạo thành một quy tắc IF-THEN hoàn chỉnh.

Decision Tree được chọn vì các lý do sau. Dễ hiểu và dễ giải thích, có thể trực quan hóa cây để thấy được quyết định được đưa ra như thế nào. Không cần chuẩn hóa dữ liệu vì thuật toán không sử dụng khoảng cách giữa các điểm. Xử lý được cả biến số và biến phân loại sau khi đã mã hóa. Hoạt động tốt với dữ liệu có nhiễu và có thể xử lý các giá trị thiếu.

Các tham số quan trọng của mô hình gồm max_depth giới hạn độ sâu tối đa của cây để tránh overfitting, thường chọn từ 3 đến 10. min_samples_split là số mẫu tối thiểu để tiếp tục chia nút, thường chọn từ 5 đến 20. min_samples_leaf là số mẫu tối thiểu tại nút lá, thường chọn từ 3 đến 10. criterion là tiêu chí để đánh giá điểm chia, có thể chọn gini hoặc entropy.

Input:
Dữ liệu đầu vào gồm các thông tin về đơn hàng và điều kiện giao hàng. Khoảng cách ảnh hưởng trực tiếp đến thời gian di chuyển. Giờ trong ngày xác định có trong giờ cao điểm hay không. Ngày trong tuần xác định là ngày thường hay cuối tuần. Loại tòa nhà ảnh hưởng đến thời gian chờ và di chuyển trong tòa nhà. Thời tiết ảnh hưởng đến tốc độ di chuyển. Mức giao thông ảnh hưởng đến thời gian trên đường. Độ ưu tiên đơn hàng xác định mức độ khẩn cấp của việc giao hàng.

Output:
Dữ liệu đầu ra là nhãn phân loại với hai giá trị. Fast nghĩa là thời gian giao hàng dưới 20 phút. Slow nghĩa là thời gian giao hàng từ 20 phút trở lên.
