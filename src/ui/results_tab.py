"""
Results tab - Tab hiển thị kết quả và xuất dữ liệu
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QComboBox,
    QLabel, QProgressBar, QTextEdit, QGroupBox, QCheckBox,
    QHeaderView, QSplitter, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

from ..api.models import SearchInput, SearchResult
from ..api.apify_client import ApifyClient
from ..core.export_manager import ExportManager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ScrapingThread(QThread):
    """Thread để chạy scraping trong background"""
    
    progress_updated = pyqtSignal(str, int)  # message, progress
    results_ready = pyqtSignal(list)  # results
    error_occurred = pyqtSignal(str)  # error message
    finished = pyqtSignal()
    
    def __init__(self, apify_client, search_input):
        super().__init__()
        self.apify_client = apify_client
        self.search_input = search_input
        self.is_running = True
    
    def run(self):
        """Chạy scraping"""
        try:
            self.progress_updated.emit("Đang bắt đầu thu thập dữ liệu...", 0)
            
            # Start run
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            run_id = loop.run_until_complete(self.apify_client.start_run(self.search_input))
            self.progress_updated.emit(f"Run đã bắt đầu với ID: {run_id}", 10)
            
            # Wait for completion
            def progress_callback(status):
                if self.is_running:
                    self.progress_updated.emit(f"Đang thu thập... Status: {status.status}", 50)
            
            status = loop.run_until_complete(
                self.apify_client.wait_for_completion(run_id, progress_callback)
            )
            
            if not self.is_running:
                return
            
            if status.is_succeeded:
                self.progress_updated.emit("Đang tải kết quả...", 80)
                
                # Get results
                results = loop.run_until_complete(
                    self.apify_client.get_dataset_items(status.default_dataset_id)
                )
                
                # Convert to SearchResult objects
                search_results = []
                for item in results:
                    try:
                        result = SearchResult.from_dict(item)
                        search_results.append(result)
                    except Exception as e:
                        logger.warning(f"Failed to parse result: {e}")
                        continue
                
                self.progress_updated.emit(f"Hoàn thành! Thu thập được {len(search_results)} địa điểm", 100)
                self.results_ready.emit(search_results)
                
            else:
                error_msg = status.error_message or "Run thất bại"
                self.error_occurred.emit(error_msg)
            
            loop.close()
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            self.error_occurred.emit(str(e))
        
        finally:
            self.finished.emit()
    
    def stop(self):
        """Dừng scraping"""
        self.is_running = False


class ResultsTab(QWidget):
    """Tab hiển thị kết quả và xuất dữ liệu"""
    
    export_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.results = []
        self.scraping_thread = None
        self.export_manager = ExportManager()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("📊 Kết quả & Xuất dữ liệu")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Progress section
        progress_group = QGroupBox("Tiến trình")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Sẵn sàng để thu thập dữ liệu")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Results section
        results_group = QGroupBox("Kết quả")
        results_layout = QVBoxLayout(results_group)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels([
            "Tên", "Địa chỉ", "Điện thoại", "Website", 
            "Đánh giá", "Số reviews", "Danh mục", "Trạng thái"
        ])
        
        # Set table properties
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.MultiSelection)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        results_layout.addWidget(self.results_table)
        
        # Results info
        self.results_info_label = QLabel("Chưa có kết quả")
        results_layout.addWidget(self.results_info_label)
        
        layout.addWidget(results_group)
        
        # Export section
        export_group = QGroupBox("Xuất dữ liệu")
        export_layout = QVBoxLayout(export_group)
        
        # Export options
        export_options_layout = QHBoxLayout()
        
        # Export format
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"])
        export_options_layout.addWidget(QLabel("Định dạng:"))
        export_options_layout.addWidget(self.export_format_combo)
        
        # Export view
        self.export_view_combo = QComboBox()
        self.export_view_combo.addItems([
            "Tất cả dữ liệu",
            "Thông tin liên hệ",
            "Vị trí & đánh giá", 
            "Reviews",
            "Leads"
        ])
        export_options_layout.addWidget(QLabel("Chế độ xem:"))
        export_options_layout.addWidget(self.export_view_combo)
        
        # Selected only checkbox
        self.selected_only_cb = QCheckBox("Chỉ xuất các dòng đã chọn")
        export_options_layout.addWidget(self.selected_only_cb)
        
        export_options_layout.addStretch()
        export_layout.addLayout(export_options_layout)
        
        # Export buttons
        export_buttons_layout = QHBoxLayout()
        
        self.export_btn = QPushButton("📤 Xuất dữ liệu")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        self.copy_btn = QPushButton("📋 Sao chép")
        self.clear_btn = QPushButton("🗑️ Xóa kết quả")
        
        export_buttons_layout.addWidget(self.export_btn)
        export_buttons_layout.addWidget(self.copy_btn)
        export_buttons_layout.addWidget(self.clear_btn)
        export_buttons_layout.addStretch()
        
        export_layout.addLayout(export_buttons_layout)
        
        layout.addWidget(export_group)
        
        # Initially disable export button
        self.export_btn.setEnabled(False)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.export_btn.clicked.connect(self.export_data)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.clear_btn.clicked.connect(self.clear_results)
        self.results_table.itemSelectionChanged.connect(self.update_selection_info)
    
    def start_scraping(self, search_input: SearchInput):
        """Bắt đầu thu thập dữ liệu"""
        try:
            # Clear previous results
            self.clear_results()
            
            # Create and start scraping thread
            self.scraping_thread = ScrapingThread(self.apify_client, search_input)
            self.scraping_thread.progress_updated.connect(self.update_progress)
            self.scraping_thread.results_ready.connect(self.display_results)
            self.scraping_thread.error_occurred.connect(self.handle_error)
            self.scraping_thread.finished.connect(self.scraping_finished)
            
            self.scraping_thread.start()
            
            # Update UI
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            self.export_btn.setEnabled(False)
            
        except Exception as e:
            logger.error(f"Failed to start scraping: {e}")
            self.handle_error(str(e))
    
    def stop_scraping(self):
        """Dừng thu thập dữ liệu"""
        if self.scraping_thread and self.scraping_thread.isRunning():
            self.scraping_thread.stop()
            self.scraping_thread.wait()
    
    def update_progress(self, message: str, progress: int):
        """Cập nhật tiến trình"""
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)
    
    def display_results(self, results: list):
        """Hiển thị kết quả"""
        self.results = results
        self.populate_table(results)
        self.update_results_info()
        self.export_btn.setEnabled(True)
    
    def populate_table(self, results: list):
        """Điền dữ liệu vào bảng"""
        self.results_table.setRowCount(len(results))
        
        for row, result in enumerate(results):
            # Name
            name_item = QTableWidgetItem(result.title or "")
            self.results_table.setItem(row, 0, name_item)
            
            # Address
            address_item = QTableWidgetItem(result.address or "")
            self.results_table.setItem(row, 1, address_item)
            
            # Phone
            phone_item = QTableWidgetItem(result.phone or "")
            self.results_table.setItem(row, 2, phone_item)
            
            # Website
            website_item = QTableWidgetItem(result.website or "")
            self.results_table.setItem(row, 3, website_item)
            
            # Rating
            rating_text = f"{result.total_score:.1f}" if result.total_score else "N/A"
            rating_item = QTableWidgetItem(rating_text)
            self.results_table.setItem(row, 4, rating_item)
            
            # Reviews count
            reviews_text = str(result.reviews_count) if result.reviews_count else "0"
            reviews_item = QTableWidgetItem(reviews_text)
            self.results_table.setItem(row, 5, reviews_item)
            
            # Category
            category_item = QTableWidgetItem(result.category_name or "")
            self.results_table.setItem(row, 6, category_item)
            
            # Status
            status_text = "Đóng cửa" if result.permanently_closed else "Mở cửa"
            status_item = QTableWidgetItem(status_text)
            if result.permanently_closed:
                status_item.setBackground(QColor(255, 200, 200))
            else:
                status_item.setBackground(QColor(200, 255, 200))
            self.results_table.setItem(row, 7, status_item)
    
    def update_results_info(self):
        """Cập nhật thông tin kết quả"""
        total = len(self.results)
        selected = len(self.results_table.selectedItems()) // 8  # 8 columns
        
        info_text = f"Tổng cộng: {total} địa điểm"
        if selected > 0:
            info_text += f" | Đã chọn: {selected} địa điểm"
        
        self.results_info_label.setText(info_text)
    
    def update_selection_info(self):
        """Cập nhật thông tin lựa chọn"""
        self.update_results_info()
    
    def handle_error(self, error_message: str):
        """Xử lý lỗi"""
        self.status_label.setText(f"Lỗi: {error_message}")
        self.progress_bar.setVisible(False)
        self.export_btn.setEnabled(False)
        
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(
            self,
            "Lỗi thu thập dữ liệu",
            f"Đã xảy ra lỗi khi thu thập dữ liệu:\n\n{error_message}"
        )
    
    def scraping_finished(self):
        """Xử lý khi scraping hoàn thành"""
        self.progress_bar.setVisible(False)
        if self.scraping_thread:
            self.scraping_thread.deleteLater()
            self.scraping_thread = None
    
    def export_data(self):
        """Xuất dữ liệu"""
        if not self.results:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Không có dữ liệu",
                "Không có dữ liệu để xuất. Vui lòng thu thập dữ liệu trước."
            )
            return
        
        try:
            # Get selected results if needed
            results_to_export = self.results
            if self.selected_only_cb.isChecked():
                selected_rows = set()
                for item in self.results_table.selectedItems():
                    selected_rows.add(item.row())
                results_to_export = [self.results[row] for row in selected_rows if row < len(self.results)]
            
            if not results_to_export:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Không có dữ liệu được chọn",
                    "Vui lòng chọn ít nhất một dòng dữ liệu để xuất."
                )
                return
            
            # Get export options
            format_index = self.export_format_combo.currentIndex()
            format_map = {0: "excel", 1: "csv", 2: "json"}
            export_format = format_map[format_index]
            
            view_index = self.export_view_combo.currentIndex()
            view_map = {0: "all", 1: "contacts", 2: "location_rating", 3: "reviews", 4: "leads"}
            export_view = view_map[view_index]
            
            # Export data
            file_path = self.export_manager.export_data(
                results_to_export, 
                export_format, 
                export_view
            )
            
            if file_path:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Xuất dữ liệu thành công",
                    f"Dữ liệu đã được xuất thành công:\n{file_path}"
                )
                
                # Emit signal
                self.export_signal.emit()
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Lỗi xuất dữ liệu",
                f"Không thể xuất dữ liệu:\n{str(e)}"
            )
    
    def copy_to_clipboard(self):
        """Sao chép dữ liệu vào clipboard"""
        if not self.results:
            return
        
        try:
            import pandas as pd
            
            # Convert results to DataFrame
            data = []
            for result in self.results:
                data.append({
                    "Tên": result.title or "",
                    "Địa chỉ": result.address or "",
                    "Điện thoại": result.phone or "",
                    "Website": result.website or "",
                    "Đánh giá": result.total_score or 0,
                    "Số reviews": result.reviews_count or 0,
                    "Danh mục": result.category_name or ""
                })
            
            df = pd.DataFrame(data)
            
            # Copy to clipboard
            df.to_clipboard(index=False)
            
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Sao chép thành công",
                f"Đã sao chép {len(data)} dòng dữ liệu vào clipboard."
            )
            
        except Exception as e:
            logger.error(f"Copy to clipboard failed: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Lỗi sao chép",
                f"Không thể sao chép dữ liệu:\n{str(e)}"
            )
    
    def clear_results(self):
        """Xóa kết quả"""
        self.results = []
        self.results_table.setRowCount(0)
        self.update_results_info()
        self.export_btn.setEnabled(False)
        self.status_label.setText("Sẵn sàng để thu thập dữ liệu")
        self.progress_bar.setVisible(False)
