#!/usr/bin/env python3
"""
Outscraper MCP Server

This server provides comprehensive tools for accessing Outscraper's data extraction services.

Tools:
- google_maps_search: Search for businesses and places on Google Maps
- google_maps_reviews: Extract reviews from Google Maps places  
- google_maps_photos: Extract photos from Google Maps places
- google_maps_directions: Get directions between locations
- google_search: Perform Google web search
- google_search_news: Search Google News
- google_play_reviews: Extract Google Play Store app reviews
- emails_and_contacts: Extract emails and contacts from domains
"""

import logging
import os
from typing import Any, List, Union, Optional, Dict
import requests
from fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outscraper-mcp")

# Create FastMCP server instance
mcp = FastMCP("outscraper-mcp")

# Outscraper API configuration
OUTSCRAPER_API_BASE = "https://api.app.outscraper.com"
API_KEY = os.getenv("OUTSCRAPER_API_KEY", "api_key")

if API_KEY == "api_key":
    logger.warning("Using placeholder API key. Please set OUTSCRAPER_API_KEY environment variable.")

class OutscraperClient:
    """Outscraper API client for making requests"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-KEY': api_key,
            'client': 'MCP Server'
        }
    
    def _handle_response(self, response: requests.Response, wait_async: bool = False) -> Union[List, Dict]:
        """Handle API response and return data"""
        if 199 < response.status_code < 300:
            if wait_async:
                response_json = response.json()
                return response_json
            else:
                return response.json().get('data', [])
        else:
            raise Exception(f'API request failed with status code: {response.status_code}, Response: {response.text}')
    
    def google_maps_search(self, query: Union[List[str], str], limit: int = 20, 
                          language: str = 'en', region: str = None, 
                          drop_duplicates: bool = False, enrichment: List[str] = None) -> Union[List, Dict]:
        """Search Google Maps for places/businesses"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        wait_async = len(queries) > 10 and limit > 1
        
        params = {
            'query': queries,
            'language': language,
            'organizationsPerQueryLimit': limit,
            'async': wait_async,
            'dropDuplicates': drop_duplicates
        }
        
        if region:
            params['region'] = region
        if enrichment:
            params['enrichment'] = enrichment
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/maps/search-v3',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response, wait_async)
    
    def google_maps_reviews(self, query: Union[List[str], str], reviews_limit: int = 10,
                           limit: int = 1, sort: str = 'most_relevant', 
                           language: str = 'en', region: str = None,
                           cutoff: int = None) -> Union[List, Dict]:
        """Get reviews from Google Maps places"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        wait_async = reviews_limit > 499 or reviews_limit == 0 or len(queries) > 10
        
        params = {
            'query': queries,
            'reviewsLimit': reviews_limit,
            'limit': limit,
            'sort': sort,
            'language': language,
            'async': wait_async
        }
        
        if region:
            params['region'] = region
        if cutoff:
            params['cutoff'] = cutoff
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/maps/reviews-v3',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response, wait_async)
    
    def google_maps_photos(self, query: Union[List[str], str], photos_limit: int = 20,
                          limit: int = 1, language: str = 'en', region: str = None) -> Union[List, Dict]:
        """Get photos from Google Maps places"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries,
            'photosLimit': photos_limit,
            'limit': limit,
            'language': language
        }
        
        if region:
            params['region'] = region
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/maps/photos',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)
    
    def google_maps_directions(self, query: Union[List[str], str], travel_mode: str = 'driving',
                              departure_time: int = None, language: str = 'en') -> Union[List, Dict]:
        """Get directions between locations"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries,
            'travelMode': travel_mode,
            'language': language
        }
        
        if departure_time:
            params['departureTime'] = departure_time
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/maps/directions',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)
    
    def google_search(self, query: Union[List[str], str], pages_per_query: int = 1,
                     language: str = 'en', region: str = None) -> Union[List, Dict]:
        """Perform Google web search"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries,
            'pagesPerQuery': pages_per_query,
            'language': language
        }
        
        if region:
            params['region'] = region
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/google-search-v3',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)
    
    def google_search_news(self, query: Union[List[str], str], pages_per_query: int = 1,
                          language: str = 'en', region: str = None, tbs: str = None) -> Union[List, Dict]:
        """Search Google News"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries,
            'pagesPerQuery': pages_per_query,
            'language': language
        }
        
        if region:
            params['region'] = region
        if tbs:
            params['tbs'] = tbs
            
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/google-search-news',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)
    
    def google_play_reviews(self, query: Union[List[str], str], reviews_limit: int = 100,
                           sort: str = 'most_relevant', language: str = 'en') -> Union[List, Dict]:
        """Get Google Play Store app reviews"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries,
            'reviewsLimit': reviews_limit,
            'sort': sort,
            'language': language
        }
        
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/google-play-reviews',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)
    
    def emails_and_contacts(self, query: Union[List[str], str]) -> Union[List, Dict]:
        """Extract emails and contacts from domains"""
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query
            
        params = {
            'query': queries
        }
        
        response = requests.get(
            f'{OUTSCRAPER_API_BASE}/emails-and-contacts',
            params=params,
            headers=self.headers
        )
        
        return self._handle_response(response)

# Initialize client
client = OutscraperClient(API_KEY)

@mcp.tool()
def google_maps_search(query: str, limit: int = 20, language: str = "en", 
                      region: Optional[str] = None, drop_duplicates: bool = False,
                      enrichment: Optional[List[str]] = None) -> str:
    """
    Search for businesses and places on Google Maps using Outscraper
    
    Args:
        query: Search query (e.g., 'restaurants brooklyn usa', 'hotels paris france')
        limit: Number of results to return (default: 20, max: 400)  
        language: Language code (default: 'en')
        region: Country/region code (e.g., 'US', 'GB', 'DE')
        drop_duplicates: Remove duplicate results (default: False)
        enrichment: Additional services to run (e.g., ['domains_service', 'emails_validator_service'])
    
    Returns:
        Formatted search results with business information
    """
    try:
        logger.info(f"Searching Google Maps for: {query}")
        
        results = client.google_maps_search(
            query=query,
            limit=limit,
            language=language,
            region=region,
            drop_duplicates=drop_duplicates,
            enrichment=enrichment
        )
        
        if not results:
            return "No results found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list) and len(results) > 0:
            places = results[0] if isinstance(results[0], list) else results
            
            for i, place in enumerate(places[:limit], 1):
                if isinstance(place, dict):
                    formatted_place = f"**{i}. {place.get('name', 'Unknown')}**\n"
                    formatted_place += f"   📍 Address: {place.get('full_address', 'N/A')}\n"
                    formatted_place += f"   ⭐ Rating: {place.get('rating', 'N/A')} ({place.get('reviews', 0)} reviews)\n"
                    formatted_place += f"   📞 Phone: {place.get('phone', 'N/A')}\n"
                    formatted_place += f"   🌐 Website: {place.get('site', 'N/A')}\n"
                    formatted_place += f"   🏷️ Type: {place.get('type', 'N/A')}\n"
                    
                    if place.get('working_hours'):
                        formatted_place += f"   🕒 Hours: {place.get('working_hours_old_format', 'N/A')}\n"
                    
                    formatted_place += f"   🆔 Place ID: {place.get('place_id', 'N/A')}\n"
                    
                    # Include enrichment data if available
                    if place.get('emails'):
                        formatted_place += f"   📧 Emails: {', '.join([email.get('value') for email in place.get('emails', [])])}\n"
                    
                    formatted_place += "---\n"
                    formatted_results.append(formatted_place)
            
            return f"Found {len(places)} places for '{query}':\n\n" + "\n".join(formatted_results)
        else:
            return f"Search results for '{query}':\n\n" + str(results)
            
    except Exception as e:
        logger.error(f"Error in google_maps_search: {str(e)}")
        return f"Error searching Google Maps: {str(e)}"

@mcp.tool()
def google_maps_reviews(query: str, reviews_limit: int = 10, limit: int = 1, 
                       sort: str = "most_relevant", language: str = "en", 
                       region: Optional[str] = None, cutoff: Optional[int] = None) -> str:
    """
    Extract reviews from Google Maps places using Outscraper
    
    Args:
        query: Place query, place ID, or business name (e.g., 'ChIJrc9T9fpYwokRdvjYRHT8nI4', 'Memphis Seoul brooklyn usa')
        reviews_limit: Number of reviews to extract per place (default: 10, 0 for unlimited)
        limit: Number of places to process (default: 1)
        sort: Sort order for reviews ('most_relevant', 'newest', 'highest_rating', 'lowest_rating')
        language: Language code (default: 'en')
        region: Country/region code (e.g., 'US', 'GB', 'DE')
        cutoff: Unix timestamp to get only reviews after this date
    
    Returns:
        Formatted reviews data with place information and individual reviews
    """
    try:
        logger.info(f"Getting reviews for: {query}")
        
        results = client.google_maps_reviews(
            query=query,
            reviews_limit=reviews_limit,
            limit=limit,
            sort=sort,
            language=language,
            region=region,
            cutoff=cutoff
        )
        
        if not results:
            return "No reviews found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list):
            for place_data in results:
                if isinstance(place_data, dict):
                    # Place information
                    place_info = f"**{place_data.get('name', 'Unknown Place')}**\n"
                    place_info += f"📍 Address: {place_data.get('address', 'N/A')}\n"
                    place_info += f"⭐ Rating: {place_data.get('rating', 'N/A')} ({place_data.get('reviews', 0)} total reviews)\n"
                    place_info += f"📞 Phone: {place_data.get('phone', 'N/A')}\n"
                    place_info += f"🌐 Website: {place_data.get('site', 'N/A')}\n\n"
                    
                    formatted_results.append(place_info)
                    
                    # Reviews
                    reviews_data = place_data.get('reviews_data', [])
                    if reviews_data:
                        formatted_results.append(f"**Reviews (showing {len(reviews_data)} reviews):**\n")
                        
                        for i, review in enumerate(reviews_data, 1):
                            review_text = f"{i}. **{review.get('autor_name', 'Anonymous')}** - {review.get('review_rating', 'N/A')}⭐\n"
                            review_text += f"   📅 Date: {review.get('review_datetime_utc', 'N/A')}\n"
                            review_text += f"   💬 Review: {review.get('review_text', 'No text')[:200]}{'...' if len(review.get('review_text', '')) > 200 else ''}\n"
                            
                            if review.get('review_likes'):
                                review_text += f"   👍 Likes: {review.get('review_likes')}\n"
                            
                            review_text += "\n"
                            formatted_results.append(review_text)
                    else:
                        formatted_results.append("No reviews found.\n")
                    
                    formatted_results.append("=" * 50 + "\n")
        
        return f"Reviews for '{query}':\n\n" + "".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in google_maps_reviews: {str(e)}")
        return f"Error getting reviews: {str(e)}"

@mcp.tool()
def google_maps_photos(query: str, photos_limit: int = 20, limit: int = 1, 
                      language: str = "en", region: Optional[str] = None) -> str:
    """
    Extract photos from Google Maps places using Outscraper
    
    Args:
        query: Place query, place ID, or business name
        photos_limit: Number of photos to extract per place (default: 20)
        limit: Number of places to process (default: 1)
        language: Language code (default: 'en')
        region: Country/region code (e.g., 'US', 'GB', 'DE')
    
    Returns:
        Formatted photos data with URLs and metadata
    """
    try:
        logger.info(f"Getting photos for: {query}")
        
        results = client.google_maps_photos(
            query=query,
            photos_limit=photos_limit,
            limit=limit,
            language=language,
            region=region
        )
        
        if not results:
            return "No photos found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list):
            for place_data in results:
                if isinstance(place_data, dict):
                    place_info = f"**{place_data.get('name', 'Unknown Place')}**\n"
                    place_info += f"📍 Address: {place_data.get('address', 'N/A')}\n"
                    place_info += f"📸 Total Photos: {place_data.get('photos_count', 0)}\n\n"
                    
                    formatted_results.append(place_info)
                    
                    # Photos
                    photos_data = place_data.get('photos_data', [])
                    if photos_data:
                        formatted_results.append(f"**Photos (showing {len(photos_data)} photos):**\n")
                        
                        for i, photo in enumerate(photos_data, 1):
                            photo_text = f"{i}. 📷 Photo URL: {photo.get('photo_url', 'N/A')}\n"
                            if photo.get('photo_width'):
                                photo_text += f"   📐 Size: {photo.get('photo_width')}x{photo.get('photo_height')}\n"
                            photo_text += "\n"
                            formatted_results.append(photo_text)
                    else:
                        formatted_results.append("No photos found.\n")
        
        return f"Photos for '{query}':\n\n" + "".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in google_maps_photos: {str(e)}")
        return f"Error getting photos: {str(e)}"

@mcp.tool()
def google_maps_directions(query: str, travel_mode: str = "driving", 
                          departure_time: Optional[int] = None, language: str = "en") -> str:
    """
    Get directions between locations using Outscraper
    
    Args:
        query: Route query (e.g., 'from Times Square to Central Park', or coordinates)
        travel_mode: Mode of travel ('driving', 'walking', 'bicycling', 'transit')
        departure_time: Unix timestamp for departure time (for transit/traffic)
        language: Language code (default: 'en')
    
    Returns:
        Formatted directions with route information
    """
    try:
        logger.info(f"Getting directions for: {query}")
        
        results = client.google_maps_directions(
            query=query,
            travel_mode=travel_mode,
            departure_time=departure_time,
            language=language
        )
        
        if not results:
            return "No directions found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list):
            for route_data in results:
                if isinstance(route_data, dict):
                    route_info = f"**Route Information**\n"
                    route_info += f"🚗 Travel Mode: {travel_mode.title()}\n"
                    route_info += f"📏 Distance: {route_data.get('distance', 'N/A')}\n"
                    route_info += f"⏱️ Duration: {route_data.get('duration', 'N/A')}\n"
                    
                    if route_data.get('duration_in_traffic'):
                        route_info += f"🚦 Duration in Traffic: {route_data.get('duration_in_traffic', 'N/A')}\n"
                    
                    route_info += "\n"
                    formatted_results.append(route_info)
                    
                    # Steps
                    steps = route_data.get('steps', [])
                    if steps:
                        formatted_results.append("**Directions:**\n")
                        
                        for i, step in enumerate(steps, 1):
                            step_text = f"{i}. {step.get('html_instructions', 'No instructions')}\n"
                            step_text += f"   📏 {step.get('distance', 'N/A')} - ⏱️ {step.get('duration', 'N/A')}\n\n"
                            formatted_results.append(step_text)
        
        return f"Directions for '{query}':\n\n" + "".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in google_maps_directions: {str(e)}")
        return f"Error getting directions: {str(e)}"

@mcp.tool()
def google_search(query: str, pages_per_query: int = 1, language: str = "en", 
                 region: Optional[str] = None) -> str:
    """
    Perform Google web search using Outscraper
    
    Args:
        query: Search query (e.g., 'best restaurants 2024', 'python programming tutorial')
        pages_per_query: Number of result pages to fetch (default: 1)
        language: Language code (default: 'en')
        region: Country/region code (e.g., 'US', 'GB', 'DE')
    
    Returns:
        Formatted search results with titles, URLs, and descriptions
    """
    try:
        logger.info(f"Performing Google search for: {query}")
        
        results = client.google_search(
            query=query,
            pages_per_query=pages_per_query,
            language=language,
            region=region
        )
        
        if not results:
            return "No search results found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list) and len(results) > 0:
            search_results = results[0] if isinstance(results[0], list) else results
            
            for i, result in enumerate(search_results, 1):
                if isinstance(result, dict):
                    formatted_result = f"**{i}. {result.get('title', 'No Title')}**\n"
                    formatted_result += f"🔗 URL: {result.get('link', 'N/A')}\n"
                    formatted_result += f"📝 Description: {result.get('snippet', 'No description')}\n"
                    
                    if result.get('displayed_link'):
                        formatted_result += f"📌 Displayed URL: {result.get('displayed_link')}\n"
                    
                    formatted_result += "---\n"
                    formatted_results.append(formatted_result)
            
            return f"Search results for '{query}':\n\n" + "\n".join(formatted_results)
        
        return f"Search results for '{query}':\n\n" + str(results)
        
    except Exception as e:
        logger.error(f"Error in google_search: {str(e)}")
        return f"Error performing Google search: {str(e)}"

@mcp.tool()
def google_search_news(query: str, pages_per_query: int = 1, language: str = "en", 
                      region: Optional[str] = None, tbs: Optional[str] = None) -> str:
    """
    Search Google News using Outscraper
    
    Args:
        query: News search query (e.g., 'AI technology news', 'climate change 2024')
        pages_per_query: Number of result pages to fetch (default: 1)
        language: Language code (default: 'en')
        region: Country/region code (e.g., 'US', 'GB', 'DE')
        tbs: Time-based search filter (e.g., 'qdr:d' for past day, 'qdr:w' for past week)
    
    Returns:
        Formatted news results with headlines, sources, and dates
    """
    try:
        logger.info(f"Searching Google News for: {query}")
        
        results = client.google_search_news(
            query=query,
            pages_per_query=pages_per_query,
            language=language,
            region=region,
            tbs=tbs
        )
        
        if not results:
            return "No news results found for the given query."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list) and len(results) > 0:
            news_results = results[0] if isinstance(results[0], list) else results
            
            for i, result in enumerate(news_results, 1):
                if isinstance(result, dict):
                    formatted_result = f"**{i}. {result.get('title', 'No Title')}**\n"
                    formatted_result += f"📰 Source: {result.get('source', 'Unknown Source')}\n"
                    formatted_result += f"📅 Date: {result.get('date', 'N/A')}\n"
                    formatted_result += f"🔗 URL: {result.get('link', 'N/A')}\n"
                    formatted_result += f"📝 Summary: {result.get('snippet', 'No summary')}\n"
                    formatted_result += "---\n"
                    formatted_results.append(formatted_result)
            
            return f"News results for '{query}':\n\n" + "\n".join(formatted_results)
        
        return f"News results for '{query}':\n\n" + str(results)
        
    except Exception as e:
        logger.error(f"Error in google_search_news: {str(e)}")
        return f"Error searching Google News: {str(e)}"

@mcp.tool()
def google_play_reviews(query: str, reviews_limit: int = 100, sort: str = "most_relevant", 
                       language: str = "en") -> str:
    """
    Extract Google Play Store app reviews using Outscraper
    
    Args:
        query: App package name or ID (e.g., 'com.facebook.katana', 'com.instagram.android')
        reviews_limit: Number of reviews to extract (default: 100)
        sort: Sort order ('most_relevant', 'newest', 'rating')
        language: Language code (default: 'en')
    
    Returns:
        Formatted app reviews with ratings, text, and user information
    """
    try:
        logger.info(f"Getting Google Play reviews for: {query}")
        
        results = client.google_play_reviews(
            query=query,
            reviews_limit=reviews_limit,
            sort=sort,
            language=language
        )
        
        if not results:
            return "No reviews found for the given app."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list) and len(results) > 0:
            reviews = results[0] if isinstance(results[0], list) else results
            
            # Add app summary if available
            if reviews and isinstance(reviews[0], dict):
                first_review = reviews[0]
                app_info = f"**App Reviews Summary**\n"
                app_info += f"📱 App: {query}\n"
                app_info += f"📊 Total Reviews Extracted: {len(reviews)}\n\n"
                formatted_results.append(app_info)
            
            formatted_results.append("**Reviews:**\n")
            
            for i, review in enumerate(reviews, 1):
                if isinstance(review, dict):
                    formatted_review = f"{i}. **{review.get('autor_name', 'Anonymous')}** - {review.get('review_rating', 'N/A')}⭐\n"
                    formatted_review += f"   📅 Date: {review.get('review_datetime_utc', 'N/A')}\n"
                    formatted_review += f"   📱 App Version: {review.get('version', 'N/A')}\n"
                    formatted_review += f"   💬 Review: {review.get('review_text', 'No text')[:250]}{'...' if len(review.get('review_text', '')) > 250 else ''}\n"
                    
                    if review.get('review_likes'):
                        formatted_review += f"   👍 Helpful: {review.get('review_likes')}\n"
                    
                    formatted_review += "\n"
                    formatted_results.append(formatted_review)
            
            return f"Google Play reviews for '{query}':\n\n" + "".join(formatted_results)
        
        return f"Google Play reviews for '{query}':\n\n" + str(results)
        
    except Exception as e:
        logger.error(f"Error in google_play_reviews: {str(e)}")
        return f"Error getting Google Play reviews: {str(e)}"

@mcp.tool()
def emails_and_contacts(query: str) -> str:
    """
    Extract emails and contacts from domains using Outscraper
    
    Args:
        query: Domain name (e.g., 'outscraper.com', 'example.org')
    
    Returns:
        Formatted contact information including emails, phones, and social links
    """
    try:
        logger.info(f"Extracting emails and contacts for: {query}")
        
        results = client.emails_and_contacts(query=query)
        
        if not results:
            return "No contact information found for the given domain."
        
        # Format results for better readability
        formatted_results = []
        
        if isinstance(results, list):
            for domain_data in results:
                if isinstance(domain_data, dict):
                    domain_info = f"**Contact Information for {domain_data.get('domain', 'Unknown Domain')}**\n\n"
                    formatted_results.append(domain_info)
                    
                    # Emails
                    emails = domain_data.get('emails', [])
                    if emails:
                        formatted_results.append("**📧 Email Addresses:**\n")
                        for email in emails:
                            email_text = f"• {email.get('value', 'N/A')}\n"
                            sources = email.get('sources', [])
                            if sources:
                                email_text += f"  Found on: {len(sources)} page(s)\n"
                            email_text += "\n"
                            formatted_results.append(email_text)
                    
                    # Phones
                    phones = domain_data.get('phones', [])
                    if phones:
                        formatted_results.append("**📞 Phone Numbers:**\n")
                        for phone in phones:
                            phone_text = f"• {phone.get('value', 'N/A')}\n"
                            sources = phone.get('sources', [])
                            if sources:
                                phone_text += f"  Found on: {len(sources)} page(s)\n"
                            phone_text += "\n"
                            formatted_results.append(phone_text)
                    
                    # Social Links
                    socials = domain_data.get('socials', {})
                    if socials:
                        formatted_results.append("**🔗 Social Media Links:**\n")
                        for platform, url in socials.items():
                            if url:
                                formatted_results.append(f"• {platform.title()}: {url}\n")
                        formatted_results.append("\n")
                    
                    # Site Data
                    site_data = domain_data.get('site_data', {})
                    if site_data:
                        formatted_results.append("**🌐 Website Information:**\n")
                        if site_data.get('title'):
                            formatted_results.append(f"• Title: {site_data.get('title')}\n")
                        if site_data.get('description'):
                            formatted_results.append(f"• Description: {site_data.get('description')}\n")
                        formatted_results.append("\n")
        
        return f"Contact information for '{query}':\n\n" + "".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in emails_and_contacts: {str(e)}")
        return f"Error extracting contact information: {str(e)}" 