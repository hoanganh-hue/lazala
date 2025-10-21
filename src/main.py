"""
Entry point cho Google Maps Scraper Desktop Application
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.main_window import MainWindow
from utils.logger import setup_logging, get_logger
from config import APP_NAME, APP_VERSION, RESOURCES_DIR

logger = get_logger(__name__)


def main():
    """Main function để khởi động ứng dụng"""
    try:
        # Setup logging
        setup_logging()
        logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        
        # Tạo QApplication
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        app.setOrganizationName("Google Maps Scraper Team")
        
        # Set application icon nếu có
        icon_path = RESOURCES_DIR / "icons" / "app_icon.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        # Set application style
        app.setStyle('Fusion')
        
        # Load stylesheet
        stylesheet_path = RESOURCES_DIR / "styles" / "main.qss"
        if stylesheet_path.exists():
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
        
        # Tạo và hiển thị main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Application started successfully")
        
        # Chạy event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        
        # Hiển thị error dialog nếu có thể
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(
                None,
                "Lỗi khởi động ứng dụng",
                f"Không thể khởi động {APP_NAME}:\n\n{str(e)}\n\nVui lòng kiểm tra log file để biết thêm chi tiết."
            )
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
