#!/usr/bin/env python3
"""
Test script for validating pipeline functionality
"""

from roster_scraper.items import ProfileItem
from roster_scraper.pipelines import (
    EmailValidationPipeline,
    BrandNameFilterPipeline,
    DeduplicationPipeline
)
from scrapy.exceptions import DropItem


def test_email_validation():
    """Test email validation pipeline"""
    print("Testing Email Validation Pipeline...")
    pipeline = EmailValidationPipeline()
    
    # Valid email
    valid_item = ProfileItem(
        name="John Doe",
        email="john.doe@example.com",
        profile_link="http://example.com/john",
        role_type="UGC"
    )
    
    try:
        result = pipeline.process_item(valid_item, None)
        print(f"✓ Valid email passed: {result['email']}")
    except DropItem as e:
        print(f"✗ Valid email failed: {e}")
    
    # Invalid email
    invalid_item = ProfileItem(
        name="Jane Doe",
        email="invalid-email",
        profile_link="http://example.com/jane",
        role_type="Video"
    )
    
    try:
        pipeline.process_item(invalid_item, None)
        print("✗ Invalid email should have been dropped")
    except DropItem:
        print("✓ Invalid email correctly dropped")
    
    print()


def test_brand_filter():
    """Test brand name filtering pipeline"""
    print("Testing Brand Name Filter Pipeline...")
    pipeline = BrandNameFilterPipeline()
    
    # Regular person name
    valid_item = ProfileItem(
        name="Sarah Johnson",
        email="sarah@example.com",
        profile_link="http://example.com/sarah",
        role_type="UGC"
    )
    
    try:
        result = pipeline.process_item(valid_item, None)
        print(f"✓ Regular name passed: {result['name']}")
    except DropItem as e:
        print(f"✗ Regular name failed: {e}")
    
    # Brand name
    brand_items = [
        ("Creative Studio", "studio"),
        ("Media Productions Inc", "inc"),
        ("Design Agency", "agency"),
        ("The Marketing Team", "the"),
    ]
    
    for name, keyword in brand_items:
        item = ProfileItem(
            name=name,
            email="contact@example.com",
            profile_link="http://example.com/brand",
            role_type="Video"
        )
        
        try:
            pipeline.process_item(item, None)
            print(f"✗ Brand name '{name}' should have been dropped")
        except DropItem:
            print(f"✓ Brand name '{name}' correctly dropped (keyword: {keyword})")
    
    print()


def test_deduplication():
    """Test deduplication pipeline"""
    print("Testing Deduplication Pipeline...")
    pipeline = DeduplicationPipeline()
    
    # First item
    item1 = ProfileItem(
        name="Alice Smith",
        email="alice@example.com",
        profile_link="http://example.com/alice",
        role_type="UGC"
    )
    
    try:
        result = pipeline.process_item(item1, None)
        print(f"✓ First item passed: {result['email']}")
    except DropItem as e:
        print(f"✗ First item failed: {e}")
    
    # Duplicate email
    item2 = ProfileItem(
        name="Alice Johnson",
        email="alice@example.com",
        profile_link="http://example.com/alice2",
        role_type="Video"
    )
    
    try:
        pipeline.process_item(item2, None)
        print("✗ Duplicate email should have been dropped")
    except DropItem:
        print("✓ Duplicate email correctly dropped")
    
    # Different email
    item3 = ProfileItem(
        name="Bob Wilson",
        email="bob@example.com",
        profile_link="http://example.com/bob",
        role_type="UGC"
    )
    
    try:
        result = pipeline.process_item(item3, None)
        print(f"✓ Different email passed: {result['email']}")
    except DropItem as e:
        print(f"✗ Different email failed: {e}")
    
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Running Pipeline Tests")
    print("=" * 50)
    print()
    
    test_email_validation()
    test_brand_filter()
    test_deduplication()
    
    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)
