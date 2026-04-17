
import sqlite3
import os
import yfinance as yf

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'portfolio.db')


def _get_connection():
    return sqlite3.connect(DB_PATH)


# B1 — Calcul de portefeuille en temps réel via yfinance

def calculer_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur d'un portefeuille d'actions en temps réel.
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
            info = ticker.history(period="2d")

            if info.empty:
                lignes.append(f"  [WARN] {symbole} : données indisponibles")
                continue

            cours = info['Close'].iloc[-1]
            if len(info) >= 2:
                cours_veille = info['Close'].iloc[-2]
                variation_pct = ((cours - cours_veille) / cours_veille) * 100
            else:
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


# D1 — Analyse du portefeuille depuis la base de données portfolio.db

def analyser_risques_portefeuille(client_id: str = 'C001') -> str:
    """Analyse les actifs les plus risqués du portefeuille d'un client. Entrée : client_id ex 'C001'."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symbole, quantite, prix_achat, secteur, risque
            FROM positions
            WHERE client_id = ?
            ORDER BY
                CASE risque
                    WHEN 'Très Élevé' THEN 1
                    WHEN 'Élevé' THEN 2
                    WHEN 'Moyen' THEN 3
                    WHEN 'Faible' THEN 4
                END
        ''', (client_id,))
        positions = cursor.fetchall()
        conn.close()

        if not positions:
            return f"Aucune position trouvée pour le client {client_id}"

        result = f"Analyse de risque du portefeuille {client_id}:\n\n"
        for symbole, qty, prix, secteur, risque in positions:
            valeur_achat = qty * prix
            niveau = {'Très Élevé': '[!!!]', 'Élevé': '[!!]', 'Moyen': '[!]', 'Faible': '[ok]'}.get(risque, '[?]')
            result += f"{niveau} {symbole} ({secteur}) - Risque: {risque}\n"
            result += f"   Quantité: {qty} | Prix d'achat: {prix:.2f}$ | Valeur: {valeur_achat:,.2f}$\n\n"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def obtenir_positions_client(client_id: str = 'C001') -> str:
    """Retourne toutes les positions d'un client avec détails. Entrée : client_id ex 'C001'."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symbole, quantite, prix_achat, date_achat, secteur
            FROM positions
            WHERE client_id = ?
        ''', (client_id,))
        positions = cursor.fetchall()
        conn.close()

        if not positions:
            return f"Aucune position pour le client {client_id}"

        result = f"Portefeuille du client {client_id}:\n\n"
        total = 0
        for symbole, qty, prix, date, secteur in positions:
            valeur = qty * prix
            total += valeur
            result += f"• {symbole} ({secteur})\n"
            result += f"  Quantité: {qty} | Achat: {prix:.2f}$ le {date} | Valeur: {valeur:,.2f}$\n\n"
        result += f"Valeur totale d'achat: {total:,.2f}$"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def analyser_secteurs_portefeuille(client_id: str = 'C001') -> str:
    """Analyse la répartition par secteur du portefeuille. Entrée : client_id ex 'C001'."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT secteur, SUM(quantite * prix_achat) as valeur, COUNT(*) as nb_positions
            FROM positions
            WHERE client_id = ?
            GROUP BY secteur
            ORDER BY valeur DESC
        ''', (client_id,))
        secteurs = cursor.fetchall()
        conn.close()

        if not secteurs:
            return f"Aucune position pour le client {client_id}"

        total = sum(s[1] for s in secteurs)
        result = f"Répartition sectorielle du portefeuille {client_id}:\n\n"
        for secteur, valeur, nb in secteurs:
            pct = (valeur / total) * 100
            result += f"• {secteur}: {valeur:,.2f}$ ({pct:.1f}%) - {nb} position(s)\n"
        result += f"\nValeur totale: {total:,.2f}$"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def obtenir_historique_symbole(symbole: str) -> str:
    """Historique des 7 derniers jours d'un symbole. Entrée : symbole ex 'AAPL'."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, prix_ouverture, prix_fermeture, prix_haut, prix_bas, volume
            FROM market_history
            WHERE symbole = ?
            ORDER BY date DESC
            LIMIT 7
        ''', (symbole.upper(),))
        history = cursor.fetchall()
        conn.close()

        if not history:
            return f"Aucun historique trouvé pour {symbole}"

        result = f"Historique de {symbole} (7 derniers jours):\n\n"
        for date, ouv, ferm, haut, bas, vol in history:
            variation = ((ferm - ouv) / ouv) * 100
            tendance = 'UP' if variation >= 0 else 'DOWN'
            result += f"[{tendance}] {date}: {ferm:.2f}$ ({variation:+.2f}%)\n"
            result += f"   Haut: {haut:.2f}$ | Bas: {bas:.2f}$ | Volume: {vol:,}\n\n"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"
