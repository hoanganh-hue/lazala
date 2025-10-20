# Google Maps Scraper Desktop App

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hoanganh-hue/lazala)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Completion](https://img.shields.io/badge/completion-100%25-success.svg)](docs/BAO_CAO_HOAN_THANH_DU_AN.md)
[![Tests](https://img.shields.io/badge/tests-32%20passed-success.svg)](tests/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)

Ứng dụng desktop Windows để thu thập dữ liệu từ Google Maps thông qua Apify API.

## 🎯 Cài đặt Nhanh (3 phút)

### 📦 Tải về và Cài đặt

**[⬇️ Tải GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)**

1. **Tải file installer** từ link trên (100-150MB)
2. **Chạy installer** - Double-click file `.exe`
3. **Hoàn tất cài đặt** - Chọn ngôn ngữ và thư mục cài đặt
4. **Khởi động** - Click icon "Google Maps Scraper" trên Desktop

📖 **[Hướng dẫn chi tiết](QUICK_START.md)** | 🔨 **[Build từ source](WINDOWS_BUILD_GUIDE.md)**

> 📊 **[Xem Báo Cáo Hoàn Thiện Dự Án](docs/BAO_CAO_HOAN_THANH_DU_AN.md)** - Đánh giá chi tiết về tỷ lệ hoàn thiện 100% và chất lượng dự án
> 
> ✅ **Tất cả 32 bài kiểm thử đều PASS** - Dự án sẵn sàng cho bản phát hành Beta

## Tính năng chính

- 🖥️ **Ứng dụng Desktop Windows** - Giao diện đồ họa thân thiện với người dùng
- 🔍 **Thu thập dữ liệu Google Maps** - Tên, địa chỉ, số điện thoại, website, đánh giá, reviews, hình ảnh
- 🎯 **Bộ lọc nâng cao** - Danh mục, đánh giá, website
- 📊 **Xuất dữ liệu** - Excel, CSV, JSON
- 🌍 **Đa ngôn ngữ** - Hỗ trợ 70+ ngôn ngữ
- 💼 **Add-ons premium** - Thông tin liên hệ, business leads
- ✅ **Dễ cài đặt** - 1 file installer duy nhất, tự động tạo desktop icon

## Cài đặt

### 📦 Tải xuống và cài đặt (Khuyến nghị - Cho người dùng cuối)

**[⬇️ Download GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)**

1. **Tải file installer** từ GitHub Releases (~100-150MB)
2. **Chạy installer** - Double-click file `.exe` và làm theo hướng dẫn
3. **Khởi động** - Click icon "Google Maps Scraper" trên Desktop
4. **Cấu hình API**: 
   - Đăng ký tài khoản miễn phí tại [Apify.com](https://apify.com)
   - Lấy API token từ Apify Console → Settings → Integrations
   - Cấu hình token trong Settings của ứng dụng

**Yêu cầu hệ thống:**
- Windows 10/11 (64-bit)
- 4GB RAM (khuyến nghị 8GB)
- 500MB dung lượng ổ cứng
- Kết nối Internet

📖 **[Hướng dẫn nhanh 5 phút](QUICK_START.md)** | 🔨 **[Build từ source code](WINDOWS_BUILD_GUIDE.md)**

### 💻 Cài đặt từ source (Dành cho developers)

```bash
# Clone repository
git clone https://github.com/hoanganh-hue/lazala.git
cd lazala

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python src/main.py

# Hoặc build executable
python build.py --clean
```

## Sử dụng

1. Mở ứng dụng
2. Nhập API token trong Settings
3. Chọn tab "Tìm kiếm cơ bản"
4. Nhập từ khóa và địa điểm
5. Click "Bắt đầu thu thập"
6. Xem kết quả và xuất dữ liệu

## Tài liệu

- 📖 **[Hướng dẫn nhanh](QUICK_START.md)** - Cài đặt và sử dụng trong 5 phút
- 🔨 **[Hướng dẫn Build](WINDOWS_BUILD_GUIDE.md)** - Build ứng dụng từ source code
- 📋 **[Tóm tắt Giải pháp](BUILD_SOLUTION_SUMMARY.md)** - Tổng quan build & deployment
- 📚 **[Hướng dẫn sử dụng](docs/huong_dan_su_dung.md)** - Hướng dẫn chi tiết cho người dùng
- 🔧 **[API Reference](docs/api_reference.md)** - Tài liệu kỹ thuật cho developers
- 📊 **[Báo cáo hoàn thiện](docs/BAO_CAO_HOAN_THANH_DU_AN.md)** - Đánh giá dự án (100% hoàn thiện)
- 📈 **[Project Metrics](docs/PROJECT_METRICS.md)** - Thống kê và metrics chi tiết
- ✅ **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Checklist triển khai
- 📝 **[CHANGELOG](CHANGELOG.md)** - Lịch sử phiên bản

## Hỗ trợ

- Issues: [GitHub Issues](https://github.com/hoanganh-hue/lazala/issues)
- Discussions: [GitHub Discussions](https://github.com/hoanganh-hue/lazala/discussions)

## License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết
