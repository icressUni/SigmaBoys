#!/usr/bin/env python3
"""
Test script to verify the duplicate prevention logic in the webhook server.
This script simulates webhook calls and tests the processed responses tracking.
"""
import os
import sys
import json
import time
from datetime import datetime

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webhook_server_refactored import (
    load_processed_responses, 
    save_processed_responses, 
    add_processed_response
)

def test_duplicate_prevention():
    """Test the duplicate prevention mechanism."""
    print("Testing duplicate prevention logic...")
    
    # Clear any existing processed responses for clean test
    save_processed_responses(set())
    
    # Test timestamps
    test_timestamps = [
        "2023-12-01T10:30:00.000Z",
        "2023-12-01T10:35:00.000Z", 
        "2023-12-01T10:40:00.000Z"
    ]
    
    print(f"Initial processed responses: {len(load_processed_responses())}")
    
    # Add first timestamp
    processed = add_processed_response(test_timestamps[0])
    print(f"After adding first timestamp: {len(processed)} processed")
    
    # Try to add the same timestamp again (should not increase count)
    processed = add_processed_response(test_timestamps[0])
    print(f"After adding same timestamp again: {len(processed)} processed")
    
    # Add different timestamps
    for ts in test_timestamps[1:]:
        processed = add_processed_response(ts)
        print(f"After adding {ts}: {len(processed)} processed")
    
    # Test the cleanup mechanism (when over 1000 entries)
    print("\nTesting cleanup mechanism with many entries...")
    
    # Add many fake timestamps to trigger cleanup
    fake_timestamps = [f"2023-12-{i:02d}T12:00:00.000Z" for i in range(1, 1005)]
    for ts in fake_timestamps:
        add_processed_response(ts)
    
    final_processed = load_processed_responses()
    print(f"After adding {len(fake_timestamps)} timestamps: {len(final_processed)} processed (should be <= 1000)")
    
    # Verify the cleanup worked
    if len(final_processed) <= 1000:
        print("✓ Cleanup mechanism working correctly")
    else:
        print("✗ Cleanup mechanism failed")
    
    print("\nTest completed!")

def test_folder_naming():
    """Test the folder naming logic."""
    print("\nTesting folder naming logic...")
    
    # Test cases for folder naming
    test_cases = [
        {
            'Timestamp': '2023-12-01T10:30:45.123Z',
            'Nombre': 'Juan Pérez',
            'expected_pattern': '20231201_103045_Juan_Perez'
        },
        {
            'Timestamp': '2023-12-01T15:45:30.000Z',
            'Nombre': 'María González-López',
            'expected_pattern': '20231201_154530_Mara_Gonzlez-Lpez'
        },
        {
            'Timestamp': '',
            'Nombre': 'Test User',
            'expected_pattern': 'response_'  # Should start with response_
        }
    ]
    
    for i, case in enumerate(test_cases):
        print(f"\nTest case {i+1}:")
        print(f"  Input: Timestamp='{case['Timestamp']}', Nombre='{case['Nombre']}'")
        
        # Simulate the folder naming logic from webhook_server_refactored.py
        response_timestamp = case.get('Timestamp', '')
        response_name = case.get('Nombre', 'Unknown')
        
        if response_timestamp:
            try:
                dt = datetime.fromisoformat(response_timestamp.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y%m%d_%H%M%S')
            except:
                date_str = response_timestamp.replace(':', '-').replace('T', '_').split('.')[0]
        else:
            date_str = f"response_{int(time.time())}"
        
        safe_name = "".join(c for c in response_name if c.isalnum() or c in (' ', '_', '-')).strip()
        if not safe_name:
            safe_name = "unknown_user"
        safe_name = safe_name.replace(' ', '_')[:20]
        
        response_id = f"{date_str}_{safe_name}"
        
        print(f"  Output: '{response_id}'")
        
        if case['Timestamp'] and case['expected_pattern'] in response_id:
            print("  ✓ Folder naming working correctly")
        elif not case['Timestamp'] and response_id.startswith('response_'):
            print("  ✓ Fallback folder naming working correctly")
        else:
            print("  ✗ Folder naming may have issues")

if __name__ == '__main__':
    print("=== Webhook Duplicate Prevention Test ===")
    test_duplicate_prevention()
    test_folder_naming()
    print("\n=== All Tests Completed ===")
