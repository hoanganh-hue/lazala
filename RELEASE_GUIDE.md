# Hướng dẫn Tạo Release và Upload File Installer

## Tổng quan

Tài liệu này hướng dẫn cách tạo release v1.0.0 và upload file installer `GoogleMapsScraper_Setup_v1.0.0.exe` lên GitHub Releases để người dùng có thể tải về.

## Phương án 1: Tự động với GitHub Actions (Khuyến nghị)

### Bước 1: Tạo và Push Tag

Chạy các lệnh sau để tạo tag và trigger GitHub Actions build:

```bash
# Tạo tag v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0 - Google Maps Scraper Desktop App"

# Push tag lên GitHub
git push origin v1.0.0
```

### Bước 2: Theo dõi GitHub Actions Build

1. Truy cập: https://github.com/hoanganh-hue/lazala/actions
2. Xem workflow "Build Windows Installer" đang chạy
3. Đợi khoảng 5-10 phút để build hoàn tất

### Bước 3: Kiểm tra Release

Sau khi workflow hoàn tất:

1. Truy cập: https://github.com/hoanganh-hue/lazala/releases
2. Sẽ thấy release mới "v1.0.0" với file installer
3. Link tải: `https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe`

### Bước 4: Cập nhật Release Notes (Tùy chọn)

1. Vào release v1.0.0
2. Click "Edit release"
3. Thêm nội dung từ template bên dưới
4. Save changes

## Phương án 2: Build Thủ công trên Windows

Nếu GitHub Actions không hoạt động, bạn có thể build thủ công:

### Bước 1: Build trên Windows

```cmd
# Chạy trên máy Windows
cd lazala
python build.py --clean
```

Kết quả:
- `dist/GoogleMapsScraper.exe` - Executable
- `installer/GoogleMapsScraper_Setup_v1.0.0.exe` - Installer

### Bước 2: Tạo GitHub Release Thủ công

1. Truy cập: https://github.com/hoanganh-hue/lazala/releases/new
2. Nhập:
   - **Tag**: `v1.0.0`
   - **Release title**: `Google Maps Scraper v1.0.0`
   - **Description**: Copy từ template bên dưới
3. Upload file: `installer/GoogleMapsScraper_Setup_v1.0.0.exe`
4. Click "Publish release"

## Template Release Notes

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

1. **Tải file installer**: [GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe) (~100-150MB)
2. **Chạy installer** - Double-click file `.exe` và làm theo hướng dẫn
3. **Khởi động** - Click icon "Google Maps Scraper" trên Desktop
4. **Cấu hình API**:
   - Đăng ký tài khoản miễn phí tại [Apify.com](https://apify.com)
   - Lấy API token từ Apify Console → Settings → Integrations
   - Nhập token trong Settings của ứng dụng

### 📋 Yêu cầu hệ thống

- Windows 10/11 (64-bit)
- 4GB RAM (khuyến nghị 8GB)
- 500MB dung lượng ổ cứng
- Kết nối Internet
- Apify API token (đăng ký miễn phí)

### 📚 Tài liệu

- [Hướng dẫn nhanh 5 phút](https://github.com/hoanganh-hue/lazala/blob/main/QUICK_START.md)
- [Hướng dẫn sử dụng chi tiết](https://github.com/hoanganh-hue/lazala/blob/main/docs/huong_dan_su_dung.md)
- [Hướng dẫn build từ source](https://github.com/hoanganh-hue/lazala/blob/main/WINDOWS_BUILD_GUIDE.md)
- [Báo cáo hoàn thiện dự án](https://github.com/hoanganh-hue/lazala/blob/main/docs/BAO_CAO_HOAN_THANH_DU_AN.md)

### 🐛 Known Issues

- 6/36 unit tests đang thất bại (sẽ được fix trong v1.0.1)
- Test coverage ở mức 68% (target: 80%+)

### 🔄 Changelog

Xem chi tiết tại [CHANGELOG.md](https://github.com/hoanganh-hue/lazala/blob/main/CHANGELOG.md)

### 🆘 Hỗ trợ

- **Issues**: [GitHub Issues](https://github.com/hoanganh-hue/lazala/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hoanganh-hue/lazala/discussions)
- **Documentation**: [README](https://github.com/hoanganh-hue/lazala/blob/main/README.md)

### 📈 Thống kê

- **Lines of code**: ~5,600 (production) + ~800 (tests)
- **Test coverage**: 68%
- **Tests**: 32/32 unit tests passed
- **Dependencies**: 7 main packages
- **Platform**: Windows 10/11 (64-bit)

### 🙏 Credits

Cảm ơn tất cả những người đã đóng góp vào dự án này!

---

**Full Changelog**: https://github.com/hoanganh-hue/lazala/commits/v1.0.0
```

## Kiểm tra Release

Sau khi tạo release, kiểm tra:

### 1. Link tải hoạt động

```bash
# Test download link
curl -L -o GoogleMapsScraper_Setup.exe \
  https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

### 2. File installer hợp lệ

- Kích thước: ~100-150MB
- Format: Windows Executable (.exe)
- Có thể chạy được trên Windows 10/11

### 3. Links trong README hoạt động

README.md đã có link tới release:
```markdown
[⬇️ Download GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)
```

## Troubleshooting

### Lỗi: GitHub Actions không chạy

**Nguyên nhân**: Workflow chỉ trigger khi push tag `v*`

**Giải pháp**:
```bash
# Xóa tag cũ (nếu có)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Tạo lại tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Lỗi: Build thất bại trên GitHub Actions

**Kiểm tra**:
1. Xem logs tại: https://github.com/hoanganh-hue/lazala/actions
2. Tìm lỗi trong build steps
3. Fix code và push lại
4. Xóa tag cũ và tạo tag mới

### Lỗi: File installer không được upload

**Kiểm tra**:
1. Build có tạo file `installer/GoogleMapsScraper_Setup_v1.0.0.exe` không
2. Workflow có step "Upload installer artifact" không
3. Xem logs của step "Create Release"

## Các bước tiếp theo

Sau khi release thành công:

### 1. Cập nhật README badges

```markdown
[![Release](https://img.shields.io/github/v/release/hoanganh-hue/lazala)](https://github.com/hoanganh-hue/lazala/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/hoanganh-hue/lazala/total)](https://github.com/hoanganh-hue/lazala/releases)
```

### 2. Thông báo release

- Đăng trên social media
- Gửi email cho users (nếu có)
- Update website (nếu có)

### 3. Monitor feedback

- Theo dõi GitHub Issues
- Kiểm tra download statistics
- Chuẩn bị hotfix nếu cần

## Script Tự động (create-release.sh)

Tạo file `create-release.sh` để tự động hóa:

```bash
#!/bin/bash

VERSION="1.0.0"
TAG="v${VERSION}"

echo "Creating release ${TAG}..."

# Check if tag exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "Tag ${TAG} already exists. Delete it first if you want to recreate."
    exit 1
fi

# Create and push tag
git tag -a "$TAG" -m "Release version ${VERSION}"
git push origin "$TAG"

echo "Tag ${TAG} created and pushed!"
echo "Check GitHub Actions: https://github.com/hoanganh-hue/lazala/actions"
echo "Check Release: https://github.com/hoanganh-hue/lazala/releases/tag/${TAG}"
```

Chạy script:
```bash
chmod +x create-release.sh
./create-release.sh
```

## Tóm tắt

**Cách nhanh nhất**:
```bash
# 1. Tạo tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 2. Push tag
git push origin v1.0.0

# 3. Đợi GitHub Actions build (5-10 phút)

# 4. Kiểm tra release
# https://github.com/hoanganh-hue/lazala/releases
```

**Kết quả**:
- ✅ Release v1.0.0 được tạo tự động
- ✅ File installer được upload
- ✅ Người dùng có thể tải về từ GitHub Releases
- ✅ Link download trong README hoạt động

---

**Lưu ý quan trọng**: 
- GitHub Actions cần quyền `contents: write` để tạo release
- Repository settings → Actions → General → Workflow permissions → "Read and write permissions"
