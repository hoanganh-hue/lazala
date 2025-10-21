"""
Data models cho API input/output
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class SearchInput:
    """Model cho input parameters của Google Maps Scraper"""
    
    # Tham số cơ bản
    search_strings_array: List[str] = field(default_factory=list)
    location_query: Optional[str] = None
    max_crawled_places_per_search: Optional[int] = None
    language: str = "en"
    
    # Bộ lọc nâng cao
    category_filter_words: List[str] = field(default_factory=list)
    search_matching: str = "all"
    place_minimum_stars: Optional[str] = None
    website: str = "allPlaces"
    skip_closed_places: bool = False
    
    # Tùy chọn thu thập chi tiết
    scrape_place_detail_page: bool = False
    scrape_table_reservation_provider: bool = False
    include_web_results: bool = False
    scrape_directories: bool = False
    max_questions: int = 0
    max_reviews: int = 0
    reviews_start_date: Optional[str] = None
    reviews_sort: str = "newest"
    max_images: int = 0
    
    # Add-ons premium
    scrape_contacts: bool = False
    maximum_leads_enrichment_records: int = 0
    leads_enrichment_departments: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API call"""
        data = {}
        
        # Chỉ thêm các field không phải default values
        if self.search_strings_array:
            data["searchStringsArray"] = self.search_strings_array
        if self.location_query:
            data["locationQuery"] = self.location_query
        if self.max_crawled_places_per_search is not None:
            data["maxCrawledPlacesPerSearch"] = self.max_crawled_places_per_search
        if self.language != "en":
            data["language"] = self.language
            
        if self.category_filter_words:
            data["categoryFilterWords"] = self.category_filter_words
        if self.search_matching != "all":
            data["searchMatching"] = self.search_matching
        if self.place_minimum_stars:
            data["placeMinimumStars"] = self.place_minimum_stars
        if self.website != "allPlaces":
            data["website"] = self.website
        if self.skip_closed_places:
            data["skipClosedPlaces"] = self.skip_closed_places
            
        if self.scrape_place_detail_page:
            data["scrapePlaceDetailPage"] = self.scrape_place_detail_page
        if self.scrape_table_reservation_provider:
            data["scrapeTableReservationProvider"] = self.scrape_table_reservation_provider
        if self.include_web_results:
            data["includeWebResults"] = self.include_web_results
        if self.scrape_directories:
            data["scrapeDirectories"] = self.scrape_directories
        if self.max_questions > 0:
            data["maxQuestions"] = self.max_questions
        if self.max_reviews > 0:
            data["maxReviews"] = self.max_reviews
        if self.reviews_start_date:
            data["reviewsStartDate"] = self.reviews_start_date
        if self.reviews_sort != "newest":
            data["reviewsSort"] = self.reviews_sort
        if self.max_images > 0:
            data["maxImages"] = self.max_images
            
        if self.scrape_contacts:
            data["scrapeContacts"] = self.scrape_contacts
        if self.maximum_leads_enrichment_records > 0:
            data["maximumLeadsEnrichmentRecords"] = self.maximum_leads_enrichment_records
        if self.leads_enrichment_departments:
            data["leadsEnrichmentDepartments"] = self.leads_enrichment_departments
            
        return data


@dataclass
class SearchResult:
    """Model cho kết quả tìm kiếm từ Google Maps"""
    
    # Thông tin cơ bản
    title: Optional[str] = None
    sub_title: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    
    # Địa chỉ
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country_code: Optional[str] = None
    
    # Tọa độ
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    plus_code: Optional[str] = None
    
    # Liên hệ
    phone: Optional[str] = None
    phone_unformatted: Optional[str] = None
    website: Optional[str] = None
    
    # Đánh giá
    total_score: Optional[float] = None
    reviews_count: Optional[int] = None
    reviews_distribution: Optional[Dict[str, int]] = None
    
    # Trạng thái
    permanently_closed: bool = False
    temporarily_closed: bool = False
    
    # IDs
    place_id: Optional[str] = None
    cid: Optional[str] = None
    fid: Optional[str] = None
    
    # Thông tin bổ sung
    opening_hours: Optional[List[Dict[str, str]]] = None
    popular_times: Optional[Dict[str, Any]] = None
    menu: Optional[str] = None
    price: Optional[str] = None
    hotel_stars: Optional[int] = None
    
    # Reviews và hình ảnh
    reviews: Optional[List[Dict[str, Any]]] = None
    images: Optional[List[Dict[str, Any]]] = None
    
    # Dữ liệu khác
    people_also_search: Optional[List[Dict[str, Any]]] = None
    reviews_tags: Optional[List[Dict[str, Any]]] = None
    questions_and_answers: Optional[List[Dict[str, Any]]] = None
    contacts_from_website: Optional[Dict[str, Any]] = None
    leads_info: Optional[List[Dict[str, Any]]] = None
    
    # Metadata
    scraped_at: Optional[datetime] = None
    search_string: Optional[str] = None
    rank: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Tạo SearchResult từ dictionary"""
        result = cls()
        
        # Map các field từ API response
        result.title = data.get("title")
        result.sub_title = data.get("subTitle")
        result.category_name = data.get("categoryName")
        result.description = data.get("description")
        
        result.address = data.get("address")
        result.neighborhood = data.get("neighborhood")
        result.street = data.get("street")
        result.city = data.get("city")
        result.postal_code = data.get("postalCode")
        result.state = data.get("state")
        result.country_code = data.get("countryCode")
        
        # Location
        location = data.get("location", {})
        result.latitude = location.get("lat")
        result.longitude = location.get("lng")
        result.plus_code = data.get("plusCode")
        
        result.phone = data.get("phone")
        result.phone_unformatted = data.get("phoneUnformatted")
        result.website = data.get("website")
        
        result.total_score = data.get("totalScore")
        result.reviews_count = data.get("reviewsCount")
        result.reviews_distribution = data.get("reviewsDistribution")
        
        result.permanently_closed = data.get("permanentlyClosed", False)
        result.temporarily_closed = data.get("temporarilyClosed", False)
        
        result.place_id = data.get("placeId")
        result.cid = data.get("cid")
        result.fid = data.get("fid")
        
        result.opening_hours = data.get("openingHours")
        result.popular_times = data.get("popularTimes")
        result.menu = data.get("menu")
        result.price = data.get("price")
        result.hotel_stars = data.get("hotelStars")
        
        result.reviews = data.get("reviews")
        result.images = data.get("images")
        
        result.people_also_search = data.get("peopleAlsoSearch")
        result.reviews_tags = data.get("reviewsTags")
        result.questions_and_answers = data.get("questionsAndAnswers")
        result.contacts_from_website = data.get("contactsFromWebsite")
        result.leads_info = data.get("leadsInfo")
        
        # Metadata
        if data.get("scrapedAt"):
            try:
                result.scraped_at = datetime.fromisoformat(data["scrapedAt"].replace("Z", "+00:00"))
            except:
                pass
        result.search_string = data.get("searchString")
        result.rank = data.get("rank")
        
        return result


@dataclass
class RunStatus:
    """Model cho trạng thái của một run"""
    
    run_id: str
    status: str  # RUNNING, SUCCEEDED, FAILED, TIMED-OUT, ABORTED
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    default_dataset_id: Optional[str] = None
    stats: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunStatus":
        """Tạo RunStatus từ dictionary"""
        run = cls(
            run_id=data["id"],
            status=data["status"]
        )
        
        if data.get("startedAt"):
            try:
                run.started_at = datetime.fromisoformat(data["startedAt"].replace("Z", "+00:00"))
            except:
                pass
                
        if data.get("finishedAt"):
            try:
                run.finished_at = datetime.fromisoformat(data["finishedAt"].replace("Z", "+00:00"))
            except:
                pass
                
        run.default_dataset_id = data.get("defaultDatasetId")
        run.stats = data.get("stats")
        
        if data.get("statusMessage"):
            run.error_message = data["statusMessage"]
            
        return run
    
    @property
    def is_running(self) -> bool:
        return self.status == "RUNNING"
    
    @property
    def is_succeeded(self) -> bool:
        return self.status == "SUCCEEDED"
    
    @property
    def is_failed(self) -> bool:
        return self.status in ["FAILED", "TIMED-OUT", "ABORTED"]
