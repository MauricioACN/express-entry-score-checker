#!/usr/bin/env python3
"""
Express Entry Analysis Runner
Runs all available analyses and provides a simple interface
"""

import sys
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print a nice banner"""
    print("\n" + "="*70)
    print("🍁 EXPRESS ENTRY SCORE ANALYZER 🍁")
    print("Comprehensive analysis of CRS scoring factors")
    print("="*70)


def run_comprehensive_analysis():
    """Run the comprehensive analysis"""
    try:
        logger.info("Starting comprehensive analysis...")
        from comprehensive_analyzer import ComprehensiveScoreAnalyzer

        analyzer = ComprehensiveScoreAnalyzer()
        analyzer.run_comprehensive_analysis()

        logger.info("✅ Comprehensive analysis completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Error in comprehensive analysis: {e}")
        return False


def run_age_analysis():
    """Run the age-focused analysis"""
    try:
        logger.info("Starting age analysis...")
        from age_analyzer import AgeScoreAnalyzer

        analyzer = AgeScoreAnalyzer()
        analyzer.run_analysis()

        logger.info("✅ Age analysis completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Error in age analysis: {e}")
        return False


def run_web_scraper():
    """Run the web scraper"""
    try:
        logger.info("Starting web scraper...")
        from express_entry_scraper import ExpressEntryScoreScraper

        scraper = ExpressEntryScoreScraper(headless=True)
        scraper.run_analysis()

        logger.info("✅ Web scraping completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Error in web scraping: {e}")
        return False


def main():
    """Main function with user menu"""
    print_banner()

    while True:
        print("\nChoose an analysis to run:")
        print("1. 🔄 Comprehensive Analysis (Recommended)")
        print("2. 👴 Age Impact Analysis")
        print("3. 🌐 Web Scraper (Experimental)")
        print("4. 🚀 Run All Analyses")
        print("5. ❌ Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            run_comprehensive_analysis()

        elif choice == '2':
            run_age_analysis()

        elif choice == '3':
            run_web_scraper()

        elif choice == '4':
            logger.info("Running all analyses...")
            results = []
            results.append(run_comprehensive_analysis())
            results.append(run_age_analysis())
            results.append(run_web_scraper())

            successful = sum(results)
            total = len(results)
            logger.info(
                f"Completed {successful}/{total} analyses successfully")

        elif choice == '5':
            print("\n👋 Thanks for using Express Entry Score Analyzer!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

        # Ask if user wants to continue
        if choice in ['1', '2', '3', '4']:
            continue_choice = input(
                "\nWould you like to run another analysis? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("\n👋 Thanks for using Express Entry Score Analyzer!")
                break


def quick_run():
    """Quick run for command line usage"""
    print_banner()
    logger.info("Running quick comprehensive analysis...")
    success = run_comprehensive_analysis()

    if success:
        print("\n🎉 Analysis complete! Check the generated files:")
        print("📊 comprehensive_crs_analysis.png - Main visualization")
        print("📋 *.csv files - Detailed data")
        print("📝 analysis_log.txt - Execution log")
    else:
        print("\n❌ Analysis failed. Check analysis_log.txt for details.")


if __name__ == "__main__":
    # Check if running with arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_run()
    else:
        main()
