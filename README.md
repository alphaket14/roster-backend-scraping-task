# Roster Backend Scraping Task

A production-ready web scraper built with Scrapy and Playwright to extract public profiles from Shoutt for UGC and Video roles. The scraper handles dynamic content, pagination, email validation, deduplication, and brand name filtering.

## Features

- **Scrapy + Playwright Integration**: Handles dynamic JavaScript-rendered content
- **Email Validation**: Validates and normalizes email addresses using `email-validator`
- **Deduplication**: Removes duplicate profiles based on email addresses
- **Brand Name Filtering**: Filters out profiles with brand-like names (Studio, Media, Agency, LLC, Inc, etc.)
- **Role-based Scraping**: Supports multiple roles (UGC, Video, etc.)
- **Pagination Support**: Automatically follows pagination to collect more profiles
- **Rate Limiting**: Built-in rate limiting and auto-throttling to respect server resources
- **Retry Mechanism**: Automatic retries for failed requests (HTTP 500, 502, 503, etc.)
- **CSV Export**: Exports collected profiles to CSV format
- **Scalable**: Designed to handle 1000+ profiles efficiently
- **CLI Arguments**: Flexible command-line interface for customization
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/alphaket14/roster-backend-scraping-task.git
cd roster-backend-scraping-task
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Basic Usage

Run the scraper with default settings (UGC and Video roles, minimum 50 profiles per role):

```bash
python run_scraper.py
```

### Advanced Usage

#### Scrape specific roles:
```bash
python run_scraper.py --roles UGC,Video
```

#### Set minimum profiles per role:
```bash
python run_scraper.py --min-per-role 100
```

#### Custom output file:
```bash
python run_scraper.py --output my_profiles.csv
```

#### Set log level:
```bash
python run_scraper.py --log-level DEBUG
```

#### Combine multiple options:
```bash
python run_scraper.py --roles "UGC,Video" --min-per-role 75 --output results.csv --log-level INFO
```

### Using Scrapy Directly

You can also run the spider directly with Scrapy:

```bash
scrapy crawl shoutt -a roles=UGC,Video -a min_per_role=50 -a output_file=profiles.csv
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--roles` | string | `UGC,Video` | Comma-separated list of roles to scrape |
| `--min-per-role` | integer | `50` | Minimum number of profiles to collect per role |
| `--output` | string | `profiles.csv` | Output CSV file name |
| `--log-level` | string | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Output Format

The scraper exports data to CSV with the following columns:

| Column | Description |
|--------|-------------|
| `name` | Profile name |
| `email` | Validated and normalized email address |
| `profile_link` | URL to the profile page |
| `role_type` | Role type (UGC, Video, etc.) |

### Example Output:

```csv
name,email,profile_link,role_type
John Doe,john.doe@example.com,https://www.shoutt.co/profile/johndoe,UGC
Jane Smith,jane.smith@example.com,https://www.shoutt.co/profile/janesmith,Video
```

## Architecture

### Components

1. **Spider (`shoutt_spider.py`)**: Main spider that crawls Shoutt profiles
   - Handles pagination automatically
   - Extracts profile data using CSS and XPath selectors
   - Supports multiple roles simultaneously

2. **Pipelines (`pipelines.py`)**: Data processing pipeline
   - `EmailValidationPipeline`: Validates email addresses
   - `BrandNameFilterPipeline`: Filters brand-like names
   - `DeduplicationPipeline`: Removes duplicates
   - `CSVExportPipeline`: Exports to CSV

3. **Items (`items.py`)**: Data model definition
   - Defines the structure of scraped data

4. **Settings (`settings.py`)**: Configuration
   - Playwright integration
   - Rate limiting and auto-throttling
   - Retry settings
   - Logging configuration

5. **CLI (`run_scraper.py`)**: Command-line interface
   - Argument parsing
   - Crawler process management

### Data Flow

```
Start URLs → Playwright Rendering → Spider Parsing → Item Creation →
Email Validation → Brand Filtering → Deduplication → CSV Export
```

## Brand Name Filter

The scraper automatically filters out profiles with the following brand-related keywords:

- Studio, Media, Agency, Productions, Designs, Labs
- Official, Channel, Team
- LLC, Inc, Ltd, Pvt, GmbH, PLC, Co, Company, Group
- The (when used as a prefix)

## Rate Limiting & Retry

- **Download Delay**: 2 seconds (randomized)
- **Auto-Throttle**: Enabled with target concurrency of 1.0
- **Retry Times**: 3 attempts
- **Retry HTTP Codes**: 500, 502, 503, 504, 522, 524, 408, 429

## Scalability

The scraper is designed to handle 1000+ profiles efficiently:

- Asynchronous request handling with Scrapy
- Memory-efficient item processing
- Incremental CSV writing
- Auto-throttling to prevent server overload
- Browser resource management with Playwright

## Logging

Logs include:
- Spider start/stop events
- Page navigation
- Items scraped count
- Dropped items (duplicates, invalid emails, brand names)
- Errors and warnings

Example log output:
```
2024-01-01 10:00:00 [scrapy.core.engine] INFO: Spider opened
2024-01-01 10:00:05 [shoutt] INFO: Parsing UGC page 1: https://www.shoutt.co/creators/ugc
2024-01-01 10:00:10 [shoutt] INFO: Following pagination to: https://www.shoutt.co/creators/ugc?page=2
2024-01-01 10:05:00 [shoutt] INFO: Total UGC profiles collected: 75
2024-01-01 10:05:00 [scrapy.core.engine] INFO: Spider closed: finished
```

## Troubleshooting

### No profiles found
- Check if the website structure has changed
- Verify the role URLs are correct
- Use `--log-level DEBUG` for detailed selector information

### Playwright browser not found
```bash
playwright install chromium
```

### Rate limiting or blocking
- Increase `DOWNLOAD_DELAY` in settings.py
- Add delays between requests
- Use proxy rotation (if available)

## Development

### Project Structure
```
roster-backend-scraping-task/
├── roster_scraper/
│   ├── __init__.py
│   ├── items.py           # Data models
│   ├── middlewares.py     # Custom middlewares
│   ├── pipelines.py       # Data processing pipelines
│   ├── settings.py        # Scrapy settings
│   └── spiders/
│       └── shoutt_spider.py  # Main spider
├── scrapy.cfg             # Scrapy configuration
├── run_scraper.py         # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Running Tests

Currently, the scraper can be tested by running it with debug logging:

```bash
python run_scraper.py --log-level DEBUG --min-per-role 5
```

## License

This project is for educational and demonstration purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
