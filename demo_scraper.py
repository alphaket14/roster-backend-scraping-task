#!/usr/bin/env python3
"""
Demo script to test the scraper with mock data
This simulates the scraping process without actually hitting the website
"""

import csv
import os
from roster_scraper.items import ProfileItem
from roster_scraper.pipelines import (
    EmailValidationPipeline,
    BrandNameFilterPipeline,
    DeduplicationPipeline,
    CSVExportPipeline
)
from scrapy.exceptions import DropItem


class MockSpider:
    """Mock spider for testing"""
    def __init__(self, output_file='demo_profiles.csv'):
        self.output_file = output_file


def generate_mock_profiles():
    """Generate mock profile data for testing"""
    profiles = [
        # Valid UGC profiles
        ("John Smith", "john.smith@gmail.com", "https://shoutt.co/profiles/johnsmith", "UGC"),
        ("Sarah Johnson", "sarah.j@yahoo.com", "https://shoutt.co/profiles/sarahj", "UGC"),
        ("Mike Brown", "mike.brown@outlook.com", "https://shoutt.co/profiles/mikebrown", "UGC"),
        ("Emily Davis", "emily.davis@proton.me", "https://shoutt.co/profiles/emilyd", "UGC"),
        ("Alex Turner", "alex.turner@mail.com", "https://shoutt.co/profiles/alexturner", "UGC"),
        
        # Valid Video profiles
        ("Lisa Anderson", "lisa.a@gmail.com", "https://shoutt.co/profiles/lisaa", "Video"),
        ("Tom Wilson", "tom.wilson@yahoo.com", "https://shoutt.co/profiles/tomw", "Video"),
        ("Rachel Green", "rachel.green@outlook.com", "https://shoutt.co/profiles/rachelg", "Video"),
        ("Chris Martin", "chris.m@proton.me", "https://shoutt.co/profiles/chrism", "Video"),
        ("Jessica Lee", "jessica.lee@mail.com", "https://shoutt.co/profiles/jessical", "Video"),
        
        # Profiles that should be filtered (brand names)
        ("Creative Studio", "info@creative.com", "https://shoutt.co/profiles/creative", "UGC"),
        ("Digital Media Inc", "contact@digital.com", "https://shoutt.co/profiles/digital", "Video"),
        ("Design Agency", "hello@design.com", "https://shoutt.co/profiles/design", "UGC"),
        ("The Productions LLC", "team@productions.com", "https://shoutt.co/profiles/prod", "Video"),
        
        # Profiles with invalid emails
        ("Bob Invalid", "not-an-email", "https://shoutt.co/profiles/bobinvalid", "UGC"),
        ("Jane Wrong", "wrong@", "https://shoutt.co/profiles/janewrong", "Video"),
        
        # Duplicate emails
        ("John Duplicate", "john.smith@gmail.com", "https://shoutt.co/profiles/johndupe", "UGC"),
        ("Sarah Copy", "sarah.j@yahoo.com", "https://shoutt.co/profiles/sarahcopy", "Video"),
        
        # More valid profiles to reach minimum count
        ("David Clark", "david.clark@gmail.com", "https://shoutt.co/profiles/davidc", "UGC"),
        ("Nina Patel", "nina.patel@yahoo.com", "https://shoutt.co/profiles/ninap", "UGC"),
        ("Mark Thompson", "mark.t@outlook.com", "https://shoutt.co/profiles/markt", "Video"),
        ("Sophie White", "sophie.white@proton.me", "https://shoutt.co/profiles/sophiew", "Video"),
    ]
    
    return profiles


def run_demo():
    """Run the demo with mock data"""
    print("=" * 60)
    print("ROSTER SCRAPER DEMO - MOCK DATA TEST")
    print("=" * 60)
    print()
    
    # Initialize pipelines
    email_pipeline = EmailValidationPipeline()
    brand_pipeline = BrandNameFilterPipeline()
    dedup_pipeline = DeduplicationPipeline()
    csv_pipeline = CSVExportPipeline()
    
    # Mock spider
    spider = MockSpider('demo_profiles.csv')
    
    # Open spider (for CSV pipeline)
    csv_pipeline.open_spider(spider)
    
    # Generate mock profiles
    profiles = generate_mock_profiles()
    
    # Process profiles through pipelines
    stats = {
        'total': 0,
        'valid': 0,
        'invalid_email': 0,
        'brand_filtered': 0,
        'duplicates': 0,
    }
    
    role_counts = {'UGC': 0, 'Video': 0}
    
    print(f"Processing {len(profiles)} mock profiles...\n")
    
    for name, email, link, role in profiles:
        stats['total'] += 1
        item = ProfileItem(
            name=name,
            email=email,
            profile_link=link,
            role_type=role
        )
        
        try:
            # Email validation
            item = email_pipeline.process_item(item, spider)
            
            # Brand filtering
            item = brand_pipeline.process_item(item, spider)
            
            # Deduplication
            item = dedup_pipeline.process_item(item, spider)
            
            # Export to CSV
            csv_pipeline.process_item(item, spider)
            
            stats['valid'] += 1
            role_counts[role] = role_counts.get(role, 0) + 1
            print(f"✓ Accepted: {name} ({role}) - {email}")
            
        except DropItem as e:
            error_msg = str(e)
            if 'Invalid email' in error_msg:
                stats['invalid_email'] += 1
                print(f"✗ Invalid email: {name}")
            elif 'Brand-like name' in error_msg:
                stats['brand_filtered'] += 1
                print(f"✗ Brand filtered: {name}")
            elif 'Duplicate email' in error_msg:
                stats['duplicates'] += 1
                print(f"✗ Duplicate: {name}")
    
    # Close spider
    csv_pipeline.close_spider(spider)
    
    # Print statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(f"Total profiles processed: {stats['total']}")
    print(f"Valid profiles exported: {stats['valid']}")
    print(f"Invalid emails: {stats['invalid_email']}")
    print(f"Brand names filtered: {stats['brand_filtered']}")
    print(f"Duplicates removed: {stats['duplicates']}")
    print()
    print("Profiles per role:")
    for role, count in role_counts.items():
        print(f"  - {role}: {count}")
    print()
    
    # Show CSV output
    if os.path.exists(spider.output_file):
        print(f"CSV file created: {spider.output_file}")
        print("\nCSV Content Preview:")
        print("-" * 60)
        with open(spider.output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                print(f"{i}. {row['name']} ({row['role_type']}) - {row['email']}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
