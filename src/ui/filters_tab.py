"""
Filters tab - Tab bộ lọc nâng cao
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QCheckBox, QRadioButton, QButtonGroup, QSlider, QLabel,
    QListWidget, QListWidgetItem, QLineEdit, QGroupBox,
    QScrollArea, QFrame, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from ..utils.constants import (
    SEARCH_MATCHING_OPTIONS, PLACE_MINIMUM_STARS_OPTIONS, 
    WEBSITE_FILTER_OPTIONS
)
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FiltersTab(QWidget):
    """Tab bộ lọc nâng cao"""
    
    def __init__(self):
        super().__init__()
        self.categories = []
        self.init_ui()
        self.setup_connections()
        self.load_categories()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🎯 Bộ lọc nâng cao")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Sử dụng các bộ lọc để thu hẹp kết quả tìm kiếm theo danh mục, đánh giá, "
            "website và các tiêu chí khác. Các bộ lọc có thể giúp bạn tìm được những "
            "địa điểm phù hợp nhất với nhu cầu."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # Create scroll area for filters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        filters_widget = QWidget()
        filters_layout = QVBoxLayout(filters_widget)
        filters_layout.setSpacing(20)
        
        # Categories filter
        categories_group = QGroupBox("🎢 Danh mục địa điểm")
        categories_layout = QVBoxLayout(categories_group)
        
        # Use categories checkbox
        self.use_categories_cb = QCheckBox("Sử dụng bộ lọc danh mục")
        self.use_categories_cb.setToolTip("Bật để lọc kết quả theo danh mục đã chọn")
        categories_layout.addWidget(self.use_categories_cb)
        
        # Search categories
        self.category_search = QLineEdit()
        self.category_search.setPlaceholderText("Tìm kiếm danh mục...")
        categories_layout.addWidget(self.category_search)
        
        # Categories list
        self.categories_list = QListWidget()
        self.categories_list.setSelectionMode(QListWidget.MultiSelection)
        self.categories_list.setMaximumHeight(200)
        categories_layout.addWidget(self.categories_list)
        
        # Categories info
        self.categories_info = QLabel("Chọn danh mục để lọc kết quả. Có thể chọn nhiều danh mục.")
        self.categories_info.setStyleSheet("color: #666; font-size: 12px;")
        categories_layout.addWidget(self.categories_info)
        
        filters_layout.addWidget(categories_group)
        
        # Search matching filter
        matching_group = QGroupBox("🔍 Khớp tên")
        matching_layout = QVBoxLayout(matching_group)
        
        self.matching_group = QButtonGroup()
        
        for value, text in SEARCH_MATCHING_OPTIONS.items():
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.matching_group.addButton(radio)
            matching_layout.addWidget(radio)
        
        # Set default
        all_radio = self.matching_group.button(0)
        if all_radio:
            all_radio.setChecked(True)
        
        matching_layout.addStretch()
        filters_layout.addWidget(matching_group)
        
        # Rating filter
        rating_group = QGroupBox("⭐ Đánh giá tối thiểu")
        rating_layout = QVBoxLayout(rating_group)
        
        # Rating slider
        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setRange(0, 9)  # 0 = no filter, 1-9 = 2.0-4.5 stars
        self.rating_slider.setValue(0)
        self.rating_slider.setTickPosition(QSlider.TicksBelow)
        self.rating_slider.setTickInterval(1)
        rating_layout.addWidget(self.rating_slider)
        
        # Rating label
        self.rating_label = QLabel("Không lọc theo đánh giá")
        self.rating_label.setAlignment(Qt.AlignCenter)
        rating_layout.addWidget(self.rating_label)
        
        # Only places with reviews checkbox
        self.only_with_reviews_cb = QCheckBox("Chỉ địa điểm có reviews")
        self.only_with_reviews_cb.setToolTip("Bỏ qua các địa điểm chưa có đánh giá")
        rating_layout.addWidget(self.only_with_reviews_cb)
        
        filters_layout.addWidget(rating_group)
        
        # Website filter
        website_group = QGroupBox("🌐 Website")
        website_layout = QVBoxLayout(website_group)
        
        self.website_group = QButtonGroup()
        
        for value, text in WEBSITE_FILTER_OPTIONS.items():
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.website_group.addButton(radio)
            website_layout.addWidget(radio)
        
        # Set default
        all_website_radio = self.website_group.button(0)
        if all_website_radio:
            all_website_radio.setChecked(True)
        
        website_layout.addStretch()
        filters_layout.addWidget(website_group)
        
        # Other filters
        other_group = QGroupBox("🔧 Bộ lọc khác")
        other_layout = QVBoxLayout(other_group)
        
        self.skip_closed_cb = QCheckBox("Bỏ qua địa điểm đã đóng cửa")
        self.skip_closed_cb.setToolTip("Không thu thập các địa điểm tạm thời hoặc vĩnh viễn đóng cửa")
        other_layout.addWidget(self.skip_closed_cb)
        
        other_layout.addStretch()
        filters_layout.addWidget(other_group)
        
        # Add stretch
        filters_layout.addStretch()
        
        # Set scroll area widget
        scroll_area.setWidget(filters_widget)
        layout.addWidget(scroll_area)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.rating_slider.valueChanged.connect(self.update_rating_label)
        self.category_search.textChanged.connect(self.filter_categories)
        self.use_categories_cb.toggled.connect(self.toggle_categories_filter)
    
    def load_categories(self):
        """Load categories từ file JSON"""
        try:
            import json
            from pathlib import Path
            
            categories_file = Path(__file__).parent.parent.parent / "resources" / "data" / "categories.json"
            if categories_file.exists():
                with open(categories_file, 'r', encoding='utf-8') as f:
                    self.categories = json.load(f)
                
                # Populate categories list
                for category in self.categories:
                    item = QListWidgetItem(category)
                    self.categories_list.addItem(item)
                
                logger.info(f"Loaded {len(self.categories)} categories")
            else:
                logger.warning("Categories file not found")
                
        except Exception as e:
            logger.error(f"Failed to load categories: {e}")
    
    def filter_categories(self, text):
        """Filter categories based on search text"""
        if not text:
            # Show all categories
            for i in range(self.categories_list.count()):
                self.categories_list.item(i).setHidden(False)
        else:
            # Filter categories
            text_lower = text.lower()
            for i in range(self.categories_list.count()):
                item = self.categories_list.item(i)
                item.setHidden(text_lower not in item.text().lower())
    
    def toggle_categories_filter(self, enabled):
        """Toggle categories filter"""
        self.categories_list.setEnabled(enabled)
        self.category_search.setEnabled(enabled)
    
    def update_rating_label(self, value):
        """Update rating label based on slider value"""
        if value == 0:
            self.rating_label.setText("Không lọc theo đánh giá")
        else:
            # Convert slider value to star rating
            star_rating = 2.0 + (value - 1) * 0.5
            self.rating_label.setText(f"Tối thiểu {star_rating} sao")
    
    def get_filters_data(self):
        """Lấy dữ liệu bộ lọc"""
        # Get selected categories
        selected_categories = []
        if self.use_categories_cb.isChecked():
            for i in range(self.categories_list.count()):
                item = self.categories_list.item(i)
                if item.isSelected():
                    selected_categories.append(item.text())
        
        # Get search matching
        matching_value = "all"
        for button in self.matching_group.buttons():
            if button.isChecked():
                matching_value = button.property("value")
                break
        
        # Get minimum stars
        minimum_stars = None
        if self.rating_slider.value() > 0:
            star_values = ["two", "twoAndHalf", "three", "threeAndHalf", "four", "fourAndHalf"]
            if self.rating_slider.value() <= len(star_values):
                minimum_stars = star_values[self.rating_slider.value() - 1]
        
        # Get website filter
        website_value = "allPlaces"
        for button in self.website_group.buttons():
            if button.isChecked():
                website_value = button.property("value")
                break
        
        return {
            "categories": selected_categories,
            "search_matching": matching_value,
            "minimum_stars": minimum_stars,
            "website": website_value,
            "skip_closed": self.skip_closed_cb.isChecked()
        }
    
    def reset_form(self):
        """Reset form về trạng thái ban đầu"""
        # Reset categories
        self.use_categories_cb.setChecked(False)
        self.categories_list.clearSelection()
        self.category_search.clear()
        
        # Reset search matching
        all_radio = self.matching_group.button(0)
        if all_radio:
            all_radio.setChecked(True)
        
        # Reset rating
        self.rating_slider.setValue(0)
        self.only_with_reviews_cb.setChecked(False)
        
        # Reset website filter
        all_website_radio = self.website_group.button(0)
        if all_website_radio:
            all_website_radio.setChecked(True)
        
        # Reset other filters
        self.skip_closed_cb.setChecked(False)
