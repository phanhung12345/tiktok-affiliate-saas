from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tiktok_affiliate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    shopify_store_url = db.Column(db.String(255))
    shopify_access_token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tiktok_product_id = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    affiliate_link = db.Column(db.String(500))
    trending_score = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class ShopifyProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    shopify_product_id = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# TikTok Trending Products Service
class TikTokTrendingService:
    def __init__(self):
        self.base_url = "https://api.tiktok.com/business/affiliate/"
        
    def get_trending_products(self, limit=50, category=None):
        """Fetch trending products from TikTok Shop"""
        # Mock data for demo - replace with actual TikTok API calls
        mock_products = [
            {
                "id": "tt_001",
                "title": "Wireless Bluetooth Earbuds",
                "description": "High-quality wireless earbuds with noise cancellation",
                "price": 29.99,
                "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=300",
                "affiliate_link": "https://tiktok.com/affiliate/earbuds",
                "trending_score": 95,
                "category": "Electronics"
            },
            {
                "id": "tt_002", 
                "title": "LED Strip Lights",
                "description": "RGB LED strip lights for room decoration",
                "price": 19.99,
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300",
                "affiliate_link": "https://tiktok.com/affiliate/led-strips",
                "trending_score": 88,
                "category": "Home & Garden"
            },
            {
                "id": "tt_003",
                "title": "Phone Camera Lens Kit",
                "description": "Professional camera lens kit for smartphones",
                "price": 39.99,
                "image_url": "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=300",
                "affiliate_link": "https://tiktok.com/affiliate/camera-lens",
                "trending_score": 92,
                "category": "Electronics"
            }
        ]
        
        return mock_products[:limit]

# Shopify Integration Service
class ShopifyService:
    def __init__(self, store_url, access_token):
        self.store_url = store_url
        self.access_token = access_token
        self.base_url = f"https://{store_url}/admin/api/2023-10/products.json"
        
    def create_product(self, product_data):
        """Create a product in Shopify store"""
        headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        
        shopify_product = {
            "product": {
                "title": product_data['title'],
                "body_html": product_data['description'],
                "vendor": "TikTok Affiliate",
                "product_type": product_data.get('category', 'General'),
                "status": "active",
                "images": [{"src": product_data['image_url']}] if product_data.get('image_url') else [],
                "variants": [{
                    "price": str(product_data['price']),
                    "inventory_management": "shopify",
                    "inventory_quantity": 100
                }]
            }
        }
        
        # Mock response for demo
        return {
            "product": {
                "id": f"shopify_{product_data['id']}",
                "title": product_data['title'],
                "handle": product_data['title'].lower().replace(' ', '-'),
                "status": "active"
            }
        }

# API Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Demo login - replace with proper authentication
    if email and password:
        access_token = create_access_token(identity=1)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': 1,
                'email': email,
                'shopify_connected': False
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/products/trending', methods=['GET'])
@jwt_required()
def get_trending_products():
    limit = request.args.get('limit', 50, type=int)
    category = request.args.get('category')
    
    tiktok_service = TikTokTrendingService()
    products = tiktok_service.get_trending_products(limit, category)
    
    return jsonify({'products': products})

@app.route('/api/shopify/connect', methods=['POST'])
@jwt_required()
def connect_shopify():
    data = request.get_json()
    store_url = data.get('store_url')
    access_token = data.get('access_token')
    
    # In production, validate the Shopify credentials
    return jsonify({'message': 'Shopify store connected successfully'})

@app.route('/api/products/import-to-shopify', methods=['POST'])
@jwt_required()
def import_to_shopify():
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    
    # Mock import process
    results = []
    for product_id in product_ids:
        results.append({
            'product_id': product_id,
            'status': 'success',
            'shopify_id': f'shopify_{product_id}'
        })
    
    return jsonify({'results': results})

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    return jsonify({
        'total_products': 150,
        'imported_products': 45,
        'trending_products': 23
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)