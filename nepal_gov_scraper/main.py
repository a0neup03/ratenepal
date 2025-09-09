#!/usr/bin/env python3
"""
Main entry point for Nepal Government Office Scraper
Clean, simple interface for running the comprehensive scraper
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from comprehensive_scraper import ComprehensiveNepalGovScraper


def main():
    """Main function with simple command line interface"""
    parser = argparse.ArgumentParser(
        description='Nepal Government Office Data Scraper - Comprehensive Edition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run standard comprehensive scraper (21+ offices)
    python main.py
    
    # Run ALL 77 DAOs + other offices (complete Nepal coverage)
    python main.py --all-77-daos
    
    # Run without live data enhancement (faster)
    python main.py --no-live-enhancement
    
    # Run ALL 77 DAOs without enhancement (fastest comprehensive)
    python main.py --all-77-daos --no-live-enhancement
    
    # Run factory test only
    python main.py --test-only
        """
    )
    
    parser.add_argument(
        '--no-live-enhancement',
        action='store_true',
        help='Skip live data enhancement from government websites'
    )
    
    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Run office factory test only (no scraping)'
    )
    
    parser.add_argument(
        '--all-77-daos',
        action='store_true',
        help='Include all 77 Nepal DAOs + other offices (comprehensive mode)'
    )
    
    args = parser.parse_args()
    
    try:
        print("🇳🇵 Nepal Government Office Scraper - Comprehensive Edition")
        print("=" * 60)
        
        if args.test_only:
            # Test factory only
            from models.office_factory import main as factory_test
            factory_test()
            return
        
        # Run comprehensive scraper
        scraper = ComprehensiveNepalGovScraper()
        
        print(f"Configuration:")
        print(f"  Include all 77 DAOs: {args.all_77_daos}")
        print(f"  Live data enhancement: {not args.no_live_enhancement}")
        print()
        
        output_file = scraper.run_comprehensive_scrape(
            enhance_with_live=not args.no_live_enhancement,
            include_all_77_daos=args.all_77_daos
        )
        
        print(f"\n✅ Scraping completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()