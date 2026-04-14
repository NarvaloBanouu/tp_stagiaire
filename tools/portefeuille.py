
import yfinance as yf


def calculer_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur d'un portefeuille d'actions.
    Entrée : "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE|..."
    Exemple : "AAPL:10|MSFT:5|TSLA:3"
    """
    try:
        positions = input_str.strip().split('|')
        valeur_totale = 0
        variation_totale = 0
        lignes = []

        for position in positions:
            symbole, quantite = position.split(':')
            symbole = symbole.strip().upper()
            quantite = int(quantite.strip())

            ticker = yf.Ticker(symbole)
            info = ticker.history(period="1d")

            if info.empty:
                lignes.append(f"  [WARN] {symbole} : données indisponibles")
                continue

            cours = info['Close'].iloc[-1]
            ouverture = info['Open'].iloc[-1]
            variation_pct = ((cours - ouverture) / ouverture) * 100
            valeur_ligne = cours * quantite

            valeur_totale += valeur_ligne
            variation_totale += valeur_ligne * (variation_pct / 100)

            tendance = 'UP' if variation_pct >= 0 else 'DOWN'
            lignes.append(
                f"  [{tendance}] {symbole} x{quantite} : {cours:.2f} $ = {valeur_ligne:,.2f} $ ({variation_pct:+.2f}%)"
            )

        variation_globale_pct = (variation_totale / valeur_totale * 100) if valeur_totale > 0 else 0
        tendance_globale = 'UP' if variation_globale_pct >= 0 else 'DOWN'

        result = "=== PORTEFEUILLE ===\n"
        result += '\n'.join(lignes)
        result += f"\n\n[{tendance_globale}] Valeur totale : {valeur_totale:,.2f} $"
        result += f"\n[{tendance_globale}] Variation du jour : {variation_totale:+,.2f} $ ({variation_globale_pct:+.2f}%)"

        return result

    except Exception as e:
        return f"Erreur lors du calcul du portefeuille : {str(e)}"
