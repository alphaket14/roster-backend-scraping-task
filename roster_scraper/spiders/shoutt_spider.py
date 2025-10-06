import scrapy
import logging
import re
from scrapy_playwright.page import PageMethod
from roster_scraper.items import ProfileItem


class ShouttSpider(scrapy.Spider):
    name = 'shoutt'
    
    # Command-line configurable parameters
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 200,  # Stop after collecting enough items (can be overridden)
    }
    
    def __init__(self, roles='UGC,Video', min_per_role=50, output_file='profiles.csv', *args, **kwargs):
        super(ShouttSpider, self).__init__(*args, **kwargs)
        self.roles = [role.strip() for role in roles.split(',')]
        self.min_per_role = int(min_per_role)
        self.output_file = output_file
        self.role_counts = {role: 0 for role in self.roles}
        
        # Base URLs for different roles
        self.role_urls = {
            'UGC': 'https://www.shoutt.co/creators/ugc',
            'Video': 'https://www.shoutt.co/creators/video',
        }
        
        logging.info(f"Starting spider for roles: {self.roles}")
        logging.info(f"Minimum profiles per role: {self.min_per_role}")
        logging.info(f"Output file: {self.output_file}")
    
    def start_requests(self):
        for role in self.roles:
            if role in self.role_urls:
                yield scrapy.Request(
                    url=self.role_urls[role],
                    callback=self.parse,
                    meta={
                        'playwright': True,
                        'playwright_page_methods': [
                            PageMethod('wait_for_selector', 'body', timeout=30000),
                        ],
                        'role_type': role,
                        'page_num': 1,
                    },
                    dont_filter=True,
                )
            else:
                logging.warning(f"Unknown role: {role}")
    
    def parse(self, response):
        role_type = response.meta.get('role_type')
        page_num = response.meta.get('page_num', 1)
        
        logging.info(f"Parsing {role_type} page {page_num}: {response.url}")
        
        # Extract profile cards - adjust selectors based on actual Shoutt structure
        # These are generic selectors that should work with most creator platforms
        profile_cards = response.css('.creator-card, .profile-card, .user-card, article, .member')
        
        if not profile_cards:
            # Try alternative selectors
            profile_cards = response.xpath('//div[contains(@class, "profile") or contains(@class, "creator") or contains(@class, "user")]')
        
        for card in profile_cards:
            # Extract profile link
            profile_link = card.css('a::attr(href)').get()
            if not profile_link:
                profile_link = card.xpath('.//a/@href').get()
            
            if profile_link and not profile_link.startswith('http'):
                profile_link = response.urljoin(profile_link)
            
            # Extract name - try multiple selectors
            name = (
                card.css('.name::text, .creator-name::text, h2::text, h3::text').get() or
                card.xpath('.//h2/text() | .//h3/text() | .//*[contains(@class, "name")]/text()').get() or
                card.css('a::text').get()
            )
            
            # Extract email - look for email patterns
            email = None
            email_elements = card.css('[href^="mailto:"]::attr(href)').getall()
            for elem in email_elements:
                email = elem.replace('mailto:', '').strip()
                break
            
            if not email:
                # Try to find email in text content
                text_content = ' '.join(card.css('::text').getall())
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails_found = re.findall(email_pattern, text_content)
                if emails_found:
                    email = emails_found[0]
            
            if name and email and profile_link:
                # Check if we need more profiles of this role
                if self.role_counts.get(role_type, 0) < self.min_per_role:
                    self.role_counts[role_type] = self.role_counts.get(role_type, 0) + 1
                    
                    yield ProfileItem(
                        name=name.strip(),
                        email=email.strip().lower(),
                        profile_link=profile_link,
                        role_type=role_type
                    )
        
        # Check if we need more profiles for this role
        current_count = self.role_counts.get(role_type, 0)
        if current_count < self.min_per_role:
            # Look for pagination - next page button
            next_page = None
            
            # Try common pagination selectors
            next_selectors = [
                '.next::attr(href)',
                '.pagination-next::attr(href)',
                'a[rel="next"]::attr(href)',
                '.page-link.next::attr(href)',
                'button.next::attr(data-href)',
            ]
            
            for selector in next_selectors:
                next_page = response.css(selector).get()
                if next_page:
                    break
            
            if not next_page:
                # Try xpath
                next_page = response.xpath('//a[contains(text(), "Next") or contains(text(), "next")]/@href').get()
            
            if next_page:
                next_page = response.urljoin(next_page)
                logging.info(f"Following pagination to: {next_page}")
                
                yield scrapy.Request(
                    url=next_page,
                    callback=self.parse,
                    meta={
                        'playwright': True,
                        'playwright_page_methods': [
                            PageMethod('wait_for_selector', 'body', timeout=30000),
                        ],
                        'role_type': role_type,
                        'page_num': page_num + 1,
                    },
                    dont_filter=True,
                )
            else:
                logging.info(f"No more pagination found for {role_type}. Collected {current_count} profiles.")
    
    def closed(self, reason):
        logging.info("Spider closed: %s", reason)
        for role, count in self.role_counts.items():
            logging.info(f"Total {role} profiles collected: {count}")
