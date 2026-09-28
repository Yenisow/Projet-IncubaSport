"""
app.py — IncubaSport Talent Radar
------------------------------------------------------------
Tableau de bord de détection statistique de jeunes talents du
football sénégalais, conçu pour le pitch devant le jury
FODEM / WorkingFit (programme IncubaSport).

Lancer avec :  streamlit run app.py
------------------------------------------------------------
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================
# 0. CONFIGURATION GÉNÉRALE & CHARTE VISUELLE
# ==============================================================
# NOTE IMPORTANTE (voir DOCUMENTATION.md, section "Charte graphique") :
# IncubaSport n'a pas encore publié de charte graphique officielle
# publique au moment de la création de ce projet. La palette
# ci-dessous est une proposition professionnelle inspirée du
# territoire (vert/or du Sénégal, sobriété "data/tech"), facile à
# remplacer par les vraies couleurs dès qu'elles seront fournies :
# il suffit de modifier les valeurs hexadécimales ci-dessous.

COLOR_PRIMARY = "#1E9E6E"     # vert — sport, croissance, terrain (éclairci pour ressortir sur fond sombre)
COLOR_ACCENT = "#F2A900"      # or — excellence, énergie, détection de pépites
COLOR_DARK = "#0E1B18"        # anthracite — utilisé pour le texte sur fond clair (badges, bandeau)
COLOR_BG = "#101512"          # fond sombre principal, confortable pour l'œil
COLOR_CARD = "#1B2420"        # fond des cartes, légèrement plus clair que le fond
COLOR_TEXT = "#EEF3F0"        # texte principal clair
COLOR_MUTED = "#9FB3AC"       # texte secondaire (labels, légendes)
COLOR_GRID = "rgba(238,243,240,0.10)"   # grille des graphiques, discrète sur fond sombre
COLOR_AXIS = "rgba(238,243,240,0.35)"   # lignes d'axe des graphiques

st.set_page_config(
    page_title="IncubaSport Talent Radar",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = f"""
<style>
.stApp {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
}}
[data-testid="stSidebar"] {{
    background-color: {COLOR_CARD};
}}
[data-testid="stSidebar"] * {{
    color: {COLOR_TEXT} !important;
}}
[data-testid="stMarkdownContainer"], p, li, label, span {{
    color: {COLOR_TEXT};
}}
h1, h2, h3, h4 {{
    color: {COLOR_TEXT};
    font-family: 'Segoe UI', sans-serif;
}}
.header-banner {{
    background: linear-gradient(90deg, {COLOR_DARK} 0%, {COLOR_PRIMARY} 100%);
    padding: 1.4rem 2rem;
    border-radius: 10px;
    margin-bottom: 1.4rem;
}}
.header-banner h1 {{
    color: white;
    margin: 0;
    font-size: 1.8rem;
}}
.header-banner p {{
    color: #E4EFEA;
    margin: 0.2rem 0 0 0;
    font-size: 0.95rem;
}}
.kpi-card {{
    background-color: {COLOR_CARD};
    border-radius: 10px;
    padding: 1rem 1.2rem;
    border-left: 5px solid {COLOR_ACCENT};
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}}
.kpi-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {COLOR_TEXT};
}}
.kpi-label {{
    font-size: 0.85rem;
    color: {COLOR_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}
.pepite-badge {{
    background-color: {COLOR_ACCENT};
    color: {COLOR_DARK};
    padding: 0.15rem 0.6rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================
# 1. CHARGEMENT DES DONNÉES
# ==============================================================
@st.cache_data
def charger_donnees():
    df = pd.read_csv("players_data.csv")
    return df


try:
    df = charger_donnees()
except FileNotFoundError:
    st.error(
        "Fichier players_data.csv introuvable. "
        "Exécutez d'abord `python generate_data.py` dans le même dossier que app.py."
    )
    st.stop()

SEUIL_PEPITE = df["score_potentiel"].quantile(0.90)

# ==============================================================
# 2. EN-TÊTE
# ==============================================================
st.markdown(
    """
    <div class="header-banner">
        <h1>⚽ IncubaSport Talent Radar</h1>
        <p>Plateforme d'analyse statistique et de détection des jeunes talents du football sénégalais —
        Projet incubé FODEM × WorkingFit</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================
# 3. BARRE LATÉRALE — FILTRES
# ==============================================================
st.sidebar.markdown("## 🎛️ Filtres de recherche")

age_min, age_max = int(df["age"].min()), int(df["age"].max())
f_age = st.sidebar.slider("Âge", age_min, age_max, (age_min, age_max))

f_poste = st.sidebar.multiselect(
    "Poste", options=sorted(df["poste"].unique()), default=sorted(df["poste"].unique())
)

f_academie = st.sidebar.multiselect(
    "Académie", options=sorted(df["academie"].unique()), default=sorted(df["academie"].unique())
)

f_score = st.sidebar.slider(
    "Score de potentiel minimum", 0, 100, 0,
    help="Filtre les joueurs dont le score de potentiel est au moins égal à cette valeur.",
)

if "page" not in st.session_state:
    st.session_state["page"] = "🏆 Vue Superviseur"
if "joueur_selectionne" not in st.session_state:
    st.session_state["joueur_selectionne"] = None

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "📄 Navigation",
    ["🏆 Vue Superviseur", "🔎 Fiche Joueur"],
    key="page",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Données synthétiques générées à partir de distributions statistiques réalistes "
    "par poste (voir `generate_data.py`). Ce MVP est conçu pour être reconnecté à des "
    "données réelles saisies par les encadreurs d'académies ou extraites par Computer Vision."
)

# Application des filtres
df_f = df[
    (df["age"].between(*f_age))
    & (df["poste"].isin(f_poste))
    & (df["academie"].isin(f_academie))
    & (df["score_potentiel"] >= f_score)
].copy()

if df_f.empty:
    st.warning("Aucun joueur ne correspond aux filtres sélectionnés. Élargissez vos critères.")
    st.stop()


# ==============================================================
# 4. FONCTIONS UTILITAIRES D'AFFICHAGE
# ==============================================================
def kpi_card(col, label, value):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def style_fig_sombre(fig, height=340):
    """Applique un thème sombre cohérent à un graphique Plotly (axes, grille, police lisibles)."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, size=13),
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color=COLOR_TEXT)),
    )
    fig.update_xaxes(
        gridcolor=COLOR_GRID, zerolinecolor=COLOR_GRID,
        linecolor=COLOR_AXIS, tickfont=dict(color=COLOR_TEXT),
    )
    fig.update_yaxes(
        gridcolor=COLOR_GRID, zerolinecolor=COLOR_GRID,
        linecolor=COLOR_AXIS, tickfont=dict(color=COLOR_TEXT),
    )
    return fig


def silhouette_svg(poste, taille=90):
    """Silhouette anonyme colorée par poste (aucune photo réelle utilisée)."""
    couleurs = {
        "Attaquant": COLOR_ACCENT,
        "Milieu": COLOR_PRIMARY,
        "Défenseur": "#5EA8D9",
        "Gardien": "#B07CE0",
    }
    c = couleurs.get(poste, COLOR_PRIMARY)
    return f"""
    <svg width="{taille}" height="{taille}" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" fill="{c}" opacity="0.12"/>
        <circle cx="50" cy="36" r="16" fill="{c}"/>
        <path d="M20 90 Q50 55 80 90 Z" fill="{c}"/>
    </svg>
    """


def radar_joueur(row, df_ref):
    """Radar chart comparant le joueur à la moyenne des joueurs du même poste."""
    sub = df_ref[df_ref["poste"] == row["poste"]]

    labels_base = ["Vitesse", "Passes réussies", "Duels gagnés", "Distance parcourue"]
    cols_base = ["vitesse_max_kmh", "passes_reussies_pct", "duels_gagnes_pct", "distance_moy_km"]
    label_special = row["metrique_specifique_nom"].replace("_", " ").replace(" pct", " (%)").capitalize()

    labels = labels_base + [label_special]

    def norm(col_name, valeur):
        vmin, vmax = sub[col_name].min(), sub[col_name].max()
        if vmax == vmin:
            return 50
        return 100 * (valeur - vmin) / (vmax - vmin)

    valeurs_joueur = [norm(c, row[c]) for c in cols_base]
    valeurs_joueur.append(norm("metrique_specifique_valeur", row["metrique_specifique_valeur"]))

    valeurs_moyenne = [50 for _ in labels]  # la moyenne du poste = 50 par construction (normalisation)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valeurs_moyenne + [valeurs_moyenne[0]],
        theta=labels + [labels[0]],
        name=f"Moyenne {row['poste']}s",
        line=dict(color=COLOR_MUTED, dash="dot"),
        fill=None,
    ))
    fig.add_trace(go.Scatterpolar(
        r=valeurs_joueur + [valeurs_joueur[0]],
        theta=labels + [labels[0]],
        name=row["nom"],
        line=dict(color=COLOR_ACCENT, width=3),
        fillcolor="rgba(242,169,0,0.25)",
        fill="toself",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100], showticklabels=False,
                gridcolor=COLOR_GRID, linecolor=COLOR_AXIS,
            ),
            angularaxis=dict(
                tickfont=dict(color=COLOR_TEXT, size=12),
                gridcolor=COLOR_GRID, linecolor=COLOR_AXIS,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(color=COLOR_TEXT)),
        margin=dict(l=30, r=30, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT),
        height=430,
    )
    return fig


def selectionner_joueur(nom):
    """Callback exécuté avant le rerun : peut modifier st.session_state['page']
    sans conflit avec le widget de navigation (key='page')."""
    st.session_state["joueur_selectionne"] = nom
    st.session_state["page"] = "🔎 Fiche Joueur"


# ==============================================================
# 5. PAGE — VUE SUPERVISEUR
# ==============================================================
if page == "🏆 Vue Superviseur":

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "Joueurs analysés", len(df_f))
    kpi_card(c2, "Académies couvertes", df_f["academie"].nunique())
    kpi_card(c3, "Âge moyen", f"{df_f['age'].mean():.1f} ans")
    kpi_card(c4, "Score de potentiel moyen", f"{df_f['score_potentiel'].mean():.1f}/100")

    st.markdown("### 🏅 Top 5 — Talents détectés par l'algorithme")
    top5 = df_f.sort_values("score_potentiel", ascending=False).head(5)

    for _, r in top5.iterrows():
        cols = st.columns([0.6, 2.2, 1.3, 1.3, 1.6, 1.1, 1.5])
        cols[0].markdown(silhouette_svg(r["poste"], 55), unsafe_allow_html=True)
        cols[1].markdown(f"**{r['nom']}**  \n{r['poste']} · {r['age']} ans")
        cols[2].markdown(f"📍 {r['academie'].split(' (')[0]}")
        cols[3].markdown(f"⚡ {r['vitesse_max_kmh']} km/h")
        badge = " <span class='pepite-badge'>💎 PÉPITE</span>" if r["score_potentiel"] >= SEUIL_PEPITE else ""
        cols[4].markdown(f"**Score : {r['score_potentiel']}/100**{badge}", unsafe_allow_html=True)
        cols[5].progress(min(int(r["score_potentiel"]), 100) / 100)
        cols[6].button(
            "Voir la fiche →",
            key=f"fiche_{r['id_joueur']}",
            on_click=selectionner_joueur,
            args=(r["nom"],),
        )

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Répartition des joueurs par académie")
        rep = df_f["academie"].value_counts().reset_index()
        rep.columns = ["academie", "nombre"]
        fig_bar = go.Figure(go.Bar(
            x=rep["nombre"], y=rep["academie"], orientation="h",
            marker_color=COLOR_PRIMARY,
        ))
        style_fig_sombre(fig_bar)
        fig_bar.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.markdown("#### Score de potentiel moyen par poste")
        rep2 = df_f.groupby("poste")["score_potentiel"].mean().reset_index().sort_values("score_potentiel")
        fig_bar2 = go.Figure(go.Bar(
            x=rep2["score_potentiel"], y=rep2["poste"], orientation="h",
            marker_color=COLOR_ACCENT,
        ))
        style_fig_sombre(fig_bar2)
        st.plotly_chart(fig_bar2, use_container_width=True)

    with st.expander("📋 Voir la table complète des joueurs filtrés"):
        st.dataframe(
            df_f[[
                "nom", "age", "poste", "academie", "vitesse_max_kmh",
                "passes_reussies_pct", "duels_gagnes_pct", "score_potentiel",
            ]].sort_values("score_potentiel", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

# ==============================================================
# 6. PAGE — FICHE JOUEUR
# ==============================================================
else:
    st.markdown("### 🔎 Fiche détaillée du joueur")

    noms_disponibles = df_f.sort_values("score_potentiel", ascending=False)["nom"].tolist()
    joueur_prefere = st.session_state.get("joueur_selectionne")
    index_defaut = noms_disponibles.index(joueur_prefere) if joueur_prefere in noms_disponibles else 0
    nom_choisi = st.selectbox("Sélectionner un joueur", noms_disponibles, index=index_defaut)
    row = df_f[df_f["nom"] == nom_choisi].iloc[0]

    col_photo, col_info, col_score = st.columns([1, 2.2, 1.3])

    with col_photo:
        st.markdown(silhouette_svg(row["poste"], 130), unsafe_allow_html=True)
        st.caption("Silhouette anonyme — aucune photo réelle n'est utilisée dans ce MVP.")

    with col_info:
        st.markdown(f"## {row['nom']}")
        st.markdown(f"**Poste :** {row['poste']}  \n**Âge :** {row['age']} ans")
        st.markdown(f"**Académie :** {row['academie']}")
        st.markdown(f"**Gabarit :** {row['taille_cm']} cm · {row['poids_kg']} kg")

    with col_score:
        est_pepite = row["score_potentiel"] >= SEUIL_PEPITE
        st.metric("Score de potentiel", f"{row['score_potentiel']}/100")
        if est_pepite:
            st.markdown("<span class='pepite-badge'>💎 PÉPITE DÉTECTÉE</span>", unsafe_allow_html=True)

    st.markdown("---")

    col_radar, col_stats = st.columns([1.4, 1])

    with col_radar:
        st.markdown("#### Radar de performance (vs moyenne du poste)")
        st.plotly_chart(radar_joueur(row, df), use_container_width=True)

    with col_stats:
        st.markdown("#### Statistiques brutes")
        st.markdown(f"⚡ **Vitesse de pointe :** {row['vitesse_max_kmh']} km/h")
        st.markdown(f"🏃 **Distance moyenne/match :** {row['distance_moy_km']} km")
        st.markdown(f"🎯 **Passes réussies :** {row['passes_reussies_pct']} %")
        st.markdown(f"🛡️ **Duels gagnés :** {row['duels_gagnes_pct']} %")
        if row["poste"] != "Gardien":
            st.markdown(f"⚽ **Buts sur la saison :** {row['buts_saison']}")
        label_special = row["metrique_specifique_nom"].replace("_", " ").capitalize()
        st.markdown(f"⭐ **{label_special} :** {row['metrique_specifique_valeur']}")

    st.markdown("---")
    st.caption(
        "💡 En production, cette fiche pourra être enrichie par des extraits vidéo "
        "et des heatmaps générées par Computer Vision à partir de vidéos filmées au smartphone "
        "lors des matchs d'académie (voir DOCUMENTATION.md, feuille de route technique)."
    )
