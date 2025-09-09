#!/usr/bin/env python3
"""
Simple test script for Nepal Government Office Scraper
Tests the enhanced DAO Kathmandu scraper
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

def main():
    """Run the enhanced DAO Kathmandu test"""
    print("🧪 Running Enhanced DAO Kathmandu Test")
    print("=" * 50)
    
    try:
        from test_enhanced_dao_kathmandu import main as test_main
        test_main()
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()