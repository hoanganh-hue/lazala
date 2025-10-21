"""
Input validator - Validate input parameters
"""

from typing import List, Dict, Any, Optional, Tuple
import re

from ..api.models import SearchInput
from ..utils.logger import get_logger

logger = get_logger(__name__)


class InputValidator:
    """Validate input parameters"""
    
    def __init__(self):
        pass
    
    def validate_search_input(self, search_input: SearchInput) -> Tuple[bool, List[str]]:
        """
        Validate search input
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate search strings
        if not search_input.search_strings_array:
            errors.append("Vui lòng nhập ít nhất một từ khóa tìm kiếm")
        else:
            for term in search_input.search_strings_array:
                if not term or not term.strip():
                    errors.append("Từ khóa tìm kiếm không được để trống")
                    break
                if len(term.strip()) < 2:
                    errors.append("Từ khóa tìm kiếm phải có ít nhất 2 ký tự")
                    break
        
        # Validate location
        if not search_input.location_query or not search_input.location_query.strip():
            errors.append("Vui lòng nhập địa điểm tìm kiếm")
        elif len(search_input.location_query.strip()) < 2:
            errors.append("Địa điểm tìm kiếm phải có ít nhất 2 ký tự")
        
        # Validate max places
        if search_input.max_crawled_places_per_search is not None:
            if search_input.max_crawled_places_per_search < 0:
                errors.append("Số lượng địa điểm phải >= 0")
            elif search_input.max_crawled_places_per_search > 10000:
                errors.append("Số lượng địa điểm không được vượt quá 10,000")
        
        # Validate language
        if search_input.language and not self._is_valid_language(search_input.language):
            errors.append("Ngôn ngữ không hợp lệ")
        
        # Validate search matching
        if search_input.search_matching and not self._is_valid_search_matching(search_input.search_matching):
            errors.append("Tùy chọn khớp tên không hợp lệ")
        
        # Validate minimum stars
        if search_input.place_minimum_stars and not self._is_valid_minimum_stars(search_input.place_minimum_stars):
            errors.append("Đánh giá tối thiểu không hợp lệ")
        
        # Validate website filter
        if search_input.website and not self._is_valid_website_filter(search_input.website):
            errors.append("Bộ lọc website không hợp lệ")
        
        # Validate reviews sort
        if search_input.reviews_sort and not self._is_valid_reviews_sort(search_input.reviews_sort):
            errors.append("Cách sắp xếp reviews không hợp lệ")
        
        # Validate numeric fields
        if search_input.max_questions is not None and search_input.max_questions < 0:
            errors.append("Số câu hỏi phải >= 0")
        
        if search_input.max_reviews is not None and search_input.max_reviews < 0:
            errors.append("Số reviews phải >= 0")
        
        if search_input.max_images is not None and search_input.max_images < 0:
            errors.append("Số hình ảnh phải >= 0")
        
        if search_input.maximum_leads_enrichment_records is not None and search_input.maximum_leads_enrichment_records < 0:
            errors.append("Số leads phải >= 0")
        
        # Validate reviews start date
        if search_input.reviews_start_date and not self._is_valid_date(search_input.reviews_start_date):
            errors.append("Ngày bắt đầu reviews không hợp lệ")
        
        return len(errors) == 0, errors
    
    def _is_valid_language(self, language: str) -> bool:
        """Validate language code"""
        valid_languages = {
            "en", "vi", "ja", "zh-CN", "zh-TW", "ko", "th", "fr", "de", "es", "it", "pt", "ru", "ar", "hi"
        }
        return language in valid_languages
    
    def _is_valid_search_matching(self, matching: str) -> bool:
        """Validate search matching option"""
        valid_options = {"all", "only_includes", "only_exact"}
        return matching in valid_options
    
    def _is_valid_minimum_stars(self, stars: str) -> bool:
        """Validate minimum stars option"""
        valid_options = {"two", "twoAndHalf", "three", "threeAndHalf", "four", "fourAndHalf"}
        return stars in valid_options
    
    def _is_valid_website_filter(self, website: str) -> bool:
        """Validate website filter option"""
        valid_options = {"allPlaces", "withWebsite", "withoutWebsite"}
        return website in valid_options
    
    def _is_valid_reviews_sort(self, sort: str) -> bool:
        """Validate reviews sort option"""
        valid_options = {"newest", "mostRelevant", "highestRanking", "lowestRanking"}
        return sort in valid_options
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Validate date string"""
        try:
            from datetime import datetime
            
            # Try different date formats
            formats = [
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ"
            ]
            
            for fmt in formats:
                try:
                    datetime.strptime(date_str, fmt)
                    return True
                except ValueError:
                    continue
            
            # Check for relative dates
            relative_patterns = [
                r'^\d+\s+(minute|hour|day|week|month|year)s?$',
                r'^\d+\s+(phút|giờ|ngày|tuần|tháng|năm)$'
            ]
            
            for pattern in relative_patterns:
                if re.match(pattern, date_str, re.IGNORECASE):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def validate_api_token(self, token: str) -> Tuple[bool, str]:
        """
        Validate API token format
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not token or not token.strip():
            return False, "API token không được để trống"
        
        token = token.strip()
        
        # Check for valid characters first (alphanumeric, underscore, hyphen)
        if not re.match(r'^[a-zA-Z0-9_-]+$', token):
            return False, "API token chứa ký tự không hợp lệ"
        
        # Check minimum length
        if len(token) < 20:
            return False, "API token quá ngắn"
        
        # Check maximum length
        if len(token) > 200:
            return False, "API token quá dài"
        
        # Check for common Apify token patterns
        if not (token.startswith('apify_api_') or token.startswith('apify_')):
            return False, "API token không có định dạng Apify hợp lệ"
        
        return True, ""
    
    def validate_location(self, location: str) -> Tuple[bool, str]:
        """
        Validate location string
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not location or not location.strip():
            return False, "Địa điểm không được để trống"
        
        location = location.strip()
        
        # Check minimum length
        if len(location) < 2:
            return False, "Địa điểm quá ngắn"
        
        # Check maximum length
        if len(location) > 200:
            return False, "Địa điểm quá dài"
        
        # Check for valid characters (letters, numbers, spaces, commas, hyphens, parentheses)
        if not re.match(r'^[a-zA-Z0-9\s,.\-()]+$', location):
            return False, "Địa điểm chứa ký tự không hợp lệ"
        
        return True, ""
    
    def validate_search_term(self, term: str) -> Tuple[bool, str]:
        """
        Validate search term
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not term or not term.strip():
            return False, "Từ khóa tìm kiếm không được để trống"
        
        term = term.strip()
        
        # Check minimum length
        if len(term) < 2:
            return False, "Từ khóa tìm kiếm quá ngắn"
        
        # Check maximum length
        if len(term) > 100:
            return False, "Từ khóa tìm kiếm quá dài"
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s.-]+$', term):
            return False, "Từ khóa tìm kiếm chứa ký tự không hợp lệ"
        
        return True, ""
    
    def sanitize_input(self, search_input: SearchInput) -> SearchInput:
        """Sanitize input data"""
        try:
            # Sanitize search strings
            if search_input.search_strings_array:
                search_input.search_strings_array = [
                    term.strip() for term in search_input.search_strings_array 
                    if term and term.strip()
                ]
            
            # Sanitize location
            if search_input.location_query:
                search_input.location_query = search_input.location_query.strip()
            
            # Sanitize category filter words
            if search_input.category_filter_words:
                search_input.category_filter_words = [
                    cat.strip() for cat in search_input.category_filter_words 
                    if cat and cat.strip()
                ]
            
            # Sanitize leads departments
            if search_input.leads_enrichment_departments:
                search_input.leads_enrichment_departments = [
                    dept.strip() for dept in search_input.leads_enrichment_departments 
                    if dept and dept.strip()
                ]
            
            # Sanitize reviews start date
            if search_input.reviews_start_date:
                search_input.reviews_start_date = search_input.reviews_start_date.strip()
            
            return search_input
            
        except Exception as e:
            logger.error(f"Failed to sanitize input: {e}")
            return search_input
