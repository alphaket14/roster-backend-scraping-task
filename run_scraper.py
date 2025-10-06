#!/usr/bin/env python3
"""
Roster Scraper CLI
A command-line tool for scraping public profiles from Shoutt.
"""

import argparse
import sys
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from roster_scraper.spiders.shoutt_spider import ShouttSpider


def main():
    parser = argparse.ArgumentParser(
        description='Scrape public profiles from Shoutt for specified roles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape UGC and Video roles with default settings
  python run_scraper.py
  
  # Scrape only UGC role with minimum 100 profiles
  python run_scraper.py --roles UGC --min-per-role 100
  
  # Custom output file
  python run_scraper.py --output custom_profiles.csv
  
  # Scrape multiple roles
  python run_scraper.py --roles "UGC,Video,Photography" --min-per-role 50
        """
    )
    
    parser.add_argument(
        '--roles',
        type=str,
        default='UGC,Video',
        help='Comma-separated list of roles to scrape (default: UGC,Video)'
    )
    
    parser.add_argument(
        '--min-per-role',
        type=int,
        default=50,
        help='Minimum number of profiles to collect per role (default: 50)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='profiles.csv',
        help='Output CSV file name (default: profiles.csv)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get Scrapy settings
    settings = get_project_settings()
    settings.set('LOG_LEVEL', args.log_level)
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Start crawling
    process.crawl(
        ShouttSpider,
        roles=args.roles,
        min_per_role=args.min_per_role,
        output_file=args.output
    )
    
    logging.info(f"Starting scraper with roles: {args.roles}")
    logging.info(f"Minimum profiles per role: {args.min_per_role}")
    logging.info(f"Output file: {args.output}")
    
    process.start()


if __name__ == '__main__':
    main()
