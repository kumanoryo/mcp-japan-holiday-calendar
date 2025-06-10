#!/usr/bin/env python3
"""
Test script for Japanese holiday MCP server
"""

from holiday_calendar import load_holiday_data, find_date_info, format_date_info

def test_data_loading():
    """Test data loading functionality"""
    print("Testing data loading...")
    data = load_holiday_data()
    if data:
        print(f"✓ Successfully loaded {len(data)} records")
        print(f"Sample record: {data[0]}")
    else:
        print("✗ Failed to load data")
    return data

def test_date_info(data):
    """Test date information retrieval"""
    print("\nTesting date information retrieval...")
    
    # Test with a known holiday
    test_date = "1955-01-01"  # New Year's Day
    date_info = find_date_info(test_date, data)
    
    if date_info:
        print(f"✓ Found information for {test_date}")
        print("Formatted output:")
        print(format_date_info(date_info))
    else:
        print(f"✗ No information found for {test_date}")

def test_holiday_search(data):
    """Test holiday search functionality"""
    print("\nTesting holiday search...")
    
    holidays_found = 0
    for item in data[:100]:  # Check first 100 records
        public_holiday = item.get('public_holiday', {})
        if public_holiday.get('flag'):
            holidays_found += 1
            print(f"Found holiday: {item['date']} - {public_holiday.get('name', 'Unknown')}")
    
    print(f"✓ Found {holidays_found} holidays in first 100 records")

if __name__ == "__main__":
    data = test_data_loading()
    if data:
        test_date_info(data)
        test_holiday_search(data)