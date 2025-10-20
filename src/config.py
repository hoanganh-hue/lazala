"""
Cấu hình ứng dụng Google Maps Scraper
"""

import os
from pathlib import Path

# Đường dẫn thư mục gốc của ứng dụng
APP_DIR = Path(__file__).parent.parent
SRC_DIR = APP_DIR / "src"
RESOURCES_DIR = APP_DIR / "resources"
LOGS_DIR = APP_DIR / "logs"

# Tạo thư mục logs nếu chưa có
LOGS_DIR.mkdir(exist_ok=True)

# Cấu hình API
APIFY_BASE_URL = "https://api.apify.com/v2"
APIFY_ACTOR_ID = "compass/crawler-google-places"
APIFY_ACTOR_URL = f"{APIFY_BASE_URL}/acts/{APIFY_ACTOR_ID}"

# Cấu hình ứng dụng
APP_NAME = "Google Maps Scraper"
APP_VERSION = "1.0.0"
CONFIG_FILE = APP_DIR / "config.ini"

# Cấu hình UI
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Cấu hình API polling
POLL_INTERVAL = 5  # seconds
MAX_POLL_ATTEMPTS = 360  # 30 minutes max

# Cấu hình export
DEFAULT_EXPORT_FORMAT = "excel"
SUPPORTED_EXPORT_FORMATS = ["excel", "csv", "json"]

# Cấu hình logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

# Ngôn ngữ hỗ trợ
SUPPORTED_LANGUAGES = {
    "en": "English",
    "vi": "Tiếng Việt", 
    "ja": "日本語",
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文",
    "ko": "한국어",
    "th": "ไทย",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "ru": "Русский",
    "ar": "العربية",
    "hi": "हिन्दी"
}

# Các giá trị enum cho API
SEARCH_MATCHING_OPTIONS = {
    "all": "Tất cả kết quả",
    "only_includes": "Chỉ tên có chứa từ khóa", 
    "only_exact": "Chỉ tên khớp chính xác"
}

PLACE_MINIMUM_STARS_OPTIONS = {
    "two": "2.0 sao",
    "twoAndHalf": "2.5 sao",
    "three": "3.0 sao", 
    "threeAndHalf": "3.5 sao",
    "four": "4.0 sao",
    "fourAndHalf": "4.5 sao"
}

WEBSITE_FILTER_OPTIONS = {
    "allPlaces": "Tất cả",
    "withWebsite": "Chỉ có website",
    "withoutWebsite": "Chỉ không có website"
}

REVIEWS_SORT_OPTIONS = {
    "newest": "Mới nhất",
    "mostRelevant": "Liên quan nhất",
    "highestRanking": "Đánh giá cao nhất",
    "lowestRanking": "Đánh giá thấp nhất"
}

# Phòng ban cho business leads
LEADS_DEPARTMENTS = [
    "Sales",
    "Marketing", 
    "C-Suite",
    "Operations",
    "Human Resources",
    "Finance",
    "IT",
    "Customer Service",
    "Business Development",
    "Product Management"
]

# Cấu hình pricing (USD per 1000)
PRICING = {
    "place_scraped": 4.00,
    "filter_applied": 1.00,
    "additional_details": 2.00,
    "company_contacts": 2.00,
    "business_leads": 5.00,
    "review_scraped": 0.50,
    "image_scraped": 0.50,
    "actor_start": 0.007
}
