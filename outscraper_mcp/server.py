#!/usr/bin/env python3
"""
Outscraper MCP Server

This server provides tools for accessing Outscraper's Google Maps data extraction services.

Tools:
- google_maps_search: Search for businesses and places on Google Maps
- google_maps_reviews: Extract reviews from Google Maps places
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
API_KEY = os.getenv("OUTSCRAPER_API_KEY")

if not API_KEY:
    logger.error("OUTSCRAPER_API_KEY environment variable is required. Please set it before running the server.")
    raise ValueError("OUTSCRAPER_API_KEY environment variable is required")

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
        logger.info(f"API Response - Status: {response.status_code}, URL: {response.url}")
        
        if 199 < response.status_code < 300:
            try:
                response_json = response.json()
                logger.info(f"Response JSON keys: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
                
                # Handle async responses (status 202)
                if response.status_code == 202:
                    if isinstance(response_json, dict) and response_json.get('status') == 'Pending':
                        return f"⏳ **Request processing asynchronously**\n\n📋 **Available tools:**\n• google_maps_search\n• google_maps_reviews\n\n🔗 **Request ID:** {response_json.get('id', 'unknown')}\n📍 **Results URL:** {response_json.get('results_location', 'N/A')}\n\n💡 **Note:** This server only provides Google Maps Search and Reviews tools."
                
                if wait_async:
                    return response_json
                else:
                    # Handle different response structures
                    if isinstance(response_json, dict):
                        # Try 'data' field first, then return whole response
                        return response_json.get('data', response_json)
                    else:
                        return response_json
            except ValueError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {response.text[:500]}")
                raise Exception(f'Invalid JSON response from API: {e}')
            except Exception as e:
                logger.error(f"Unexpected error parsing response: {e}")
                logger.error(f"Raw response: {response.text[:500]}")
                raise Exception(f'Failed to parse API response: {e}')
        else:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_json = response.json()
                if isinstance(error_json, dict) and 'message' in error_json:
                    error_msg += f": {error_json['message']}"
            except:
                error_msg += f": {response.text[:200]}"
            
            logger.error(error_msg)
            raise Exception(error_msg)
    
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
            
        try:
            response = requests.get(
                f'{OUTSCRAPER_API_BASE}/maps/search-v3',
                params=params,
                headers=self.headers,
                timeout=30
            )
            return self._handle_response(response, wait_async)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during Google Maps search: {e}")
            raise Exception(f"Network error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during Google Maps search: {e}")
            raise
    
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
            
        try:
            response = requests.get(
                f'{OUTSCRAPER_API_BASE}/maps/reviews-v3',
                params=params,
                headers=self.headers,
                timeout=30
            )
            return self._handle_response(response, wait_async)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during Google Maps reviews: {e}")
            raise Exception(f"Network error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during Google Maps reviews: {e}")
            raise

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
        logger.error(f"Query: {query}, Limit: {limit}, Language: {language}")
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






 