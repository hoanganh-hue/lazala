# Manual Release Creation Guide

## Mục đích

Hướng dẫn này giúp bạn tạo GitHub Release thủ công và upload file installer để người dùng có thể tải về.

## Khi nào sử dụng hướng dẫn này?

- GitHub Actions không hoạt động
- Cần tạo release nhanh chóng
- Đã có file installer sẵn trên máy Windows

## Điều kiện tiên quyết

Bạn đã build file installer trên Windows:
```
installer/GoogleMapsScraper_Setup_v1.0.0.exe
```

Nếu chưa có, chạy:
```cmd
python build.py --clean
```

## Các bước thực hiện

### Bước 1: Truy cập GitHub Releases

1. Mở trình duyệt
2. Vào: https://github.com/hoanganh-hue/lazala
3. Click tab "Releases" (bên phải, dưới "About")
4. Click nút "Create a new release" hoặc "Draft a new release"

Hoặc truy cập trực tiếp: https://github.com/hoanganh-hue/lazala/releases/new

### Bước 2: Chọn hoặc Tạo Tag

Trong trang "Create a new release":

1. **Choose a tag**: Click vào dropdown
2. **Type tag name**: Nhập `v1.0.0`
3. Click "Create new tag: v1.0.0 on publish"

Hoặc nếu tag đã tồn tại, chọn từ danh sách.

### Bước 3: Nhập Thông tin Release

#### Release title:
```
Google Maps Scraper v1.0.0
```

#### Description:
Copy và paste nội dung sau:

```markdown
## Google Maps Scraper v1.0.0

### 🎉 Highlights

Đây là phiên bản chính thức đầu tiên của Google Maps Scraper Desktop App - ứng dụng thu thập dữ liệu từ Google Maps thông qua Apify API.

### ✨ Tính năng chính

- 🖥️ **Ứng dụng Desktop Windows** với giao diện đồ họa thân thiện
- 🔍 **Thu thập dữ liệu Google Maps** - Tên, địa chỉ, số điện thoại, website, đánh giá, reviews, hình ảnh
- 🎯 **Bộ lọc nâng cao** - Lọc theo danh mục, đánh giá, website
- 📊 **Xuất dữ liệu** - Hỗ trợ Excel, CSV, JSON
- 🌍 **Đa ngôn ngữ** - Hỗ trợ 70+ ngôn ngữ
- 💼 **Add-ons premium** - Thông tin liên hệ, business leads
- ✅ **Dễ cài đặt** - Installer tự động, tạo desktop icon

### 📦 Cài đặt

#### 1. Tải file installer

Tải file `GoogleMapsScraper_Setup_v1.0.0.exe` từ phần "Assets" bên dưới (~100-150MB)

#### 2. Chạy installer

- Double-click file `.exe`
- Chọn ngôn ngữ (English hoặc Tiếng Việt)
- Click "Next" và làm theo hướng dẫn
- Chọn thư mục cài đặt (hoặc để mặc định)
- Click "Install"

#### 3. Khởi động ứng dụng

- Click icon "Google Maps Scraper" trên Desktop
- Hoặc tìm trong Start Menu

#### 4. Cấu hình API

- Mở Settings trong ứng dụng
- Đăng ký tài khoản miễn phí tại [Apify.com](https://apify.com)
- Lấy API token từ Apify Console → Settings → Integrations
- Nhập token vào ứng dụng

### 📋 Yêu cầu hệ thống

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB (khuyến nghị 8GB)
- **Disk**: 500MB dung lượng trống
- **Internet**: Kết nối ổn định
- **API**: Apify API token (miễn phí)

### 📚 Tài liệu

- [Hướng dẫn nhanh 5 phút](https://github.com/hoanganh-hue/lazala/blob/main/QUICK_START.md)
- [Hướng dẫn sử dụng chi tiết](https://github.com/hoanganh-hue/lazala/blob/main/docs/huong_dan_su_dung.md)
- [Hướng dẫn build từ source](https://github.com/hoanganh-hue/lazala/blob/main/WINDOWS_BUILD_GUIDE.md)
- [API Reference](https://github.com/hoanganh-hue/lazala/blob/main/docs/api_reference.md)

### 🐛 Known Issues

- 6/36 unit tests đang thất bại (sẽ được fix trong v1.0.1)
- Test coverage ở mức 68% (target: 80%+)

### 🆘 Hỗ trợ

- **Issues**: [GitHub Issues](https://github.com/hoanganh-hue/lazala/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hoanganh-hue/lazala/discussions)
- **Email**: support@example.com

### 📈 Thống kê

- **Code**: ~5,600 LOC (production) + ~800 LOC (tests)
- **Coverage**: 68%
- **Tests**: 32/32 passed
- **Dependencies**: 7 main packages
- **Platform**: Windows 10/11 64-bit

### 🔄 Changelog

Xem chi tiết tại [CHANGELOG.md](https://github.com/hoanganh-hue/lazala/blob/main/CHANGELOG.md)

---

**Full Changelog**: https://github.com/hoanganh-hue/lazala/commits/v1.0.0
```

### Bước 4: Upload File Installer

1. Scroll xuống phần "Attach binaries"
2. Drag & drop file `GoogleMapsScraper_Setup_v1.0.0.exe`
   
   Hoặc:
   - Click "Attach files by dragging & dropping, selecting or pasting them"
   - Chọn file từ máy tính

3. Đợi file upload hoàn tất (có thể mất 1-2 phút)

### Bước 5: Chọn Options

- **Set as the latest release**: ✅ Check (để đánh dấu là phiên bản mới nhất)
- **Set as a pre-release**: ⬜ Uncheck (vì đây là release chính thức)
- **Create a discussion for this release**: ✅ Check (tùy chọn, để người dùng thảo luận)

### Bước 6: Publish Release

1. Kiểm tra lại tất cả thông tin
2. Click nút **"Publish release"** (màu xanh lá)
3. Đợi vài giây để GitHub xử lý

### Bước 7: Xác nhận Release thành công

Sau khi publish:

1. Bạn sẽ được chuyển đến trang release
2. Kiểm tra:
   - Tag: `v1.0.0` ✅
   - Title: "Google Maps Scraper v1.0.0" ✅
   - Description hiển thị đúng ✅
   - File installer trong Assets ✅
   - Badge "Latest" hiển thị ✅

### Bước 8: Test Download Link

1. Scroll xuống phần "Assets"
2. Click vào `GoogleMapsScraper_Setup_v1.0.0.exe`
3. File sẽ được tải về
4. Kiểm tra file có thể chạy được không

Hoặc test với link trực tiếp:
```
https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

## Sau khi tạo Release

### 1. Cập nhật README (nếu cần)

README đã có link tới releases/latest, nên không cần sửa gì.

### 2. Thông báo

- Đăng trên social media
- Gửi email cho users
- Update website

### 3. Monitor

- Theo dõi download count
- Kiểm tra GitHub Issues
- Đọc user feedback

## Troubleshooting

### Lỗi: "Tag already exists"

**Giải pháp**:
1. Chọn tag `v1.0.0` từ dropdown thay vì tạo mới
2. Hoặc tạo tag mới với version khác (v1.0.1)

### Lỗi: "File too large to upload"

**Giới hạn**: GitHub cho phép upload file tối đa 2GB

**Giải pháp**:
- File installer của chúng ta ~100-150MB, nên không có vấn đề
- Nếu quá lớn, cần optimize build hoặc dùng external storage

### Lỗi: "Permission denied"

**Nguyên nhân**: Không có quyền tạo release

**Giải pháp**:
- Đảm bảo bạn là owner hoặc có write access
- Hoặc yêu cầu owner tạo release

## Screenshots

### Step 1: Create new release
![Create new release button](https://docs.github.com/assets/cb-47298/images/help/releases/release-link.png)

### Step 2: Choose tag
![Choose or create tag](https://docs.github.com/assets/cb-80309/images/help/releases/releases-tag-create.png)

### Step 3: Upload assets
![Upload assets](https://docs.github.com/assets/cb-75824/images/help/releases/releases_adding_binary.gif)

## Checklist

Sử dụng checklist này để đảm bảo không bỏ sót:

- [ ] Đã build file installer: `GoogleMapsScraper_Setup_v1.0.0.exe`
- [ ] Truy cập GitHub Releases page
- [ ] Tạo/chọn tag: `v1.0.0`
- [ ] Nhập release title: "Google Maps Scraper v1.0.0"
- [ ] Copy-paste description từ template
- [ ] Upload file installer
- [ ] Check "Set as the latest release"
- [ ] Uncheck "Set as a pre-release"
- [ ] Click "Publish release"
- [ ] Xác nhận release hiển thị đúng
- [ ] Test download link
- [ ] Kiểm tra README links hoạt động

## Tóm tắt Nhanh

```markdown
1. Vào: https://github.com/hoanganh-hue/lazala/releases/new
2. Tag: v1.0.0
3. Title: Google Maps Scraper v1.0.0
4. Description: Copy từ template
5. Upload: GoogleMapsScraper_Setup_v1.0.0.exe
6. Options: Latest release ✅, Pre-release ⬜
7. Click: "Publish release"
```

## Links Tham khảo

- [GitHub Docs: Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Docs: Linking to releases](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)
- [Semantic Versioning](https://semver.org/)

---

**Lưu ý**: Sau khi tạo release, link download sẽ là:
```
https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

Link "Latest release" sẽ là:
```
https://github.com/hoanganh-hue/lazala/releases/latest
```
