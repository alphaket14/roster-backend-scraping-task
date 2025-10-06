# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re
import logging
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from email_validator import validate_email, EmailNotValidError


class EmailValidationPipeline:
    """Validate email addresses"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        email = adapter.get('email')
        
        if not email:
            raise DropItem(f"Missing email in {item}")
        
        try:
            # Validate email
            valid = validate_email(email, check_deliverability=False)
            adapter['email'] = valid.normalized
        except EmailNotValidError as e:
            raise DropItem(f"Invalid email {email}: {e}")
        
        return item


class BrandNameFilterPipeline:
    """Filter out brand-like names"""
    
    BRAND_KEYWORDS = [
        'studio', 'media', 'agency', 'productions', 'designs', 'labs',
        'official', 'channel', 'team', 'llc', 'inc', 'ltd', 'pvt',
        'gmbh', 'plc', 'co', 'company', 'group', 'the'
    ]
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter.get('name', '').lower()
        
        for keyword in self.BRAND_KEYWORDS:
            if keyword in name:
                raise DropItem(f"Brand-like name detected: {adapter.get('name')}")
        
        return item


class DeduplicationPipeline:
    """Remove duplicate profiles based on email"""
    
    def __init__(self):
        self.seen_emails = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        email = adapter.get('email')
        
        if email in self.seen_emails:
            raise DropItem(f"Duplicate email found: {email}")
        else:
            self.seen_emails.add(email)
            return item


class CSVExportPipeline:
    """Export items to CSV"""
    
    def __init__(self):
        self.files = {}
        self.writers = {}
    
    def open_spider(self, spider):
        output_file = getattr(spider, 'output_file', 'profiles.csv')
        self.file = open(output_file, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=['name', 'email', 'profile_link', 'role_type']
        )
        self.writer.writeheader()
        logging.info(f"CSV export started: {output_file}")
    
    def close_spider(self, spider):
        self.file.close()
        logging.info("CSV export completed")
    
    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item
