"""
Search tab - Tab tìm kiếm cơ bản
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QComboBox, QPushButton, QTextEdit,
    QLabel, QGroupBox, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from ..utils.constants import SUPPORTED_LANGUAGES
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SearchTab(QWidget):
    """Tab tìm kiếm cơ bản"""
    
    start_scraping_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🔍 Tìm kiếm cơ bản")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Nhập từ khóa và địa điểm để bắt đầu thu thập dữ liệu từ Google Maps. "
            "Bạn có thể tìm kiếm nhiều từ khóa cùng lúc để có kết quả đa dạng hơn."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # Main form
        form_group = QGroupBox("Thông tin tìm kiếm")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        
        # Search terms
        search_terms_group = QGroupBox("Từ khóa tìm kiếm")
        search_terms_layout = QVBoxLayout(search_terms_group)
        
        self.search_terms_text = QTextEdit()
        self.search_terms_text.setPlaceholderText(
            "Nhập từ khóa tìm kiếm, mỗi từ khóa trên một dòng:\n"
            "Ví dụ:\n"
            "restaurant\n"
            "hotel\n"
            "coffee shop\n"
            "pharmacy"
        )
        self.search_terms_text.setMaximumHeight(120)
        search_terms_layout.addWidget(self.search_terms_text)
        
        # Add/Remove buttons
        buttons_layout = QHBoxLayout()
        self.add_term_btn = QPushButton("➕ Thêm từ khóa")
        self.remove_term_btn = QPushButton("➖ Xóa từ khóa")
        self.clear_terms_btn = QPushButton("🗑️ Xóa tất cả")
        
        buttons_layout.addWidget(self.add_term_btn)
        buttons_layout.addWidget(self.remove_term_btn)
        buttons_layout.addWidget(self.clear_terms_btn)
        buttons_layout.addStretch()
        
        search_terms_layout.addLayout(buttons_layout)
        form_layout.addRow(search_terms_group)
        
        # Location
        location_group = QGroupBox("Địa điểm")
        location_layout = QVBoxLayout(location_group)
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Ví dụ: Hanoi, Vietnam hoặc New York, USA")
        location_layout.addWidget(self.location_input)
        
        # Location buttons
        location_buttons_layout = QHBoxLayout()
        self.validate_location_btn = QPushButton("🔍 Kiểm tra địa điểm")
        self.current_location_btn = QPushButton("📍 Vị trí hiện tại")
        
        location_buttons_layout.addWidget(self.validate_location_btn)
        location_buttons_layout.addWidget(self.current_location_btn)
        location_buttons_layout.addStretch()
        
        location_layout.addLayout(location_buttons_layout)
        form_layout.addRow(location_group)
        
        # Max places
        self.max_places_spin = QSpinBox()
        self.max_places_spin.setRange(0, 9999)
        self.max_places_spin.setValue(50)
        self.max_places_spin.setSpecialValueText("Tất cả")
        self.max_places_spin.setToolTip("Số lượng địa điểm tối đa để thu thập. Để 0 để thu thập tất cả.")
        form_layout.addRow("Số lượng địa điểm:", self.max_places_spin)
        
        # Language
        self.language_combo = QComboBox()
        for code, name in SUPPORTED_LANGUAGES.items():
            self.language_combo.addItem(f"{name} ({code})", code)
        
        # Set Vietnamese as default
        vietnamese_index = self.language_combo.findData("vi")
        if vietnamese_index >= 0:
            self.language_combo.setCurrentIndex(vietnamese_index)
        else:
            # Fallback to English
            english_index = self.language_combo.findData("en")
            if english_index >= 0:
                self.language_combo.setCurrentIndex(english_index)
        
        form_layout.addRow("Ngôn ngữ kết quả:", self.language_combo)
        
        layout.addWidget(form_group)
        
        # Action buttons
        buttons_group = QGroupBox("Thao tác")
        buttons_layout = QHBoxLayout(buttons_group)
        
        self.start_btn = QPushButton("▶️ Bắt đầu thu thập")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        self.save_config_btn = QPushButton("💾 Lưu cấu hình")
        self.load_config_btn = QPushButton("📁 Tải cấu hình")
        
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_config_btn)
        buttons_layout.addWidget(self.load_config_btn)
        
        layout.addWidget(buttons_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        self.start_btn.clicked.connect(self.start_scraping)
        self.add_term_btn.clicked.connect(self.add_search_term)
        self.remove_term_btn.clicked.connect(self.remove_search_term)
        self.clear_terms_btn.clicked.connect(self.clear_search_terms)
        self.validate_location_btn.clicked.connect(self.validate_location)
        self.current_location_btn.clicked.connect(self.use_current_location)
        self.save_config_btn.clicked.connect(self.save_configuration)
        self.load_config_btn.clicked.connect(self.load_configuration)
    
    def start_scraping(self):
        """Bắt đầu thu thập dữ liệu"""
        # Validate input
        search_terms = self.get_search_terms()
        if not search_terms:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Thiếu thông tin",
                "Vui lòng nhập ít nhất một từ khóa tìm kiếm."
            )
            return
        
        location = self.location_input.text().strip()
        if not location:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Thiếu thông tin",
                "Vui lòng nhập địa điểm tìm kiếm."
            )
            return
        
        # Emit signal
        self.start_scraping_signal.emit()
        logger.info(f"Starting scraping for terms: {search_terms}, location: {location}")
    
    def add_search_term(self):
        """Thêm từ khóa tìm kiếm"""
        from PyQt5.QtWidgets import QInputDialog
        
        term, ok = QInputDialog.getText(
            self,
            "Thêm từ khóa",
            "Nhập từ khóa tìm kiếm:"
        )
        
        if ok and term.strip():
            current_text = self.search_terms_text.toPlainText()
            if current_text and not current_text.endswith('\n'):
                current_text += '\n'
            current_text += term.strip()
            self.search_terms_text.setPlainText(current_text)
    
    def remove_search_term(self):
        """Xóa từ khóa tìm kiếm"""
        from PyQt5.QtWidgets import QInputDialog
        
        terms = self.get_search_terms()
        if not terms:
            return
        
        term, ok = QInputDialog.getItem(
            self,
            "Xóa từ khóa",
            "Chọn từ khóa cần xóa:",
            terms,
            0,
            False
        )
        
        if ok and term:
            terms.remove(term)
            self.search_terms_text.setPlainText('\n'.join(terms))
    
    def clear_search_terms(self):
        """Xóa tất cả từ khóa"""
        from PyQt5.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc chắn muốn xóa tất cả từ khóa tìm kiếm?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.search_terms_text.clear()
    
    def validate_location(self):
        """Kiểm tra địa điểm"""
        location = self.location_input.text().strip()
        if not location:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Thiếu thông tin",
                "Vui lòng nhập địa điểm trước khi kiểm tra."
            )
            return
        
        # TODO: Implement location validation with OpenStreetMap API
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Kiểm tra địa điểm",
            f"Tính năng kiểm tra địa điểm '{location}' sẽ được thêm trong phiên bản tiếp theo."
        )
    
    def use_current_location(self):
        """Sử dụng vị trí hiện tại"""
        # TODO: Implement geolocation
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Vị trí hiện tại",
            "Tính năng sử dụng vị trí hiện tại sẽ được thêm trong phiên bản tiếp theo."
        )
    
    def save_configuration(self):
        """Lưu cấu hình"""
        # TODO: Implement save configuration
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Lưu cấu hình",
            "Tính năng lưu cấu hình sẽ được thêm trong phiên bản tiếp theo."
        )
    
    def load_configuration(self):
        """Tải cấu hình"""
        # TODO: Implement load configuration
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Tải cấu hình",
            "Tính năng tải cấu hình sẽ được thêm trong phiên bản tiếp theo."
        )
    
    def get_search_terms(self):
        """Lấy danh sách từ khóa tìm kiếm"""
        text = self.search_terms_text.toPlainText().strip()
        if not text:
            return []
        
        terms = [term.strip() for term in text.split('\n') if term.strip()]
        return terms
    
    def get_search_data(self):
        """Lấy dữ liệu tìm kiếm"""
        return {
            "search_strings": self.get_search_terms(),
            "location": self.location_input.text().strip(),
            "max_places": self.max_places_spin.value() if self.max_places_spin.value() > 0 else None,
            "language": self.language_combo.currentData()
        }
    
    def reset_form(self):
        """Reset form về trạng thái ban đầu"""
        self.search_terms_text.clear()
        self.location_input.clear()
        self.max_places_spin.setValue(50)
        
        # Reset language to Vietnamese
        vietnamese_index = self.language_combo.findData("vi")
        if vietnamese_index >= 0:
            self.language_combo.setCurrentIndex(vietnamese_index)
