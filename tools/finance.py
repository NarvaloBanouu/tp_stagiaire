# Cet outil récupère les cours boursiers et cryptomonnaies en temps réel
# via la bibliothèque yfinance (Yahoo Finance).

import yfinance as yf

# Mapping symbole utilisateur -> (symbole Yahoo Finance, nom)
# Les actions européennes utilisent un suffixe de marché sur Yahoo Finance
ACTIONS = {
    "AAPL":  ("AAPL",  "Apple Inc."),
    "MSFT":  ("MSFT",  "Microsoft Corp."),
    "GOOGL": ("GOOGL", "Alphabet (Google)"),
    "LVMH":  ("MC.PA", "LVMH Moet Hennessy"),
    "TSLA":  ("TSLA",  "Tesla Inc."),
    "AIR":   ("AIR.PA","Airbus SE"),
}

CRYPTOS = {
    "BTC":  "Bitcoin",
    "ETH":  "Ethereum",
    "SOL":  "Solana",
    "BNB":  "BNB",
    "DOGE": "Dogecoin",
}


def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours reel d'une action via yfinance avec variation du jour et volume."""
    symbole = symbole.strip().upper()
    if symbole in ACTIONS:
        yf_symbole, nom = ACTIONS[symbole]
    else:
        yf_symbole, nom = symbole, symbole
    try:
        ticker = yf.Ticker(yf_symbole)
        info = ticker.history(period="2d")
        if info.empty:
            return f"Action '{symbole}' : donnees indisponibles ou symbole invalide."
        cours = info['Close'].iloc[-1]
        volume = info['Volume'].iloc[-1]
        if len(info) >= 2:
            cours_veille = info['Close'].iloc[-2]
            variation_pct = ((cours - cours_veille) / cours_veille) * 100
        else:
            ouverture = info['Open'].iloc[-1]
            variation_pct = ((cours - ouverture) / ouverture) * 100
        tendance = 'UP' if variation_pct >= 0 else 'DOWN'
        return f"{symbole} ({nom}) [{tendance}] : {cours:.2f} ({variation_pct:+.2f}%) | Volume : {volume:,}"
    except Exception as e:
        return f"Erreur pour '{symbole}' : {str(e)}"


def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours reel d'une cryptomonnaie via yfinance avec variation du jour et volume."""
    symbole = symbole.strip().upper()
    yf_symbole = f"{symbole}-USD"
    try:
        ticker = yf.Ticker(yf_symbole)
        info = ticker.history(period="2d")
        if info.empty:
            return f"Crypto '{symbole}' : donnees indisponibles ou symbole invalide."
        cours = info['Close'].iloc[-1]
        volume = info['Volume'].iloc[-1]
        if len(info) >= 2:
            cours_veille = info['Close'].iloc[-2]
            variation_pct = ((cours - cours_veille) / cours_veille) * 100
        else:
            ouverture = info['Open'].iloc[-1]
            variation_pct = ((cours - ouverture) / ouverture) * 100
        tendance = 'UP' if variation_pct >= 0 else 'DOWN'
        nom = CRYPTOS.get(symbole, symbole)
        return f"{symbole} ({nom}) [{tendance}] : {cours:.2f} $ ({variation_pct:+.2f}%) | Volume : {volume:,}"
    except Exception as e:
        return f"Erreur pour '{symbole}' : {str(e)}"
