# 🚀 Hướng dẫn Tạo Release và Upload Installer

## 📋 Tổng quan

Tài liệu này hướng dẫn bạn tạo GitHub Release cho ứng dụng Google Maps Scraper và upload file installer để người dùng có thể tải về từ link:
```
https://github.com/hoanganh-hue/lazala/releases/new
```

## ✅ Điều kiện đã hoàn thành

Repository đã có đầy đủ:
- ✅ Build scripts (build.py, build.spec)
- ✅ Installer configuration (installer.iss)
- ✅ GitHub Actions workflow (build-windows.yml)
- ✅ Documentation (README, QUICK_START, BUILD_GUIDE)
- ✅ Release scripts (create-release.sh, create-release.bat)
- ✅ Version 1.0.0 đã được cấu hình

## 🎯 Hai phương án để tạo Release

### Phương án 1: Tự động với GitHub Actions (Khuyến nghị) ⭐

Chỉ cần chạy 2 lệnh:

```bash
# Tạo tag v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag lên GitHub
git push origin v1.0.0
```

**Hoặc sử dụng script tự động**:

**Trên Windows:**
```cmd
create-release.bat
```

**Trên Linux/Mac:**
```bash
./create-release.sh
```

**Sau đó:**
1. GitHub Actions sẽ tự động build (5-10 phút)
2. Tạo release v1.0.0 tự động
3. Upload file installer tự động
4. Link download sẵn sàng: `https://github.com/hoanganh-hue/lazala/releases/latest`

📖 **Chi tiết**: Xem [RELEASE_GUIDE.md](RELEASE_GUIDE.md)

---

### Phương án 2: Thủ công (Nếu GitHub Actions không hoạt động)

#### Bước 1: Build trên Windows

Chạy trên máy Windows 10/11:
```cmd
# Clone repo (nếu chưa có)
git clone https://github.com/hoanganh-hue/lazala.git
cd lazala

# Build
python build.py --clean
```

Kết quả:
- `dist/GoogleMapsScraper.exe` (~100MB)
- `installer/GoogleMapsScraper_Setup_v1.0.0.exe` (~100-150MB)

#### Bước 2: Tạo Release thủ công

1. Vào: https://github.com/hoanganh-hue/lazala/releases/new
2. Nhập:
   - **Tag**: `v1.0.0`
   - **Title**: `Google Maps Scraper v1.0.0`
   - **Description**: Copy từ template trong MANUAL_RELEASE_GUIDE.md
3. Upload file: `installer/GoogleMapsScraper_Setup_v1.0.0.exe`
4. Click "Publish release"

📖 **Chi tiết**: Xem [MANUAL_RELEASE_GUIDE.md](MANUAL_RELEASE_GUIDE.md)

---

## 🔍 Kiểm tra sau khi tạo Release

### 1. Kiểm tra Release page
Truy cập: https://github.com/hoanganh-hue/lazala/releases

Xác nhận:
- ✅ Release v1.0.0 hiển thị
- ✅ Badge "Latest" có hiển thị
- ✅ File installer trong Assets
- ✅ Release notes hiển thị đúng

### 2. Test download link

Link trực tiếp:
```
https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

Link latest:
```
https://github.com/hoanganh-hue/lazala/releases/latest
```

### 3. Kiểm tra README links

README đã có sẵn links:
```markdown
[⬇️ Tải GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)
```

Các links này sẽ hoạt động ngay sau khi release được tạo.

---

## 📚 Tài liệu Tham khảo

| Tài liệu | Mô tả |
|----------|-------|
| [RELEASE_GUIDE.md](RELEASE_GUIDE.md) | Hướng dẫn tự động với GitHub Actions |
| [MANUAL_RELEASE_GUIDE.md](MANUAL_RELEASE_GUIDE.md) | Hướng dẫn tạo release thủ công |
| [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) | Hướng dẫn build trên Windows |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Checklist triển khai |
| [QUICK_START.md](QUICK_START.md) | Hướng dẫn cho người dùng cuối |

---

## 🛠️ Troubleshooting

### Lỗi: "Tag already exists"

Nếu tag v1.0.0 đã tồn tại:

```bash
# Xóa tag local
git tag -d v1.0.0

# Xóa tag remote
git push origin :refs/tags/v1.0.0

# Tạo lại tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Lỗi: GitHub Actions không chạy

Kiểm tra:
1. Repository Settings → Actions → General
2. Workflow permissions: "Read and write permissions" ✅
3. Allow GitHub Actions to create and approve pull requests ✅

### Lỗi: Build thất bại trên GitHub Actions

1. Xem logs: https://github.com/hoanganh-hue/lazala/actions
2. Tìm step bị lỗi
3. Fix code và push lại
4. Xóa tag cũ và tạo tag mới

### Lỗi: File quá lớn để upload

GitHub cho phép upload file tối đa 2GB. File installer của chúng ta ~100-150MB nên không có vấn đề.

---

## 📊 Workflow Tự động (GitHub Actions)

Khi bạn push tag `v1.0.0`, GitHub Actions sẽ:

```
1. Checkout code
2. Setup Python 3.10
3. Install dependencies
4. Run tests (32 tests)
5. Build executable với PyInstaller
6. Install Inno Setup
7. Create installer
8. Upload artifacts
9. Create GitHub Release
10. Upload installer to release
```

Thời gian: ~5-10 phút

Xem workflow tại: `.github/workflows/build-windows.yml`

---

## 🎉 Sau khi Release thành công

### Link tải sẽ hoạt động:

**Latest release:**
```
https://github.com/hoanganh-hue/lazala/releases/latest
```

**Direct download:**
```
https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

### README links sẽ hoạt động:

```markdown
[⬇️ Download GoogleMapsScraper_Setup_v1.0.0.exe](https://github.com/hoanganh-hue/lazala/releases/latest)
```

### Người dùng có thể:

1. Vào GitHub Releases
2. Tải file installer
3. Cài đặt ứng dụng
4. Click icon trên Desktop
5. Sử dụng ứng dụng

---

## ⚡ Quick Start (Tóm tắt nhanh)

**Cách nhanh nhất để tạo release:**

```bash
# Phương án 1: Dùng script
./create-release.sh  # hoặc create-release.bat trên Windows

# Phương án 2: Thủ công
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

**Đợi 5-10 phút → Release sẵn sàng!**

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Xem [RELEASE_GUIDE.md](RELEASE_GUIDE.md) hoặc [MANUAL_RELEASE_GUIDE.md](MANUAL_RELEASE_GUIDE.md)
2. Kiểm tra [GitHub Actions logs](https://github.com/hoanganh-hue/lazala/actions)
3. Tạo issue tại: https://github.com/hoanganh-hue/lazala/issues

---

**Lưu ý**: Repository này đang chạy trong môi trường Linux. Để build file .exe Windows, bạn cần:
- Sử dụng GitHub Actions (khuyến nghị - tự động build trên Windows)
- Hoặc build thủ công trên máy Windows

File exe **KHÔNG THỂ** build trên Linux, chỉ có thể build trên Windows hoặc qua GitHub Actions với Windows runner.
