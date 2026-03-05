# BÀI TẬP LỚN MÔN HỌC: INTRODUCTION TO AI

## Học kỳ II - Năm học 2025 – 2026

## Bộ môn Khoa học Máy tính

## Trường Đại học Bách Khoa, ĐHQG-HCM

## Giảng viên hướng dẫn: TS. Trương Vĩnh Lân

## Ngày 1 3 tháng 2 năm 202 6

## Phiên bản hiện tại: v1.

## 1 Giới thiệu

```
Bài tập lớn của học phần Giới thiệu về Trí tuệ Nhân tạo nhằm giúp sinh viên vận dụng các kiến
thức lý thuyết đã học để giải quyết các bài toán thực tế. Thông qua việc mô hình hóa một bài toán
thực tế dưới dạng bài toán trí tuệ nhân tạo, sinh viên sẽ áp dụng các kỹ thuật như tìm kiếm, suy
luận, xác suất và/hoặc học máy để xây dựng một hệ thống AI hoàn chỉnh.
```
```
Nội dung bài tập tập trung vào ba trụ cột chính của trí tuệ nhân tạo: tìm kiếm , biểu diễn và suy
luận tri thức , và học máy. Sinh viên được yêu cầu lựa chọn một bài toán thực tế và triển khai các
thành phần tương ứng, bao gồm: mô hình hóa và tìm kiếm, heuristic hoặc bài toán thỏa mãn ràng
buộc (CSP), biểu diễn và suy luận logic, mạng Bayes và xác suất, cũng như học máy.
```
```
Các nhóm phải xây dựng một hệ thống AI tích hợp, trong đó dữ liệu và tri thức được xử lý thông
qua các cơ chế suy luận, học máy và tìm kiếm để đưa ra quyết định. Thông qua bài tập lớn này,
sinh viên không chỉ củng cố kiến thức lý thuyết mà còn phát triển kỹ năng thực hành, tư duy phân
tích và khả năng trình bày, viết báo cáo khoa học.
```
## 2 Mục tiêu

```
Sinh viên sẽ tự chọn một bài toán AI thực tế, sau đó:
```
- Mô hình hoá nó như bài toán trí tuệ nhân tạo

**BKTP.HCM** (^)


- Áp dụng tìm kiếm, suy luận, xác suất, và/hoặc học máy
- Xây dựng một hệ thống AI hoàn chỉnh

## 3 Yêu cầu tổng quát

```
Mỗi nhóm (3- 5 SV) chọn một bài toán thực tế, ví dụ (chỉ để minh hoạ , không bắt buộc):
```
- Lập lịch học/lịch thi
- Điều phối giao hàng
- Game AI
- Chẩn đoán bệnh
- Hệ gợi ý
- Phát hiện gian lận
- Lập kế hoạch du lịch
- Quản lý tài nguyên
- Phân loại văn bản, ảnh, spam,...

## 4 Cấu trúc bắt buộc của bài toán

```
Dù chọn đề tài gì, hệ thống AI bắt buộc phải có ít nhất 4 trong 5 thành phần sau:
```
```
(A) Biểu diễn & tìm kiếm (L.O.1)
```
```
Mô hình bài toán thành:
```
- State
- Action
- Goal
- Cost

```
Và dùng ít nhất một thuật toán:
```
- BFS/DFS/Uniform Cost
- Best-first
- A*

```
(B) Heuristic hoặc CSP (L.O.1)
```
```
Phải có ít nhất một:
```
- Heuristic function hoặc
- Constraint Satisfaction (backtracking, hill climbing, GA ...)

```
(C) Biễu diễn & suy luận tri thức (L.O.2.1)
```
```
Sử dụng một trong các cách sau:
```

- Logic mệnh đề
- Logic vị từ
- Luật IF – THEN

```
để biểu diễn một phần tri thức của hệ.
```
```
(D) Mạng Bayes hoặc xác suất (L.O.2.2)
```
```
Phải mô hình hoá một yếu tố không chắc chắn, ví dụ:
```
- rủi ro
- lỗi
- nhiễu
- hành vi người dùng

```
bằng Bayes Network hoặc Naive Bayes.
```
```
(E) Học máy (L.O.3)
```
```
Áp dụng ít nhất một thuật toán:
```
- Naive Bayes
- Decision Tree
- Perceptron

```
cho một bài toán con (dự đoán, phân loại, xếp hạng...)
```
## 5 Yêu cầu về hệ thống (L.O.4)

```
Nhóm phải xây dựng một hệ thống AI hoàn chỉnh, trong đó:
```
```
Dữ liệu / Tri thức - > Suy luận / ML / Search -> Quyết định
```
```
Hệ thống phải:
```
- nhận input
- xử lý bằng AI
- xuất output có ý nghĩa

## 6 Báo cáo bắt buộc

```
Báo cáo (10 - 20 trang) phải có các mục:
```
- Mô tả bài toán thực tế
- Mô hình AI (state, knowledge, uncertainty, learning)
- Các thuật toán sử dụng
- Thực nghiệm
- Phân tích kết quả
- Kết luận


```
Toàn bộ bài làm phải có front-end là Google Colab Notebook. Sinh viên có thể (và được
khuyến khích) viết thêm các module hỗ trợ bằng Python, sau đó import và sử dụng trực
tiếp trong Colab.
File Colab nộp lên phải đảm bảo yêu cầu:
```
- Khi chọn chức năng Runtime → Run all, toàn bộ notebook phải chạy thành công mà
    không phát sinh lỗi.
- Không được mount vào các dịch vụ cloud cá nhân (Google Drive, Dropbox, ...).
- Dữ liệu cần được download từ nguồn công khai (có link cụ thể trong notebook) và giải
    nén trực tiếp vào môi trường máy chủ Colab.
- Các bước chuẩn bị dữ liệu, cài đặt thư viện bổ sung (nếu có) phải được ghi rõ và chạy
    tự động trong notebook.

```
Ngoài notebook, sản phẩm nộp phải bao gồm:
```
- Báo cáo PDF: trình bày EDA, pipeline, các thí nghiệm đã thực hiện, so sánh kết quả và
    phân tích.
- Các file đặc trưng đã trích xuất (embedding, vector đặc trưng) được lưu ở định dạng
    .npy hoặc .h5, nộp kèm theo hoặc ghi rõ đường link tải.
- Cấu trúc thư mục trong file nộp (.zip) phải rõ ràng: gồm thư mục notebooks/,
    modules/, reports/, và features/.
- Sinh viên được khuyến khích tải toàn bộ mã nguồn và tài liệu lên GitHub, sau đó chia
    sẻ đường link trong Colab và báo cáo. Việc này sẽ được cộng điểm khuyến khích vì
    thể hiện khả năng quản lý và công bố mã nguồn khoa học. README của repository
    GitHub cần có đầy đủ thông tin:
       - Tên môn học, mã môn học, học kỳ, năm học.
       - Thông tin giảng viên hướng dẫn (GVHD).
       - Thông tin các thành viên nhóm: họ tên, mã số sinh viên, email.
       - Mục tiêu của bài tập lớn.
       - Hướng dẫn chạy notebook (yêu cầu thư viện, cách tải dữ liệu).
       - Cấu trúc thư mục của dự án.
       - Link tới báo cáo PDF và link Colab notebook (nếu có).

## 7 Hình thức làm việc

```
Sinh viên cần tự chia thành các nhóm từ 3 - 5 thành viên. Mỗi nhóm sẽ thực hiện toàn bộ các
bài tập lớn (bao gồm cả phần mở rộng nếu có) theo nhóm đã đăng ký.
```

- Đăng ký nhóm: Các nhóm cần đăng ký tên nhóm và danh sách thành viên vào trang
    Google Sheet được chia sẻ trên LMS của môn học.
- Tài liệu minh chứng: Trong quá trình làm việc, các nhóm được khuyến khích xây dựng
    kho tư liệu minh chứng (hình ảnh, video họp nhóm, biên bản thảo luận, ...) để chứng
    minh sự hợp tác thực tế.
- Phân công công việc: Trong báo cáo nộp cuối kỳ, mỗi nhóm bắt buộc phải có bảng
    phân công công việc chi tiết cho từng thành viên, kèm theo tỷ lệ phần trăm hoàn
    thành. Điểm của mỗi thành viên sẽ được tính theo công thức:
    Điểm cá nhân = Điểm nhóm × Tỷ lệ đóng góp (%).

## 8 Tiêu chí đánh giá

```
Bài tập lớn sẽ được chấm điểm dựa trên các tiêu chí sau:
```
- Mô hình hoá bài toán AI: 25%
- Tìm kiếm/Heuristic /CSP: 20%
- Bayes/Xác suất: 15%
- Học máy: 15%
- Hệ thống tích hợp: 15%
- Báo cáo & Demo: 10%

```
Lưu ý: Trong suốt thời gian học, các nhóm được yêu cầu nộp báo cáo tiến độ định kỳ
(progress report) theo lịch mà giảng viên công bố. Đây là căn cứ để đánh giá sự tham gia,
tiến độ, và sự phân công công việc trong nhóm.
```
## 9 Thời hạn & cách nộp

- Hình thức nộp: Bài tập lớn được nộp thông qua thư mục Google Drive đã được giảng
    viên tạo và chia sẻ cho toàn lớp.
- Thời hạn: Thời gian nộp cụ thể xem trên LMS của môn học.


