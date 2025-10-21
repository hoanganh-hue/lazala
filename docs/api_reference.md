# API Reference - Google Maps Scraper Desktop App

## Mục lục
1. [Tổng quan](#tổng-quan)
2. [Cấu trúc dự án](#cấu-trúc-dự-án)
3. [API Models](#api-models)
4. [Core Components](#core-components)
5. [UI Components](#ui-components)
6. [Configuration](#configuration)
7. [Error Handling](#error-handling)
8. [Testing](#testing)

## Tổng quan

Google Maps Scraper Desktop App được xây dựng với kiến trúc modular, sử dụng PyQt5 cho giao diện người dùng và tích hợp với Apify API để thu thập dữ liệu từ Google Maps.

### Kiến trúc tổng thể

```
src/
├── main.py                 # Entry point
├── config.py              # Configuration
├── api/                   # API layer
│   ├── apify_client.py    # Apify API client
│   ├── auth.py           # Authentication
│   └── models.py         # Data models
├── ui/                    # User interface
│   ├── main_window.py     # Main window
│   ├── search_tab.py      # Search tab
│   ├── filters_tab.py     # Filters tab
│   ├── details_tab.py     # Details tab
│   ├── addons_tab.py      # Add-ons tab
│   ├── results_tab.py     # Results tab
│   └── settings_dialog.py # Settings dialog
├── core/                  # Core business logic
│   ├── export_manager.py  # Export functionality
│   ├── data_processor.py  # Data processing
│   └── validator.py       # Input validation
└── utils/                 # Utilities
    ├── logger.py          # Logging
    ├── constants.py       # Constants
    └── helpers.py         # Helper functions
```

## Cấu trúc dự án

### Entry Point

**File**: `src/main.py`

```python
def main():
    """Main function để khởi động ứng dụng"""
    # Setup logging
    setup_logging()
    
    # Tạo QApplication
    app = QApplication(sys.argv)
    
    # Tạo và hiển thị main window
    main_window = MainWindow()
    main_window.show()
    
    # Chạy event loop
    sys.exit(app.exec_())
```

### Configuration

**File**: `src/config.py`

Chứa tất cả cấu hình ứng dụng:

```python
# API Configuration
APIFY_BASE_URL = "https://api.apify.com/v2"
APIFY_ACTOR_ID = "compass/crawler-google-places"

# App Configuration
APP_NAME = "Google Maps Scraper"
APP_VERSION = "1.0.0"

# UI Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "vi": "Tiếng Việt",
    # ... more languages
}
```

## API Models

### SearchInput

**File**: `src/api/models.py`

Model cho input parameters của Google Maps Scraper:

```python
@dataclass
class SearchInput:
    # Tham số cơ bản
    search_strings_array: List[str] = field(default_factory=list)
    location_query: Optional[str] = None
    max_crawled_places_per_search: Optional[int] = None
    language: str = "en"
    
    # Bộ lọc nâng cao
    category_filter_words: List[str] = field(default_factory=list)
    search_matching: str = "all"
    place_minimum_stars: Optional[str] = None
    website: str = "allPlaces"
    skip_closed_places: bool = False
    
    # Tùy chọn thu thập chi tiết
    scrape_place_detail_page: bool = False
    max_reviews: int = 0
    max_images: int = 0
    
    # Add-ons premium
    scrape_contacts: bool = False
    maximum_leads_enrichment_records: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API call"""
        # Implementation...
```

### SearchResult

Model cho kết quả tìm kiếm:

```python
@dataclass
class SearchResult:
    # Thông tin cơ bản
    title: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Đánh giá
    total_score: Optional[float] = None
    reviews_count: Optional[int] = None
    
    # Tọa độ
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Metadata
    scraped_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Tạo SearchResult từ dictionary"""
        # Implementation...
```

### RunStatus

Model cho trạng thái của một run:

```python
@dataclass
class RunStatus:
    run_id: str
    status: str  # RUNNING, SUCCEEDED, FAILED, TIMED-OUT, ABORTED
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    default_dataset_id: Optional[str] = None
    error_message: Optional[str] = None
    
    @property
    def is_running(self) -> bool:
        return self.status == "RUNNING"
    
    @property
    def is_succeeded(self) -> bool:
        return self.status == "SUCCEEDED"
    
    @property
    def is_failed(self) -> bool:
        return self.status in ["FAILED", "TIMED-OUT", "ABORTED"]
```

## Core Components

### ApifyClient

**File**: `src/api/apify_client.py`

Client để tương tác với Apify API:

```python
class ApifyClient:
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.base_url = APIFY_ACTOR_URL
    
    async def start_run(self, search_input: SearchInput) -> str:
        """Bắt đầu một run mới"""
        # Implementation...
    
    async def get_run_status(self, run_id: str) -> RunStatus:
        """Lấy trạng thái của run"""
        # Implementation...
    
    async def wait_for_completion(self, run_id: str, progress_callback=None) -> RunStatus:
        """Chờ run hoàn thành"""
        # Implementation...
    
    async def get_dataset_items(self, dataset_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lấy items từ dataset"""
        # Implementation...
    
    async def test_connection(self) -> bool:
        """Test kết nối API"""
        # Implementation...
```

### AuthManager

**File**: `src/api/auth.py`

Quản lý xác thực API token:

```python
class AuthManager:
    def __init__(self):
        self._token: Optional[str] = None
        self._load_token()
    
    def set_token(self, token: str) -> bool:
        """Set API token và lưu vào config file"""
        # Implementation...
    
    def get_token(self) -> Optional[str]:
        """Lấy API token hiện tại"""
        return self._token
    
    def has_token(self) -> bool:
        """Kiểm tra có API token không"""
        return self._token is not None and self._token.strip() != ""
    
    def validate_token_format(self, token: str) -> bool:
        """Validate format của API token"""
        # Implementation...
```

### ExportManager

**File**: `src/core/export_manager.py`

Quản lý xuất dữ liệu:

```python
class ExportManager:
    def __init__(self):
        self.export_dir = Path.home() / "Downloads" / "GoogleMapsScraper"
    
    def export_data(
        self, 
        results: List[SearchResult], 
        format_type: str, 
        view_type: str = "all"
    ) -> Optional[str]:
        """Xuất dữ liệu ra file"""
        # Implementation...
    
    def _export_excel(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to Excel file"""
        # Implementation...
    
    def _export_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to CSV file"""
        # Implementation...
    
    def _export_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to JSON file"""
        # Implementation...
```

### DataProcessor

**File**: `src/core/data_processor.py`

Xử lý và phân tích dữ liệu:

```python
class DataProcessor:
    def process_results(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Xử lý và phân tích kết quả"""
        # Implementation...
    
    def _calculate_statistics(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Tính toán thống kê"""
        # Implementation...
    
    def _clean_data(self, results: List[SearchResult]) -> List[SearchResult]:
        """Làm sạch dữ liệu"""
        # Implementation...
    
    def filter_results(
        self, 
        results: List[SearchResult], 
        filters: Dict[str, Any]
    ) -> List[SearchResult]:
        """Lọc kết quả theo điều kiện"""
        # Implementation...
    
    def deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Loại bỏ kết quả trùng lặp"""
        # Implementation...
    
    def sort_results(
        self, 
        results: List[SearchResult], 
        sort_by: str = "rating",
        reverse: bool = True
    ) -> List[SearchResult]:
        """Sắp xếp kết quả"""
        # Implementation...
```

### InputValidator

**File**: `src/core/validator.py`

Validate input parameters:

```python
class InputValidator:
    def validate_search_input(self, search_input: SearchInput) -> Tuple[bool, List[str]]:
        """Validate search input"""
        # Implementation...
    
    def validate_api_token(self, token: str) -> Tuple[bool, str]:
        """Validate API token format"""
        # Implementation...
    
    def validate_location(self, location: str) -> Tuple[bool, str]:
        """Validate location string"""
        # Implementation...
    
    def validate_search_term(self, term: str) -> Tuple[bool, str]:
        """Validate search term"""
        # Implementation...
    
    def sanitize_input(self, search_input: SearchInput) -> SearchInput:
        """Sanitize input data"""
        # Implementation...
```

## UI Components

### MainWindow

**File**: `src/ui/main_window.py`

Cửa sổ chính của ứng dụng:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.apify_client = ApifyClient(self.auth_manager)
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.search_tab = SearchTab()
        self.filters_tab = FiltersTab()
        self.details_tab = DetailsTab()
        self.addons_tab = AddonsTab()
        self.results_tab = ResultsTab()
        
        # Add tabs
        self.tab_widget.addTab(self.search_tab, "🔍 Tìm kiếm cơ bản")
        # ... more tabs
    
    def start_scraping(self):
        """Bắt đầu thu thập dữ liệu"""
        # Implementation...
    
    def get_search_input(self):
        """Lấy search input từ các tabs"""
        # Implementation...
```

### SearchTab

**File**: `src/ui/search_tab.py`

Tab tìm kiếm cơ bản:

```python
class SearchTab(QWidget):
    start_scraping_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
    
    def get_search_data(self):
        """Lấy dữ liệu tìm kiếm"""
        return {
            "search_strings": self.get_search_terms(),
            "location": self.location_input.text().strip(),
            "max_places": self.max_places_spin.value() if self.max_places_spin.value() > 0 else None,
            "language": self.language_combo.currentData()
        }
```

### ResultsTab

**File**: `src/ui/results_tab.py`

Tab hiển thị kết quả:

```python
class ResultsTab(QWidget):
    export_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.results = []
        self.export_manager = ExportManager()
        self.init_ui()
    
    def start_scraping(self, search_input: SearchInput):
        """Bắt đầu thu thập dữ liệu"""
        # Create and start scraping thread
        self.scraping_thread = ScrapingThread(self.apify_client, search_input)
        self.scraping_thread.start()
    
    def display_results(self, results: list):
        """Hiển thị kết quả"""
        self.results = results
        self.populate_table(results)
        self.update_results_info()
    
    def export_data(self):
        """Xuất dữ liệu"""
        # Implementation...
```

### ScrapingThread

Thread để chạy scraping trong background:

```python
class ScrapingThread(QThread):
    progress_updated = pyqtSignal(str, int)  # message, progress
    results_ready = pyqtSignal(list)  # results
    error_occurred = pyqtSignal(str)  # error message
    finished = pyqtSignal()
    
    def run(self):
        """Chạy scraping"""
        # Implementation...
```

## Configuration

### Environment Variables

Ứng dụng có thể được cấu hình thông qua các biến môi trường:

```bash
# Log level
GOOGLE_MAPS_SCRAPER_LOG_LEVEL=INFO

# API timeout
GOOGLE_MAPS_SCRAPER_TIMEOUT=60

# Export directory
GOOGLE_MAPS_SCRAPER_EXPORT_DIR=/path/to/export
```

### Config File

Cấu hình được lưu trong file `config.ini`:

```ini
[apify]
api_token = apify_api_your_token_here

[app]
default_language = vi
default_export_format = excel
auto_save_results = true
log_level = INFO

[advanced]
max_concurrent_requests = 3
request_timeout = 60
```

## Error Handling

### Exception Hierarchy

```python
class GoogleMapsScraperError(Exception):
    """Base exception for all application errors"""
    pass

class APIError(GoogleMapsScraperError):
    """API related errors"""
    pass

class ValidationError(GoogleMapsScraperError):
    """Input validation errors"""
    pass

class ExportError(GoogleMapsScraperError):
    """Export related errors"""
    pass
```

### Error Handling Patterns

```python
try:
    # API call
    result = await apify_client.start_run(search_input)
except aiohttp.ClientError as e:
    logger.error(f"Network error: {e}")
    raise APIError(f"Network error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise GoogleMapsScraperError(f"Unexpected error: {e}")
```

### Logging

```python
import logging
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Log levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── test_api.py          # API tests
├── test_core.py         # Core functionality tests
├── test_ui.py           # UI tests (if needed)
└── conftest.py          # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=src

# Run with verbose output
pytest -v
```

### Test Examples

```python
import pytest
from src.api.models import SearchInput
from src.core.validator import InputValidator

class TestInputValidator:
    def test_validate_search_input_valid(self):
        validator = InputValidator()
        search_input = SearchInput(
            search_strings_array=["restaurant"],
            location_query="Hanoi, Vietnam"
        )
        
        is_valid, errors = validator.validate_search_input(search_input)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_search_input_invalid(self):
        validator = InputValidator()
        search_input = SearchInput(
            search_strings_array=[],  # Empty
            location_query=""  # Empty
        )
        
        is_valid, errors = validator.validate_search_input(search_input)
        
        assert is_valid is False
        assert len(errors) > 0
```

### Mocking

```python
from unittest.mock import Mock, patch

@patch('aiohttp.ClientSession.get')
async def test_api_connection(mock_get):
    mock_response = Mock()
    mock_response.status = 200
    mock_get.return_value.__aenter__.return_value = mock_response
    
    client = ApifyClient(auth_manager)
    result = await client.test_connection()
    
    assert result is True
```

## Deployment

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller build.spec

# Output will be in dist/GoogleMapsScraper.exe
```

### Creating Installer

Sử dụng Inno Setup để tạo installer:

```inno
[Setup]
AppName=Google Maps Scraper
AppVersion=1.0.0
DefaultDirName={pf}\GoogleMapsScraper
DefaultGroupName=Google Maps Scraper
OutputDir=installer
OutputBaseFilename=GoogleMapsScraper_Setup

[Files]
Source: "dist\GoogleMapsScraper.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"
Source: "LICENSE"; DestDir: "{app}"

[Icons]
Name: "{group}\Google Maps Scraper"; Filename: "{app}\GoogleMapsScraper.exe"
Name: "{commondesktop}\Google Maps Scraper"; Filename: "{app}\GoogleMapsScraper.exe"
```

---

**Lưu ý**: Tài liệu này được cập nhật thường xuyên. Vui lòng kiểm tra phiên bản mới nhất trên GitHub.
