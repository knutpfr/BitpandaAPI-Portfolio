import { useState, useEffect } from 'react';
import './styles.css';
import axios from 'axios';

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Lade Portfolio-Daten beim Laden der Seite
    fetchPortfolioData();
  }, []);
  
  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/portfolio');
      console.log('Portfolio-Daten erhalten:', response.data);
      setPortfolio(response.data);
      setError(null);
    } catch (err) {
      console.error('API-Fehler:', err);
      setError('Fehler beim Laden der Portfolio-Daten: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container">Lade Daten...</div>;
  }
  
  if (error) {
    return (
      <div className="container error">
        <h2>Fehler</h2>
        <p>{error}</p>
        <button onClick={fetchPortfolioData}>Erneut versuchen</button>
      </div>
    );
  }
  
  return (
    <div className="container">
      <h1>Bitpanda Portfolio Übersicht</h1>
      
      <section className="section">
        <h2>Krypto-Wallets</h2>
        {portfolio && portfolio.crypto_wallets && portfolio.crypto_wallets.length > 0 ? (
          <>
            <div className="wallet-list">
              {portfolio.crypto_wallets.map((wallet, index) => (
                <div className="wallet-item" key={index}>
                  <div className="wallet-symbol">{wallet.symbol}</div>
                  <div className="wallet-details">
                    <div>Menge: {wallet.balance}</div>
                    <div>Preis (EUR): {wallet.price_eur}</div>
                    <div>Wert (EUR): {wallet.balance_eur}</div>
                  </div>
                </div>
              ))}
            </div>
            <div className="total">
              <strong>Gesamtwert aller Krypto-Wallets:</strong> {portfolio.total_value_eur} EUR
            </div>
          </>
        ) : (
          <p>Keine Krypto-Wallets mit Guthaben gefunden.</p>
        )}
      </section>
      
      <section className="section">
        <h2>Fiat-Wallets</h2>
        {portfolio && portfolio.fiat_wallets && portfolio.fiat_wallets.length > 0 ? (
          <div className="wallet-list">
            {portfolio.fiat_wallets.map((wallet, index) => (
              <div className="wallet-item" key={index}>
                <div className="wallet-symbol">{wallet.symbol}</div>
                <div className="wallet-details">
                  <div>{wallet.balance} {wallet.symbol}</div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>Keine Fiat-Wallets mit Guthaben gefunden.</p>
        )}
      </section>
      
      <button onClick={fetchPortfolioData} className="refresh-button">
        Daten aktualisieren
      </button>
    </div>
  );
}

export default App;
