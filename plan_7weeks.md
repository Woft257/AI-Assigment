# Kế Hoạch Code - 7 Tuần

## Phân công công việc

| Thành viên | Phần việc |
|------------|------------|
| **Hà** | (A) Search & Pathfinding - A* |
| **Hoài** | (B) CSP + (D) Bayes |
| **Tuấn** | (C) Rules + (E) ML |

---

## Tuần 1: Thiết kế & Chuẩn bị Data

### Mục tiêu
Thiết kế cấu trúc và tạo data mẫu, chưa code thuật toán chính

### Hà (A)
- [ ] Thiết kế class Node: node_id (str), point_x (float), point_y (float)
- [ ] Thiết kế class Edge: target_node (str), distance (float), max_speed (float)
- [ ] Thiết kế class Graph: adj_list (dict)
- [ ] Tạo bản đồ mẫu (5-10 nodes) - KHÔNG code A*)

### Hoài (B+D)
- [ ] Thiết kế dữ liệu đơn hàng: order_id, weight, customer_location
- [ ] Thiết kế dữ liệu shipper: shipper_id, max_weight, max_time
- [ ] Định nghĩa CSP variables: X_{i,j} - KHÔNG code giải thuật
- [ ] Định nghĩa 4 ràng buộc CSP - KHÔNG code giải thuật

### Tuấn (C+E)
- [ ] Thiết kế dữ liệu huấn luyện ML: 500-1000 samples (chưa train)
- [ ] Thiết kế class Order với các thuộc tính
- [ ] Liệt kê 14 rules - KHÔNG code engine

### Deliverable
- [ ] Cấu trúc class/data đã thiết kế
- [ ] Data mẫu đã tạo

---

## Tuần 2: A* Pathfinding (Hà)

### Mục tiêu
Code và test thuật toán A*

### Hà
- [ ] Code hàm get_euclidean_distance(node_a, node_b)
- [ ] Code hàm calculate_travel_time(distance, speed)
- [ ] Code hàm calculate_heuristic()
- [ ] Code A* với 4 biến: open_set, g_score, f_score, came_from
- [ ] Code hàm reconstruct_path()
- [ ] Test A* với graph mẫu

### Deliverable
- [ ] A* chạy đúng

---

## Tuần 3: CSP - Phân công đơn hàng (Hoài)

### Mục tiêu
Code và test CSP

### Hoài
- [ ] Import OR-Tools
- [ ] Code CSP variables X_{i,j} (N=20, M=3)
- [ ] Code 4 ràng buộc CSP
- [ ] Code giải bằng CP-SAT Solver
- [ ] Test với 20 đơn, 3 shipper

### Deliverable
- [ ] CSP chạy đúng, in ra lịch phân công

---

## Tuần 4: Bayes Network (Hoài)

### Mục tiêu
Code và test Bayesian Network

### Hoài
- [ ] Import pgmpy
- [ ] Code 3 biến: Time_Slot, Road_Type, Traffic_Level
- [ ] Code DAG: Time_Slot → Traffic_Level ← Road_Type
- [ ] Code CPTs (Conditional Probability Tables)
- [ ] Code hàm infer_traffic_level()
- [ ] Test: Peak + Main → Traffic_Level?

### Deliverable
- [ ] Bayes Network hoạt động, trả về traffic_level

---

## Tuần 5: Rule-based System (Tuấn)

### Mục tiêu
Code và test hệ thống IF-THEN

### Tuấn
- [ ] Code class Rule với condition và action
- [ ] Code class RuleEngine: add_rule(), evaluate(), fire_rule()
- [ ] Code 14 rules cụ thể
- [ ] Test các trường hợp: Food+VIP, Express+Rush hour...

### Deliverable
- [ ] Rules hoạt động đúng

---

## Tuần 6: Decision Tree ML (Tuấn)

### Mục tiêu
Train và evaluate ML model

### Tuấn
- [ ] Tiền xử lý: LabelEncoder, tạo derived features
- [ ] Chia train/test (80/20)
- [ ] Code DecisionTreeClassifier (max_depth=5)
- [ ] Đánh giá: Accuracy, Precision, Recall, F1, Confusion Matrix
- [ ] Test với input mới

### Deliverable
- [ ] Decision Tree accuracy ≥ 85%

---

## Tuần 7: Tích hợp & Hoàn thiện

### Mục tiêu
Tích hợp 5 phần, test end-to-end, nộp bài

### Cả nhóm
- [ ] Pipeline tích hợp: A* → Bayes → Rules → ML → CSP
- [ ] Test end-to-end
- [ ] Fix bugs
- [ ] Chạy "Runtime → Run all" trên Colab
- [ ] Viết báo cáo PDF
- [ ] Upload GitHub
- [ ] Nộp bài

### Deliverable
- [ ] Pipeline hoàn chỉnh, Colab không lỗi
- [ ] Báo cáo PDF
- [ ] Đã nộp bài

---

## Tổng kết

| Tuần | Hà (A) | Hoài (B+D) | Tuấn (C+E) |
|------|--------|-------------|-------------|
| 1 | Thiết kế Node/Edge/Graph | Thiết kế data CSP | Thiết kế data ML, Rules |
| 2 | Code A* | - | - |
| 3 | - | Code CSP | - |
| 4 | - | Code Bayes | - |
| 5 | - | - | Code Rules |
| 6 | - | - | Code Decision Tree |
| 7 | Tích hợp | Tích hợp | Tích hợp |

---

## Deadline: Chủ nhật mỗi tuần
