# Hướng dẫn Build ứng dụng Windows Desktop

## Tổng quan

Tài liệu này hướng dẫn chi tiết cách build ứng dụng **Google Maps Scraper** thành file cài đặt Windows (.exe) duy nhất, cho phép người dùng tải xuống và cài đặt ứng dụng desktop trên Windows.

## Kết quả cuối cùng

Sau khi hoàn tất, bạn sẽ có:
- 📦 **File installer**: `GoogleMapsScraper_Setup_v1.0.0.exe` 
- 💻 **Ứng dụng desktop Windows** với icon trên desktop
- 🚀 **Khởi động nhanh**: Click icon để mở ứng dụng GUI

## Yêu cầu hệ thống

### Hệ thống build (máy phát triển)
- **OS**: Windows 10/11 (64-bit) - **BẮT BUỘC**
- **Python**: 3.10, 3.11, hoặc 3.12
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB)
- **Dung lượng ổ cứng**: 5GB trống
- **Inno Setup**: 6.0 trở lên (để tạo installer)
- **Internet**: Kết nối ổn định để tải dependencies

### Hệ thống người dùng cuối
- **OS**: Windows 10/11 (64-bit)
- **RAM**: Tối thiểu 4GB
- **Dung lượng ổ cứng**: 500MB trống

## Bước 1: Cài đặt môi trường phát triển

### 1.1. Cài đặt Python

1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. **Quan trọng**: Chọn "Add Python to PATH" khi cài đặt
3. Xác nhận cài đặt:
   ```cmd
   python --version
   ```
   Phải hiển thị: `Python 3.10.x` hoặc cao hơn

### 1.2. Clone repository

```cmd
git clone https://github.com/hoanganh-hue/lazala.git
cd lazala
```

### 1.3. Tạo và kích hoạt Virtual Environment

```cmd
REM Tạo virtual environment
python -m venv venv

REM Kích hoạt virtual environment
venv\Scripts\activate

REM Xác nhận đã kích hoạt (dấu nhắc sẽ có (venv) ở đầu)
```

### 1.4. Cài đặt dependencies

```cmd
REM Cài đặt tất cả dependencies
pip install -r requirements.txt

REM Xác nhận PyInstaller đã được cài đặt
pyinstaller --version
```

### 1.5. Cài đặt Inno Setup (để tạo installer)

1. Tải Inno Setup từ [jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
2. Cài đặt với tùy chọn mặc định
3. Đảm bảo chọn "Add to PATH" khi cài đặt
4. Xác nhận cài đặt:
   ```cmd
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /?
   ```

## Bước 2: Kiểm tra ứng dụng trước khi build

### 2.1. Chạy tests

```cmd
REM Chạy tất cả unit tests
python run_tests.py --type unit

REM Kết quả mong đợi: 32 tests passed
```

### 2.2. Test chạy ứng dụng từ source

```cmd
REM Chạy ứng dụng trực tiếp
python src/main.py
```

Ứng dụng GUI sẽ mở lên. Kiểm tra các chức năng cơ bản:
- Giao diện hiển thị đúng
- Menu và tabs hoạt động
- Settings dialog mở được

Đóng ứng dụng sau khi kiểm tra.

## Bước 3: Build executable

### Tùy chọn 1: Build tự động (Khuyến nghị)

```cmd
REM Build đầy đủ với tests và installer
python build.py --clean

REM Hoặc build nhanh (bỏ qua tests)
python build.py --clean --skip-tests
```

### Tùy chọn 2: Build thủ công

#### Bước 3.1: Clean build directories

```cmd
REM Xóa thư mục build cũ
rmdir /s /q build
rmdir /s /q dist
```

#### Bước 3.2: Build với PyInstaller

```cmd
REM Build executable
pyinstaller build.spec

REM Kiểm tra kết quả
dir dist\GoogleMapsScraper.exe
```

Bạn sẽ thấy file `GoogleMapsScraper.exe` trong thư mục `dist/`.

#### Bước 3.3: Test executable

```cmd
REM Test chạy executable
dist\GoogleMapsScraper.exe
```

Ứng dụng sẽ mở lên như khi chạy từ source code.

## Bước 4: Tạo Windows Installer

### 4.1. Kiểm tra file installer.iss

File `installer.iss` đã được cấu hình sẵn với:
- Tên ứng dụng và version
- Thư mục cài đặt mặc định
- Desktop icon
- Start menu shortcuts
- Uninstaller

### 4.2. Build installer

```cmd
REM Tạo installer với Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

Hoặc sử dụng build script:

```cmd
python build.py
```

### 4.3. Kiểm tra kết quả

Bạn sẽ thấy file installer trong thư mục `installer/`:

```
installer/
  └── GoogleMapsScraper_Setup_v1.0.0.exe
```

Kích thước file: ~100-150MB (bao gồm Python runtime và tất cả dependencies)

## Bước 5: Test Installer

### 5.1. Test cài đặt

1. Double-click file `GoogleMapsScraper_Setup_v1.0.0.exe`
2. Chọn ngôn ngữ (English hoặc Vietnamese)
3. Đồng ý license và đọc thông tin
4. Chọn thư mục cài đặt (mặc định: `C:\Program Files\Google Maps Scraper`)
5. Chọn tạo desktop icon (khuyến nghị)
6. Click "Install"

### 5.2. Xác nhận cài đặt thành công

Sau khi cài đặt:
- ✅ Icon xuất hiện trên desktop: **Google Maps Scraper**
- ✅ Ứng dụng trong Start Menu: **Google Maps Scraper**
- ✅ Ứng dụng trong Programs and Features

### 5.3. Test chạy ứng dụng

1. Click icon trên desktop
2. Ứng dụng GUI mở lên
3. Test các chức năng:
   - Mở Settings
   - Nhập API token
   - Test kết nối
   - Tìm kiếm cơ bản

### 5.4. Test gỡ cài đặt

1. Mở Settings > Apps & Features (hoặc Control Panel > Programs and Features)
2. Tìm "Google Maps Scraper"
3. Click "Uninstall"
4. Chọn có/không giữ dữ liệu cấu hình
5. Xác nhận gỡ cài đặt thành công

## Bước 6: Phân phối và Deployment

### 6.1. Tạo release trên GitHub

```cmd
REM Tag version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Trên GitHub:
1. Vào repository → Releases → "Create a new release"
2. Chọn tag `v1.0.0`
3. Tiêu đề: "Google Maps Scraper v1.0.0"
4. Upload file `GoogleMapsScraper_Setup_v1.0.0.exe`
5. Viết release notes:

```markdown
## Google Maps Scraper v1.0.0

### Tính năng chính
- Thu thập dữ liệu từ Google Maps
- Giao diện đồ họa thân thiện
- Xuất dữ liệu Excel/CSV/JSON
- Hỗ trợ 70+ ngôn ngữ

### Cài đặt
1. Tải file `GoogleMapsScraper_Setup_v1.0.0.exe`
2. Chạy installer và làm theo hướng dẫn
3. Mở ứng dụng từ desktop icon

### Yêu cầu
- Windows 10/11 (64-bit)
- 4GB RAM
- Apify API token (đăng ký tại apify.com)
```

6. Publish release

### 6.2. Chia sẻ link download

Link download trực tiếp:
```
https://github.com/hoanganh-hue/lazala/releases/download/v1.0.0/GoogleMapsScraper_Setup_v1.0.0.exe
```

### 6.3. Cập nhật README

Cập nhật phần "Cài đặt" trong README.md:

```markdown
## Cài đặt

### Tải về
Tải phiên bản mới nhất từ [Releases](https://github.com/hoanganh-hue/lazala/releases)

### Cài đặt
1. Tải file `GoogleMapsScraper_Setup_v1.0.0.exe`
2. Double-click để chạy installer
3. Làm theo hướng dẫn trên màn hình
4. Click icon trên desktop để mở ứng dụng
```

## Cấu trúc thư mục sau khi cài đặt

```
C:\Program Files\Google Maps Scraper\
├── GoogleMapsScraper.exe          # Ứng dụng chính
├── README.md                       # Tài liệu
├── LICENSE                         # License
├── docs\                          # Tài liệu chi tiết
│   ├── huong_dan_su_dung.md
│   ├── api_reference.md
│   └── ...
├── logs\                          # Log files (tự động tạo)
└── cache\                         # Cache data (tự động tạo)

Desktop:
└── Google Maps Scraper.lnk        # Desktop shortcut

Start Menu:
└── Google Maps Scraper\
    ├── Google Maps Scraper.lnk
    └── Uninstall.lnk
```

## Troubleshooting

### Lỗi: "Python not found"
**Giải pháp**: Cài đặt Python và đảm bảo chọn "Add to PATH"

### Lỗi: "PyInstaller not found"
**Giải pháp**: 
```cmd
pip install pyinstaller
```

### Lỗi: "Inno Setup not found"
**Giải pháp**: Cài đặt Inno Setup hoặc cập nhật đường dẫn trong `build.py`

### Lỗi: "Module not found" khi chạy executable
**Giải pháp**: Thêm module vào `hiddenimports` trong `build.spec`

### Executable size quá lớn (>200MB)
**Giải pháp**: 
1. Loại bỏ unused imports trong code
2. Thêm packages vào `excludes` trong `build.spec`
3. Sử dụng UPX compression (optional)

### Ứng dụng khởi động chậm
**Nguyên nhân**: PyInstaller cần giải nén dependencies khi khởi động lần đầu
**Giải pháp**: Chấp nhận hoặc sử dụng `--onedir` thay vì `--onefile`

## Build Options chi tiết

### build.py options

```cmd
# Clean build directories
python build.py --clean

# Install dependencies trước khi build
python build.py --dependencies

# Skip tests (faster)
python build.py --skip-tests

# Skip installer creation (chỉ build executable)
python build.py --skip-installer

# Build đầy đủ
python build.py --clean --dependencies
```

### build.spec options

Chỉnh sửa `build.spec` để customize:

```python
# Console mode (hiện console window)
console=True  # Debug mode
console=False  # Production mode

# Single file vs directory
# Single file: tất cả trong 1 .exe
# Directory: .exe + dependencies trong folder

# Icon
icon="path/to/icon.ico"

# Excludes (giảm size)
excludes=['tkinter', 'matplotlib', 'scipy']
```

## Best Practices

### 1. Version Control
- Tag mỗi release: `git tag -a v1.0.0`
- Cập nhật CHANGELOG.md
- Cập nhật version trong `installer.iss` và `build.spec`

### 2. Testing
- Luôn chạy tests trước khi build
- Test executable trên máy sạch (không có Python)
- Test installer trên nhiều Windows versions

### 3. Security
- Không hardcode API keys
- Validate tất cả user input
- Sử dụng HTTPS cho API calls
- Sign executable với code signing certificate (optional)

### 4. Documentation
- Cập nhật user guide với screenshots
- Tạo video hướng dẫn
- FAQ cho các lỗi thường gặp

## Tài nguyên bổ sung

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

## Hỗ trợ

- **Issues**: [GitHub Issues](https://github.com/hoanganh-hue/lazala/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hoanganh-hue/lazala/discussions)

---

**Lưu ý quan trọng**: 
- Build **PHẢI** thực hiện trên Windows để tạo Windows executable
- Không thể build Windows .exe trên Linux/macOS
- Installer chỉ chạy được trên Windows 10/11 (64-bit)
