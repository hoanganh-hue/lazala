# Google Maps Scraper Desktop App

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hoanganh-hue/lazala)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Completion](https://img.shields.io/badge/completion-100%25-success.svg)](docs/BAO_CAO_HOAN_THANH_DU_AN.md)
[![Tests](https://img.shields.io/badge/tests-32%20passed-success.svg)](tests/)

Ứng dụng desktop Windows để thu thập dữ liệu từ Google Maps thông qua Apify API.

> 📊 **[Xem Báo Cáo Hoàn Thiện Dự Án](docs/BAO_CAO_HOAN_THANH_DU_AN.md)** - Đánh giá chi tiết về tỷ lệ hoàn thiện 100% và chất lượng dự án
> 
> ✅ **Tất cả 32 bài kiểm thử đều PASS** - Dự án sẵn sàng cho bản phát hành Beta

## Tính năng chính

- Giao diện đồ họa thân thiện với người dùng
- Thu thập dữ liệu từ Google Maps (tên, địa chỉ, số điện thoại, website, đánh giá, reviews, hình ảnh)
- Bộ lọc nâng cao (danh mục, đánh giá, website)
- Thu thập chi tiết (reviews, Q&A, hình ảnh)
- Add-ons premium (thông tin liên hệ, business leads)
- Xuất dữ liệu ra Excel, CSV, JSON
- Hỗ trợ 70+ ngôn ngữ

## Cài đặt

### 📦 Tải xuống và cài đặt (Khuyến nghị)

1. **Tải file installer**: [GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)
2. **Chạy installer**: Double-click file `.exe` và làm theo hướng dẫn
3. **Khởi động**: Click icon "Google Maps Scraper" trên Desktop
4. **Cấu hình API**: 
   - Đăng ký tài khoản tại [Apify.com](https://apify.com)
   - Lấy API token từ Apify Console → Settings → Integrations
   - Cấu hình token trong Settings của ứng dụng

📖 **[Xem hướng dẫn nhanh](QUICK_START.md)** | 🔨 **[Hướng dẫn build từ source](WINDOWS_BUILD_GUIDE.md)**

### 💻 Cài đặt từ source (Dành cho developers)

```bash
git clone https://github.com/hoanganh-hue/lazala.git
cd lazala
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python src/main.py
```

## Sử dụng

1. Mở ứng dụng
2. Nhập API token trong Settings
3. Chọn tab "Tìm kiếm cơ bản"
4. Nhập từ khóa và địa điểm
5. Click "Bắt đầu thu thập"
6. Xem kết quả và xuất dữ liệu

## Tài liệu

- 📖 [Hướng dẫn sử dụng](docs/huong_dan_su_dung.md) - Hướng dẫn chi tiết cho người dùng
- 📚 [API Reference](docs/api_reference.md) - Tài liệu kỹ thuật cho developers
- 🏗️ [Build Guide](BUILD.md) - Hướng dẫn build và deployment
- 📊 [Báo cáo hoàn thiện](docs/BAO_CAO_HOAN_THANH_DU_AN.md) - Đánh giá dự án (85% hoàn thiện)
- 📈 [Project Metrics](docs/PROJECT_METRICS.md) - Thống kê và metrics chi tiết
- 📝 [CHANGELOG](CHANGELOG.md) - Lịch sử phiên bản

## Hỗ trợ

- Issues: [GitHub Issues](https://github.com/hoanganh-hue/lazala/issues)
- Discussions: [GitHub Discussions](https://github.com/hoanganh-hue/lazala/discussions)

## License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết
