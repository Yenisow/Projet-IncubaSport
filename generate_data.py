"""
generate_data.py
------------------------------------------------------------
Génère un jeu de données synthétique mais RÉALISTE de jeunes
footballeurs évoluant dans des académies de formation à Dakar
et dans la région (Mbour, Thiès, Saint-Louis, Diourbel).

Les statistiques ne sont pas tirées au hasard : elles suivent
des lois normales (gaussiennes) dont la moyenne et l'écart-type
sont différents selon le POSTE du joueur, ce qui reproduit la
réalité du terrain (un attaquant marque plus de buts qu'un
défenseur, un milieu fait plus de passes, etc.).

Quelques "pépites" (outliers positifs) sont injectées
volontairement pour simuler les jeunes talents hors normes que
le projet a justement pour mission de détecter.

Sortie : players_data.csv (utilisé par app.py)
------------------------------------------------------------
"""

import numpy as np
import pandas as pd

# ------------------------------------------------------------------
# Reproductibilité : toujours le même jeu de données à chaque exécution
# ------------------------------------------------------------------
RNG = np.random.default_rng(seed=42)

N_JOUEURS = 180

ACADEMIES = [
    "Génération Foot (Dakar)",
    "Diambars (Saly)",
    "Aspire Academy Dakar",
    "AS Pikine Formation",
    "Académie Mbour Sport",
    "Thiès Foot Élite",
    "Saint-Louis Jeunes Talents",
    "Diourbel Espoir Foot",
]

POSTES = ["Attaquant", "Milieu", "Défenseur", "Gardien"]

PRENOMS = [
    "Mamadou", "Ousmane", "Ibrahima", "Cheikh", "Moussa", "Abdoulaye",
    "Modou", "Alioune", "Pape", "Babacar", "Amadou", "Serigne",
    "El Hadji", "Souleymane", "Mor", "Lamine", "Youssou", "Assane",
    "Boubacar", "Aliou", "Idrissa", "Saliou", "Malick", "Fallou",
]

NOMS = [
    "Diop", "Ndiaye", "Fall", "Sarr", "Gueye", "Diallo", "Sow", "Ba",
    "Diouf", "Faye", "Sy", "Kane", "Mbaye", "Cissé", "Niang", "Thiam",
    "Sene", "Ndoye", "Camara", "Toure", "Diagne", "Seck", "Wade", "Lo",
]

# ------------------------------------------------------------------
# Paramètres statistiques (moyenne, écart-type) PAR POSTE
# Bornes = min / max plausibles pour éviter les valeurs aberrantes
# irréalistes (ex : 130% de passes réussies)
# ------------------------------------------------------------------
PARAMS = {
    "Attaquant": {
        "vitesse_kmh":        (32.0, 2.0, 26, 37),
        "distance_km":        (8.5, 0.8, 6.5, 10.5),
        "passes_reussies_pct":(72, 6, 55, 90),
        "duels_gagnes_pct":   (55, 8, 35, 80),
        "buts_saison":        (9, 4, 0, 22),
        "tirs_cadres_pct":    (48, 8, 25, 75),
    },
    "Milieu": {
        "vitesse_kmh":        (29.5, 1.8, 24, 34),
        "distance_km":        (10.8, 0.9, 8.5, 13.0),
        "passes_reussies_pct":(80, 6, 60, 95),
        "duels_gagnes_pct":   (58, 7, 38, 82),
        "buts_saison":        (3, 2, 0, 12),
        "tirs_cadres_pct":    (40, 10, 15, 70),
    },
    "Défenseur": {
        "vitesse_kmh":        (28.5, 1.7, 23, 33),
        "distance_km":        (9.8, 0.8, 7.5, 12.0),
        "passes_reussies_pct":(78, 6, 58, 93),
        "duels_gagnes_pct":   (64, 7, 42, 88),
        "buts_saison":        (1, 1, 0, 6),
        "tirs_cadres_pct":    (35, 12, 10, 70),
    },
    "Gardien": {
        "vitesse_kmh":        (25.0, 1.5, 20, 29),
        "distance_km":        (5.5, 0.6, 4.0, 7.0),
        "passes_reussies_pct":(68, 8, 45, 90),
        "duels_gagnes_pct":   (60, 9, 35, 85),
        "buts_saison":        (0, 0, 0, 0),
        "tirs_cadres_pct":    (0, 0, 0, 0),
    },
}

# Métriques spécifiques au poste (utilisées pour le radar)
METRIQUE_SPECIALE = {
    "Attaquant":  ("efficacite_finition_pct", 38, 9, 15, 70),
    "Milieu":     ("interceptions_par_match", 2.6, 0.9, 0.5, 5.5),
    "Défenseur":  ("tacles_reussis_pct", 70, 8, 45, 92),
    "Gardien":    ("arrets_pct", 68, 8, 45, 90),
}


def tirage_borne(moyenne, ecart_type, borne_min, borne_max, n=1):
    """Tire des valeurs dans une loi normale, tronquées à des bornes réalistes."""
    valeurs = RNG.normal(moyenne, ecart_type, n)
    return np.clip(valeurs, borne_min, borne_max)


def genere_joueurs(n=N_JOUEURS):
    lignes = []
    noms_utilises = set()

    for i in range(n):
        poste = RNG.choice(POSTES, p=[0.28, 0.30, 0.30, 0.12])
        age = int(np.clip(RNG.normal(17, 1.2), 15, 19))
        academie = RNG.choice(ACADEMIES)

        # Nom unique
        while True:
            nom_complet = f"{RNG.choice(PRENOMS)} {RNG.choice(NOMS)}"
            if nom_complet not in noms_utilises:
                noms_utilises.add(nom_complet)
                break

        p = PARAMS[poste]
        vitesse = tirage_borne(*p["vitesse_kmh"])[0]
        distance = tirage_borne(*p["distance_km"])[0]
        passes = tirage_borne(*p["passes_reussies_pct"])[0]
        duels = tirage_borne(*p["duels_gagnes_pct"])[0]
        buts = tirage_borne(*p["buts_saison"])[0]
        tirs_cadres = tirage_borne(*p["tirs_cadres_pct"])[0]

        nom_metrique, m_moy, m_std, m_min, m_max = METRIQUE_SPECIALE[poste]
        val_metrique = tirage_borne(m_moy, m_std, m_min, m_max)[0]

        taille = int(np.clip(RNG.normal(176 if poste != "Gardien" else 183, 6), 160, 198))
        poids = round(np.clip(RNG.normal(0.42 * taille - 4, 3), 52, 88), 1)

        ligne = {
            "id_joueur": f"IS-{i+1:03d}",
            "nom": nom_complet,
            "age": age,
            "poste": poste,
            "academie": academie,
            "taille_cm": taille,
            "poids_kg": poids,
            "vitesse_max_kmh": round(vitesse, 1),
            "distance_moy_km": round(distance, 2),
            "passes_reussies_pct": round(passes, 1),
            "duels_gagnes_pct": round(duels, 1),
            "buts_saison": int(round(buts)),
            "tirs_cadres_pct": round(tirs_cadres, 1),
            "metrique_specifique_nom": nom_metrique,
            "metrique_specifique_valeur": round(val_metrique, 1),
        }
        lignes.append(ligne)

    df = pd.DataFrame(lignes)

    # ----------------------------------------------------------------
    # Injection volontaire de quelques "pépites" (talents exceptionnels)
    # -> outliers positifs cohérents, pas du bruit aléatoire
    # ----------------------------------------------------------------
    idx_pepites = RNG.choice(df.index, size=7, replace=False)
    for idx in idx_pepites:
        df.loc[idx, "vitesse_max_kmh"] = round(df.loc[idx, "vitesse_max_kmh"] * RNG.uniform(1.10, 1.18), 1)
        df.loc[idx, "duels_gagnes_pct"] = round(min(96, df.loc[idx, "duels_gagnes_pct"] * RNG.uniform(1.08, 1.15)), 1)
        df.loc[idx, "passes_reussies_pct"] = round(min(97, df.loc[idx, "passes_reussies_pct"] * RNG.uniform(1.05, 1.10)), 1)
        df.loc[idx, "metrique_specifique_valeur"] = round(
            df.loc[idx, "metrique_specifique_valeur"] * RNG.uniform(1.10, 1.20), 1
        )

    # ----------------------------------------------------------------
    # Score de potentiel (0-100) : moyenne pondérée normalisée par poste
    # Pondération pensée pour rester crédible devant un jury technique :
    # vitesse 20%, passes 20%, duels 20%, métrique spécifique au poste 30%,
    # discipline/forme physique (âge optimal 16-18) 10%
    # ----------------------------------------------------------------
    def score_potentiel(row):
        sub = df[df["poste"] == row["poste"]]

        def normalise(valeur, serie):
            vmin, vmax = serie.min(), serie.max()
            if vmax == vmin:
                return 50.0
            return 100 * (valeur - vmin) / (vmax - vmin)

        s_vitesse = normalise(row["vitesse_max_kmh"], sub["vitesse_max_kmh"])
        s_passes = normalise(row["passes_reussies_pct"], sub["passes_reussies_pct"])
        s_duels = normalise(row["duels_gagnes_pct"], sub["duels_gagnes_pct"])
        s_metrique = normalise(row["metrique_specifique_valeur"], sub["metrique_specifique_valeur"])
        s_age = 100 - abs(row["age"] - 17) * 15  # pic à 17 ans, dégressif

        score = (
            0.20 * s_vitesse
            + 0.20 * s_passes
            + 0.20 * s_duels
            + 0.30 * s_metrique
            + 0.10 * max(s_age, 0)
        )
        return round(np.clip(score, 0, 100), 1)

    df["score_potentiel"] = df.apply(score_potentiel, axis=1)
    df = df.sort_values("score_potentiel", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = genere_joueurs()
    df.to_csv("players_data.csv", index=False, encoding="utf-8-sig")
    print(f"✅ {len(df)} joueurs générés -> players_data.csv")
    print(df[["nom", "poste", "academie", "score_potentiel"]].head(10).to_string(index=False))
