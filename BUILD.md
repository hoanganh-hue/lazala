# Build & Deploy Guide - Google Maps Scraper Desktop App

## Mục lục
1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt môi trường phát triển](#cài-đặt-môi-trường-phát-triển)
3. [Build ứng dụng](#build-ứng-dụng)
4. [Tạo installer](#tạo-installer)
5. [Testing](#testing)
6. [Deployment](#deployment)

## Yêu cầu hệ thống

### Phát triển
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.10 hoặc cao hơn
- **RAM**: Tối thiểu 8GB, khuyến nghị 16GB
- **Dung lượng ổ cứng**: 2GB trống
- **Internet**: Kết nối ổn định

### Build
- **PyInstaller**: 6.3.0+
- **Inno Setup**: 6.0+ (để tạo installer)
- **Git**: Để clone repository

## Cài đặt môi trường phát triển

### Bước 1: Clone repository

```bash
git clone https://github.com/yourusername/google-maps-scraper-app.git
cd google-maps-scraper-app
```

### Bước 2: Tạo virtual environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt development dependencies
pip install pytest pytest-cov black flake8
```

### Bước 4: Cấu hình môi trường

```bash
# Copy file cấu hình mẫu
copy env.example .env

# Chỉnh sửa file .env với thông tin của bạn
notepad .env
```

## Build ứng dụng

### Sử dụng build script (Khuyến nghị)

```bash
# Build đầy đủ (clean + test + build + installer)
python build.py --clean --dependencies

# Build nhanh (bỏ qua tests)
python build.py --skip-tests

# Chỉ build executable (không tạo installer)
python build.py --skip-installer
```

### Build thủ công

#### Bước 1: Clean build directories

```bash
# Xóa các thư mục build cũ
rmdir /s build dist __pycache__
```

#### Bước 2: Chạy tests

```bash
# Chạy unit tests
python run_tests.py --type unit

# Chạy tất cả tests
python run_tests.py --type all
```

#### Bước 3: Build executable

```bash
# Build với PyInstaller
pyinstaller build.spec
```

#### Bước 4: Kiểm tra kết quả

```bash
# Kiểm tra file executable
dir dist\GoogleMapsScraper.exe

# Test chạy ứng dụng
dist\GoogleMapsScraper.exe
```

## Tạo installer

### Cài đặt Inno Setup

1. Tải Inno Setup từ [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
2. Cài đặt với cài đặt mặc định
3. Đảm bảo Inno Setup được thêm vào PATH

### Tạo installer

```bash
# Sử dụng build script
python build.py

# Hoặc chạy trực tiếp
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Kết quả

- **Executable**: `dist/GoogleMapsScraper.exe`
- **Installer**: `installer/GoogleMapsScraper_Setup_v1.0.0.exe`

## Testing

### Chạy tests

```bash
# Chạy tất cả tests
python run_tests.py

# Chạy unit tests
python run_tests.py --type unit

# Chạy với coverage
python run_tests.py --coverage

# Chạy tests cụ thể
pytest tests/test_api.py -v
```

### Test coverage

```bash
# Tạo coverage report
pytest --cov=src --cov-report=html

# Xem report
start htmlcov/index.html
```

### Manual testing

1. **Test cài đặt**:
   - Chạy installer
   - Kiểm tra ứng dụng được cài đặt đúng
   - Test uninstall

2. **Test chức năng**:
   - Cấu hình API token
   - Thực hiện tìm kiếm cơ bản
   - Test các tính năng nâng cao
   - Test xuất dữ liệu

3. **Test UI**:
   - Kiểm tra responsive design
   - Test trên các độ phân giải khác nhau
   - Test accessibility

## Deployment

### Chuẩn bị release

1. **Cập nhật version**:
   ```python
   # Trong src/__init__.py
   __version__ = "1.0.1"
   ```

2. **Cập nhật changelog**:
   ```markdown
   # CHANGELOG.md
   ## [1.0.1] - 2024-01-15
   - Fixed bug in export functionality
   - Improved error handling
   ```

3. **Build release**:
   ```bash
   python build.py --clean --dependencies
   ```

### Tạo GitHub Release

1. **Tag version**:
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   git push origin v1.0.1
   ```

2. **Tạo release trên GitHub**:
   - Vào GitHub repository
   - Click "Releases" > "Create a new release"
   - Chọn tag v1.0.1
   - Upload installer file
   - Viết release notes

### Distribution

#### GitHub Releases
- Upload installer file lên GitHub Releases
- Cung cấp link download trực tiếp

#### Website
- Tạo trang download trên website
- Cung cấp thông tin chi tiết về ứng dụng

#### Social Media
- Thông báo release trên các kênh social media
- Cung cấp screenshots và demo video

## Troubleshooting

### Lỗi thường gặp

#### "Module not found" khi build
```bash
# Kiểm tra dependencies
pip list

# Cài đặt lại dependencies
pip install -r requirements.txt --force-reinstall
```

#### "PyInstaller failed"
```bash
# Kiểm tra spec file
pyinstaller --debug build.spec

# Build với verbose output
pyinstaller --log-level=DEBUG build.spec
```

#### "Inno Setup not found"
- Đảm bảo Inno Setup đã được cài đặt
- Kiểm tra đường dẫn trong build.py
- Cập nhật đường dẫn nếu cần

#### "Tests failing"
```bash
# Chạy tests với verbose output
pytest -v

# Chạy test cụ thể
pytest tests/test_api.py::TestSearchInput::test_to_dict_basic -v
```

### Performance optimization

#### Build time
- Sử dụng `--skip-tests` cho development builds
- Sử dụng `--onefile` thay vì `--onedir` nếu cần

#### Executable size
- Loại bỏ unused imports
- Sử dụng `excludes` trong PyInstaller spec
- Compress với UPX (nếu cần)

#### Runtime performance
- Sử dụng async/await cho API calls
- Implement caching cho dữ liệu
- Optimize UI updates

## CI/CD

### GitHub Actions

Tạo file `.github/workflows/build.yml`:

```yaml
name: Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: python run_tests.py --type unit
    
    - name: Build executable
      run: python build.py --skip-installer
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: executable
        path: dist/GoogleMapsScraper.exe
```

### Automated releases

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build installer
      run: python build.py
    
    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

## Best Practices

### Code Quality
- Sử dụng type hints
- Viết docstrings cho functions
- Follow PEP 8 style guide
- Sử dụng linter (flake8, black)

### Testing
- Viết tests cho mọi function
- Sử dụng mocking cho external dependencies
- Maintain test coverage > 80%
- Test trên nhiều Python versions

### Security
- Không hardcode API keys
- Validate tất cả user input
- Sử dụng secure file handling
- Regular security updates

### Performance
- Profile code để tìm bottlenecks
- Sử dụng async programming
- Implement proper error handling
- Monitor memory usage

---

**Lưu ý**: Hướng dẫn này được cập nhật thường xuyên. Vui lòng kiểm tra phiên bản mới nhất trên GitHub.
