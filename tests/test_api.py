"""
Tests cho API module
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from src.api.models import SearchInput, SearchResult, RunStatus
from src.api.auth import AuthManager
from src.api.apify_client import ApifyClient


class TestSearchInput:
    """Test SearchInput model"""
    
    def test_to_dict_basic(self):
        """Test basic to_dict conversion"""
        search_input = SearchInput(
            search_strings_array=["restaurant"],
            location_query="Hanoi, Vietnam",
            max_crawled_places_per_search=50,
            language="vi"
        )
        
        result = search_input.to_dict()
        
        assert result["searchStringsArray"] == ["restaurant"]
        assert result["locationQuery"] == "Hanoi, Vietnam"
        assert result["maxCrawledPlacesPerSearch"] == 50
        assert result["language"] == "vi"
    
    def test_to_dict_advanced(self):
        """Test advanced to_dict conversion"""
        search_input = SearchInput(
            search_strings_array=["hotel"],
            location_query="Ho Chi Minh City, Vietnam",
            scrape_place_detail_page=True,
            max_reviews=100,
            scrape_contacts=True,
            maximum_leads_enrichment_records=10
        )
        
        result = search_input.to_dict()
        
        assert result["searchStringsArray"] == ["hotel"]
        assert result["locationQuery"] == "Ho Chi Minh City, Vietnam"
        assert result["scrapePlaceDetailPage"] is True
        assert result["maxReviews"] == 100
        assert result["scrapeContacts"] is True
        assert result["maximumLeadsEnrichmentRecords"] == 10
    
    def test_to_dict_defaults(self):
        """Test that default values are not included"""
        search_input = SearchInput()
        
        result = search_input.to_dict()
        
        # Should be empty or only include non-default values
        assert "searchStringsArray" not in result
        assert "language" not in result  # Default "en" should not be included
        assert "scrapePlaceDetailPage" not in result  # Default False should not be included


class TestSearchResult:
    """Test SearchResult model"""
    
    def test_from_dict_basic(self):
        """Test basic from_dict conversion"""
        data = {
            "title": "Test Restaurant",
            "address": "123 Test Street",
            "phone": "+84 123 456 789",
            "website": "https://test.com",
            "totalScore": 4.5,
            "reviewsCount": 100,
            "placeId": "test_place_id"
        }
        
        result = SearchResult.from_dict(data)
        
        assert result.title == "Test Restaurant"
        assert result.address == "123 Test Street"
        assert result.phone == "+84 123 456 789"
        assert result.website == "https://test.com"
        assert result.total_score == 4.5
        assert result.reviews_count == 100
        assert result.place_id == "test_place_id"
    
    def test_from_dict_location(self):
        """Test location parsing"""
        data = {
            "title": "Test Place",
            "location": {
                "lat": 21.0285,
                "lng": 105.8542
            },
            "plusCode": "7P2X+8Q Hanoi, Vietnam"
        }
        
        result = SearchResult.from_dict(data)
        
        assert result.latitude == 21.0285
        assert result.longitude == 105.8542
        assert result.plus_code == "7P2X+8Q Hanoi, Vietnam"


class TestRunStatus:
    """Test RunStatus model"""
    
    def test_from_dict_running(self):
        """Test parsing running status"""
        data = {
            "id": "test_run_id",
            "status": "RUNNING",
            "startedAt": "2024-01-01T10:00:00Z",
            "defaultDatasetId": "test_dataset_id"
        }
        
        status = RunStatus.from_dict(data)
        
        assert status.run_id == "test_run_id"
        assert status.status == "RUNNING"
        assert status.is_running is True
        assert status.is_succeeded is False
        assert status.is_failed is False
        assert status.default_dataset_id == "test_dataset_id"
    
    def test_from_dict_succeeded(self):
        """Test parsing succeeded status"""
        data = {
            "id": "test_run_id",
            "status": "SUCCEEDED",
            "startedAt": "2024-01-01T10:00:00Z",
            "finishedAt": "2024-01-01T10:05:00Z",
            "defaultDatasetId": "test_dataset_id"
        }
        
        status = RunStatus.from_dict(data)
        
        assert status.status == "SUCCEEDED"
        assert status.is_running is False
        assert status.is_succeeded is True
        assert status.is_failed is False
    
    def test_from_dict_failed(self):
        """Test parsing failed status"""
        data = {
            "id": "test_run_id",
            "status": "FAILED",
            "statusMessage": "Test error message"
        }
        
        status = RunStatus.from_dict(data)
        
        assert status.status == "FAILED"
        assert status.is_running is False
        assert status.is_succeeded is False
        assert status.is_failed is True
        assert status.error_message == "Test error message"


class TestAuthManager:
    """Test AuthManager"""
    
    def test_set_token(self):
        """Test setting token"""
        auth_manager = AuthManager()
        
        # Test valid token
        result = auth_manager.set_token("apify_api_test_token_123456789")
        assert result is True
        assert auth_manager.get_token() == "apify_api_test_token_123456789"
        assert auth_manager.has_token() is True
    
    def test_set_invalid_token(self):
        """Test setting invalid token"""
        auth_manager = AuthManager()
        
        # Test empty token
        result = auth_manager.set_token("")
        assert result is False
        assert not auth_manager.has_token()
        
        # Test None token
        result = auth_manager.set_token(None)
        assert result is False
        assert not auth_manager.has_token()
    
    def test_validate_token_format(self):
        """Test token format validation"""
        auth_manager = AuthManager()
        
        # Valid tokens
        assert auth_manager.validate_token_format("apify_api_test_token_123456789") is True
        assert auth_manager.validate_token_format("apify_test_token_123456789") is True
        
        # Invalid tokens
        assert auth_manager.validate_token_format("") is False
        assert auth_manager.validate_token_format("short") is False
        assert auth_manager.validate_token_format("invalid@token") is False
    
    def test_clear_token(self):
        """Test clearing token"""
        auth_manager = AuthManager()
        
        # Set token first
        auth_manager.set_token("apify_api_test_token_123456789")
        assert auth_manager.has_token() is True
        
        # Clear token
        auth_manager.clear_token()
        assert not auth_manager.has_token()
        assert auth_manager.get_token() is None


class TestApifyClient:
    """Test ApifyClient"""
    
    @pytest.fixture
    def auth_manager(self):
        """Create auth manager for testing"""
        auth_manager = AuthManager()
        auth_manager.set_token("apify_api_test_token_123456789")
        return auth_manager
    
    @pytest.fixture
    def apify_client(self, auth_manager):
        """Create Apify client for testing"""
        return ApifyClient(auth_manager)
    
    def test_get_headers(self, apify_client):
        """Test getting headers"""
        headers = apify_client._get_headers()
        
        assert "Content-Type" in headers
        assert "Authorization" in headers
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Bearer apify_api_test_token_123456789"
    
    def test_get_headers_no_token(self):
        """Test getting headers without token"""
        auth_manager = AuthManager()
        apify_client = ApifyClient(auth_manager)
        
        with pytest.raises(ValueError, match="API token chưa được cấu hình"):
            apify_client._get_headers()
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, apify_client):
        """Test successful connection test"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 200
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await apify_client.test_connection()
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, apify_client):
        """Test failed connection test"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 401
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await apify_client.test_connection()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_start_run_success(self, apify_client):
        """Test successful run start"""
        search_input = SearchInput(
            search_strings_array=["restaurant"],
            location_query="Hanoi, Vietnam"
        )
        
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json.return_value = {
                "data": {"id": "test_run_id"}
            }
            mock_post.return_value.__aenter__.return_value = mock_response
            
            run_id = await apify_client.start_run(search_input)
            
            assert run_id == "test_run_id"
    
    @pytest.mark.asyncio
    async def test_start_run_failure(self, apify_client):
        """Test failed run start"""
        search_input = SearchInput(
            search_strings_array=["restaurant"],
            location_query="Hanoi, Vietnam"
        )
        
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = Mock()
            mock_response.status = 400
            mock_response.text.return_value = "Bad Request"
            mock_post.return_value.__aenter__.return_value = mock_response
            
            with pytest.raises(Exception, match="Không thể bắt đầu run"):
                await apify_client.start_run(search_input)
