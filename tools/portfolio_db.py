import sqlite3

def get_portfolio_connection():
    return sqlite3.connect('portfolio.db')

def analyser_risques_portefeuille(client_id: str = 'C001') -> str:
    try:
        conn = get_portfolio_connection()
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

        result = f"📊 Analyse de risque du portefeuille {client_id}:\n\n"

        for symbole, qty, prix, secteur, risque in positions:
            valeur_achat = qty * prix
            emoji = {'Très Élevé': '🔴', 'Élevé': '🟠', 'Moyen': '🟡', 'Faible': '🟢'}.get(risque, '⚪')
            result += f"{emoji} {symbole} ({secteur}) - Risque: {risque}\n"
            result += f"   Quantité: {qty} | Prix d'achat: {prix:.2f}$ | Valeur: {valeur_achat:,.2f}$\n\n"

        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def obtenir_positions_client(client_id: str = 'C001') -> str:
    try:
        conn = get_portfolio_connection()
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

        result = f"💼 Portefeuille du client {client_id}:\n\n"
        total = 0

        for symbole, qty, prix, date, secteur in positions:
            valeur = qty * prix
            total += valeur
            result += f"• {symbole} ({secteur})\n"
            result += f"  Quantité: {qty} | Achat: {prix:.2f}$ le {date} | Valeur: {valeur:,.2f}$\n\n"

        result += f"💰 Valeur totale d'achat: {total:,.2f}$"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def analyser_secteurs_portefeuille(client_id: str = 'C001') -> str:
    try:
        conn = get_portfolio_connection()
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
        result = f"📈 Répartition sectorielle du portefeuille {client_id}:\n\n"

        for secteur, valeur, nb in secteurs:
            pct = (valeur / total) * 100
            result += f"• {secteur}: {valeur:,.2f}$ ({pct:.1f}%) - {nb} position(s)\n"

        result += f"\n💰 Valeur totale: {total:,.2f}$"
        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"


def obtenir_historique_symbole(symbole: str) -> str:
    try:
        conn = get_portfolio_connection()
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

        result = f"📊 Historique de {symbole} (7 derniers jours):\n\n"

        for date, ouv, ferm, haut, bas, vol in history:
            variation = ((ferm - ouv) / ouv) * 100
            emoji = '📈' if variation >= 0 else '📉'
            result += f"{emoji} {date}: {ferm:.2f}$ ({variation:+.2f}%)\n"
            result += f"   Haut: {haut:.2f}$ | Bas: {bas:.2f}$ | Volume: {vol:,}\n\n"

        return result

    except sqlite3.Error as e:
        return f"Erreur base de données: {str(e)}"
