"""
Helper functions cho ứng dụng
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime, date


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Check if it has 7-15 digits (international standard)
    return 7 <= len(digits) <= 15


def format_phone(phone: str) -> str:
    """Format phone number"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        # US format: (123) 456-7890
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        # US format with country code: +1 (123) 456-7890
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        # International format: +1234567890
        return f"+{digits}"


def clean_text(text: str) -> str:
    """Clean và normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?@#$%&*()+=/:;]', '', text)
    
    return text


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text với ellipsis"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency"""
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "VND":
        return f"{amount:,.0f} VND"
    else:
        return f"{amount:.2f} {currency}"


def calculate_estimated_cost(
    max_places: int,
    filters_count: int = 0,
    scrape_details: bool = False,
    scrape_contacts: bool = False,
    max_leads: int = 0,
    max_reviews: int = 0,
    max_images: int = 0
) -> float:
    """Tính toán chi phí ước tính"""
    from ..config import PRICING
    
    cost = 0.0
    
    # Base cost per place
    cost += max_places * PRICING["place_scraped"] / 1000
    
    # Filter costs
    if filters_count > 0:
        cost += max_places * filters_count * PRICING["filter_applied"] / 1000
    
    # Additional details cost
    if scrape_details:
        cost += max_places * PRICING["additional_details"] / 1000
    
    # Contacts cost
    if scrape_contacts:
        cost += max_places * PRICING["company_contacts"] / 1000
    
    # Leads cost
    if max_leads > 0:
        cost += max_places * max_leads * PRICING["business_leads"] / 1000
    
    # Reviews cost
    if max_reviews > 0:
        cost += max_places * max_reviews * PRICING["review_scraped"] / 1000
    
    # Images cost
    if max_images > 0:
        cost += max_places * max_images * PRICING["image_scraped"] / 1000
    
    # Actor start cost
    cost += PRICING["actor_start"]
    
    return cost


def parse_date_string(date_str: str) -> Optional[date]:
    """Parse date string thành date object"""
    if not date_str:
        return None
    
    # Common date formats
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y", 
        "%m/%d/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    
    for fmt in formats:
        try:
            if fmt.endswith("T%H:%M:%S") or fmt.endswith("T%H:%M:%SZ"):
                dt = datetime.strptime(date_str, fmt)
                return dt.date()
            else:
                return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def format_date_for_api(date_obj: date) -> str:
    """Format date object cho API"""
    return date_obj.strftime("%Y-%m-%d")


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value từ dictionary"""
    try:
        return data.get(key, default)
    except (KeyError, TypeError):
        return default


def flatten_dict(data: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by_key(data: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    """Group list of dictionaries by key"""
    result = {}
    for item in data:
        group_key = item.get(key, "unknown")
        if group_key not in result:
            result[group_key] = []
        result[group_key].append(item)
    return result


def remove_duplicates(data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """Remove duplicates từ list of dictionaries based on key"""
    seen = set()
    result = []
    for item in data:
        item_key = item.get(key)
        if item_key not in seen:
            seen.add(item_key)
            result.append(item)
    return result
