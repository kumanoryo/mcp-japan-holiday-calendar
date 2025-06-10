from typing import Any, Optional
import json
import os
from datetime import datetime, date
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("japanese-holiday")

# Constants
DATA_FILE_PATH = "data/calendar_holiday.json"

# Global cache for holiday data
_holiday_data_cache: Optional[list[dict[str, Any]]] = None
_date_index_cache: Optional[dict[str, dict[str, Any]]] = None
_month_index_cache: Optional[dict[str, list[dict[str, Any]]]] = None

def load_holiday_data() -> list[dict[str, Any]]:
    """Load holiday data from JSON file with caching."""
    global _holiday_data_cache, _date_index_cache, _month_index_cache
    
    # Return cached data if available
    if _holiday_data_cache is not None:
        return _holiday_data_cache
    
    # Load data from file
    # Try Docker path first, then local development path
    docker_path = DATA_FILE_PATH
    local_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_FILE_PATH)
    
    file_path = docker_path if os.path.exists(docker_path) else local_path
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = []
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
            
            # Cache the data
            _holiday_data_cache = data
            
            # Build optimized indexes
            _build_indexes(data)
            
            print(f"Loaded {len(data)} holiday records with optimized indexes")
            return data
    except Exception as e:
        print(f"Error loading holiday data: {e}")
        return []

def _build_indexes(data: list[dict[str, Any]]) -> None:
    """Build optimized indexes for fast lookups."""
    global _date_index_cache, _month_index_cache
    
    # Build date index: date -> record (O(1) lookup)
    _date_index_cache = {}
    for item in data:
        date_str = item.get('date')
        if date_str:
            _date_index_cache[date_str] = item
    
    # Build month index: "YYYY-MM" -> [records] (O(k) lookup where k = days in month)
    _month_index_cache = {}
    for item in data:
        date_str = item.get('date')
        if date_str and len(date_str) >= 7:  # YYYY-MM-DD format
            month_key = date_str[:7]  # YYYY-MM
            if month_key not in _month_index_cache:
                _month_index_cache[month_key] = []
            _month_index_cache[month_key].append(item)
    
    print(f"Built date index: {len(_date_index_cache)} entries")
    print(f"Built month index: {len(_month_index_cache)} months")

def find_date_info(target_date: str, data: list[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
    """Find information for a specific date using optimized index."""
    global _date_index_cache
    
    # Use optimized index if available
    if _date_index_cache is not None:
        return _date_index_cache.get(target_date)
    
    # Fallback to linear search (for backward compatibility)
    if data is None:
        data = load_holiday_data()
    
    for item in data:
        if item.get('date') == target_date:
            return item
    return None

def format_date_info(date_info: dict[str, Any]) -> str:
    """Format date information into a readable string."""
    date_str = date_info.get('date', 'Unknown')
    dayofweek = date_info.get('dayofweek', {}).get('name', 'Unknown')
    
    result = f"日付: {date_str} ({dayofweek}曜日)\n"
    
    # Public holiday info
    public_holiday = date_info.get('public_holiday', {})
    if public_holiday.get('flag'):
        result += f"祝日: {public_holiday.get('name', '')}\n"
    else:
        result += "祝日: なし\n"
    
    # Bank holiday info
    bank_holiday = date_info.get('bank_holiday', {})
    if bank_holiday.get('flag'):
        result += "銀行休業日: はい\n"
    else:
        result += "銀行休業日: いいえ\n"
    
    # Business date count
    business_count = date_info.get('business_date_count', {})
    if business_count.get('up') is not None:
        result += f"当月営業日数 (経過): {business_count.get('up', 0)}\n"
        result += f"当月営業日数 (残り): {business_count.get('down', 0)}\n"
    
    # Day before/after holiday
    day_before = date_info.get('day_before_holiday', {})
    day_after = date_info.get('day_after_holiday', {})
    if day_before.get('flag'):
        result += "前日が祝日: はい\n"
    if day_after.get('flag'):
        result += "翌日が祝日: はい\n"
    
    return result

@mcp.tool()
async def get_holiday_info(target_date: str) -> str:
    """Get holiday information for a specific date.

    Args:
        target_date: Date in YYYY-MM-DD format (e.g. 2025-01-01)
    """
    # Validate date format
    try:
        datetime.strptime(target_date, '%Y-%m-%d')
    except ValueError:
        return "日付の形式が正しくありません。YYYY-MM-DD形式で入力してください。"
    
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    date_info = find_date_info(target_date)
    if not date_info:
        return f"{target_date}の情報が見つかりませんでした。"
    
    return format_date_info(date_info)

@mcp.tool()
async def get_holidays_in_month(year: int, month: int) -> str:
    """Get all holidays in a specific month using optimized index.

    Args:
        year: Year (e.g. 2025)
        month: Month (1-12)
    """
    if not (1 <= month <= 12):
        return "月は1から12の間で指定してください。"
    
    global _month_index_cache
    
    # Ensure data is loaded
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    month_key = f"{year}-{month:02d}"
    holidays = []
    
    # Use optimized month index if available
    if _month_index_cache is not None:
        month_data = _month_index_cache.get(month_key, [])
        for item in month_data:
            public_holiday = item.get('public_holiday', {})
            if public_holiday.get('flag'):
                holidays.append({
                    'date': item.get('date', ''),
                    'name': public_holiday.get('name', ''),
                    'dayofweek': item.get('dayofweek', {}).get('name', '')
                })
    else:
        # Fallback to linear search
        for item in data:
            date_obj = item.get('date', '')
            if date_obj.startswith(month_key):
                public_holiday = item.get('public_holiday', {})
                if public_holiday.get('flag'):
                    holidays.append({
                        'date': date_obj,
                        'name': public_holiday.get('name', ''),
                        'dayofweek': item.get('dayofweek', {}).get('name', '')
                    })
    
    if not holidays:
        return f"{year}年{month}月には祝日がありません。"
    
    result = f"{year}年{month}月の祝日:\n\n"
    for holiday in holidays:
        result += f"• {holiday['date']} ({holiday['dayofweek']}曜日): {holiday['name']}\n"
    
    return result

@mcp.tool()
async def get_next_holiday() -> str:
    """Get the next upcoming holiday from today."""
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    
    next_holidays = []
    for item in data:
        date_str = item.get('date', '')
        if date_str >= today_str:
            public_holiday = item.get('public_holiday', {})
            if public_holiday.get('flag'):
                next_holidays.append({
                    'date': date_str,
                    'name': public_holiday.get('name', ''),
                    'dayofweek': item.get('dayofweek', {}).get('name', '')
                })
                break
    
    if not next_holidays:
        return "次の祝日が見つかりませんでした。"
    
    holiday = next_holidays[0]
    return f"次の祝日: {holiday['date']} ({holiday['dayofweek']}曜日) - {holiday['name']}"

@mcp.tool()
async def get_business_days_count(year: int, month: int) -> str:
    """Get business days count for a specific month using optimized index.

    Args:
        year: Year (e.g. 2025)
        month: Month (1-12)
    """
    if not (1 <= month <= 12):
        return "月は1から12の間で指定してください。"
    
    global _month_index_cache
    
    # Ensure data is loaded
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    month_key = f"{year}-{month:02d}"
    business_days = 0
    total_days = 0
    
    # Use optimized month index if available
    if _month_index_cache is not None:
        month_data = _month_index_cache.get(month_key, [])
        for item in month_data:
            total_days += 1
            bank_holiday = item.get('bank_holiday', {})
            if not bank_holiday.get('flag'):
                business_days += 1
    else:
        # Fallback to linear search
        for item in data:
            date_obj = item.get('date', '')
            if date_obj.startswith(month_key):
                total_days += 1
                bank_holiday = item.get('bank_holiday', {})
                if not bank_holiday.get('flag'):
                    business_days += 1
    
    if total_days == 0:
        return f"{year}年{month}月のデータが見つかりませんでした。"
    
    return f"{year}年{month}月:\n営業日数: {business_days}日\n総日数: {total_days}日\n休業日数: {total_days - business_days}日"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')