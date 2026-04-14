
import sqlite3
import os

DB_PATH = 'database.db'


def _get_connection():
    """Retourne une connexion à la base de données."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Base de données '{DB_PATH}' introuvable. "
            "Exécutez 'python init_db.py' pour la créer."
        )
    return sqlite3.connect(DB_PATH)


def rechercher_client(query: str) -> str:
    """Recherche un client par nom ou par identifiant."""
    query = query.strip()
    conn = _get_connection()
    cursor = conn.cursor()

    # Recherche par ID
    cursor.execute('SELECT * FROM clients WHERE id = ?', (query.upper(),))
    result = cursor.fetchone()

    # Si pas trouvé, recherche par nom
    if not result:
        cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', (f'%{query}%',))
        result = cursor.fetchone()

    conn.close()

    if result:
        return f"Client : {result[1]} | Solde : {result[4]:.2f} EUR | Type de compte : {result[5]}"
    return f"Aucun client trouvé pour : '{query}'"


def rechercher_produit(query: str) -> str:
    """Recherche un produit par nom ou identifiant. Retourne prix HT, TVA, prix TTC, stock."""
    query = query.strip()
    conn = _get_connection()
    cursor = conn.cursor()

    # Recherche par ID
    cursor.execute('SELECT * FROM produits WHERE id = ?', (query.upper(),))
    result = cursor.fetchone()

    # Si pas trouvé, recherche par nom
    if not result:
        cursor.execute('SELECT * FROM produits WHERE nom LIKE ?', (f'%{query}%',))
        result = cursor.fetchone()

    conn.close()

    if result:
        tva = result[2] * 0.20
        prix_ttc = result[2] + tva
        return (f"Produit : {result[1]} | Prix HT : {result[2]:.2f} EUR "
                f"| TVA : {tva:.2f} EUR | Prix TTC : {prix_ttc:.2f} EUR | Stock : {result[3]}")
    return f"Aucun produit trouvé pour : '{query}'"


def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom, type_compte, solde_compte FROM clients')
    results = cursor.fetchall()
    conn.close()

    result = "Liste des clients :\n"
    for row in results:
        result += f"  {row[0]} : {row[1]} | {row[2]} | Solde : {row[3]:.2f} EUR\n"
    return result


