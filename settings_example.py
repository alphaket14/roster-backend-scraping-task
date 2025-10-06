# Scrapy settings example configuration
# Copy this to settings.py and modify as needed for advanced customization

# Concurrency settings - adjust based on your needs and server tolerance
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2  # Seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True

# Auto-throttle settings - helps prevent server overload
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Retry settings - configure retry behavior
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Playwright browser settings
PLAYWRIGHT_BROWSER_TYPE = "chromium"  # Options: chromium, firefox, webkit
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to False to see browser in action (debugging)
    # "proxy": {  # Uncomment to use proxy
    #     "server": "http://proxy-server:port",
    # },
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # milliseconds

# User agent - customize to avoid detection
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Item count limit - maximum items to scrape
CLOSESPIDER_ITEMCOUNT = 200  # Adjust based on requirements

# Feed export settings
FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_FIELDS = ["name", "email", "profile_link", "role_type"]

# Custom settings for brand filtering
# Add to BrandNameFilterPipeline.BRAND_KEYWORDS in pipelines.py
# BRAND_KEYWORDS = [
#     'studio', 'media', 'agency', 'productions', ...
# ]
