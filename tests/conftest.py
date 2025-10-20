"""
Pytest configuration and fixtures
"""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from src.api.models import SearchInput, SearchResult
from src.api.auth import AuthManager
from src.api.apify_client import ApifyClient
from datetime import datetime


@pytest.fixture
def sample_search_input():
    """Create sample search input for testing"""
    return SearchInput(
        search_strings_array=["restaurant", "hotel"],
        location_query="Hanoi, Vietnam",
        max_crawled_places_per_search=50,
        language="vi",
        scrape_place_detail_page=True,
        max_reviews=100,
        scrape_contacts=True
    )


@pytest.fixture
def sample_search_result():
    """Create sample search result for testing"""
    return SearchResult(
        title="Test Restaurant",
        address="123 Test Street, Hanoi",
        phone="+84 123 456 789",
        website="https://test.com",
        total_score=4.5,
        reviews_count=100,
        city="Hanoi",
        country_code="VN",
        latitude=21.0285,
        longitude=105.8542,
        category_name="Restaurant",
        scraped_at=datetime.now()
    )


@pytest.fixture
def sample_search_results(sample_search_result):
    """Create list of sample search results"""
    results = [sample_search_result]
    
    # Add more sample results
    result2 = SearchResult(
        title="Test Hotel",
        address="456 Hotel Street, Ho Chi Minh City",
        phone="+84 987 654 321",
        website="https://hotel.com",
        total_score=4.2,
        reviews_count=50,
        city="Ho Chi Minh City",
        country_code="VN",
        latitude=10.8231,
        longitude=106.6297,
        category_name="Hotel",
        scraped_at=datetime.now()
    )
    results.append(result2)
    
    return results


@pytest.fixture
def auth_manager():
    """Create auth manager for testing"""
    manager = AuthManager()
    yield manager
    # Cleanup: clear token after test
    manager.clear_token()


@pytest.fixture
def apify_client(auth_manager):
    """Create Apify client for testing"""
    # Set a test token
    auth_manager.set_token("apify_api_test_token_123456789")
    return ApifyClient(auth_manager)


@pytest.fixture
def mock_api_response():
    """Mock API response data"""
    return {
        "data": {
            "id": "test_run_id",
            "status": "SUCCEEDED",
            "startedAt": "2024-01-01T10:00:00Z",
            "finishedAt": "2024-01-01T10:05:00Z",
            "defaultDatasetId": "test_dataset_id"
        }
    }


@pytest.fixture
def mock_dataset_items():
    """Mock dataset items"""
    return {
        "data": [
            {
                "title": "Test Restaurant 1",
                "address": "123 Test Street, Hanoi",
                "phone": "+84 123 456 789",
                "website": "https://test1.com",
                "totalScore": 4.5,
                "reviewsCount": 100,
                "location": {
                    "lat": 21.0285,
                    "lng": 105.8542
                },
                "categoryName": "Restaurant",
                "placeId": "test_place_1"
            },
            {
                "title": "Test Restaurant 2",
                "address": "456 Test Street, Hanoi",
                "phone": "+84 987 654 321",
                "website": "https://test2.com",
                "totalScore": 4.2,
                "reviewsCount": 50,
                "location": {
                    "lat": 21.0300,
                    "lng": 105.8600
                },
                "categoryName": "Restaurant",
                "placeId": "test_place_2"
            }
        ]
    }


@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        "test_api_token": "apify_api_test_token_123456789",
        "test_location": "Hanoi, Vietnam",
        "test_search_terms": ["restaurant", "hotel", "coffee shop"],
        "test_max_places": 10
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add unit marker to all tests by default
        if not any(marker.name in ["slow", "integration"] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
