
# Bitpanda Portfolio Tracker  <img src="https://play-lh.googleusercontent.com/6Szd6rn27xvFo0-iEQbzEUirgIbST1OLsQXJb5U5rphR7nLsNtZ2QrhQs_OjbxEjCg" alt="Bildbeschreibung" width="24" style="border-radius: 50%; overflow: hidden;" />




A lightweight Python application that connects to your Bitpanda account via the official API to provide a comprehensive overview of your crypto and fiat assets.

## ✨ Features

- 🔐 Secure API key management using environment variables
- 💰 Display all your crypto wallets with current balance
- 💱 Calculate real-time EUR value of your crypto assets
- 💵 View your fiat wallet balances
- 📈 Calculate total portfolio value

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- A Bitpanda account with API access

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bitpanda-portfolio-tracker.git
   cd bitpanda-portfolio-tracker
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Bitpanda API key:
   ```
   API_KEY=your_api_key_here
   ```

### Usage

Simply run the main script:

```
python main.py
```

The script will:
1. Connect to your Bitpanda account
2. Fetch your wallet information
3. Display a detailed overview of your portfolio with the current EUR values

## 📝 Example Output

```
API-Schlüssel erfolgreich geladen!
Abfrage von asset_wallets mit Endpunkt /wallets...
Erfolgreich abgerufen: asset_wallets
Abfrage von fiat_wallets mit Endpunkt /fiatwallets...
Erfolgreich abgerufen: fiat_wallets
Abfrage von ticker mit Endpunkt /ticker...
Erfolgreich abgerufen: ticker


==== Bitpanda Portfolio Übersicht ====

Krypto-Wallets:

Aktualisiere Preisdaten...

  BTC: 0.01231241 (432.98 EUR)
  ETH: 0.43214321 (987.65 EUR)
  XRP: 321.32132100 (123.45 EUR)

  Gesamtwert aller Krypto-Wallets: 1544.08 EUR

Fiat-Wallets:
  EUR: 250.00 EUR
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Store your API key securely
- Consider using read-only API keys when possible

## 📦 Dependencies

- [python-dotenv](https://github.com/theskumar/python-dotenv) - For loading environment variables
- [requests](https://docs.python-requests.org/en/master/) - For making API calls

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/knutpfr/bitpanda-portfolio-tracker/issues).

---

*This project is not affiliated with, maintained, authorized, endorsed, or sponsored by Bitpanda GmbH.*
