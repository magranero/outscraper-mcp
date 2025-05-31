#!/usr/bin/env python3
"""
Example usage of the Outscraper MCP Server

This script demonstrates how to use the Outscraper MCP server tools
to search for businesses and extract reviews.

Before running this script, make sure you have:
1. Set the OUTSCRAPER_API_KEY environment variable
2. Installed all dependencies with `uv sync`
"""

import os
import csv
from outscraper_mcp_server import OutscraperClient

def main():
    # Check if API key is set
    api_key = os.getenv("OUTSCRAPER_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ Please set your OUTSCRAPER_API_KEY environment variable")
        print("   Get your API key from: https://app.outscraper.com/api-docs/")
        return
    
    # Initialize the Outscraper client
    client = OutscraperClient(api_key)
    
    print("🔍 Outscraper MCP Server Example\n")
    
    # Example 1: Search for businesses
    print("1. Searching for pediatric dentists in Novato, CA...")
    try:
        search_results = client.google_maps_search(
            query="pediatric dentist Novato CA",
            limit=3,
            region="US"
        )
        
        if search_results:
            print(f"   Found {len(search_results)} results:")
            for i, business in enumerate(search_results, 1):
                print(f"   {i}. {business.get('name', 'N/A')}")
                print(f"      📍 {business.get('full_address', 'N/A')}")
                print(f"      ⭐ {business.get('rating', 'N/A')} ({business.get('reviews', 0)} reviews)")
                print(f"      📞 {business.get('phone', 'N/A')}")
                print()
        else:
            print("   No results found.")
    
    except Exception as e:
        print(f"   ❌ Error searching: {str(e)}")
    
    # Example 2: Extract reviews from the first business found
    if search_results and len(search_results) > 0:
        business = search_results[0]
        place_id = business.get('place_id')
        business_name = business.get('name')
        
        print(f"2. Extracting latest 5 reviews for '{business_name}'...")
        try:
            reviews_data = client.google_maps_reviews(
                query=place_id,
                reviews_limit=5,
                sort="newest"
            )
            
            if reviews_data and len(reviews_data) > 0:
                reviews = reviews_data[0].get('reviews_data', [])
                print(f"   Found {len(reviews)} reviews:")
                
                for i, review in enumerate(reviews, 1):
                    reviewer = review.get('author_title', 'Anonymous')
                    rating = review.get('review_rating', 'N/A')
                    date = review.get('review_datetime_utc', 'N/A')
                    text = review.get('review_text', 'No text')
                    
                    print(f"   {i}. {reviewer} - {rating}⭐")
                    print(f"      📅 {date}")
                    print(f"      💬 {text[:100]}{'...' if len(text) > 100 else ''}")
                    print()
                
                # Save reviews to CSV
                save_reviews_to_csv(reviews, f"{business_name.replace(' ', '_')}_reviews.csv")
            else:
                print("   No reviews found.")
                
        except Exception as e:
            print(f"   ❌ Error extracting reviews: {str(e)}")

def save_reviews_to_csv(reviews, filename):
    """Save reviews to a CSV file"""
    headers = [
        'reviewer_name', 'rating', 'date', 'review_text', 
        'likes', 'review_id', 'reviewer_url'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for review in reviews:
            row = [
                review.get('author_title', ''),
                review.get('review_rating', ''),
                review.get('review_datetime_utc', ''),
                review.get('review_text', ''),
                review.get('review_likes', ''),
                review.get('review_id', ''),
                review.get('author_link', '')
            ]
            writer.writerow(row)
    
    print(f"   💾 Reviews saved to {filename}")

if __name__ == "__main__":
    main() 