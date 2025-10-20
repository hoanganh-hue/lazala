"""
Tests cho Core module
"""

import pytest
from datetime import datetime

from src.core.export_manager import ExportManager
from src.core.data_processor import DataProcessor
from src.core.validator import InputValidator
from src.api.models import SearchInput, SearchResult


class TestExportManager:
    """Test ExportManager"""
    
    @pytest.fixture
    def export_manager(self):
        """Create export manager for testing"""
        return ExportManager()
    
    @pytest.fixture
    def sample_results(self):
        """Create sample results for testing"""
        results = []
        
        # Create sample result 1
        result1 = SearchResult()
        result1.title = "Test Restaurant 1"
        result1.address = "123 Test Street, Hanoi"
        result1.phone = "+84 123 456 789"
        result1.website = "https://test1.com"
        result1.total_score = 4.5
        result1.reviews_count = 100
        result1.city = "Hanoi"
        result1.country_code = "VN"
        result1.latitude = 21.0285
        result1.longitude = 105.8542
        result1.category_name = "Restaurant"
        result1.scraped_at = datetime.now()
        results.append(result1)
        
        # Create sample result 2
        result2 = SearchResult()
        result2.title = "Test Hotel 1"
        result2.address = "456 Hotel Street, Ho Chi Minh City"
        result2.phone = "+84 987 654 321"
        result2.website = "https://test2.com"
        result2.total_score = 4.2
        result2.reviews_count = 50
        result2.city = "Ho Chi Minh City"
        result2.country_code = "VN"
        result2.latitude = 10.8231
        result2.longitude = 106.6297
        result2.category_name = "Hotel"
        result2.scraped_at = datetime.now()
        results.append(result2)
        
        return results
    
    def test_convert_to_all_data(self, export_manager, sample_results):
        """Test converting to all data format"""
        data = export_manager._convert_to_all_data(sample_results)
        
        assert len(data) == 2
        assert data[0]["Tên"] == "Test Restaurant 1"
        assert data[0]["Địa chỉ"] == "123 Test Street, Hanoi"
        assert data[0]["Điện thoại"] == "+84 123 456 789"
        assert data[0]["Website"] == "https://test1.com"
        assert data[0]["Đánh giá"] == 4.5
        assert data[0]["Số reviews"] == 100
        assert data[0]["Thành phố"] == "Hanoi"
        assert data[0]["Quốc gia"] == "VN"
        assert data[0]["Vĩ độ"] == 21.0285
        assert data[0]["Kinh độ"] == 105.8542
        assert data[0]["Danh mục"] == "Restaurant"
    
    def test_convert_to_contacts_data(self, export_manager, sample_results):
        """Test converting to contacts data format"""
        data = export_manager._convert_to_contacts_data(sample_results)
        
        assert len(data) == 2
        assert data[0]["Tên"] == "Test Restaurant 1"
        assert data[0]["Địa chỉ"] == "123 Test Street, Hanoi"
        assert data[0]["Điện thoại"] == "+84 123 456 789"
        assert data[0]["Website"] == "https://test1.com"
        assert data[0]["Email"] == ""  # No contact info in sample
    
    def test_convert_to_location_rating_data(self, export_manager, sample_results):
        """Test converting to location & rating data format"""
        data = export_manager._convert_to_location_rating_data(sample_results)
        
        assert len(data) == 2
        assert data[0]["Tên"] == "Test Restaurant 1"
        assert data[0]["Thành phố"] == "Hanoi"
        assert data[0]["Tỉnh/Thành"] == ""
        assert data[0]["Quốc gia"] == "VN"
        assert data[0]["Vĩ độ"] == 21.0285
        assert data[0]["Kinh độ"] == 105.8542
        assert data[0]["Đánh giá"] == 4.5
        assert data[0]["Số reviews"] == 100
        assert data[0]["Trạng thái"] == "Mở cửa"
    
    def test_export_data_no_results(self, export_manager):
        """Test exporting with no results"""
        result = export_manager.export_data([], "excel", "all")
        assert result is None
    
    def test_export_data_invalid_format(self, export_manager, sample_results):
        """Test exporting with invalid format"""
        result = export_manager.export_data(sample_results, "invalid", "all")
        assert result is None


class TestDataProcessor:
    """Test DataProcessor"""
    
    @pytest.fixture
    def data_processor(self):
        """Create data processor for testing"""
        return DataProcessor()
    
    @pytest.fixture
    def sample_results(self):
        """Create sample results for testing"""
        results = []
        
        # Create sample result 1
        result1 = SearchResult()
        result1.title = "Test Restaurant 1"
        result1.address = "123 Test Street, Hanoi"
        result1.phone = "+84 123 456 789"
        result1.website = "https://test1.com"
        result1.total_score = 4.5
        result1.reviews_count = 100
        result1.city = "Hanoi"
        result1.category_name = "Restaurant"
        result1.permanently_closed = False
        results.append(result1)
        
        # Create sample result 2
        result2 = SearchResult()
        result2.title = "Test Hotel 1"
        result2.address = "456 Hotel Street, Ho Chi Minh City"
        result2.phone = "+84 987 654 321"
        result2.website = "https://test2.com"
        result2.total_score = 4.2
        result2.reviews_count = 50
        result2.city = "Ho Chi Minh City"
        result2.category_name = "Hotel"
        result2.permanently_closed = False
        results.append(result2)
        
        # Create sample result 3 (closed)
        result3 = SearchResult()
        result3.title = "Closed Restaurant"
        result3.address = "789 Closed Street, Hanoi"
        result3.total_score = 3.0
        result3.reviews_count = 10
        result3.city = "Hanoi"
        result3.category_name = "Restaurant"
        result3.permanently_closed = True
        results.append(result3)
        
        return results
    
    def test_calculate_statistics(self, data_processor, sample_results):
        """Test calculating statistics"""
        stats = data_processor._calculate_statistics(sample_results)
        
        assert stats["total_places"] == 3
        assert stats["places_with_phone"] == 2
        assert stats["places_with_website"] == 2
        assert stats["places_with_reviews"] == 3
        assert stats["closed_places"] == 1
        assert stats["average_rating"] == pytest.approx(3.9, rel=1e-1)
        assert stats["total_reviews"] == 160
        assert stats["phone_percentage"] == pytest.approx(66.67, rel=1e-1)
        assert stats["website_percentage"] == pytest.approx(66.67, rel=1e-1)
        assert stats["reviews_percentage"] == 100.0
        
        # Check top categories
        assert len(stats["top_categories"]) == 2
        assert stats["top_categories"][0] == ("Restaurant", 2)
        assert stats["top_categories"][1] == ("Hotel", 1)
        
        # Check top cities
        assert len(stats["top_cities"]) == 2
        assert stats["top_cities"][0] == ("Hanoi", 2)
        assert stats["top_cities"][1] == ("Ho Chi Minh City", 1)
    
    def test_clean_phone(self, data_processor):
        """Test phone cleaning"""
        # Test normal phone
        assert data_processor._clean_phone("+84 123 456 789") == "+84 123 456 789"
        
        # Test phone with prefix
        assert data_processor._clean_phone("Tel: +84 123 456 789") == "+84 123 456 789"
        assert data_processor._clean_phone("Phone: +84 123 456 789") == "+84 123 456 789"
        assert data_processor._clean_phone("Điện thoại: +84 123 456 789") == "+84 123 456 789"
        
        # Test empty phone
        assert data_processor._clean_phone("") == ""
        assert data_processor._clean_phone(None) == ""
        
        # Test phone with extra spaces
        assert data_processor._clean_phone("  +84 123 456 789  ") == "+84 123 456 789"
    
    def test_clean_website(self, data_processor):
        """Test website cleaning"""
        # Test normal website
        assert data_processor._clean_website("https://test.com") == "https://test.com"
        
        # Test website without protocol
        assert data_processor._clean_website("test.com") == "https://test.com"
        assert data_processor._clean_website("www.test.com") == "https://www.test.com"
        
        # Test empty website
        assert data_processor._clean_website("") == ""
        assert data_processor._clean_website(None) == ""
        
        # Test website with extra spaces
        assert data_processor._clean_website("  test.com  ") == "https://test.com"
    
    def test_is_valid_coordinate(self, data_processor):
        """Test coordinate validation"""
        # Valid coordinates
        assert data_processor._is_valid_coordinate(21.0285, 105.8542) is True
        assert data_processor._is_valid_coordinate(-90, -180) is True
        assert data_processor._is_valid_coordinate(90, 180) is True
        
        # Invalid coordinates
        assert data_processor._is_valid_coordinate(91, 105.8542) is False  # Latitude too high
        assert data_processor._is_valid_coordinate(-91, 105.8542) is False  # Latitude too low
        assert data_processor._is_valid_coordinate(21.0285, 181) is False  # Longitude too high
        assert data_processor._is_valid_coordinate(21.0285, -181) is False  # Longitude too low
        
        # Invalid types
        assert data_processor._is_valid_coordinate("invalid", 105.8542) is False
        assert data_processor._is_valid_coordinate(21.0285, "invalid") is False
        assert data_processor._is_valid_coordinate(None, 105.8542) is False
    
    def test_filter_results(self, data_processor, sample_results):
        """Test filtering results"""
        # Filter by minimum rating
        filters = {"min_rating": 4.0}
        filtered = data_processor.filter_results(sample_results, filters)
        assert len(filtered) == 2  # Only 2 results with rating >= 4.0
        
        # Filter by has website
        filters = {"has_website": True}
        filtered = data_processor.filter_results(sample_results, filters)
        assert len(filtered) == 2  # Only 2 results with website
        
        # Filter by skip closed
        filters = {"skip_closed": True}
        filtered = data_processor.filter_results(sample_results, filters)
        assert len(filtered) == 2  # Only 2 results that are not closed
        
        # Filter by categories
        filters = {"categories": ["Restaurant"]}
        filtered = data_processor.filter_results(sample_results, filters)
        assert len(filtered) == 2  # Only 2 results with Restaurant category
    
    def test_deduplicate_results(self, data_processor):
        """Test deduplicating results"""
        # Create duplicate results
        result1 = SearchResult()
        result1.title = "Test Restaurant"
        result1.address = "123 Test Street"
        result1.place_id = "place_1"
        
        result2 = SearchResult()
        result2.title = "Test Restaurant"
        result2.address = "123 Test Street"
        result2.place_id = "place_1"  # Same place_id
        
        result3 = SearchResult()
        result3.title = "Different Restaurant"
        result3.address = "456 Different Street"
        result3.place_id = "place_2"
        
        results = [result1, result2, result3]
        unique_results = data_processor.deduplicate_results(results)
        
        assert len(unique_results) == 2  # Should remove duplicate
    
    def test_sort_results(self, data_processor, sample_results):
        """Test sorting results"""
        # Sort by rating (descending)
        sorted_results = data_processor.sort_results(sample_results, "rating", True)
        assert sorted_results[0].total_score == 4.5  # Highest rating first
        assert sorted_results[-1].total_score == 3.0  # Lowest rating last
        
        # Sort by reviews (descending)
        sorted_results = data_processor.sort_results(sample_results, "reviews", True)
        assert sorted_results[0].reviews_count == 100  # Most reviews first
        assert sorted_results[-1].reviews_count == 10  # Least reviews last
        
        # Sort by name (ascending)
        sorted_results = data_processor.sort_results(sample_results, "name", False)
        assert sorted_results[0].title == "Closed Restaurant"  # Alphabetically first
        assert sorted_results[-1].title == "Test Restaurant 1"  # Alphabetically last


class TestInputValidator:
    """Test InputValidator"""
    
    @pytest.fixture
    def validator(self):
        """Create validator for testing"""
        return InputValidator()
    
    def test_validate_search_input_valid(self, validator):
        """Test validating valid search input"""
        search_input = SearchInput(
            search_strings_array=["restaurant"],
            location_query="Hanoi, Vietnam",
            max_crawled_places_per_search=50,
            language="vi"
        )
        
        is_valid, errors = validator.validate_search_input(search_input)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_search_input_invalid(self, validator):
        """Test validating invalid search input"""
        search_input = SearchInput(
            search_strings_array=[],  # Empty search strings
            location_query="",  # Empty location
            max_crawled_places_per_search=-1,  # Invalid max places
            language="invalid"  # Invalid language
        )
        
        is_valid, errors = validator.validate_search_input(search_input)
        
        assert is_valid is False
        assert len(errors) > 0
        assert "Vui lòng nhập ít nhất một từ khóa tìm kiếm" in errors
        assert "Vui lòng nhập địa điểm tìm kiếm" in errors
        assert "Số lượng địa điểm phải >= 0" in errors
        assert "Ngôn ngữ không hợp lệ" in errors
    
    def test_validate_api_token(self, validator):
        """Test validating API token"""
        # Valid tokens
        is_valid, error = validator.validate_api_token("apify_api_test_token_123456789")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validator.validate_api_token("apify_test_token_123456789")
        assert is_valid is True
        assert error == ""
        
        # Invalid tokens
        is_valid, error = validator.validate_api_token("")
        assert is_valid is False
        assert "không được để trống" in error
        
        is_valid, error = validator.validate_api_token("short")
        assert is_valid is False
        assert "quá ngắn" in error
        
        is_valid, error = validator.validate_api_token("invalid@token")
        assert is_valid is False
        assert "ký tự không hợp lệ" in error
    
    def test_validate_location(self, validator):
        """Test validating location"""
        # Valid locations
        is_valid, error = validator.validate_location("Hanoi, Vietnam")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validator.validate_location("New York, USA")
        assert is_valid is True
        assert error == ""
        
        # Invalid locations
        is_valid, error = validator.validate_location("")
        assert is_valid is False
        assert "không được để trống" in error
        
        is_valid, error = validator.validate_location("A")
        assert is_valid is False
        assert "quá ngắn" in error
        
        is_valid, error = validator.validate_location("Hanoi@Vietnam")
        assert is_valid is False
        assert "ký tự không hợp lệ" in error
    
    def test_validate_search_term(self, validator):
        """Test validating search term"""
        # Valid terms
        is_valid, error = validator.validate_search_term("restaurant")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validator.validate_search_term("coffee shop")
        assert is_valid is True
        assert error == ""
        
        # Invalid terms
        is_valid, error = validator.validate_search_term("")
        assert is_valid is False
        assert "không được để trống" in error
        
        is_valid, error = validator.validate_search_term("A")
        assert is_valid is False
        assert "quá ngắn" in error
        
        is_valid, error = validator.validate_search_term("restaurant@shop")
        assert is_valid is False
        assert "ký tự không hợp lệ" in error
    
    def test_sanitize_input(self, validator):
        """Test sanitizing input"""
        search_input = SearchInput(
            search_strings_array=["  restaurant  ", "", "  hotel  "],
            location_query="  Hanoi, Vietnam  ",
            category_filter_words=["  food  ", "", "  drink  "],
            leads_enrichment_departments=["  sales  ", "", "  marketing  "]
        )
        
        sanitized = validator.sanitize_input(search_input)
        
        assert sanitized.search_strings_array == ["restaurant", "hotel"]
        assert sanitized.location_query == "Hanoi, Vietnam"
        assert sanitized.category_filter_words == ["food", "drink"]
        assert sanitized.leads_enrichment_departments == ["sales", "marketing"]
