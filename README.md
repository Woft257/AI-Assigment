# AI Delivery Scheduling System (Hệ thống AI Phân công Giao hàng)

## 📌 1. Thông tin môn học
- **Tên môn học:** Introduction to AI (Giới thiệu về Trí tuệ Nhân tạo)
- **Mã môn học:** CO3061
- **Học kỳ:** II
- **Năm học:** 2025 - 2026
- **Trường:** Đại học Bách Khoa, ĐHQG-HCM

## 👨‍🏫 2. Thông tin Giảng viên hướng dẫn
- **Giảng viên hướng dẫn (GVHD):** TS. Trương Vĩnh Lân

## 👥 3. Thông tin thành viên nhóm
| Họ tên | Mã số sinh viên | Email |
|--------|-----------------|-------|
| Huỳnh Hoàng Tuấn | 2353267 | tuan.huynhhoang2005@hcmut.edu.vn |
| Đinh Nguỵ Nguyệt Hà | 2352286 | ha.dinhnguy2005@hcmut.edu.vn |
| Nguyễn Xuân Hoài | 2352345 | hoai.nguyen874131@hcmut.edu.vn |

## 🎯 4. Mục tiêu của bài tập lớn
Bài tập lớn hướng tới việc mô hình hóa bài toán Điều phối và Phân công Giao hàng trong môi trường thực tế thành một bài toán AI toàn diện. Hệ thống kết hợp cả 5 trụ cột AI để đưa ra quyết định tự động:
1. **(A) Biểu diễn & Tìm kiếm:** Thuật toán **A*** tìm đường đi ngắn nhất cho shipper.
2. **(D) Mạng Bayes (Uncertainty):** Mô hình hóa xác suất kẹt xe dựa trên thời gian và loại đường.
3. **(E) Học máy (Machine Learning):** Sử dụng **Decision Tree** để dự đoán khả năng giao hàng nhanh/chậm (Fast/Slow ETA) của từng đơn hàng.
4. **(C) Suy luận tri thức:** Hệ thống luật **IF-THEN (14 Rules)** tự động tính phụ phí, thời gian giới hạn và độ ưu tiên.
5. **(B) Bài toán thỏa mãn ràng buộc (CSP):** Thuật toán **Backtracking + Branch & Bound** để giải quyết việc phân công tối ưu hàng loạt đơn hàng cho đội ngũ Shipper sao cho tổng thời gian giao hàng là nhỏ nhất mà không vi phạm tải trọng.

## 🚀 5. Hướng dẫn chạy hệ thống & Notebook
Dự án được thiết kế dưới dạng Google Colab Notebook để thầy cô có thể dễ dàng chạy kiểm thử (Run All) mà không cần cài đặt phức tạp.

**Yêu cầu hệ thống:**
- Python 3.8+
- Các thư viện bắt buộc: `pandas`, `scikit-learn`

**Cách chạy trên Google Colab (Dành cho Giảng viên):**
1. Nhấn vào **[Link Google Colab Notebook]** (Xem ở phần 7).
2. Hệ thống đã được lập trình sẵn để tự động:
   - Git clone repository này về Colab.
   - Cài đặt thư viện tự động (`!pip install pandas scikit-learn`).
   - Tự động load dữ liệu từ file CSV đi kèm.
3. Trên thanh công cụ, chọn **Runtime -> Run All** (Thời gian chạy môi trường: ~10 giây) để chiêm ngưỡng toàn bộ hệ thống từ Train ML, Bayes Inference đến CSP phân công giao hàng.

**Cách chạy dưới Local (Máy tính cá nhân):**
```bash
# 1. Clone repository
git clone https://github.com/Woft257/AI-Assigment.git
cd AI-Assigment

# 2. Cài thư viện
pip install pandas scikit-learn

# 3. Chạy pipeline toàn hệ thống
python main_pipeline.py
```

## 📁 6. Cấu trúc thư mục của dự án
Theo chuẩn cấu trúc yêu cầu của bài tập lớn:
```text
AI-Assigment/
│
├── notebooks/                  # Chứa file Google Colab Notebook làm front-end nộp bài
│   └── AI_Delivery_System.ipynb
│
├── modules/                    # Thư mục mã nguồn xử lý thuật toán chính (tự code thuần)
│   ├── search.py               # (Phần A) Thuật toán tìm đường A*
│   ├── csp_solver.py           # (Phần B) Bộ giải Constraint Satisfaction Problem (Backtracking)
│   ├── rules.py                # (Phần C) Hệ chuyên gia với 14 Rules IF-THEN
│   ├── traffic_ai.py           # (Phần D) Suy luận Mạng Bayes tính kẹt xe
│   └── ml.py                   # (Phần E) Huấn luyện Decision Tree dự đoán ETA
│
├── features/                   # Chứa file model trích xuất
│   └── decision_tree_model.pkl # Model Decision Tree đã được train và lưu lại
│
├── reports/                    # Chứa báo cáo PDF giải thích chi tiết thực nghiệm
│   └── report-nhom-7.pdf       # Báo cáo chi tiết của nhóm
│
├── data/                       # Chứa bộ dữ liệu gốc (không đưa lên cloud ngoài)
│   ├── uds-orders-aug2024.csv  # Dữ liệu 1500+ đơn hàng thật của Xe dù (Tháng 8/2024)
│   ├── train.csv               # Dữ liệu 33K+ mẫu giao thông thực tế TP.HCM cho Bayes
│   └── ...
│
├── main_pipeline.py            # Script chạy tích hợp (A->D->E->C->B) dưới dạng terminal
└── README.md                   # File hướng dẫn này
```

## 🔗 7. Links đính kèm
- **Google Colab Notebook:** [Click để mở Notebook trên Colab](https://colab.research.google.com/github/Woft257/AI-Assigment/blob/main/notebooks/AI_Delivery_System.ipynb)
- **Báo cáo PDF:** [report-nhom-7.pdf](./reports/report-nhom-7.pdf)
