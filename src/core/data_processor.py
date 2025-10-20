"""
Data processor - Xử lý dữ liệu
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..api.models import SearchResult
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """Xử lý và phân tích dữ liệu"""
    
    def __init__(self):
        pass
    
    def process_results(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Xử lý và phân tích kết quả"""
        try:
            stats = self._calculate_statistics(results)
            processed_results = self._clean_data(results)
            
            return {
                "results": processed_results,
                "statistics": stats,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process results: {e}")
            return {
                "results": results,
                "statistics": {},
                "error": str(e)
            }
    
    def _calculate_statistics(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Tính toán thống kê"""
        if not results:
            return {}
        
        total_places = len(results)
        places_with_phone = sum(1 for r in results if r.phone)
        places_with_website = sum(1 for r in results if r.website)
        places_with_reviews = sum(1 for r in results if r.reviews_count and r.reviews_count > 0)
        closed_places = sum(1 for r in results if r.permanently_closed)
        
        # Calculate average rating
        ratings = [r.total_score for r in results if r.total_score]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Calculate total reviews
        total_reviews = sum(r.reviews_count for r in results if r.reviews_count)
        
        # Category distribution
        categories = {}
        for result in results:
            if result.category_name:
                categories[result.category_name] = categories.get(result.category_name, 0) + 1
        
        # Top categories
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # City distribution
        cities = {}
        for result in results:
            if result.city:
                cities[result.city] = cities.get(result.city, 0) + 1
        
        top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_places": total_places,
            "places_with_phone": places_with_phone,
            "places_with_website": places_with_website,
            "places_with_reviews": places_with_reviews,
            "closed_places": closed_places,
            "average_rating": round(avg_rating, 2),
            "total_reviews": total_reviews,
            "phone_percentage": round((places_with_phone / total_places) * 100, 2),
            "website_percentage": round((places_with_website / total_places) * 100, 2),
            "reviews_percentage": round((places_with_reviews / total_places) * 100, 2),
            "top_categories": top_categories,
            "top_cities": top_cities
        }
    
    def _clean_data(self, results: List[SearchResult]) -> List[SearchResult]:
        """Làm sạch dữ liệu"""
        cleaned_results = []
        
        for result in results:
            try:
                # Clean text fields
                if result.title:
                    result.title = result.title.strip()
                if result.address:
                    result.address = result.address.strip()
                if result.phone:
                    result.phone = self._clean_phone(result.phone)
                if result.website:
                    result.website = self._clean_website(result.website)
                
                # Validate coordinates
                if result.latitude and result.longitude:
                    if not self._is_valid_coordinate(result.latitude, result.longitude):
                        result.latitude = None
                        result.longitude = None
                
                cleaned_results.append(result)
                
            except Exception as e:
                logger.warning(f"Failed to clean result {result.title}: {e}")
                cleaned_results.append(result)
        
        return cleaned_results
    
    def _clean_phone(self, phone: str) -> str:
        """Làm sạch số điện thoại"""
        if not phone:
            return ""
        
        # Remove extra whitespace
        phone = phone.strip()
        
        # Remove common prefixes
        prefixes_to_remove = ["Tel:", "Phone:", "Điện thoại:", "SĐT:"]
        for prefix in prefixes_to_remove:
            if phone.startswith(prefix):
                phone = phone[len(prefix):].strip()
        
        return phone
    
    def _clean_website(self, website: str) -> str:
        """Làm sạch website URL"""
        if not website:
            return ""
        
        website = website.strip()
        
        # Add protocol if missing
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        return website
    
    def _is_valid_coordinate(self, lat: float, lng: float) -> bool:
        """Kiểm tra tọa độ hợp lệ"""
        try:
            lat = float(lat)
            lng = float(lng)
            
            # Check latitude range (-90 to 90)
            if not -90 <= lat <= 90:
                return False
            
            # Check longitude range (-180 to 180)
            if not -180 <= lng <= 180:
                return False
            
            return True
            
        except (ValueError, TypeError):
            return False
    
    def filter_results(
        self, 
        results: List[SearchResult], 
        filters: Dict[str, Any]
    ) -> List[SearchResult]:
        """Lọc kết quả theo điều kiện"""
        filtered_results = []
        
        for result in results:
            if self._matches_filters(result, filters):
                filtered_results.append(result)
        
        return filtered_results
    
    def _matches_filters(self, result: SearchResult, filters: Dict[str, Any]) -> bool:
        """Kiểm tra kết quả có khớp với bộ lọc không"""
        try:
            # Filter by minimum rating
            if "min_rating" in filters and filters["min_rating"]:
                if not result.total_score or result.total_score < filters["min_rating"]:
                    return False
            
            # Filter by minimum reviews
            if "min_reviews" in filters and filters["min_reviews"]:
                if not result.reviews_count or result.reviews_count < filters["min_reviews"]:
                    return False
            
            # Filter by has website
            if "has_website" in filters:
                if filters["has_website"] and not result.website:
                    return False
                if not filters["has_website"] and result.website:
                    return False
            
            # Filter by has phone
            if "has_phone" in filters:
                if filters["has_phone"] and not result.phone:
                    return False
                if not filters["has_phone"] and result.phone:
                    return False
            
            # Filter by closed status
            if "skip_closed" in filters and filters["skip_closed"]:
                if result.permanently_closed or result.temporarily_closed:
                    return False
            
            # Filter by categories
            if "categories" in filters and filters["categories"]:
                if not result.category_name or result.category_name not in filters["categories"]:
                    return False
            
            # Filter by city
            if "cities" in filters and filters["cities"]:
                if not result.city or result.city not in filters["cities"]:
                    return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Error checking filters for {result.title}: {e}")
            return True  # Include by default if filter check fails
    
    def deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Loại bỏ kết quả trùng lặp"""
        seen = set()
        unique_results = []
        
        for result in results:
            # Create a unique key based on place_id or combination of name and address
            if result.place_id:
                key = result.place_id
            else:
                key = f"{result.title}_{result.address}".lower()
            
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        return unique_results
    
    def sort_results(
        self, 
        results: List[SearchResult], 
        sort_by: str = "rating",
        reverse: bool = True
    ) -> List[SearchResult]:
        """Sắp xếp kết quả"""
        try:
            if sort_by == "rating":
                return sorted(results, key=lambda x: x.total_score or 0, reverse=reverse)
            elif sort_by == "reviews":
                return sorted(results, key=lambda x: x.reviews_count or 0, reverse=reverse)
            elif sort_by == "name":
                return sorted(results, key=lambda x: x.title or "", reverse=reverse)
            elif sort_by == "city":
                return sorted(results, key=lambda x: x.city or "", reverse=reverse)
            else:
                return results
                
        except Exception as e:
            logger.error(f"Failed to sort results: {e}")
            return results
