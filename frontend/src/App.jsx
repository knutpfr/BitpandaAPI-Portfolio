import { useState, useEffect } from 'react';
import './styles.css';
import axios from 'axios';
import PieChart from './PieChart';

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
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

  useEffect(() => {
    // Initiales Laden
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

  // Prepare data for crypto portfolio pie chart
  const prepareCryptoChartData = () => {
    if (!portfolio || !portfolio.crypto_wallets || portfolio.crypto_wallets.length === 0) {
      return [];
    }

    return portfolio.crypto_wallets.map(wallet => ({
      label: `${getCryptoIcon(wallet.symbol)} ${wallet.symbol}`,
      value: wallet.balance_eur,
      color: getCryptoColor(wallet.symbol, 0.8),
      borderColor: getCryptoColor(wallet.symbol, 1),
    }));
  };

  // Prepare data for complete portfolio pie chart (crypto + fiat)
  const prepareCompletePortfolioData = () => {
    const data = [];

    // Add crypto wallets
    if (portfolio && portfolio.crypto_wallets) {
      portfolio.crypto_wallets.forEach(wallet => {
        data.push({
          label: `${getCryptoIcon(wallet.symbol)} ${wallet.symbol}`,
          value: wallet.balance_eur,
          color: getCryptoColor(wallet.symbol, 0.8),
          borderColor: getCryptoColor(wallet.symbol, 1),
        });
      });
    }

    // Add fiat wallets (convert to EUR if needed)
    if (portfolio && portfolio.fiat_wallets) {
      portfolio.fiat_wallets.forEach(wallet => {
        // For demo purposes, assume 1:1 EUR conversion for simplicity
        // In real implementation, you'd convert USD to EUR using current rates
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
    // Prüfen, ob Demo-Modus aktiv ist
  const isDemoMode = portfolio && portfolio.hasOwnProperty('demo_mode') ? portfolio.demo_mode : false;
  return (
    <div className="container">
      <h1>Bitpanda Portfolio</h1>
      {/* Demo-Mode Banner */}
      {isDemoMode && (
        <div className="demo-banner">
          🔍 Demo-Modus aktiv - Es werden Beispieldaten angezeigt
        </div>
      )}
        {/* Theme Toggle Button */}
      <div className="theme-toggle" onClick={toggleTheme} title={`Zu ${theme === 'dark' ? 'Hell' : 'Dunkel'} wechseln`}>
        {theme === 'dark' ? '☀️' : '🌙'}
      </div>
      
      {/* Krypto-Wallets Section */}
      <section className="section">
        <h2>💰 Krypto-Wallets</h2>
        {portfolio && portfolio.crypto_wallets && portfolio.crypto_wallets.length > 0 ? (
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
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">📊</div>
            <p>Keine Krypto-Wallets mit Guthaben gefunden</p>
          </div>
        )}
      </section>
      
      {/* Fiat-Wallets Section */}
      <section className="section">
        <h2>🏦 Fiat-Wallets</h2>
        {portfolio && portfolio.fiat_wallets && portfolio.fiat_wallets.length > 0 ? (
          <div className="wallet-list">
            {portfolio.fiat_wallets.map((wallet, index) => (
              <div 
                className="wallet-item" 
                key={index}
                style={{animationDelay: `${(portfolio.crypto_wallets?.length + index) * 0.1}s`}}
              >
                <div className="wallet-symbol">
                  {getCryptoIcon(wallet.symbol)} {wallet.symbol}
                </div>
                <div className="wallet-details">
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Guthaben</span>
                    <span className="wallet-detail-value">
                      {formatCurrency(wallet.balance, wallet.symbol)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">💳</div>
            <p>Keine Fiat-Wallets mit Guthaben gefunden</p>
          </div>
        )}
      </section>      
      
      {/* Portfolio Visualisierung - Pie Charts */}
      <section className="section">
        <h2>📊 Portfolio-Visualisierung</h2>
        <div className="portfolio-charts">
          {/* Gesamtes Portfolio Chart (Krypto + Fiat) */}
          {portfolio && (prepareCryptoChartData().length > 0 || (portfolio.fiat_wallets && portfolio.fiat_wallets.length > 0)) && (
            <PieChart 
              data={prepareCompletePortfolioData()} 
              title="Gesamt-Portfolio"
              icon="🏦"
            />
          )}
        </div>
        
        {/* Fallback wenn keine Daten vorhanden */}
        {(!portfolio || ((!portfolio.crypto_wallets || portfolio.crypto_wallets.length === 0) && 
                        (!portfolio.fiat_wallets || portfolio.fiat_wallets.length === 0))) && (
          <div className="empty-state">
            <div className="empty-state-icon">📈</div>
            <p>Keine Portfolio-Daten für Visualisierung verfügbar</p>
          </div>
        )}
      </section>

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
