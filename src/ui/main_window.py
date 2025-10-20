"""
Main window cho Google Maps Scraper application
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QWidget, QMenuBar, QToolBar, QStatusBar, QAction,
    QMessageBox, QProgressBar, QLabel
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QKeySequence

from .search_tab import SearchTab
from .filters_tab import FiltersTab
from .details_tab import DetailsTab
from .addons_tab import AddonsTab
from .results_tab import ResultsTab
from .settings_dialog import SettingsDialog

from ..api.auth import AuthManager
from ..api.apify_client import ApifyClient
from ..config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Main window của ứng dụng"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.auth_manager = AuthManager()
        self.apify_client = ApifyClient(self.auth_manager)
        
        # Initialize UI
        self.init_ui()
        self.setup_connections()
        self.update_status()
        
        logger.info("Main window initialized")
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle(f"{APP_NAME} - Thu thập dữ liệu Google Maps")
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set window icon
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.search_tab = SearchTab()
        self.filters_tab = FiltersTab()
        self.details_tab = DetailsTab()
        self.addons_tab = AddonsTab()
        self.results_tab = ResultsTab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.search_tab, "🔍 Tìm kiếm cơ bản")
        self.tab_widget.addTab(self.filters_tab, "🎯 Bộ lọc nâng cao")
        self.tab_widget.addTab(self.details_tab, "📋 Thu thập chi tiết")
        self.tab_widget.addTab(self.addons_tab, "⭐ Add-ons Premium")
        self.tab_widget.addTab(self.results_tab, "📊 Kết quả & Xuất dữ liệu")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create tool bar
        self.create_tool_bar()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Tạo menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New search action
        new_action = QAction("&Tìm kiếm mới", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip("Bắt đầu tìm kiếm mới")
        new_action.triggered.connect(self.new_search)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        # Save configuration action
        save_config_action = QAction("&Lưu cấu hình", self)
        save_config_action.setShortcut(QKeySequence.Save)
        save_config_action.setStatusTip("Lưu cấu hình tìm kiếm")
        save_config_action.triggered.connect(self.save_configuration)
        file_menu.addAction(save_config_action)
        
        # Load configuration action
        load_config_action = QAction("&Tải cấu hình", self)
        load_config_action.setShortcut(QKeySequence.Open)
        load_config_action.setStatusTip("Tải cấu hình tìm kiếm")
        load_config_action.triggered.connect(self.load_configuration)
        file_menu.addAction(load_config_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("&Thoát", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip("Thoát ứng dụng")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Settings action
        settings_action = QAction("&Cài đặt", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.setStatusTip("Mở cài đặt ứng dụng")
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About action
        about_action = QAction("&Giới thiệu", self)
        about_action.setStatusTip("Thông tin về ứng dụng")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """Tạo tool bar"""
        toolbar = self.addToolBar("Main")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        # New search action
        new_action = QAction("🆕 Tìm kiếm mới", self)
        new_action.setStatusTip("Bắt đầu tìm kiếm mới")
        new_action.triggered.connect(self.new_search)
        toolbar.addAction(new_action)
        
        toolbar.addSeparator()
        
        # Start scraping action
        self.start_action = QAction("▶️ Bắt đầu thu thập", self)
        self.start_action.setStatusTip("Bắt đầu thu thập dữ liệu")
        self.start_action.triggered.connect(self.start_scraping)
        toolbar.addAction(self.start_action)
        
        # Stop scraping action
        self.stop_action = QAction("⏹️ Dừng", self)
        self.stop_action.setStatusTip("Dừng thu thập dữ liệu")
        self.stop_action.triggered.connect(self.stop_scraping)
        self.stop_action.setEnabled(False)
        toolbar.addAction(self.stop_action)
        
        toolbar.addSeparator()
        
        # Export action
        export_action = QAction("📤 Xuất dữ liệu", self)
        export_action.setStatusTip("Xuất kết quả ra file")
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        # Settings action
        settings_action = QAction("⚙️ Cài đặt", self)
        settings_action.setStatusTip("Mở cài đặt")
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def create_status_bar(self):
        """Tạo status bar"""
        self.status_bar = self.statusBar()
        
        # API status label
        self.api_status_label = QLabel("API: Chưa kết nối")
        self.status_bar.addWidget(self.api_status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        self.status_bar.addPermanentWidget(self.status_label)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Connect search tab signals
        self.search_tab.start_scraping_signal.connect(self.start_scraping)
        
        # Connect results tab signals
        self.results_tab.export_signal.connect(self.export_data)
    
    def on_tab_changed(self, index):
        """Xử lý khi chuyển tab"""
        tab_names = [
            "Tìm kiếm cơ bản",
            "Bộ lọc nâng cao", 
            "Thu thập chi tiết",
            "Add-ons Premium",
            "Kết quả & Xuất dữ liệu"
        ]
        
        if 0 <= index < len(tab_names):
            self.status_label.setText(f"Tab: {tab_names[index]}")
    
    def new_search(self):
        """Bắt đầu tìm kiếm mới"""
        # Reset all tabs
        self.search_tab.reset_form()
        self.filters_tab.reset_form()
        self.details_tab.reset_form()
        self.addons_tab.reset_form()
        self.results_tab.clear_results()
        
        # Switch to search tab
        self.tab_widget.setCurrentIndex(0)
        
        self.status_label.setText("Tìm kiếm mới")
        logger.info("New search started")
    
    def save_configuration(self):
        """Lưu cấu hình"""
        # TODO: Implement save configuration
        QMessageBox.information(self, "Lưu cấu hình", "Tính năng lưu cấu hình sẽ được thêm trong phiên bản tiếp theo.")
    
    def load_configuration(self):
        """Tải cấu hình"""
        # TODO: Implement load configuration
        QMessageBox.information(self, "Tải cấu hình", "Tính năng tải cấu hình sẽ được thêm trong phiên bản tiếp theo.")
    
    def start_scraping(self):
        """Bắt đầu thu thập dữ liệu"""
        try:
            # Validate API token
            if not self.auth_manager.has_token():
                QMessageBox.warning(
                    self,
                    "Thiếu API Token",
                    "Vui lòng cấu hình API token trong Settings trước khi bắt đầu thu thập dữ liệu."
                )
                self.show_settings()
                return
            
            # Get search input from tabs
            search_input = self.get_search_input()
            
            # Validate search input
            if not search_input.search_strings_array:
                QMessageBox.warning(
                    self,
                    "Thiếu thông tin",
                    "Vui lòng nhập ít nhất một từ khóa tìm kiếm."
                )
                self.tab_widget.setCurrentIndex(0)
                return
            
            if not search_input.location_query:
                QMessageBox.warning(
                    self,
                    "Thiếu thông tin", 
                    "Vui lòng nhập địa điểm tìm kiếm."
                )
                self.tab_widget.setCurrentIndex(0)
                return
            
            # Switch to results tab
            self.tab_widget.setCurrentIndex(4)
            
            # Update UI state
            self.start_action.setEnabled(False)
            self.stop_action.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText("Đang thu thập dữ liệu...")
            
            # Start scraping in background
            self.results_tab.start_scraping(search_input)
            
            logger.info("Scraping started")
            
        except Exception as e:
            logger.error(f"Failed to start scraping: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể bắt đầu thu thập dữ liệu:\n{str(e)}"
            )
            self.reset_ui_state()
    
    def stop_scraping(self):
        """Dừng thu thập dữ liệu"""
        try:
            self.results_tab.stop_scraping()
            self.reset_ui_state()
            self.status_label.setText("Đã dừng thu thập dữ liệu")
            logger.info("Scraping stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop scraping: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể dừng thu thập dữ liệu:\n{str(e)}"
            )
    
    def export_data(self):
        """Xuất dữ liệu"""
        try:
            self.results_tab.export_data()
            
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể xuất dữ liệu:\n{str(e)}"
            )
    
    def show_settings(self):
        """Hiển thị dialog cài đặt"""
        dialog = SettingsDialog(self.auth_manager, self)
        if dialog.exec_() == SettingsDialog.Accepted:
            self.update_status()
            logger.info("Settings updated")
    
    def show_about(self):
        """Hiển thị thông tin về ứng dụng"""
        QMessageBox.about(
            self,
            f"Giới thiệu {APP_NAME}",
            f"""
            <h3>{APP_NAME}</h3>
            <p>Phiên bản: {APP_VERSION}</p>
            <p>Ứng dụng desktop để thu thập dữ liệu từ Google Maps thông qua Apify API.</p>
            <p><b>Tính năng chính:</b></p>
            <ul>
            <li>Thu thập dữ liệu từ Google Maps</li>
            <li>Bộ lọc nâng cao</li>
            <li>Thu thập chi tiết (reviews, hình ảnh)</li>
            <li>Add-ons premium</li>
            <li>Xuất dữ liệu ra Excel, CSV, JSON</li>
            </ul>
            <p><b>Phát triển bởi:</b> Google Maps Scraper Team</p>
            <p><b>Website:</b> <a href="https://apify.com/compass/crawler-google-places">Apify Google Maps Scraper</a></p>
            """
        )
    
    def get_search_input(self):
        """Lấy search input từ các tabs"""
        from ..api.models import SearchInput
        
        search_input = SearchInput()
        
        # Get data from search tab
        search_data = self.search_tab.get_search_data()
        search_input.search_strings_array = search_data.get("search_strings", [])
        search_input.location_query = search_data.get("location", "")
        search_input.max_crawled_places_per_search = search_data.get("max_places")
        search_input.language = search_data.get("language", "en")
        
        # Get data from filters tab
        filters_data = self.filters_tab.get_filters_data()
        search_input.category_filter_words = filters_data.get("categories", [])
        search_input.search_matching = filters_data.get("search_matching", "all")
        search_input.place_minimum_stars = filters_data.get("minimum_stars")
        search_input.website = filters_data.get("website", "allPlaces")
        search_input.skip_closed_places = filters_data.get("skip_closed", False)
        
        # Get data from details tab
        details_data = self.details_tab.get_details_data()
        search_input.scrape_place_detail_page = details_data.get("scrape_details", False)
        search_input.scrape_table_reservation_provider = details_data.get("reservation_data", False)
        search_input.include_web_results = details_data.get("web_results", False)
        search_input.scrape_directories = details_data.get("directories", False)
        search_input.max_questions = details_data.get("max_questions", 0)
        search_input.max_reviews = details_data.get("max_reviews", 0)
        search_input.reviews_start_date = details_data.get("reviews_start_date")
        search_input.reviews_sort = details_data.get("reviews_sort", "newest")
        search_input.max_images = details_data.get("max_images", 0)
        
        # Get data from addons tab
        addons_data = self.addons_tab.get_addons_data()
        search_input.scrape_contacts = addons_data.get("scrape_contacts", False)
        search_input.maximum_leads_enrichment_records = addons_data.get("max_leads", 0)
        search_input.leads_enrichment_departments = addons_data.get("leads_departments", [])
        
        return search_input
    
    def update_status(self):
        """Cập nhật trạng thái"""
        if self.auth_manager.has_token():
            self.api_status_label.setText("API: Đã kết nối")
            self.api_status_label.setStyleSheet("color: green;")
        else:
            self.api_status_label.setText("API: Chưa kết nối")
            self.api_status_label.setStyleSheet("color: red;")
    
    def reset_ui_state(self):
        """Reset UI state"""
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Sẵn sàng")
    
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        try:
            # Stop any running scraping
            if self.stop_action.isEnabled():
                self.stop_scraping()
            
            logger.info("Application closing")
            event.accept()
            
        except Exception as e:
            logger.error(f"Error during close: {e}")
            event.accept()
