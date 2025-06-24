import { useState, useEffect } from 'react';
import './styles.css';
import axios from 'axios';
import PieChart from './PieChart';

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [chartMode, setChartMode] = useState('total'); // 'total', 'crypto', 'fiat'
  const [theme, setTheme] = useState(() => {
    // Theme aus localStorage laden oder Standard "dark"
    return localStorage.getItem('bitpanda-theme') || 'dark';
  });

  // Theme Toggle Function
  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('bitpanda-theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  // Theme anwenden beim Laden der Komponente
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Manuelles Laden (setzt loading auf true, zeigt Loading-Spinner)
  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('/api/portfolio');
      setPortfolio(response.data);
      setLastUpdate(new Date());
    } catch (err) {
      setError('Fehler beim Laden der Portfolio-Daten: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Automatisches Laden (setzt loading nicht, UI bleibt erhalten)
  const autoFetchPortfolioData = async () => {
    try {
      const response = await axios.get('/api/portfolio');
      setPortfolio(response.data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      console.error('Auto-refresh failed:', err);
    }
  };

  // Benutzer-Info laden
  const fetchUserInfo = async () => {
    try {
      const response = await axios.get('/api/user');
      setUserInfo(response.data);
    } catch (err) {
      console.error('User info fetch failed:', err);
    }
  };

  useEffect(() => {
    // Initiales Laden
    fetchUserInfo();
    fetchPortfolioData();

    // Intervall für automatisches Laden (alle 60 Sekunden)
    const interval = setInterval(() => {
      autoFetchPortfolioData();
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  // Loading State mit modernem Spinner
  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="loading-spinner"></div>
          <h2>Portfolio wird geladen...</h2>
          <p>Bitpanda-Daten werden abgerufen</p>
        </div>
      </div>
    );
  }
  
  // Error State
  if (error) {
    return (
      <div className="container">
        <div className="section error">
          <h2>⚠️ Fehler aufgetreten</h2>
          <p>{error}</p>
          <button onClick={fetchPortfolioData} className="refresh-button">
            🔄 Erneut versuchen
          </button>
        </div>
      </div>
    );
  }

  // Helper function to format currency
  const formatCurrency = (amount, currency = 'EUR') => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  // Helper function to format crypto amounts
  const formatCrypto = (amount) => {
    return new Intl.NumberFormat('de-DE', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 8
    }).format(amount);
  };
  // Helper function to get crypto icon
  const getCryptoIcon = (symbol) => {
    const icons = {
      'BTC': '₿',
      'ETH': 'Ξ',
      'ADA': '₳',
      'DOT': '●',
      'LINK': '🔗',
      'LTC': 'Ł',
      'XRP': '◆',
      'BCH': '◊',
      'BNB': '▲',
      'USDT': '$',
      'USDC': '$',
      'EUR': '€',
      'USD': '$'
    };
    return icons[symbol] || '🪙';
  };

  // Helper function to get colors for different cryptocurrencies
  const getCryptoColor = (symbol, alpha = 1) => {
    const colors = {
      'BTC': `rgba(247, 147, 26, ${alpha})`,      // Bitcoin Orange
      'ETH': `rgba(98, 126, 234, ${alpha})`,      // Ethereum Blue
      'ADA': `rgba(0, 51, 173, ${alpha})`,        // Cardano Blue
      'DOT': `rgba(230, 1, 122, ${alpha})`,       // Polkadot Pink
      'LINK': `rgba(43, 109, 255, ${alpha})`,     // Chainlink Blue
      'LTC': `rgba(191, 191, 191, ${alpha})`,     // Litecoin Silver
      'XRP': `rgba(35, 37, 53, ${alpha})`,        // XRP Dark
      'BCH': `rgba(139, 195, 74, ${alpha})`,      // Bitcoin Cash Green
      'BNB': `rgba(243, 186, 47, ${alpha})`,      // Binance Yellow
      'USDT': `rgba(80, 175, 149, ${alpha})`,     // Tether Green
      'USDC': `rgba(42, 122, 255, ${alpha})`,     // USD Coin Blue
      'EUR': `rgba(0, 212, 170, ${alpha})`,       // Fiat Green
      'USD': `rgba(0, 184, 153, ${alpha})`,       // Fiat Green (darker)
    };
    return colors[symbol] || `rgba(102, 102, 102, ${alpha})`; // Default Gray
  };
  // Prepare data for crypto pie chart
  const prepareCryptoChartData = () => {
    if (!portfolio?.assets) return [];
    
    return portfolio.assets.map(asset => ({
      label: `${getCryptoIcon(asset.symbol)} ${asset.symbol}`,
      value: asset.value,
      color: getCryptoColor(asset.symbol, 0.8),
      borderColor: getCryptoColor(asset.symbol, 1),
    }));
  };

  // Prepare data for fiat-only portfolio pie chart
  const prepareFiatChartData = () => {
    const data = [];

    // Add fiat wallets
    if (portfolio && portfolio.fiat_wallets) {
      portfolio.fiat_wallets.forEach(wallet => {
        // Für Demo-Zwecke: USD zu EUR Umrechnung (0.85), sonst 1:1
        const eurValue = wallet.symbol === 'EUR' ? wallet.balance : 
                        wallet.symbol === 'USD' ? wallet.balance * 0.85 : wallet.balance;
        
        data.push({
          label: `${getCryptoIcon(wallet.symbol)} ${wallet.symbol}`,
          value: eurValue,
          color: getCryptoColor(wallet.symbol, 0.8),
          borderColor: getCryptoColor(wallet.symbol, 1),
        });
      });
    }

    return data;
  };

  // Get current chart data based on mode
  const getCurrentChartData = () => {
    switch (chartMode) {
      case 'crypto':
        return prepareCryptoChartData();
      case 'fiat':
        return prepareFiatChartData();
      case 'total':
      default:
        return prepareCompletePortfolioData();
    }
  };

  // Get chart title and icon based on mode
  const getChartTitleAndIcon = () => {
    switch (chartMode) {
      case 'crypto':
        return { title: 'Krypto-Assets', icon: '💰' };
      case 'fiat':
        return { title: 'Fiat-Währungen', icon: '🏦' };
      case 'total':
      default:
        return { title: 'Gesamt-Portfolio', icon: '📊' };
    }
  };

  // Toggle chart mode with animation
  const toggleChartMode = () => {
    const modes = ['total', 'crypto', 'fiat'];
    const currentIndex = modes.indexOf(chartMode);
    const nextIndex = (currentIndex + 1) % modes.length;
    setChartMode(modes[nextIndex]);
  };

  // Prepare data for complete portfolio pie chart (crypto + fiat)
  const prepareCompletePortfolioData = () => {
    const data = [];

    // Add crypto assets
    if (portfolio?.assets) {
      portfolio.assets.forEach(asset => {
        data.push({
          label: `${getCryptoIcon(asset.symbol)} ${asset.symbol}`,
          value: asset.value,
          color: getCryptoColor(asset.symbol, 0.8),
          borderColor: getCryptoColor(asset.symbol, 1),
        });
      });
    }

    // Add fiat wallets
    if (portfolio?.fiat_wallets) {
      portfolio.fiat_wallets.forEach(wallet => {
        data.push({
          label: `${getCryptoIcon(wallet.symbol)} ${wallet.symbol}`,
          value: wallet.balance,
          color: getCryptoColor(wallet.symbol, 0.8),
          borderColor: getCryptoColor(wallet.symbol, 1),
        });
      });
    }

    return data;
  };// Prüfen, ob Demo-Modus aktiv ist
  const isDemoMode = (portfolio && portfolio.is_demo) || (userInfo && userInfo.is_demo);
  
  // Logout-Funktion
  const handleLogout = async () => {
    try {
      await axios.get('/logout');
      window.location.href = '/login';
    } catch (err) {
      console.error('Logout-Fehler:', err);
      window.location.href = '/login';
    }
  };

  return (
    <div className="container">
      {/* Header mit Benutzer-Info */}
      <header className="app-header">
        <h1>
          <span className="logo">₿</span> Bitpanda Portfolio
        </h1>
        <div className="header-controls">
          <div className="user-info">
            {userInfo && (
              <>
                <span className="username">👤 {userInfo.username}</span>
                {isDemoMode && <span className="demo-badge">DEMO</span>}
              </>
            )}
          </div>
          <div className="theme-toggle" onClick={toggleTheme} title={`Zu ${theme === 'dark' ? 'Hell' : 'Dunkel'} wechseln`}>
            {theme === 'dark' ? '☀️' : '🌙'}
          </div>
          <button className="logout-btn" onClick={handleLogout} title="Abmelden">
            🚪 Logout
          </button>
        </div>
      </header>

      {/* Demo-Mode Banner */}
      {isDemoMode && (
        <div className="demo-banner">
          🔍 <strong>Demo-Modus aktiv</strong> - Es werden Beispieldaten angezeigt. 
          <span className="demo-banner-text">Registrieren Sie sich mit einem echten API-Schlüssel für Live-Daten.</span>
        </div>
      )}
        {/* Portfolio Übersicht */}
      {portfolio && (
        <section className="portfolio-overview">
          <div className="portfolio-stats">
            <div className="stat-card total-value">
              <div className="stat-icon">💎</div>
              <div className="stat-content">
                <h3>Gesamtwert</h3>
                <p className="stat-value">{formatCurrency(portfolio.total_value)}</p>
                {portfolio.total_change_24h !== undefined && (
                  <p className={`stat-change ${portfolio.total_change_24h >= 0 ? 'positive' : 'negative'}`}>
                    {portfolio.total_change_24h >= 0 ? '📈' : '📉'} 
                    {formatCurrency(Math.abs(portfolio.total_change_24h))} 
                    ({portfolio.total_change_24h_percentage >= 0 ? '+' : ''}{portfolio.total_change_24h_percentage?.toFixed(2)}%)
                  </p>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Krypto-Assets Section */}
      <section className="section">
        <h2>💰 Krypto-Assets</h2>
        {portfolio && portfolio.assets && portfolio.assets.length > 0 ? (
          <>
            <div className="wallet-list">
              {portfolio.assets.map((asset, index) => (
                <div 
                  className="wallet-item" 
                  key={index}
                  data-symbol={asset.symbol}
                  style={{animationDelay: `${index * 0.1}s`}}
                >
                  <div className="wallet-symbol">
                    {asset.logo_url ? (
                      <img src={asset.logo_url} alt={asset.symbol} className="crypto-logo" />
                    ) : (
                      getCryptoIcon(asset.symbol)
                    )}
                    <span>{asset.symbol}</span>
                    <small className="asset-name">{asset.name}</small>
                  </div>                  <div className="wallet-details">
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">Anzahl</span>
                      <span className="wallet-detail-value">{formatCrypto(asset.amount)} {asset.symbol}</span>
                    </div>
                    {asset.current_price && (
                      <div className="wallet-detail-row">
                        <span className="wallet-detail-label">Aktueller Preis</span>
                        <span className="wallet-detail-value">{formatCurrency(asset.current_price)}</span>
                      </div>
                    )}
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">Portfolio-Wert</span>
                      <span className="wallet-detail-value total-value">{formatCurrency(asset.value)}</span>
                    </div>
                    {asset.change_24h !== undefined && (
                      <div className="wallet-detail-row">
                        <span className="wallet-detail-label">24h Änderung</span>
                        <span className={`wallet-detail-value ${asset.change_24h >= 0 ? 'positive' : 'negative'}`}>
                          {asset.change_24h >= 0 ? '+' : ''}{formatCurrency(asset.change_24h)} 
                          ({asset.change_24h_percentage >= 0 ? '+' : ''}{asset.change_24h_percentage?.toFixed(2)}%)
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : portfolio ? (
          <div className="empty-state">
            <div className="empty-state-icon">�</div>
            <p>Keine Assets mit Guthaben gefunden</p>
          </div>
        ) : null}
      </section>

      {/* Original Krypto-Wallets Section (für Rückwärtskompatibilität) */}
      {portfolio && portfolio.crypto_wallets && portfolio.crypto_wallets.length > 0 && (
        <section className="section">
        <h2>💰 Krypto-Wallets</h2>
          <>
            <div className="wallet-list">
              {portfolio.crypto_wallets.map((wallet, index) => (
                <div 
                  className="wallet-item" 
                  key={index}
                  data-symbol={wallet.symbol}
                  style={{animationDelay: `${index * 0.1}s`}}
                >
                  <div className="wallet-symbol">
                    {getCryptoIcon(wallet.symbol)} {wallet.symbol}
                  </div>
                  <div className="wallet-details">
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">Menge</span>
                      <span className="wallet-detail-value">{formatCrypto(wallet.balance)}</span>
                    </div>
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">Preis</span>
                      <span className="wallet-detail-value">{formatCurrency(wallet.price_eur)}</span>
                    </div>
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">Gesamtwert</span>
                      <span className="wallet-detail-value">{formatCurrency(wallet.balance_eur)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="total">
              <strong>💎 Gesamtwert Krypto-Portfolio: {formatCurrency(portfolio.total_value_eur)}</strong>
            </div>
          </>
        </section>
      )}

      {/* Fiat-Wallets Section */}
      {portfolio && portfolio.fiat_wallets && portfolio.fiat_wallets.length > 0 && (
        <section className="section">
          <h2>💶 Fiat-Guthaben</h2>
          <div className="wallet-list">
            {portfolio.fiat_wallets.map((wallet, index) => (
              <div 
                className="wallet-item fiat-wallet" 
                key={`fiat-${index}`}
                data-symbol={wallet.symbol}
                style={{animationDelay: `${(portfolio.assets?.length || 0) + index * 0.1}s`}}
              >
                <div className="wallet-symbol">
                  <span className="crypto-icon">{getCryptoIcon(wallet.symbol)}</span>
                  <div className="asset-info">
                    <span className="asset-symbol">{wallet.symbol}</span>
                    <small className="asset-name">{wallet.name}</small>
                    <span className="fiat-badge">FIAT</span>
                  </div>
                </div>
                <div className="wallet-details">
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Guthaben</span>
                    <span className="wallet-detail-value total">{formatCurrency(wallet.balance, wallet.symbol)}</span>
                  </div>
                  {wallet.symbol !== 'EUR' && (
                    <div className="wallet-detail-row">
                      <span className="wallet-detail-label">In EUR (ca.)</span>
                      <span className="wallet-detail-value">{formatCurrency(wallet.balance * 0.85)}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}      {/* Portfolio Visualisierung - Interactive Pie Chart */}
      {portfolio && (
        <section className="section chart-section">
          <div className="chart-header">
            <h2>📊 Portfolio-Visualisierung</h2>
            <div className="chart-toggle-container">
              <button 
                className={`chart-toggle-btn ${chartMode === 'total' ? 'active' : ''}`}
                onClick={() => setChartMode('total')}
                title="Gesamtes Portfolio anzeigen"
              >
                📊 Gesamt
              </button>
              <button 
                className={`chart-toggle-btn ${chartMode === 'crypto' ? 'active' : ''}`}
                onClick={() => setChartMode('crypto')}
                title="Nur Krypto-Assets anzeigen"
              >
                💰 Krypto
              </button>
              <button 
                className={`chart-toggle-btn ${chartMode === 'fiat' ? 'active' : ''}`}
                onClick={() => setChartMode('fiat')}
                title="Nur Fiat-Währungen anzeigen"
              >
                🏦 Fiat
              </button>
            </div>
          </div>
          
          <div className="portfolio-charts">
            {/* Dynamic Portfolio Chart */}
            {getCurrentChartData().length > 0 ? (
              <div className={`chart-container chart-mode-${chartMode}`} key={chartMode}>
                <PieChart 
                  data={getCurrentChartData()} 
                  title={getChartTitleAndIcon().title}
                  icon={getChartTitleAndIcon().icon}
                />
                {/* <div className="chart-stats"> 
                  <div className="chart-stat-item">
                    <span className="chart-stat-label">Assets:</span>
                    <span className="chart-stat-value">{getCurrentChartData().length}</span>
                  </div>
                  <div className="chart-stat-item">
                    <span className="chart-stat-label">Wert:</span>
                    <span className="chart-stat-value">
                      {formatCurrency(getCurrentChartData().reduce((sum, item) => sum + item.value, 0))}
                    </span>
                  </div>
                </div>*/}
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">
                  {chartMode === 'crypto' ? '💰' : chartMode === 'fiat' ? '🏦' : '📈'}
                </div>
                <p>
                  {chartMode === 'crypto' 
                    ? 'Keine Krypto-Assets verfügbar' 
                    : chartMode === 'fiat' 
                    ? 'Keine Fiat-Währungen verfügbar'
                    : 'Keine Portfolio-Daten verfügbar'
                  }
                </p>
                {chartMode !== 'total' && (
                  <button 
                    className="chart-toggle-btn secondary"
                    onClick={() => setChartMode('total')}
                  >
                    📊 Gesamtansicht zeigen
                  </button>
                )}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Update Info und Refresh Button */}
      <div style={{textAlign: 'center', marginTop: '2rem'}}>
        {lastUpdate && (
          <p style={{color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.875rem'}}>
            🕒 Letzte Aktualisierung: {lastUpdate.toLocaleTimeString('de-DE')}
          </p>        )}
        <button onClick={fetchPortfolioData} className="refresh-button">
          🔄 Portfolio aktualisieren
        </button>
          {/* Status Indicator */}
        <div className={`status-indicator ${portfolio ? 'online' : 'offline'}`}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: portfolio ? 'var(--crypto-positive)' : 'var(--crypto-negative)'
          }}></div>
          {portfolio ? 'Verbunden' : 'Getrennt'}
        </div>
        
        {/* GitHub Link */}
        <a 
          href="https://github.com/knutpfr" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="github-link"
          title="Besuche mein GitHub Profil"
        >
          <div className="github-status-dot"></div>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  );
}

export default App;
