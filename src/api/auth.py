"""
Authentication manager cho Apify API
"""

import os
import configparser
from typing import Optional
from pathlib import Path

from ..config import CONFIG_FILE


class AuthManager:
    """Quản lý xác thực API token"""
    
    def __init__(self):
        self._token: Optional[str] = None
        self._load_token()
    
    def _load_token(self) -> None:
        """Load API token từ config file"""
        if CONFIG_FILE.exists():
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE, encoding='utf-8')
            
            if 'apify' in config and 'api_token' in config['apify']:
                self._token = config['apify']['api_token']
    
    def set_token(self, token: str) -> bool:
        """Set API token và lưu vào config file"""
        if not token or not token.strip():
            # Clear token if invalid value is provided
            self._token = None
            return False
            
        self._token = token.strip()
        self._save_token()
        return True
    
    def _save_token(self) -> None:
        """Lưu API token vào config file"""
        config = configparser.ConfigParser()
        
        # Load existing config nếu có
        if CONFIG_FILE.exists():
            config.read(CONFIG_FILE, encoding='utf-8')
        
        # Tạo section nếu chưa có
        if 'apify' not in config:
            config.add_section('apify')
        
        config.set('apify', 'api_token', self._token)
        
        # Tạo thư mục nếu chưa có
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Lưu file
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            config.write(f)
    
    def get_token(self) -> Optional[str]:
        """Lấy API token hiện tại"""
        return self._token
    
    def has_token(self) -> bool:
        """Kiểm tra có API token không"""
        return self._token is not None and self._token.strip() != ""
    
    def clear_token(self) -> None:
        """Xóa API token"""
        self._token = None
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
    
    def validate_token_format(self, token: str) -> bool:
        """Validate format của API token"""
        if not token or not token.strip():
            return False
        
        # Apify API token thường có format: apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        token = token.strip()
        if len(token) < 20:
            return False
            
        return True
