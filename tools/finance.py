import yfinance as yf

def obtenir_cours_action(symbole: str) -> str:
    try:
        symbole = symbole.strip().upper()
        ticker = yf.Ticker(symbole)
        info = ticker.history(period="1d")

        if info.empty:
            return f"Action '{symbole}' non trouvée ou données indisponibles."

        cours = info['Close'].iloc[-1]
        ouverture = info['Open'].iloc[-1]
        variation_pct = ((cours - ouverture) / ouverture) * 100
        volume = info['Volume'].iloc[-1]

        tendance = 'UP' if variation_pct >= 0 else 'DOWN'
        return f"{symbole} [{tendance}] : {cours:.2f} $ ({variation_pct:+.2f}%) | Volume : {volume:,.0f}"
    except Exception as e:
        return f"Erreur lors de la récupération de {symbole} : {str(e)}"


def obtenir_cours_crypto(symbole: str) -> str:
    try:
        symbole = symbole.strip().upper()
        ticker_symbol = f"{symbole}-USD"
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.history(period="1d")

        if info.empty:
            return f"Crypto '{symbole}' non trouvée ou données indisponibles."

        cours = info['Close'].iloc[-1]
        ouverture = info['Open'].iloc[-1]
        variation_pct = ((cours - ouverture) / ouverture) * 100
        volume = info['Volume'].iloc[-1]

        tendance = 'UP' if variation_pct >= 0 else 'DOWN'
        return f"{symbole} [{tendance}] : {cours:.2f} $ ({variation_pct:+.2f}%) | Volume : {volume:,.0f}"
    except Exception as e:
        return f"Erreur lors de la récupération de {symbole} : {str(e)}"
















