# Hướng dẫn sử dụng Google Maps Scraper Desktop App

## Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt](#cài-đặt)
3. [Cấu hình API](#cấu-hình-api)
4. [Sử dụng ứng dụng](#sử-dụng-ứng-dụng)
5. [Các tính năng chi tiết](#các-tính-năng-chi-tiết)
6. [Xuất dữ liệu](#xuất-dữ-liệu)
7. [Xử lý sự cố](#xử-lý-sự-cố)
8. [FAQ](#faq)

## Giới thiệu

Google Maps Scraper Desktop App là ứng dụng desktop Windows cho phép bạn thu thập dữ liệu từ Google Maps một cách dễ dàng thông qua giao diện đồ họa thân thiện. Ứng dụng sử dụng Apify API để truy cập và thu thập thông tin từ Google Maps.

### Tính năng chính:
- 🔍 Tìm kiếm địa điểm theo từ khóa và địa điểm
- 🎯 Bộ lọc nâng cao (danh mục, đánh giá, website)
- 📋 Thu thập chi tiết (reviews, hình ảnh, Q&A)
- ⭐ Add-ons premium (thông tin liên hệ, business leads)
- 📊 Xuất dữ liệu ra Excel, CSV, JSON
- 🌍 Hỗ trợ 70+ ngôn ngữ

## Cài đặt

### Yêu cầu hệ thống:
- Windows 10/11 (64-bit)
- RAM: Tối thiểu 4GB, khuyến nghị 8GB
- Dung lượng ổ cứng: 500MB trống
- Kết nối Internet

### Các bước cài đặt:

1. **Tải file cài đặt**
   - Tải file `GoogleMapsScraper_Setup.exe` từ trang releases
   - Chạy file với quyền Administrator

2. **Chạy installer**
   - Làm theo hướng dẫn trong installer
   - Chọn thư mục cài đặt (mặc định: `C:\Program Files\GoogleMapsScraper`)
   - Tạo shortcut trên Desktop (tùy chọn)

3. **Khởi động ứng dụng**
   - Double-click vào shortcut trên Desktop
   - Hoặc tìm "Google Maps Scraper" trong Start Menu

## Cấu hình API

### Bước 1: Đăng ký tài khoản Apify

1. Truy cập [https://console.apify.com](https://console.apify.com)
2. Click "Sign Up" để tạo tài khoản mới
3. Xác thực email và hoàn tất đăng ký

### Bước 2: Lấy API Token

1. Đăng nhập vào Apify Console
2. Vào **Settings** > **Integrations**
3. Copy API token (có dạng: `apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### Bước 3: Cấu hình trong ứng dụng

1. Mở Google Maps Scraper
2. Click **⚙️ Cài đặt** trên toolbar
3. Paste API token vào ô "API Token"
4. Click **🔍 Test kết nối** để kiểm tra
5. Click **💾 Lưu** để lưu cài đặt

## Sử dụng ứng dụng

### Giao diện chính

Ứng dụng có 5 tab chính:

1. **🔍 Tìm kiếm cơ bản** - Nhập từ khóa và địa điểm
2. **🎯 Bộ lọc nâng cao** - Lọc kết quả theo danh mục, đánh giá
3. **📋 Thu thập chi tiết** - Cấu hình thu thập reviews, hình ảnh
4. **⭐ Add-ons Premium** - Tính năng trả phí (contacts, leads)
5. **📊 Kết quả & Xuất dữ liệu** - Xem và xuất kết quả

### Thực hiện tìm kiếm cơ bản

1. **Nhập từ khóa tìm kiếm**
   - Mỗi từ khóa trên một dòng
   - Ví dụ: `restaurant`, `hotel`, `coffee shop`

2. **Nhập địa điểm**
   - Ví dụ: `Hanoi, Vietnam`, `New York, USA`
   - Có thể dùng tên thành phố, quốc gia

3. **Cấu hình tùy chọn**
   - Số lượng địa điểm: Để trống = thu thập tất cả
   - Ngôn ngữ: Chọn ngôn ngữ cho kết quả

4. **Bắt đầu thu thập**
   - Click **▶️ Bắt đầu thu thập**
   - Chờ quá trình hoàn thành

## Các tính năng chi tiết

### Tab Bộ lọc nâng cao

#### Danh mục địa điểm
- Chọn từ 4,000+ danh mục có sẵn
- Tìm kiếm danh mục bằng ô tìm kiếm
- Có thể chọn nhiều danh mục

#### Khớp tên
- **Tất cả kết quả**: Hiển thị mọi kết quả
- **Chỉ tên có chứa từ khóa**: Lọc theo tên chứa từ khóa
- **Chỉ tên khớp chính xác**: Chỉ hiển thị tên khớp hoàn toàn

#### Đánh giá tối thiểu
- Sử dụng slider để chọn mức đánh giá (2.0 - 4.5 sao)
- Tùy chọn "Chỉ địa điểm có reviews"

#### Website
- **Tất cả**: Không lọc theo website
- **Chỉ có website**: Chỉ địa điểm có website
- **Chỉ không có website**: Chỉ địa điểm không có website

### Tab Thu thập chi tiết

#### Thông tin chi tiết địa điểm
- **Thu thập trang chi tiết đầy đủ**: Bật để enable các tùy chọn khác
- **Thông tin đặt bàn**: Thu thập thông tin reservation
- **Kết quả web**: Thu thập phần "Web results"
- **Địa điểm bên trong**: Thu thập địa điểm trong mall, shopping center

#### Câu hỏi & Trả lời
- Số câu hỏi: 0 = chỉ câu đầu tiên, 999 = tất cả

#### Reviews
- Số reviews: 0 = tất cả reviews
- Từ ngày: Chỉ thu thập reviews từ ngày này
- Sắp xếp theo: Mới nhất, Liên quan nhất, Đánh giá cao/thấp nhất

#### Hình ảnh
- Số hình ảnh: 0 = không thu thập

### Tab Add-ons Premium

⚠️ **Cảnh báo**: Các tính năng này có phí bổ sung!

#### Thu thập thông tin liên hệ công ty
- Thu thập email công ty từ website
- Thu thập social media profiles
- Giá: $2/1,000 địa điểm có website

#### Thu thập thông tin business leads
- Thu thập thông tin nhân viên (tên, email, chức vụ, LinkedIn)
- Lọc theo phòng ban
- Giá: $5/1,000 leads

⚠️ **Cảnh báo GDPR**: Thông tin này chứa dữ liệu cá nhân. Chỉ sử dụng khi có lý do chính đáng.

## Xuất dữ liệu

### Các định dạng xuất

1. **Excel (.xlsx)**
   - Định dạng bảng tính
   - Hỗ trợ nhiều sheet
   - Tốt cho phân tích dữ liệu

2. **CSV (.csv)**
   - Định dạng văn bản đơn giản
   - Tương thích với nhiều ứng dụng
   - Kích thước file nhỏ

3. **JSON (.json)**
   - Định dạng dữ liệu có cấu trúc
   - Giữ nguyên cấu trúc dữ liệu
   - Tốt cho lập trình viên

### Các chế độ xem

1. **Tất cả dữ liệu**: Xuất toàn bộ thông tin
2. **Thông tin liên hệ**: Chỉ tên, địa chỉ, điện thoại, website
3. **Vị trí & đánh giá**: Tọa độ, đánh giá, số reviews
4. **Reviews**: Thông tin chi tiết về reviews
5. **Leads**: Thông tin business leads

### Cách xuất dữ liệu

1. Sau khi thu thập xong, chuyển sang tab **📊 Kết quả & Xuất dữ liệu**
2. Chọn định dạng xuất từ dropdown
3. Chọn chế độ xem
4. Tùy chọn "Chỉ xuất các dòng đã chọn" nếu muốn
5. Click **📤 Xuất dữ liệu**
6. Chọn vị trí lưu file
7. File sẽ được lưu trong thư mục Downloads/GoogleMapsScraper

## Xử lý sự cố

### Lỗi thường gặp

#### "API token chưa được cấu hình"
- **Nguyên nhân**: Chưa nhập API token
- **Giải pháp**: Vào Settings > API và nhập API token

#### "Không thể kết nối đến Apify"
- **Nguyên nhân**: API token không hợp lệ hoặc mất kết nối Internet
- **Giải pháp**: 
  - Kiểm tra kết nối Internet
  - Kiểm tra lại API token
  - Test kết nối trong Settings

#### "Không có dữ liệu để xuất"
- **Nguyên nhân**: Chưa thu thập dữ liệu hoặc thu thập thất bại
- **Giải pháp**: Thực hiện tìm kiếm trước khi xuất

#### "Run thất bại"
- **Nguyên nhân**: Lỗi từ phía Apify hoặc tham số không hợp lệ
- **Giải pháp**:
  - Kiểm tra lại tham số đầu vào
  - Thử lại sau vài phút
  - Liên hệ support nếu vấn đề tiếp tục

### Kiểm tra log

1. Vào thư mục cài đặt ứng dụng
2. Mở thư mục `logs`
3. Xem file log mới nhất để biết chi tiết lỗi

## FAQ

### Câu hỏi thường gặp

**Q: Tôi có thể thu thập bao nhiêu địa điểm?**
A: Không có giới hạn cứng, nhưng chi phí sẽ tăng theo số lượng. Khuyến nghị bắt đầu với 50-100 địa điểm để test.

**Q: Dữ liệu có được cập nhật real-time không?**
A: Dữ liệu được thu thập tại thời điểm chạy, không phải real-time. Để có dữ liệu mới nhất, cần chạy lại tìm kiếm.

**Q: Tôi có thể sử dụng ứng dụng mà không cần API token không?**
A: Không, API token là bắt buộc để kết nối với Apify và thu thập dữ liệu.

**Q: Chi phí sử dụng như thế nào?**
A: Apify sử dụng mô hình pay-per-event. Xem bảng giá trong tab Add-ons Premium hoặc tại [Apify Pricing](https://apify.com/pricing).

**Q: Dữ liệu có được lưu trữ trên server không?**
A: Dữ liệu chỉ được lưu trên máy tính của bạn. Apify không lưu trữ dữ liệu lâu dài.

**Q: Tôi có thể sử dụng ứng dụng trên Mac/Linux không?**
A: Hiện tại ứng dụng chỉ hỗ trợ Windows. Phiên bản Mac/Linux sẽ được phát triển trong tương lai.

**Q: Làm sao để tôi biết có bao nhiêu credits còn lại?**
A: Thông tin credits sẽ được hiển thị trong Settings > API sau khi kết nối thành công.

**Q: Tôi có thể hủy run đang chạy không?**
A: Có, click nút "⏹️ Dừng" trên toolbar để dừng run đang chạy.

**Q: Dữ liệu có bị giới hạn theo vùng địa lý không?**
A: Không, bạn có thể thu thập dữ liệu từ bất kỳ đâu trên thế giới.

**Q: Tôi có thể lưu cấu hình tìm kiếm không?**
A: Tính năng lưu/tải cấu hình sẽ được thêm trong phiên bản tiếp theo.

### Liên hệ hỗ trợ

Nếu bạn gặp vấn đề không được giải quyết trong hướng dẫn này:

1. **Kiểm tra log file** trong thư mục logs
2. **Tìm kiếm trên GitHub Issues** để xem có ai gặp vấn đề tương tự
3. **Tạo issue mới** trên GitHub với thông tin chi tiết
4. **Liên hệ qua email**: support@example.com

### Cập nhật ứng dụng

Ứng dụng sẽ tự động kiểm tra cập nhật khi khởi động. Bạn cũng có thể:

1. Vào Help > Check for Updates
2. Tải phiên bản mới từ trang releases
3. Cài đặt đè lên phiên bản cũ

---

**Chúc bạn sử dụng ứng dụng hiệu quả!** 🚀
