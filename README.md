# Outscraper MCP Server

A comprehensive Model Context Protocol (MCP) server that provides access to Outscraper's powerful data extraction services. This server implements **8 complete tools** for extracting data from Google services and domains.

## 🚀 Features

### Complete Outscraper Service Coverage
- **🗺️ Google Maps Search** - Search for businesses and places with detailed information
- **⭐ Google Maps Reviews** - Extract customer reviews from any Google Maps place  
- **📸 Google Maps Photos** - Get photos from Google Maps places with metadata
- **🧭 Google Maps Directions** - Get directions between locations with multiple travel modes
- **🔍 Google Search** - Perform general Google web searches with structured results
- **📰 Google News Search** - Search Google News with time-based filtering
- **📱 Google Play Reviews** - Extract app reviews from Google Play Store
- **📧 Email & Contact Extraction** - Extract emails, phones, and social links from domains

### Advanced Capabilities
- **Data Enrichment** - Automatically enhance results with additional contact information
- **Multi-language Support** - Search and extract data in different languages
- **Regional Filtering** - Target specific countries/regions for localized results
- **Flexible Sorting** - Sort results by relevance, date, rating, etc.
- **Batch Processing** - Process multiple queries efficiently
- **Time-based Filtering** - Get only recent reviews or news articles

## 📦 Installation

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Outscraper API key

### Install with uv (recommended)
```bash
git clone <repository-url>
cd outscraper-mcp
uv sync
```

### Install with pip
```bash
git clone <repository-url>
cd outscraper-mcp
pip install -e .
```

## 🔧 Configuration

### Get Your API Key
1. Sign up at [Outscraper](https://app.outscraper.com/profile)
2. Get your API key from the profile page

### Set Environment Variable
```bash
export OUTSCRAPER_API_KEY="your_api_key_here"
```

Or create a `.env` file:
```env
OUTSCRAPER_API_KEY=your_api_key_here
```

## 🛠️ Tools Reference

### google_maps_search
Search for businesses and places on Google Maps
```python
# Parameters:
query: str              # Search query (e.g., 'restaurants brooklyn usa')
limit: int = 20         # Number of results (max: 400)
language: str = "en"    # Language code
region: str = None      # Country/region code (e.g., 'US', 'GB')
drop_duplicates: bool = False  # Remove duplicate results
enrichment: List[str] = None   # Additional services ['domains_service', 'emails_validator_service']
```

### google_maps_reviews
Extract reviews from Google Maps places
```python
# Parameters:
query: str              # Place query, place ID, or business name
reviews_limit: int = 10 # Number of reviews per place (0 for unlimited)
limit: int = 1          # Number of places to process
sort: str = "most_relevant"  # Sort order: 'most_relevant', 'newest', 'highest_rating', 'lowest_rating'
language: str = "en"    # Language code
region: str = None      # Country/region code
cutoff: int = None      # Unix timestamp for reviews after specific date
```

### google_maps_photos
Extract photos from Google Maps places
```python
# Parameters:
query: str              # Place query, place ID, or business name
photos_limit: int = 20  # Number of photos per place
limit: int = 1          # Number of places to process
language: str = "en"    # Language code
region: str = None      # Country/region code
```

### google_maps_directions
Get directions between locations
```python
# Parameters:
query: str              # Route query (e.g., 'from Times Square to Central Park')
travel_mode: str = "driving"  # 'driving', 'walking', 'bicycling', 'transit'
departure_time: int = None    # Unix timestamp for departure time
language: str = "en"    # Language code
```

### google_search
Perform Google web search
```python
# Parameters:
query: str              # Search query
pages_per_query: int = 1 # Number of result pages
language: str = "en"    # Language code
region: str = None      # Country/region code
```

### google_search_news
Search Google News
```python
# Parameters:
query: str              # News search query
pages_per_query: int = 1 # Number of result pages
language: str = "en"    # Language code
region: str = None      # Country/region code
tbs: str = None         # Time filter: 'qdr:d' (day), 'qdr:w' (week), 'qdr:m' (month)
```

### google_play_reviews
Extract Google Play Store app reviews
```python
# Parameters:
query: str              # App package name (e.g., 'com.facebook.katana')
reviews_limit: int = 100 # Number of reviews to extract
sort: str = "most_relevant"  # 'most_relevant', 'newest', 'rating'
language: str = "en"    # Language code
```

### emails_and_contacts
Extract emails and contacts from domains
```python
# Parameters:
query: str              # Domain name (e.g., 'outscraper.com')
```

## 🚀 Running the Server

### Stdio Transport (Default)
```bash
python -m outscraper_mcp
# or
outscraper-mcp
```

### HTTP Transport
```python
from outscraper_mcp import mcp

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
```

## 💡 Usage Examples

### Example 1: Find Restaurants and Get Reviews
```python
# 1. Search for restaurants
results = google_maps_search(
    query="italian restaurants manhattan nyc",
    limit=5,
    language="en",
    region="US"
)

# 2. Get reviews for a specific place
reviews = google_maps_reviews(
    query="ChIJrc9T9fpYwokRdvjYRHT8nI4",  # Place ID from search results
    reviews_limit=20,
    sort="newest"
)
```

### Example 2: Research Competition
```python
# 1. Search for competitors
competitors = google_search(
    query="best pizza delivery apps 2024",
    pages_per_query=2,
    region="US"
)

# 2. Get app reviews
app_reviews = google_play_reviews(
    query="com.dominos.android",
    reviews_limit=50,
    sort="newest"
)
```

### Example 3: Lead Generation
```python
# 1. Find businesses
businesses = google_maps_search(
    query="digital marketing agencies chicago",
    limit=20,
    enrichment=["domains_service", "emails_validator_service"]
)

# 2. Extract contact information
for business in businesses:
    if business.get('site'):
        domain = business['site'].replace('https://', '').replace('http://', '')
        contacts = emails_and_contacts(query=domain)
```

## 🔄 Integration with MCP Clients

This server is compatible with any MCP client, including:
- [Claude Desktop](https://claude.ai/desktop)
- [Zed Editor](https://zed.dev)
- Custom MCP clients

### Claude Desktop Configuration
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "outscraper-mcp",
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 📊 Rate Limits & Pricing

- Check [Outscraper Pricing](https://outscraper.com/pricing/) for current rates
- API key usage is tracked per request
- Consider implementing caching for frequently accessed data

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you've installed FastMCP 2.0
2. **API Key Error**: Verify your API key is set correctly
3. **No Results**: Check if your query parameters are valid
4. **Rate Limits**: Implement delays between requests if needed

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

Experimental Software License - see LICENSE file for details.

**Notice:** This software is experimental and free to use for all purposes. Created by Jay Ozer.

## 🔗 Links

- [Outscraper API Documentation](https://app.outscraper.com/api-docs)
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

**Built with Blu Goldens** 