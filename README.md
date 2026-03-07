# AI Delivery Scheduling System

## Thông tin môn học

- **Tên môn:** Introduction to AI
- **Mã môn:** CO3061
- **Học kỳ:** II
- **Năm học:** 2025-2026
- **Trường:** Đại học Bách Khoa, ĐHQG-HCM
- **Giảng viên hướng dẫn:** TS. Trương Vĩnh Lân

---

## Thông tin các thành viên nhóm

| Họ tên | Mã số sinh viên | Email |
|--------|-----------------|-------|
| Huỳnh Hoàng Tuấn | 2353267 | tuan.huynhhoang2005@hcmut.edu.vn |
| Đinh Nguỵ Nguyệt Hà | 2352286 | ha.dinhnguy2005@hcmut.edu.vn |
| Nguyễn Xuân Hoài | 2352345 | hoai.nguyen874131@hcmut.edu.vn |

---

## Mục tiêu của bài tập lớn

Xây dựng hệ thống AI điều phối giao hàng shipper với 5 thành phần bắt buộc:

### (A) Biểu diễn & Tìm kiếm

Tìm đường đi ngắn nhất từ cửa hàng đến khách hàng bằng thuật toán A*.

**Định nghĩa dữ liệu:**
- **Node:** (node_id, point_x, point_y) - id định danh, tọa độ x (kinh độ), tọa độ y (vĩ độ)
- **Edge:** (target_node, distance, max_speed) - đích đến, khoảng cách, tốc độ tối đa
- **Graph:** adj_list theo cấu trúc key-value chứa node - edge

**Các hàm cần thiết:**
- `get_euclidean_distance(node_a, node_b)`: Tính khoảng cách giữa 2 node
- `calculate_travel_time(distance, speed)`: Tính thời gian di chuyển
- `calculate_heuristic(current_node, goal_node, max_global_speed)`: Hàm heuristic
- `a_star_search(graph, start_id, goal_id, max_global_speed)`: Thuật toán A*

**4 biến bắt buộc trong A*:**
- **open_set:** Hàng đợi ưu tiên, node có f_score bé nhất ở đỉnh
- **g_score:** Thời gian di chuyển ít nhất từ điểm xuất phát đến node n
- **f_score:** Hàm mục tiêu f(n) = g(n) + h(n)
- **came_from:** Bảng truy vết đường đi

### (B) Heuristic hoặc CSP

Phân công đơn hàng cho shipper sử dụng CSP (Constraint Satisfaction Problem).

**Dữ liệu mô hình:**
- **N:** Số lượng đơn hàng cần giao trong cụm
- **M:** Số lượng shipper khả dụng trong cụm
- **w_i:** Khối lượng thực tế của đơn hàng thứ i (kg)
- **t_i:** Thời gian di chuyển dự kiến để hoàn tất đơn hàng i (phút)
- **W_max:** Trọng tải chuyên chở tối đa của phương tiện
- **T_max:** Giới hạn thời gian tối đa cho phép của một chuyến giao hàng

**Variables:**
- x_{i,j} = 1 nếu shipper j giao đơn i, ngược lại = 0
- Ma trận nhị phân kích thước NxM

**Ràng buộc:**
- Mỗi đơn hàng chỉ do đúng một shipper đảm nhận
- Tổng khối lượng các đơn hàng được gán cho shipper j không vượt quá W_max
- Tổng thời gian di chuyển của shipper j không vượt quá T_max

**Giải bằng:** Backtracking hoặc OR-Tools CP-SAT Solver

### (C) Suy luận tri thức

Hệ thống IF-THEN để xác định thời gian giao hàng tối đa và phụ phí.

**Biến đầu vào:**
- order_type: loại hàng hóa (food, document, fragile, electronic, clothing)
- is_vip: khách hàng VIP hay không (True/False)
- distance_category: phân loại khoảng cách (short, medium, long)
- customer_location: vị trí khách hàng (residential, commercial, industrial)
- order_weight: trọng lượng đơn hàng (kg)
- delivery_time_requested: thời gian giao hàng yêu cầu (express, normal, flexible)
- is_rush_hour: có phải giờ cao điểm không (True/False)
- weather: thời tiết (clear, rain, storm, fog)

**Biến đầu ra:**
- delivery_time_limit: thời gian giao hàng tối đa (phút)
- priority_level: mức độ ưu tiên (low, normal, high, urgent)
- estimated_surcharge: phụ phí ước tính (VND)

**Các luật (Rules):**
- Rule 1: IF order_type = "food" THEN delivery_time_limit = 30
- Rule 2: IF order_type = "document" THEN delivery_time_limit = 60
- Rule 3: IF order_type = "fragile" THEN delivery_time_limit = 45
- Rule 4: IF order_type = "electronic" THEN delivery_time_limit = 90
- Rule 5: IF order_type = "clothing" THEN delivery_time_limit = 120
- Rule 6: IF is_vip = True THEN priority_level = "high"
- Rule 7: IF delivery_time_requested = "express" THEN priority_level = "urgent"
- Rule 8: IF is_rush_hour = True THEN estimated_surcharge + 10000
- Rule 9: IF weather = "rain" THEN estimated_surcharge + 15000
- Rule 10: IF weather = "storm" THEN estimated_surcharge + 25000
- Rule 11: IF distance_category = "long" THEN estimated_surcharge + 20000
- Rule 12: IF order_weight > 10 THEN estimated_surcharge + 15000
- Rule 13: IF order_weight > 20 THEN estimated_surcharge + 30000
- Rule 14: IF customer_location = "industrial" THEN estimated_surcharge + 10000

### (D) Mạng Bayes

Mô hình hóa mức độ kẹt xe để phản ánh tính không chắc chắn của môi trường.

**3 biến ngẫu nhiên:**
- **Time_Slot:** ∈ {Peak, Normal} - Khung giờ cao điểm / bình thường
- **Road_Type:** ∈ {Main, Alley} - Đường chính / hẻm nhánh
- **Traffic_Level:** ∈ {Low, Medium, High} - Mức độ giao thông

**Cấu trúc DAG:**
- Time_Slot → Traffic_Level
- Road_Type → Traffic_Level

**Công thức:** P(Traffic_Level | Time_Slot, Road_Type)

**Kết nối với các phần khác:**
- Input: Lấy is_rush_hour từ Phần C, lộ trình từ A* để phân tích tỷ lệ đường
- Output: Trả về traffic_level để làm feature cho Decision Tree (Phần E) và hệ số phạt cho CSP (Phần B)

### (E) Học máy

Xây dựng mô hình Decision Tree để dự đoán ETA (giao dưới 20 phút hay không).

**Biến đầu vào:**
- distance_km: khoảng cách từ cửa hàng đến khách hàng (km)
- time_hour: giờ trong ngày (0-23)
- day_of_week: ngày trong tuần (0-6)
- building_type: loại tòa nhà (apartment, house, office, mall, school)
- traffic_level: mức giao thông (low, medium, high)
- order_priority: độ ưu tiên đơn hàng (low, normal, high, urgent)
- is_weekend: có phải cuối tuần không (True/False)

**Biến đầu ra:**
- eta_label: fast (dưới 20 phút) hoặc slow (từ 20 phút trở lên)

**Các bước mô hình:**
1. Tạo 500-1000 mẫu dữ liệu tổng hợp (synthetic data)
2. Mã hóa biến phân loại bằng LabelEncoder
3. Chia dữ liệu 80% train, 20% test
4. Huấn luyện DecisionTreeClassifier với max_depth=5

**Đánh giá:** accuracy, precision, recall, F1-score, confusion matrix

---

(Các phần khác sẽ được bổ sung sau khi code hoàn thiện)

## Link

- **Colab Notebook:** [Link]()
- **Báo cáo PDF:** [Link]()
- **GitHub Repository:** [Link](https://github.com/Woft257/AI-Assigment)
