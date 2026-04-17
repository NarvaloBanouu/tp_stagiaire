# Cet outil effectue des calculs financiers
# courants : TVA, intérêts composés, marge commerciale, et mensualités de prêt.
# Il accepte des paramètres séparés par des virgules.

import re


def _parse_float(s: str) -> float:
    """Convertit une chaîne en float en ignorant les symboles monétaires et espaces."""
    cleaned = re.sub(r'[^\d.\-]', '', s.strip())
    if not cleaned:
        raise ValueError(f"Valeur numerique manquante ou invalide : '{s.strip()}'")
    return float(cleaned)


def calculer_tva(input_str: str) -> str:
    """Calcule TVA et prix TTC. Entrée : "prix_ht,taux_tva" ex: "100,20" """
    try:
        parties = input_str.strip().split(',')
        prix_ht, taux_tva = _parse_float(parties[0]), _parse_float(parties[1])
        montant_tva = prix_ht * (taux_tva / 100)
        prix_ttc = prix_ht + montant_tva
        return f"HT: {prix_ht:.2f}€  TVA({taux_tva}%): {montant_tva:.2f}€  TTC: {prix_ttc:.2f}€"
    except Exception as e:
        return f"Erreur calculer_tva : {e}. Format attendu : 'prix_ht,taux_tva' ex '899,20'"


def calculer_interets_composes(input_str: str) -> str:
    """Intérêts composés. Entrée : "capital,taux_annuel,duree_annees" """
    try:
        c, t, n = input_str.strip().split(',')
        capital, taux, duree = _parse_float(c), _parse_float(t), int(_parse_float(n))
        capital_final = capital * ((1 + taux/100) ** duree)
        return f"Capital final : {capital_final:,.2f}€ (gain : {capital_final-capital:,.2f}€)"
    except Exception as e:
        return f"Erreur calculer_interets : {e}. Format attendu : 'capital,taux,annees' ex '10000,5,3'"


def calculer_marge(input_str: str) -> str:
    """Marge commerciale. Entrée : "prix_vente,cout_achat" ex "1200,899" """
    try:
        pv, ca = input_str.strip().split(',')
        prix_vente, cout_achat = _parse_float(pv), _parse_float(ca)
        marge = prix_vente - cout_achat
        taux_marge = (marge / cout_achat) * 100
        return f"Marge : {marge:.2f}€ | Taux de marge : {taux_marge:.1f}%"
    except Exception as e:
        return f"Erreur calculer_marge : {e}. Format attendu : 'prix_vente,cout_achat' ex '1200,899'"


def calculer_mensualite_pret(input_str: str) -> str:
    """Mensualité de prêt. Entrée : "capital,taux_annuel,duree_mois" """
    try:
        c, t, d = input_str.strip().split(',')
        K, r, n = _parse_float(c), _parse_float(t)/100/12, int(_parse_float(d))
        M = K * (r * (1+r)**n) / ((1+r)**n - 1)
        return f"Mensualité : {M:.2f}€/mois | Coût total : {M*n:,.2f}€"
    except Exception as e:
        return f"Erreur calculer_mensualite : {e}. Format attendu : 'capital,taux,mois' ex '200000,3.5,240'"
