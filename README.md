# TikTok Affiliate SaaS

A comprehensive SaaS platform for finding trending TikTok Shop affiliate products and automatically importing them to Shopify stores.

## Features

🚀 **Core Functionality**
- Discover trending TikTok Shop products
- Real-time trending score analysis
- One-click Shopify integration
- Bulk product import
- Automated affiliate link management

📊 **Analytics Dashboard**
- Product performance tracking
- Import success metrics
- Trending analysis
- Revenue insights

🔧 **Technical Stack**
- **Backend**: Flask, SQLAlchemy, JWT Authentication
- **Frontend**: React, Material-UI, Axios
- **Database**: PostgreSQL
- **Cache**: Redis
- **Background Jobs**: Celery
- **Deployment**: Docker, Docker Compose

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/phanhung12345/tiktok-affiliate-saas.git
cd tiktok-affiliate-saas
```

2. **Start with Docker**
```bash
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Database: localhost:5432

### Manual Setup

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Products
- `GET /api/products/trending` - Get trending TikTok products
- `POST /api/products/import-to-shopify` - Import products to Shopify

### Shopify Integration
- `POST /api/shopify/connect` - Connect Shopify store
- `GET /api/shopify/products` - List imported products

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Configuration

### Environment Variables

**Backend (.env)**
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
TIKTOK_API_KEY=your-tiktok-api-key
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Shopify Integration

1. Create a private app in your Shopify admin
2. Generate access token with product permissions
3. Connect your store in the SaaS dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, email support@tiktokaffiliate.com or create an issue.