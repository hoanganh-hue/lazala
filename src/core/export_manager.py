"""
Export manager - Quản lý xuất dữ liệu
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..api.models import SearchResult
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ExportManager:
    """Quản lý xuất dữ liệu ra các định dạng khác nhau"""
    
    def __init__(self):
        self.export_dir = Path.home() / "Downloads" / "GoogleMapsScraper"
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def export_data(
        self, 
        results: List[SearchResult], 
        format_type: str, 
        view_type: str = "all"
    ) -> Optional[str]:
        """
        Xuất dữ liệu ra file
        
        Args:
            results: Danh sách kết quả
            format_type: Định dạng xuất (excel, csv, json)
            view_type: Loại view (all, contacts, location_rating, reviews, leads)
        
        Returns:
            Đường dẫn file đã xuất hoặc None nếu thất bại
        """
        try:
            if not results:
                logger.warning("No results to export")
                return None
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_maps_data_{timestamp}"
            
            # Convert results to appropriate format
            if view_type == "all":
                data = self._convert_to_all_data(results)
            elif view_type == "contacts":
                data = self._convert_to_contacts_data(results)
            elif view_type == "location_rating":
                data = self._convert_to_location_rating_data(results)
            elif view_type == "reviews":
                data = self._convert_to_reviews_data(results)
            elif view_type == "leads":
                data = self._convert_to_leads_data(results)
            else:
                data = self._convert_to_all_data(results)
            
            # Export based on format
            if format_type == "excel":
                return self._export_excel(data, filename)
            elif format_type == "csv":
                return self._export_csv(data, filename)
            elif format_type == "json":
                return self._export_json(data, filename)
            else:
                logger.error(f"Unsupported format: {format_type}")
                return None
                
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return None
    
    def _convert_to_all_data(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Convert to all data format"""
        data = []
        for result in results:
            item = {
                "Tên": result.title or "",
                "Tiêu đề phụ": result.sub_title or "",
                "Danh mục": result.category_name or "",
                "Mô tả": result.description or "",
                "Địa chỉ": result.address or "",
                "Khu vực": result.neighborhood or "",
                "Đường": result.street or "",
                "Thành phố": result.city or "",
                "Mã bưu điện": result.postal_code or "",
                "Tỉnh/Thành": result.state or "",
                "Quốc gia": result.country_code or "",
                "Vĩ độ": result.latitude or "",
                "Kinh độ": result.longitude or "",
                "Plus Code": result.plus_code or "",
                "Điện thoại": result.phone or "",
                "Điện thoại (không format)": result.phone_unformatted or "",
                "Website": result.website or "",
                "Đánh giá": result.total_score or 0,
                "Số reviews": result.reviews_count or 0,
                "Đóng cửa vĩnh viễn": result.permanently_closed,
                "Đóng cửa tạm thời": result.temporarily_closed,
                "Place ID": result.place_id or "",
                "CID": result.cid or "",
                "FID": result.fid or "",
                "Menu": result.menu or "",
                "Giá": result.price or "",
                "Sao khách sạn": result.hotel_stars or "",
                "Thời gian thu thập": result.scraped_at.isoformat() if result.scraped_at else "",
                "Chuỗi tìm kiếm": result.search_string or "",
                "Thứ hạng": result.rank or ""
            }
            data.append(item)
        return data
    
    def _convert_to_contacts_data(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Convert to contacts data format"""
        data = []
        for result in results:
            item = {
                "Tên": result.title or "",
                "Địa chỉ": result.address or "",
                "Điện thoại": result.phone or "",
                "Website": result.website or "",
                "Email": "",
                "Facebook": "",
                "LinkedIn": "",
                "Twitter": "",
                "Instagram": ""
            }
            
            # Extract contact info if available
            if result.contacts_from_website:
                contacts = result.contacts_from_website
                item["Email"] = contacts.get("email", "")
                item["Facebook"] = contacts.get("facebook", "")
                item["LinkedIn"] = contacts.get("linkedin", "")
                item["Twitter"] = contacts.get("twitter", "")
                item["Instagram"] = contacts.get("instagram", "")
            
            data.append(item)
        return data
    
    def _convert_to_location_rating_data(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Convert to location & rating data format"""
        data = []
        for result in results:
            item = {
                "Tên": result.title or "",
                "Địa chỉ": result.address or "",
                "Thành phố": result.city or "",
                "Tỉnh/Thành": result.state or "",
                "Quốc gia": result.country_code or "",
                "Vĩ độ": result.latitude or "",
                "Kinh độ": result.longitude or "",
                "Đánh giá": result.total_score or 0,
                "Số reviews": result.reviews_count or 0,
                "Phân bố reviews": json.dumps(result.reviews_distribution) if result.reviews_distribution else "",
                "Trạng thái": "Đóng cửa" if result.permanently_closed else "Mở cửa"
            }
            data.append(item)
        return data
    
    def _convert_to_reviews_data(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Convert to reviews data format"""
        data = []
        for result in results:
            if result.reviews:
                for review in result.reviews:
                    item = {
                        "Tên địa điểm": result.title or "",
                        "Địa chỉ": result.address or "",
                        "Tên reviewer": review.get("authorName", ""),
                        "Đánh giá": review.get("rating", 0),
                        "Nội dung review": review.get("text", ""),
                        "Thời gian": review.get("publishedAt", ""),
                        "Ngôn ngữ": review.get("language", ""),
                        "Đã dịch": review.get("translated", False)
                    }
                    data.append(item)
            else:
                # Add place without reviews
                item = {
                    "Tên địa điểm": result.title or "",
                    "Địa chỉ": result.address or "",
                    "Tên reviewer": "",
                    "Đánh giá": 0,
                    "Nội dung review": "",
                    "Thời gian": "",
                    "Ngôn ngữ": "",
                    "Đã dịch": False
                }
                data.append(item)
        return data
    
    def _convert_to_leads_data(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Convert to leads data format"""
        data = []
        for result in results:
            if result.leads_info:
                for lead in result.leads_info:
                    item = {
                        "Tên công ty": result.title or "",
                        "Địa chỉ công ty": result.address or "",
                        "Website công ty": result.website or "",
                        "Tên đầy đủ": lead.get("fullName", ""),
                        "Email": lead.get("email", ""),
                        "Điện thoại": lead.get("phone", ""),
                        "Chức vụ": lead.get("jobTitle", ""),
                        "Phòng ban": lead.get("department", ""),
                        "LinkedIn": lead.get("linkedin", ""),
                        "Ngành": lead.get("industry", ""),
                        "Số nhân viên": lead.get("companySize", ""),
                        "Mô tả công ty": lead.get("companyDescription", "")
                    }
                    data.append(item)
            else:
                # Add company without leads
                item = {
                    "Tên công ty": result.title or "",
                    "Địa chỉ công ty": result.address or "",
                    "Website công ty": result.website or "",
                    "Tên đầy đủ": "",
                    "Email": "",
                    "Điện thoại": "",
                    "Chức vụ": "",
                    "Phòng ban": "",
                    "LinkedIn": "",
                    "Ngành": "",
                    "Số nhân viên": "",
                    "Mô tả công ty": ""
                }
                data.append(item)
        return data
    
    def _export_excel(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to Excel file"""
        file_path = self.export_dir / f"{filename}.xlsx"
        
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        logger.info(f"Exported {len(data)} records to Excel: {file_path}")
        return str(file_path)
    
    def _export_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to CSV file"""
        file_path = self.export_dir / f"{filename}.csv"
        
        if not data:
            return str(file_path)
        
        # Get all fieldnames
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Exported {len(data)} records to CSV: {file_path}")
        return str(file_path)
    
    def _export_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export to JSON file"""
        file_path = self.export_dir / f"{filename}.json"
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        
        logger.info(f"Exported {len(data)} records to JSON: {file_path}")
        return str(file_path)
