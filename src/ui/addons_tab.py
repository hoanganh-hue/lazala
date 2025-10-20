"""
Add-ons tab - Tab add-ons premium
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QCheckBox, QSpinBox, QListWidget, QListWidgetItem,
    QGroupBox, QLabel, QScrollArea, QFrame, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ..utils.constants import LEADS_DEPARTMENTS
from ..utils.helpers import calculate_estimated_cost
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AddonsTab(QWidget):
    """Tab add-ons premium"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
        self.load_departments()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("⭐ Add-ons Premium")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Các tính năng premium để thu thập thông tin liên hệ và business leads. "
            "Các tính năng này có phí bổ sung nhưng cung cấp dữ liệu giá trị cao cho "
            "lead generation và sales prospecting."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # Warning banner
        warning_label = QLabel(
            "💰 CẢNH BÁO: Các tính năng này có phí bổ sung. Vui lòng kiểm tra bảng giá trước khi sử dụng."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("""
            color: #d63384; 
            background-color: #f8d7da; 
            padding: 15px; 
            border-radius: 8px; 
            border: 1px solid #f5c6cb;
            font-weight: bold;
        """)
        layout.addWidget(warning_label)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        addons_widget = QWidget()
        addons_layout = QVBoxLayout(addons_widget)
        addons_layout.setSpacing(20)
        
        # Company contacts group
        contacts_group = QGroupBox("📧 Thu thập thông tin liên hệ công ty")
        contacts_layout = QVBoxLayout(contacts_group)
        
        # Main checkbox
        self.scrape_contacts_cb = QCheckBox("Bật thu thập thông tin liên hệ")
        self.scrape_contacts_cb.setToolTip(
            "Thu thập email công ty và social media profiles từ website của địa điểm. "
            "Giá: $2/1,000 địa điểm có website."
        )
        contacts_layout.addWidget(self.scrape_contacts_cb)
        
        # Description
        contacts_desc = QLabel(
            "Tính năng này sẽ:\n"
            "• Tìm và thu thập email công ty từ website\n"
            "• Thu thập social media profiles (Facebook, LinkedIn, Twitter, etc.)\n"
            "• Chỉ áp dụng cho các địa điểm có website\n"
            "• Loại trừ các chuỗi lớn (McDonald's, Starbucks, etc.)"
        )
        contacts_desc.setStyleSheet("color: #666; font-size: 12px; margin: 10px 0;")
        contacts_layout.addWidget(contacts_desc)
        
        addons_layout.addWidget(contacts_group)
        
        # Business leads group
        leads_group = QGroupBox("👥 Thu thập thông tin business leads")
        leads_layout = QVBoxLayout(leads_group)
        
        # Max leads per place
        leads_form_layout = QFormLayout()
        
        self.max_leads_spin = QSpinBox()
        self.max_leads_spin.setRange(0, 100)
        self.max_leads_spin.setValue(0)
        self.max_leads_spin.setSpecialValueText("Tắt")
        self.max_leads_spin.setToolTip(
            "Số leads tối đa mỗi địa điểm. 0 = tắt, 1-100 = số lượng. "
            "Giá: $5/1,000 leads."
        )
        leads_form_layout.addRow("Số leads tối đa mỗi địa điểm:", self.max_leads_spin)
        
        leads_layout.addLayout(leads_form_layout)
        
        # Departments filter
        departments_label = QLabel("Lọc theo phòng ban:")
        leads_layout.addWidget(departments_label)
        
        self.departments_list = QListWidget()
        self.departments_list.setSelectionMode(QListWidget.MultiSelection)
        self.departments_list.setMaximumHeight(150)
        leads_layout.addWidget(self.departments_list)
        
        # Select all/none buttons
        dept_buttons_layout = QHBoxLayout()
        self.select_all_depts_btn = QPushButton("Chọn tất cả")
        self.select_none_depts_btn = QPushButton("Bỏ chọn tất cả")
        
        dept_buttons_layout.addWidget(self.select_all_depts_btn)
        dept_buttons_layout.addWidget(self.select_none_depts_btn)
        dept_buttons_layout.addStretch()
        
        leads_layout.addLayout(dept_buttons_layout)
        
        # Leads description
        leads_desc = QLabel(
            "Tính năng này sẽ thu thập:\n"
            "• Tên đầy đủ của nhân viên\n"
            "• Email công việc\n"
            "• Số điện thoại\n"
            "• Chức vụ/Job title\n"
            "• LinkedIn profile\n"
            "• Thông tin công ty (ngành, số nhân viên, etc.)"
        )
        leads_desc.setStyleSheet("color: #666; font-size: 12px; margin: 10px 0;")
        leads_layout.addWidget(leads_desc)
        
        # GDPR warning
        gdpr_warning = QLabel(
            "⚠️ CẢNH BÁO GDPR: Thông tin này chứa dữ liệu cá nhân. "
            "Chỉ sử dụng khi có lý do chính đáng và tuân thủ các quy định về bảo vệ dữ liệu."
        )
        gdpr_warning.setWordWrap(True)
        gdpr_warning.setStyleSheet("""
            color: #dc3545; 
            background-color: #f8d7da; 
            padding: 10px; 
            border-radius: 5px; 
            border: 1px solid #f5c6cb;
            font-size: 12px;
        """)
        leads_layout.addWidget(gdpr_warning)
        
        addons_layout.addWidget(leads_group)
        
        # Cost estimation group
        cost_group = QGroupBox("💰 Ước tính chi phí")
        cost_layout = QVBoxLayout(cost_group)
        
        self.cost_label = QLabel("Chi phí ước tính: $0.00")
        self.cost_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #28a745; 
            padding: 10px; 
            background-color: #d4edda; 
            border-radius: 5px;
        """)
        cost_layout.addWidget(self.cost_label)
        
        # Update cost button
        self.update_cost_btn = QPushButton("🔄 Cập nhật chi phí")
        self.update_cost_btn.setToolTip("Cập nhật chi phí dựa trên cấu hình hiện tại")
        cost_layout.addWidget(self.update_cost_btn)
        
        addons_layout.addWidget(cost_group)
        
        # Add stretch
        addons_layout.addStretch()
        
        # Set scroll area widget
        scroll_area.setWidget(addons_widget)
        layout.addWidget(scroll_area)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.scrape_contacts_cb.toggled.connect(self.update_cost_estimation)
        self.max_leads_spin.valueChanged.connect(self.update_cost_estimation)
        self.select_all_depts_btn.clicked.connect(self.select_all_departments)
        self.select_none_depts_btn.clicked.connect(self.select_none_departments)
        self.update_cost_btn.clicked.connect(self.update_cost_estimation)
    
    def load_departments(self):
        """Load departments list"""
        for dept in LEADS_DEPARTMENTS:
            item = QListWidgetItem(dept)
            self.departments_list.addItem(item)
    
    def select_all_departments(self):
        """Select all departments"""
        for i in range(self.departments_list.count()):
            self.departments_list.item(i).setSelected(True)
    
    def select_none_departments(self):
        """Select none departments"""
        for i in range(self.departments_list.count()):
            self.departments_list.item(i).setSelected(False)
    
    def update_cost_estimation(self):
        """Update cost estimation"""
        try:
            # Get current configuration (simplified)
            max_places = 100  # Default assumption
            filters_count = 0  # Will be calculated from other tabs
            scrape_details = False  # Will be calculated from details tab
            scrape_contacts = self.scrape_contacts_cb.isChecked()
            max_leads = self.max_leads_spin.value()
            max_reviews = 0  # Will be calculated from details tab
            max_images = 0  # Will be calculated from details tab
            
            cost = calculate_estimated_cost(
                max_places=max_places,
                filters_count=filters_count,
                scrape_details=scrape_details,
                scrape_contacts=scrape_contacts,
                max_leads=max_leads,
                max_reviews=max_reviews,
                max_images=max_images
            )
            
            self.cost_label.setText(f"Chi phí ước tính: ${cost:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to update cost estimation: {e}")
            self.cost_label.setText("Chi phí ước tính: Lỗi tính toán")
    
    def get_addons_data(self):
        """Lấy dữ liệu add-ons"""
        # Get selected departments
        selected_departments = []
        for i in range(self.departments_list.count()):
            item = self.departments_list.item(i)
            if item.isSelected():
                selected_departments.append(item.text())
        
        return {
            "scrape_contacts": self.scrape_contacts_cb.isChecked(),
            "max_leads": self.max_leads_spin.value(),
            "leads_departments": selected_departments
        }
    
    def reset_form(self):
        """Reset form về trạng thái ban đầu"""
        self.scrape_contacts_cb.setChecked(False)
        self.max_leads_spin.setValue(0)
        
        # Clear department selections
        for i in range(self.departments_list.count()):
            self.departments_list.item(i).setSelected(False)
        
        # Update cost estimation
        self.update_cost_estimation()
