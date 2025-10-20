"""
Settings dialog - Dialog cài đặt
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QTabWidget, QWidget,
    QGroupBox, QComboBox, QCheckBox, QSpinBox, QTextEdit,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

from ..api.auth import AuthManager
from ..api.apify_client import ApifyClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SettingsDialog(QDialog):
    """Dialog cài đặt ứng dụng"""
    
    def __init__(self, auth_manager: AuthManager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.apify_client = ApifyClient(auth_manager)
        self.init_ui()
        self.setup_connections()
        self.load_settings()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("Cài đặt")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # API Settings tab
        self.api_tab = self.create_api_tab()
        self.tab_widget.addTab(self.api_tab, "🔑 API")
        
        # App Settings tab
        self.app_tab = self.create_app_tab()
        self.tab_widget.addTab(self.app_tab, "⚙️ Ứng dụng")
        
        # About tab
        self.about_tab = self.create_about_tab()
        self.tab_widget.addTab(self.about_tab, "ℹ️ Giới thiệu")
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.test_connection_btn = QPushButton("🔍 Test kết nối")
        self.save_btn = QPushButton("💾 Lưu")
        self.cancel_btn = QPushButton("❌ Hủy")
        
        buttons_layout.addWidget(self.test_connection_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_api_tab(self):
        """Tạo tab API settings"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🔑 Cài đặt API")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Cấu hình API token để kết nối với Apify. Bạn có thể lấy API token từ "
            "<a href='https://console.apify.com/settings/integrations'>Apify Console</a>."
        )
        desc_label.setWordWrap(True)
        desc_label.setOpenExternalLinks(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # API Token group
        api_group = QGroupBox("API Token")
        api_layout = QFormLayout(api_group)
        
        self.api_token_input = QLineEdit()
        self.api_token_input.setEchoMode(QLineEdit.Password)
        self.api_token_input.setPlaceholderText("Nhập API token của bạn...")
        self.api_token_input.setToolTip("API token từ Apify Console > Settings > Integrations")
        api_layout.addRow("API Token:", self.api_token_input)
        
        # Show/Hide token button
        self.show_token_btn = QPushButton("👁️ Hiện")
        self.show_token_btn.setCheckable(True)
        self.show_token_btn.clicked.connect(self.toggle_token_visibility)
        api_layout.addRow("", self.show_token_btn)
        
        layout.addWidget(api_group)
        
        # Connection status
        status_group = QGroupBox("Trạng thái kết nối")
        status_layout = QVBoxLayout(status_group)
        
        self.connection_status_label = QLabel("Chưa kết nối")
        self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")
        status_layout.addWidget(self.connection_status_label)
        
        self.connection_info_label = QLabel("")
        self.connection_info_label.setStyleSheet("color: #666; font-size: 12px;")
        status_layout.addWidget(self.connection_info_label)
        
        layout.addWidget(status_group)
        
        # Instructions
        instructions_group = QGroupBox("Hướng dẫn")
        instructions_layout = QVBoxLayout(instructions_group)
        
        instructions_text = QTextEdit()
        instructions_text.setReadOnly(True)
        instructions_text.setMaximumHeight(150)
        instructions_text.setHtml("""
        <h4>Cách lấy API Token:</h4>
        <ol>
        <li>Truy cập <a href="https://console.apify.com">Apify Console</a></li>
        <li>Đăng nhập hoặc tạo tài khoản mới</li>
        <li>Vào <b>Settings</b> > <b>Integrations</b></li>
        <li>Copy API token và paste vào ô trên</li>
        <li>Click <b>Test kết nối</b> để kiểm tra</li>
        </ol>
        <p><b>Lưu ý:</b> API token được lưu trữ an toàn trên máy tính của bạn.</p>
        """)
        instructions_layout.addWidget(instructions_text)
        
        layout.addWidget(instructions_group)
        
        layout.addStretch()
        return tab
    
    def create_app_tab(self):
        """Tạo tab App settings"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("⚙️ Cài đặt ứng dụng")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # General settings
        general_group = QGroupBox("Cài đặt chung")
        general_layout = QFormLayout(general_group)
        
        # Default language
        self.default_language_combo = QComboBox()
        self.default_language_combo.addItems(["Tiếng Việt", "English", "中文", "日本語"])
        general_layout.addRow("Ngôn ngữ mặc định:", self.default_language_combo)
        
        # Default export format
        self.default_export_combo = QComboBox()
        self.default_export_combo.addItems(["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"])
        general_layout.addRow("Định dạng xuất mặc định:", self.default_export_combo)
        
        # Auto-save results
        self.auto_save_cb = QCheckBox("Tự động lưu kết quả")
        self.auto_save_cb.setToolTip("Tự động lưu kết quả sau khi thu thập xong")
        general_layout.addRow("", self.auto_save_cb)
        
        layout.addWidget(general_group)
        
        # Advanced settings
        advanced_group = QGroupBox("Cài đặt nâng cao")
        advanced_layout = QFormLayout(advanced_group)
        
        # Log level
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["Debug", "Info", "Warning", "Error"])
        advanced_layout.addRow("Mức độ log:", self.log_level_combo)
        
        # Max concurrent requests
        self.max_requests_spin = QSpinBox()
        self.max_requests_spin.setRange(1, 10)
        self.max_requests_spin.setValue(3)
        self.max_requests_spin.setToolTip("Số lượng request đồng thời tối đa")
        advanced_layout.addRow("Request đồng thời:", self.max_requests_spin)
        
        # Request timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(30, 300)
        self.timeout_spin.setValue(60)
        self.timeout_spin.setSuffix(" giây")
        self.timeout_spin.setToolTip("Timeout cho mỗi request")
        advanced_layout.addRow("Timeout:", self.timeout_spin)
        
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        return tab
    
    def create_about_tab(self):
        """Tạo tab About"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("ℹ️ Giới thiệu")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # App info
        info_group = QGroupBox("Thông tin ứng dụng")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <h3>Google Maps Scraper Desktop App</h3>
        <p><b>Phiên bản:</b> 1.0.0</p>
        <p><b>Phát triển bởi:</b> Google Maps Scraper Team</p>
        <p><b>Mô tả:</b> Ứng dụng desktop để thu thập dữ liệu từ Google Maps thông qua Apify API</p>
        
        <h4>Tính năng chính:</h4>
        <ul>
        <li>Thu thập dữ liệu từ Google Maps</li>
        <li>Bộ lọc nâng cao</li>
        <li>Thu thập chi tiết (reviews, hình ảnh, Q&A)</li>
        <li>Add-ons premium (contacts, leads)</li>
        <li>Xuất dữ liệu ra Excel, CSV, JSON</li>
        <li>Hỗ trợ 70+ ngôn ngữ</li>
        </ul>
        
        <h4>Liên kết hữu ích:</h4>
        <ul>
        <li><a href="https://apify.com/compass/crawler-google-places">Apify Google Maps Scraper</a></li>
        <li><a href="https://docs.apify.com">Apify Documentation</a></li>
        <li><a href="https://console.apify.com">Apify Console</a></li>
        </ul>
        """)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        # Credits
        credits_group = QGroupBox("Credits")
        credits_layout = QVBoxLayout(credits_group)
        
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setMaximumHeight(100)
        credits_text.setHtml("""
        <p><b>Powered by:</b></p>
        <ul>
        <li>Apify Platform</li>
        <li>PyQt5</li>
        <li>Python</li>
        </ul>
        """)
        credits_layout.addWidget(credits_text)
        
        layout.addWidget(credits_group)
        
        layout.addStretch()
        return tab
    
    def setup_connections(self):
        """Setup signal connections"""
        self.test_connection_btn.clicked.connect(self.test_connection)
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Auto-test connection when token changes
        self.api_token_input.textChanged.connect(self.on_token_changed)
    
    def load_settings(self):
        """Load settings từ config"""
        # Load API token
        token = self.auth_manager.get_token()
        if token:
            self.api_token_input.setText(token)
            self.update_connection_status()
        
        # Load app settings (placeholder - will be implemented later)
        self.default_language_combo.setCurrentIndex(0)
        self.default_export_combo.setCurrentIndex(0)
        self.auto_save_cb.setChecked(True)
        self.log_level_combo.setCurrentIndex(1)  # Info
        self.max_requests_spin.setValue(3)
        self.timeout_spin.setValue(60)
    
    def toggle_token_visibility(self):
        """Toggle hiển thị/ẩn API token"""
        if self.show_token_btn.isChecked():
            self.api_token_input.setEchoMode(QLineEdit.Normal)
            self.show_token_btn.setText("🙈 Ẩn")
        else:
            self.api_token_input.setEchoMode(QLineEdit.Password)
            self.show_token_btn.setText("👁️ Hiện")
    
    def on_token_changed(self):
        """Xử lý khi token thay đổi"""
        # Clear connection status
        self.connection_status_label.setText("Chưa kiểm tra")
        self.connection_status_label.setStyleSheet("color: orange; font-weight: bold;")
        self.connection_info_label.setText("")
    
    def test_connection(self):
        """Test kết nối API"""
        token = self.api_token_input.text().strip()
        
        if not token:
            QMessageBox.warning(
                self,
                "Thiếu API Token",
                "Vui lòng nhập API token trước khi test kết nối."
            )
            return
        
        # Validate token format
        if not self.auth_manager.validate_token_format(token):
            QMessageBox.warning(
                self,
                "API Token không hợp lệ",
                "API token có định dạng không đúng. Vui lòng kiểm tra lại."
            )
            return
        
        # Test connection
        self.test_connection_btn.setEnabled(False)
        self.test_connection_btn.setText("🔄 Đang test...")
        
        # Set token temporarily for testing
        old_token = self.auth_manager.get_token()
        self.auth_manager.set_token(token)
        
        # Test in background
        QTimer.singleShot(100, self._do_test_connection)
    
    def _do_test_connection(self):
        """Thực hiện test kết nối"""
        try:
            import asyncio
            
            # Create new event loop for testing
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Test connection
            result = loop.run_until_complete(self.apify_client.test_connection())
            
            loop.close()
            
            if result:
                self.connection_status_label.setText("✅ Kết nối thành công")
                self.connection_status_label.setStyleSheet("color: green; font-weight: bold;")
                self.connection_info_label.setText("API token hợp lệ và có thể kết nối đến Apify.")
            else:
                self.connection_status_label.setText("❌ Kết nối thất bại")
                self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")
                self.connection_info_label.setText("Không thể kết nối đến Apify. Vui lòng kiểm tra API token.")
        
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            self.connection_status_label.setText("❌ Lỗi kết nối")
            self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connection_info_label.setText(f"Lỗi: {str(e)}")
        
        finally:
            self.test_connection_btn.setEnabled(True)
            self.test_connection_btn.setText("🔍 Test kết nối")
    
    def update_connection_status(self):
        """Cập nhật trạng thái kết nối"""
        if self.auth_manager.has_token():
            self.connection_status_label.setText("✅ Đã cấu hình")
            self.connection_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.connection_info_label.setText("API token đã được cấu hình. Click 'Test kết nối' để kiểm tra.")
        else:
            self.connection_status_label.setText("❌ Chưa cấu hình")
            self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connection_info_label.setText("Chưa có API token. Vui lòng nhập API token.")
    
    def save_settings(self):
        """Lưu cài đặt"""
        try:
            # Save API token
            token = self.api_token_input.text().strip()
            if token:
                if not self.auth_manager.validate_token_format(token):
                    QMessageBox.warning(
                        self,
                        "API Token không hợp lệ",
                        "API token có định dạng không đúng. Vui lòng kiểm tra lại."
                    )
                    return
                
                self.auth_manager.set_token(token)
            
            # Save app settings (placeholder)
            # TODO: Implement app settings saving
            
            QMessageBox.information(
                self,
                "Lưu thành công",
                "Cài đặt đã được lưu thành công."
            )
            
            self.accept()
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            QMessageBox.critical(
                self,
                "Lỗi lưu cài đặt",
                f"Không thể lưu cài đặt:\n{str(e)}"
            )
