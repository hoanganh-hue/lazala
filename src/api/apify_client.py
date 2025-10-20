"""
Apify API client cho Google Maps Scraper
"""

import asyncio
import aiohttp
import requests
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

from .models import SearchInput, SearchResult, RunStatus
from .auth import AuthManager
from ..config import APIFY_ACTOR_URL, POLL_INTERVAL, MAX_POLL_ATTEMPTS
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ApifyClient:
    """Client để tương tác với Apify API"""
    
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.base_url = APIFY_ACTOR_URL
        self.session: Optional[aiohttp.ClientSession] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Lấy headers cho API request"""
        if not self.auth_manager.has_token():
            raise ValueError("API token chưa được cấu hình")
        
        token = self.auth_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def _get_url_with_token(self, endpoint: str) -> str:
        """Lấy URL với token parameter"""
        if not self.auth_manager.has_token():
            raise ValueError("API token chưa được cấu hình")
        
        token = self.auth_manager.get_token()
        separator = "&" if "?" in endpoint else "?"
        return f"{endpoint}{separator}token={token}"
    
    async def start_run(self, search_input: SearchInput) -> str:
        """Bắt đầu một run mới"""
        url = f"{self.base_url}/runs"
        headers = self._get_headers()
        payload = search_input.to_dict()
        
        logger.info(f"Starting run với payload: {payload}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    run_id = data["data"]["id"]
                    logger.info(f"Run started với ID: {run_id}")
                    return run_id
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to start run: {response.status} - {error_text}")
                    raise Exception(f"Không thể bắt đầu run: {response.status} - {error_text}")
    
    async def get_run_status(self, run_id: str) -> RunStatus:
        """Lấy trạng thái của run"""
        url = f"https://api.apify.com/v2/actor-runs/{run_id}"
        headers = self._get_headers()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return RunStatus.from_dict(data["data"])
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get run status: {response.status} - {error_text}")
                    raise Exception(f"Không thể lấy trạng thái run: {response.status} - {error_text}")
    
    async def wait_for_completion(self, run_id: str, progress_callback=None) -> RunStatus:
        """Chờ run hoàn thành"""
        logger.info(f"Waiting for run {run_id} to complete...")
        
        for attempt in range(MAX_POLL_ATTEMPTS):
            try:
                status = await self.get_run_status(run_id)
                
                if progress_callback:
                    progress_callback(status)
                
                if status.is_succeeded:
                    logger.info(f"Run {run_id} completed successfully")
                    return status
                elif status.is_failed:
                    logger.error(f"Run {run_id} failed: {status.error_message}")
                    return status
                
                # Chờ trước khi poll tiếp
                await asyncio.sleep(POLL_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error polling run status: {e}")
                if attempt == MAX_POLL_ATTEMPTS - 1:
                    raise
                await asyncio.sleep(POLL_INTERVAL)
        
        raise TimeoutError(f"Run {run_id} không hoàn thành trong thời gian cho phép")
    
    async def get_dataset_items(self, dataset_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lấy items từ dataset"""
        url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
        if limit:
            url += f"?limit={limit}"
        
        headers = self._get_headers()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Retrieved {len(data['data'])} items from dataset {dataset_id}")
                    return data["data"]
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get dataset items: {response.status} - {error_text}")
                    raise Exception(f"Không thể lấy dữ liệu: {response.status} - {error_text}")
    
    async def run_sync(self, search_input: SearchInput) -> List[SearchResult]:
        """Chạy sync và lấy kết quả ngay lập tức"""
        url = f"{self.base_url}/run-sync-get-dataset-items"
        headers = self._get_headers()
        payload = search_input.to_dict()
        
        logger.info(f"Running sync với payload: {payload}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data["data"]
                    logger.info(f"Sync completed, retrieved {len(items)} items")
                    
                    # Convert to SearchResult objects
                    results = []
                    for item in items:
                        try:
                            result = SearchResult.from_dict(item)
                            results.append(result)
                        except Exception as e:
                            logger.warning(f"Failed to parse item: {e}")
                            continue
                    
                    return results
                else:
                    error_text = await response.text()
                    logger.error(f"Sync failed: {response.status} - {error_text}")
                    raise Exception(f"Sync thất bại: {response.status} - {error_text}")
    
    async def test_connection(self) -> bool:
        """Test kết nối API"""
        try:
            url = "https://api.apify.com/v2/users/me"
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        logger.info("API connection test successful")
                        return True
                    else:
                        logger.error(f"API connection test failed: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"API connection test error: {e}")
            return False
    
    def get_usage_info(self) -> Dict[str, Any]:
        """Lấy thông tin usage (placeholder)"""
        # TODO: Implement usage info từ Apify API
        return {
            "credits_used": 0,
            "credits_remaining": 0,
            "subscription_plan": "Free"
        }
