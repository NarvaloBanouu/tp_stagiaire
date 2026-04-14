#!/usr/bin/env python3
"""
Script d'initialisation de la base de données portfolio pour D1.
Crée les tables pour les positions, prix et historiques de marché.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def init_portfolio_database():
    """Initialise la base de données portfolio.db avec données de démonstration."""

    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    # Suppression des tables existantes
    cursor.execute('DROP TABLE IF EXISTS positions')
    cursor.execute('DROP TABLE IF EXISTS market_history')

    print('[OK] Anciennes tables supprimées')

    # Table des positions (portefeuille client)
    cursor.execute('''
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL,
            symbole TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix_achat REAL NOT NULL,
            date_achat TEXT NOT NULL,
            secteur TEXT,
            risque TEXT
        )
    ''')

    # Table d'historique de marché
    cursor.execute('''
        CREATE TABLE market_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbole TEXT NOT NULL,
            date TEXT NOT NULL,
            prix_ouverture REAL,
            prix_fermeture REAL,
            prix_haut REAL,
            prix_bas REAL,
            volume INTEGER
        )
    ''')

    # Insertion de positions de démonstration
    positions = [
        ('C001', 'AAPL', 50, 150.00, '2024-01-15', 'Technologie', 'Moyen'),
        ('C001', 'MSFT', 30, 320.00, '2024-02-20', 'Technologie', 'Faible'),
        ('C001', 'TSLA', 20, 180.00, '2024-03-10', 'Automobile', 'Élevé'),
        ('C001', 'NVDA', 15, 450.00, '2024-01-05', 'Technologie', 'Élevé'),
        ('C002', 'GOOGL', 25, 140.00, '2024-02-01', 'Technologie', 'Moyen'),
        ('C002', 'AMZN', 40, 175.00, '2024-01-20', 'E-commerce', 'Moyen'),
        ('C003', 'BTC-USD', 2, 45000.00, '2023-12-15', 'Crypto', 'Très Élevé'),
        ('C003', 'ETH-USD', 10, 2500.00, '2024-01-10', 'Crypto', 'Très Élevé'),
    ]

    cursor.executemany('''
        INSERT INTO positions (client_id, symbole, quantite, prix_achat, date_achat, secteur, risque)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', positions)

    print(f'[OK] {len(positions)} positions insérées')

    # Insertion d'historique de marché (derniers 30 jours)
    symboles = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'AMZN']
    base_prices = {'AAPL': 180, 'MSFT': 380, 'TSLA': 220, 'NVDA': 520, 'GOOGL': 150, 'AMZN': 190}

    history_count = 0
    for symbole in symboles:
        base_price = base_prices[symbole]
        for i in range(30):
            date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
            # Simulation de variation de prix
            variation = random.uniform(-0.05, 0.05)
            prix_ouv = base_price * (1 + variation)
            prix_ferm = prix_ouv * (1 + random.uniform(-0.03, 0.03))
            prix_haut = max(prix_ouv, prix_ferm) * (1 + random.uniform(0, 0.02))
            prix_bas = min(prix_ouv, prix_ferm) * (1 - random.uniform(0, 0.02))
            volume = random.randint(10000000, 50000000)

            cursor.execute('''
                INSERT INTO market_history (symbole, date, prix_ouverture, prix_fermeture, prix_haut, prix_bas, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (symbole, date, prix_ouv, prix_ferm, prix_haut, prix_bas, volume))
            history_count += 1

    print(f'[OK] {history_count} entrées d\'historique insérées')

    conn.commit()
    conn.close()

    print('\n✅ Base de données portfolio.db créée avec succès')
    print('   - Table positions : portefeuille des clients')
    print('   - Table market_history : historique des cours')

if __name__ == '__main__':
    init_portfolio_database()
