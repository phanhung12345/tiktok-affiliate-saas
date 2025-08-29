import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// API Service
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login Component
const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await api.post('/auth/login', { email, password });
      localStorage.setItem('access_token', response.data.access_token);
      onLogin(response.data.user);
    } catch (error) {
      alert('Login failed: ' + error.response?.data?.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <h2>TikTok Affiliate SaaS</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

// Shopify Connection Component
const ShopifyConnect = ({ user, onConnect }) => {
  const [storeUrl, setStoreUrl] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [loading, setLoading] = useState(false);

  const handleConnect = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await api.post('/shopify/connect', {
        store_url: storeUrl,
        access_token: accessToken
      });
      onConnect();
      alert('Shopify store connected successfully!');
    } catch (error) {
      alert('Connection failed: ' + error.response?.data?.error);
    }
    
    setLoading(false);
  };

  if (user.shopify_connected) {
    return (
      <div className="shopify-connected">
        <h3>✅ Shopify Store Connected</h3>
        <p>Your store is ready for product imports!</p>
      </div>
    );
  }

  return (
    <div className="shopify-connect">
      <h3>Connect Your Shopify Store</h3>
      <form onSubmit={handleConnect}>
        <input
          type="text"
          placeholder="Store URL (e.g., mystore.myshopify.com)"
          value={storeUrl}
          onChange={(e) => setStoreUrl(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Private App Access Token"
          value={accessToken}
          onChange={(e) => setAccessToken(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Connecting...' : 'Connect Store'}
        </button>
      </form>
    </div>
  );
};

// Product List Component
const ProductList = ({ user }) => {
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);

  useEffect(() => {
    fetchTrendingProducts();
  }, []);

  const fetchTrendingProducts = async () => {
    setLoading(true);
    try {
      const response = await api.get('/products/trending?limit=20');
      setProducts(response.data.products);
    } catch (error) {
      alert('Failed to fetch products');
    }
    setLoading(false);
  };

  const handleProductSelect = (productId) => {
    setSelectedProducts(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const importToShopify = async () => {
    if (!user.shopify_connected) {
      alert('Please connect your Shopify store first');
      return;
    }

    setImporting(true);
    try {
      const response = await api.post('/products/import-to-shopify', {
        product_ids: selectedProducts
      });
      
      const successful = response.data.results.filter(r => r.status === 'success').length;
      alert(`Successfully imported ${successful} products to Shopify!`);
      setSelectedProducts([]);
    } catch (error) {
      alert('Import failed: ' + error.response?.data?.error);
    }
    setImporting(false);
  };

  if (loading) return <div>Loading trending products...</div>;

  return (
    <div className="product-list">
      <div className="product-header">
        <h3>Trending TikTok Products</h3>
        <div className="actions">
          <button onClick={fetchTrendingProducts}>Refresh</button>
          {selectedProducts.length > 0 && (
            <button 
              onClick={importToShopify} 
              disabled={importing}
              className="import-btn"
            >
              {importing ? 'Importing...' : `Import ${selectedProducts.length} Products`}
            </button>
          )}
        </div>
      </div>
      
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <input
              type="checkbox"
              checked={selectedProducts.includes(product.id)}
              onChange={() => handleProductSelect(product.id)}
            />
            <img src={product.image_url} alt={product.title} />
            <h4>{product.title}</h4>
            <p className="price">${product.price}</p>
            <p className="trending-score">Trending Score: {product.trending_score}</p>
            <p className="category">{product.category}</p>
            <a href={product.affiliate_link} target="_blank" rel="noopener noreferrer">
              View on TikTok
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

// Dashboard Component
const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/dashboard/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats');
    }
  };

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.total_products || 0}</h3>
          <p>Total Products</p>
        </div>
        <div className="stat-card">
          <h3>{stats.imported_products || 0}</h3>
          <p>Imported to Shopify</p>
        </div>
        <div className="stat-card">
          <h3>{stats.trending_products || 0}</h3>
          <p>High Trending Score</p>
        </div>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setUser({ id: 1, email: 'demo@example.com', shopify_connected: false });
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const handleShopifyConnect = () => {
    setUser(prev => ({ ...prev, shopify_connected: true }));
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>TikTok Affiliate SaaS</h1>
        <nav>
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={activeTab === 'products' ? 'active' : ''}
            onClick={() => setActiveTab('products')}
          >
            Products
          </button>
          <button 
            className={activeTab === 'shopify' ? 'active' : ''}
            onClick={() => setActiveTab('shopify')}
          >
            Shopify
          </button>
          <button onClick={handleLogout}>Logout</button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard user={user} />}
        {activeTab === 'products' && <ProductList user={user} />}
        {activeTab === 'shopify' && (
          <ShopifyConnect user={user} onConnect={handleShopifyConnect} />
        )}
      </main>
    </div>
  );
};

export default App;