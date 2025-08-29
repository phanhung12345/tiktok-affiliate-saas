import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import random
from typing import List, Dict, Optional

class TikTokAffiliateScraper:
    """
    Advanced TikTok affiliate product scraper with trending analysis
    """
    
    def __init__(self):
        self.base_url = "https://affiliate.tiktokglobalshop.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://affiliate.tiktokglobalshop.com/',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_trending_products(self, limit: int = 50, category: str = None) -> List[Dict]:
        """
        Fetch trending products from TikTok Shop affiliate program
        """
        try:
            # Mock trending products with realistic data
            trending_products = [
                {
                    "id": "tt_001",
                    "title": "Wireless Bluetooth Earbuds Pro",
                    "description": "Premium wireless earbuds with active noise cancellation and 30-hour battery life",
                    "price": 29.99,
                    "original_price": 59.99,
                    "discount_percentage": 50,
                    "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400",
                    "affiliate_link": "https://tiktok.com/affiliate/earbuds-pro",
                    "trending_score": 95,
                    "category": "Electronics",
                    "commission_rate": 15.5,
                    "sales_count": 12450,
                    "rating": 4.8,
                    "review_count": 3420,
                    "tags": ["trending", "electronics", "audio", "wireless"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "tt_002",
                    "title": "RGB LED Strip Lights 50ft",
                    "description": "Smart RGB LED strip lights with app control and music sync",
                    "price": 19.99,
                    "original_price": 39.99,
                    "discount_percentage": 50,
                    "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
                    "affiliate_link": "https://tiktok.com/affiliate/led-strips",
                    "trending_score": 88,
                    "category": "Home & Garden",
                    "commission_rate": 12.0,
                    "sales_count": 8930,
                    "rating": 4.6,
                    "review_count": 2150,
                    "tags": ["trending", "home", "lighting", "smart"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "tt_003",
                    "title": "Phone Camera Lens Kit 11-in-1",
                    "description": "Professional smartphone camera lens kit with wide angle, macro, and telephoto lenses",
                    "price": 39.99,
                    "original_price": 79.99,
                    "discount_percentage": 50,
                    "image_url": "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400",
                    "affiliate_link": "https://tiktok.com/affiliate/camera-lens-kit",
                    "trending_score": 92,
                    "category": "Electronics",
                    "commission_rate": 18.0,
                    "sales_count": 6780,
                    "rating": 4.7,
                    "review_count": 1890,
                    "tags": ["trending", "photography", "mobile", "accessories"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "tt_004",
                    "title": "Portable Blender Bottle",
                    "description": "USB rechargeable portable blender for smoothies and protein shakes",
                    "price": 24.99,
                    "original_price": 49.99,
                    "discount_percentage": 50,
                    "image_url": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400",
                    "affiliate_link": "https://tiktok.com/affiliate/portable-blender",
                    "trending_score": 85,
                    "category": "Kitchen & Dining",
                    "commission_rate": 14.5,
                    "sales_count": 5420,
                    "rating": 4.5,
                    "review_count": 1230,
                    "tags": ["trending", "kitchen", "portable", "health"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "tt_005",
                    "title": "Magnetic Phone Car Mount",
                    "description": "360° rotating magnetic car phone holder with strong grip",
                    "price": 14.99,
                    "original_price": 29.99,
                    "discount_percentage": 50,
                    "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400",
                    "affiliate_link": "https://tiktok.com/affiliate/car-mount",
                    "trending_score": 78,
                    "category": "Automotive",
                    "commission_rate": 16.0,
                    "sales_count": 9870,
                    "rating": 4.4,
                    "review_count": 2340,
                    "tags": ["trending", "automotive", "phone", "accessories"],
                    "created_at": datetime.now().isoformat()
                }
            ]
            
            # Filter by category if specified
            if category:
                trending_products = [p for p in trending_products if p['category'].lower() == category.lower()]
            
            # Sort by trending score
            trending_products.sort(key=lambda x: x['trending_score'], reverse=True)
            
            return trending_products[:limit]
            
        except Exception as e:
            print(f"Error fetching trending products: {e}")
            return []
    
    def analyze_product_trends(self, product_id: str) -> Dict:
        """
        Analyze trending metrics for a specific product
        """
        try:
            # Mock trend analysis
            trend_data = {
                "product_id": product_id,
                "trend_direction": "up",
                "trend_percentage": random.uniform(5, 25),
                "peak_hours": ["18:00", "19:00", "20:00", "21:00"],
                "demographic_data": {
                    "age_groups": {
                        "18-24": 35,
                        "25-34": 40,
                        "35-44": 20,
                        "45+": 5
                    },
                    "gender": {
                        "female": 60,
                        "male": 40
                    }
                },
                "geographic_data": {
                    "US": 45,
                    "UK": 15,
                    "CA": 12,
                    "AU": 8,
                    "Other": 20
                },
                "engagement_metrics": {
                    "views": random.randint(100000, 1000000),
                    "likes": random.randint(10000, 100000),
                    "shares": random.randint(1000, 10000),
                    "comments": random.randint(500, 5000)
                },
                "conversion_rate": random.uniform(2.5, 8.5),
                "last_updated": datetime.now().isoformat()
            }
            
            return trend_data
            
        except Exception as e:
            print(f"Error analyzing product trends: {e}")
            return {}
    
    def get_product_categories(self) -> List[Dict]:
        """
        Get available product categories
        """
        categories = [
            {"id": "electronics", "name": "Electronics", "product_count": 15420},
            {"id": "home_garden", "name": "Home & Garden", "product_count": 12350},
            {"id": "fashion", "name": "Fashion & Beauty", "product_count": 18900},
            {"id": "kitchen", "name": "Kitchen & Dining", "product_count": 8760},
            {"id": "automotive", "name": "Automotive", "product_count": 5430},
            {"id": "sports", "name": "Sports & Outdoors", "product_count": 9870},
            {"id": "toys", "name": "Toys & Games", "product_count": 6540},
            {"id": "health", "name": "Health & Personal Care", "product_count": 11230}
        ]
        
        return categories
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for products by keyword
        """
        try:
            # Mock search results
            all_products = self.get_trending_products(100)
            
            # Filter products based on query
            search_results = []
            query_lower = query.lower()
            
            for product in all_products:
                if (query_lower in product['title'].lower() or 
                    query_lower in product['description'].lower() or
                    any(query_lower in tag.lower() for tag in product['tags'])):
                    search_results.append(product)
            
            return search_results[:limit]
            
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_commission_rates(self) -> Dict:
        """
        Get commission rates by category
        """
        commission_rates = {
            "Electronics": {"min": 8.0, "max": 20.0, "average": 14.5},
            "Home & Garden": {"min": 6.0, "max": 18.0, "average": 12.0},
            "Fashion & Beauty": {"min": 10.0, "max": 25.0, "average": 17.5},
            "Kitchen & Dining": {"min": 8.0, "max": 22.0, "average": 15.0},
            "Automotive": {"min": 12.0, "max": 28.0, "average": 20.0},
            "Sports & Outdoors": {"min": 9.0, "max": 24.0, "average": 16.5},
            "Toys & Games": {"min": 7.0, "max": 19.0, "average": 13.0},
            "Health & Personal Care": {"min": 11.0, "max": 26.0, "average": 18.5}
        }
        
        return commission_rates

# Usage example
if __name__ == "__main__":
    scraper = TikTokAffiliateScraper()
    
    # Get trending products
    trending = scraper.get_trending_products(limit=10)
    print(f"Found {len(trending)} trending products")
    
    # Analyze trends for first product
    if trending:
        trends = scraper.analyze_product_trends(trending[0]['id'])
        print(f"Trend analysis: {trends}")
    
    # Search for specific products
    search_results = scraper.search_products("wireless earbuds")
    print(f"Search results: {len(search_results)} products found")