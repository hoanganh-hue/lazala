"""
Details tab - Tab thu thập chi tiết
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QCheckBox, QSpinBox, QComboBox, QDateEdit, QGroupBox,
    QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

from ..utils.constants import REVIEWS_SORT_OPTIONS
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DetailsTab(QWidget):
    """Tab thu thập chi tiết"""
    
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
        title_label = QLabel("📋 Thu thập chi tiết")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Cấu hình các tùy chọn thu thập chi tiết như reviews, hình ảnh, câu hỏi & trả lời. "
            "Các tùy chọn này sẽ làm tăng thời gian thu thập nhưng cung cấp dữ liệu phong phú hơn."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setSpacing(20)
        
        # Place details group
        place_details_group = QGroupBox("🏢 Thông tin chi tiết địa điểm")
        place_details_layout = QVBoxLayout(place_details_group)
        
        # Main checkbox to enable place details
        self.scrape_details_cb = QCheckBox("Thu thập trang chi tiết đầy đủ")
        self.scrape_details_cb.setToolTip(
            "Bật để thu thập thông tin chi tiết từ trang địa điểm. "
            "Cần thiết để enable các tùy chọn bên dưới."
        )
        place_details_layout.addWidget(self.scrape_details_cb)
        
        # Additional details checkboxes
        self.reservation_data_cb = QCheckBox("Thông tin đặt bàn (Reservation data)")
        self.reservation_data_cb.setToolTip("Thu thập thông tin về dịch vụ đặt bàn")
        place_details_layout.addWidget(self.reservation_data_cb)
        
        self.web_results_cb = QCheckBox("Kết quả web (Web results)")
        self.web_results_cb.setToolTip("Thu thập phần 'Web results' ở cuối trang địa điểm")
        place_details_layout.addWidget(self.web_results_cb)
        
        self.directories_cb = QCheckBox("Địa điểm bên trong (Directories)")
        self.directories_cb.setToolTip("Thu thập các địa điểm bên trong (ví dụ: cửa hàng trong mall)")
        place_details_layout.addWidget(self.directories_cb)
        
        details_layout.addWidget(place_details_group)
        
        # Questions & Answers group
        qa_group = QGroupBox("❓ Câu hỏi & Trả lời")
        qa_layout = QFormLayout(qa_group)
        
        self.max_questions_spin = QSpinBox()
        self.max_questions_spin.setRange(0, 999)
        self.max_questions_spin.setValue(0)
        self.max_questions_spin.setSpecialValueText("Chỉ câu đầu tiên")
        self.max_questions_spin.setToolTip("Số câu hỏi tối đa để thu thập. 0 = chỉ câu đầu tiên, 999 = tất cả")
        qa_layout.addRow("Số câu hỏi:", self.max_questions_spin)
        
        details_layout.addWidget(qa_group)
        
        # Reviews group
        reviews_group = QGroupBox("⭐ Reviews")
        reviews_layout = QFormLayout(reviews_group)
        
        self.max_reviews_spin = QSpinBox()
        self.max_reviews_spin.setRange(0, 5000)
        self.max_reviews_spin.setValue(0)
        self.max_reviews_spin.setSpecialValueText("Tất cả reviews")
        self.max_reviews_spin.setToolTip("Số reviews tối đa để thu thập. 0 = tất cả reviews")
        reviews_layout.addRow("Số reviews:", self.max_reviews_spin)
        
        # Reviews start date
        self.reviews_start_date = QDateEdit()
        self.reviews_start_date.setDate(QDate.currentDate().addDays(-30))
        self.reviews_start_date.setCalendarPopup(True)
        self.reviews_start_date.setSpecialValueText("Không giới hạn")
        self.reviews_start_date.setToolTip("Chỉ thu thập reviews từ ngày này trở về sau")
        reviews_layout.addRow("Từ ngày:", self.reviews_start_date)
        
        # Reviews sort
        self.reviews_sort_combo = QComboBox()
        for value, text in REVIEWS_SORT_OPTIONS.items():
            self.reviews_sort_combo.addItem(text, value)
        self.reviews_sort_combo.setToolTip("Cách sắp xếp reviews")
        reviews_layout.addRow("Sắp xếp theo:", self.reviews_sort_combo)
        
        details_layout.addWidget(reviews_group)
        
        # Images group
        images_group = QGroupBox("📸 Hình ảnh")
        images_layout = QFormLayout(images_group)
        
        self.max_images_spin = QSpinBox()
        self.max_images_spin.setRange(0, 999)
        self.max_images_spin.setValue(0)
        self.max_images_spin.setSpecialValueText("Không thu thập")
        self.max_images_spin.setToolTip("Số hình ảnh tối đa để thu thập. 0 = không thu thập")
        images_layout.addRow("Số hình ảnh:", self.max_images_spin)
        
        details_layout.addWidget(images_group)
        
        # Warning label
        warning_label = QLabel(
            "⚠️ Lưu ý: Các tùy chọn thu thập chi tiết sẽ làm tăng thời gian xử lý và chi phí. "
            "Hãy cân nhắc kỹ trước khi bật các tùy chọn này."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #ff6b35; background-color: #fff3cd; padding: 10px; border-radius: 5px;")
        details_layout.addWidget(warning_label)
        
        # Add stretch
        details_layout.addStretch()
        
        # Set scroll area widget
        scroll_area.setWidget(details_widget)
        layout.addWidget(scroll_area)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.scrape_details_cb.toggled.connect(self.toggle_details_options)
        
        # Initially disable dependent options
        self.toggle_details_options(False)
    
    def toggle_details_options(self, enabled):
        """Toggle options that depend on scrape_details_cb"""
        self.reservation_data_cb.setEnabled(enabled)
        self.web_results_cb.setEnabled(enabled)
        self.directories_cb.setEnabled(enabled)
        
        # If disabled, uncheck dependent options
        if not enabled:
            self.reservation_data_cb.setChecked(False)
            self.web_results_cb.setChecked(False)
            self.directories_cb.setChecked(False)
    
    def get_details_data(self):
        """Lấy dữ liệu thu thập chi tiết"""
        return {
            "scrape_details": self.scrape_details_cb.isChecked(),
            "reservation_data": self.reservation_data_cb.isChecked(),
            "web_results": self.web_results_cb.isChecked(),
            "directories": self.directories_cb.isChecked(),
            "max_questions": self.max_questions_spin.value(),
            "max_reviews": self.max_reviews_spin.value(),
            "reviews_start_date": self.reviews_start_date.date().toString("yyyy-MM-dd") if self.reviews_start_date.date().isValid() else None,
            "reviews_sort": self.reviews_sort_combo.currentData(),
            "max_images": self.max_images_spin.value()
        }
    
    def reset_form(self):
        """Reset form về trạng thái ban đầu"""
        self.scrape_details_cb.setChecked(False)
        self.reservation_data_cb.setChecked(False)
        self.web_results_cb.setChecked(False)
        self.directories_cb.setChecked(False)
        self.max_questions_spin.setValue(0)
        self.max_reviews_spin.setValue(0)
        self.reviews_start_date.setDate(QDate.currentDate().addDays(-30))
        self.reviews_sort_combo.setCurrentIndex(0)
        self.max_images_spin.setValue(0)
