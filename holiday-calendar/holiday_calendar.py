from typing import Any, Optional
import json
import os
from datetime import datetime, date
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("japanese-holiday")

# Constants
DATA_FILE_PATH = "data/calendar_holiday.json"

def load_holiday_data() -> list[dict[str, Any]]:
    """Load holiday data from JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), DATA_FILE_PATH)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = []
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
            return data
    except Exception as e:
        print(f"Error loading holiday data: {e}")
        return []

def find_date_info(target_date: str, data: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    """Find information for a specific date."""
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
    
    date_info = find_date_info(target_date, data)
    if not date_info:
        return f"{target_date}の情報が見つかりませんでした。"
    
    return format_date_info(date_info)

@mcp.tool()
async def get_holidays_in_month(year: int, month: int) -> str:
    """Get all holidays in a specific month.

    Args:
        year: Year (e.g. 2025)
        month: Month (1-12)
    """
    if not (1 <= month <= 12):
        return "月は1から12の間で指定してください。"
    
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    holidays = []
    for item in data:
        date_obj = item.get('date', '')
        if date_obj.startswith(f"{year}-{month:02d}"):
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
    """Get business days count for a specific month.

    Args:
        year: Year (e.g. 2025)
        month: Month (1-12)
    """
    if not (1 <= month <= 12):
        return "月は1から12の間で指定してください。"
    
    data = load_holiday_data()
    if not data:
        return "休日データの読み込みに失敗しました。"
    
    business_days = 0
    total_days = 0
    
    for item in data:
        date_obj = item.get('date', '')
        if date_obj.startswith(f"{year}-{month:02d}"):
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