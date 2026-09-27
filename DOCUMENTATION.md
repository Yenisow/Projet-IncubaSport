# IncubaSport Talent Radar
### Documentation de projet — préparation du pitch devant le jury FODEM × WorkingFit

---

## 1. Résumé du projet

**IncubaSport Talent Radar** est une plateforme d'analyse statistique et de détection
des jeunes talents du football sénégalais. Elle remplace le recrutement "à l'œil" par
un tableau de bord objectif qui croise des métriques physiques et techniques pour
faire émerger, dès la formation en académie, les joueurs à fort potentiel.

Ce dossier contient :

| Fichier | Rôle |
|---|---|
| `generate_data.py` | Génère le jeu de données synthétique (180 joueurs) |
| `players_data.csv` | Données prêtes à l'emploi (déjà générées) |
| `app.py` | Le tableau de bord Streamlit |
| `requirements.txt` | Dépendances Python à installer |
| `DOCUMENTATION.md` | Ce document |

---

## 2. Le pitch (structure recommandée, 3 à 5 minutes)

### 2.1 Le problème (l'accroche — 30 secondes)
> « Le football africain regorge de talents bruts. Mais chaque année, des jeunes
> passent sous le radar parce qu'aucune donnée objective ne permet de les comparer
> ou de les repérer à distance. Le recrutement se fait encore à l'œil, ce qui coûte
> cher aux clubs et laisse des jeunes sur le carreau. »

Points à appuyer :
- L'Afrique forme des talents (Sadio Mané, Kalidou Koulibaly...) mais l'essentiel de
  la détection reste informelle, locale, dépendante du réseau d'un recruteur.
- Les académies dakaroises et régionales n'ont aujourd'hui aucun outil pour
  objectiver et faire connaître le niveau de leurs jeunes.

### 2.2 La solution (1 minute)
Une plateforme qui **standardise l'évaluation** : au lieu de regarder des matchs
entiers, un recruteur ou un responsable d'académie consulte un tableau de bord qui
croise vitesse, endurance, passes, duels et une métrique clé propre à chaque poste,
et en tire un **score de potentiel sur 100**.

→ Montrer ici la **Vue Superviseur** (top 5 talents) puis une **Fiche Joueur** avec
son radar de performance. C'est le moment le plus visuel du pitch : ne pas se
précipiter, laisser le jury regarder le radar.

### 2.3 La faisabilité technique (votre "super-pouvoir" — 1 minute)
C'est le point le plus important pour un jury FODEM/WorkingFit : montrer que vous
n'avez besoin de sous-traiter aucune brique technique.

À dire explicitement :
- « J'ai conçu et codé l'intégralité de la chaîne : la modélisation des données, le
  calcul du score de potentiel, et le tableau de bord interactif que vous avez sous
  les yeux. »
- Citer vos outils avec assurance : **Python, Pandas, Streamlit, Plotly** — et, si on
  vous demande la suite, **SQL** pour industrialiser le stockage et **Power BI** pour
  un reporting destiné aux dirigeants d'académies non-techniques.
- Rappeler votre profil : Data Analyst, 3 ans d'expérience SQL/Python/Power BI,
  Master Big Data & Data Stratégie — c'est la preuve que le socle technique est déjà
  solide, pas un pari.

### 2.4 Le modèle économique (1 minute)
Trois flux de revenus complémentaires, à présenter du plus accessible au plus
ambitieux :

1. **Abonnement SaaS pour les académies locales** (formule d'entrée) : suivi de leurs
   propres joueurs, alertes de progression, export de rapports pour les parents et
   sponsors.
2. **Vente de rapports de détection** aux clubs nord-africains et européens en quête
   de jeunes joueurs à fort potentiel et à coût d'acquisition maîtrisé.
3. **Partenariats institutionnels** avec les fédérations et ligues régionales pour
   standardiser l'évaluation des jeunes à l'échelle nationale, voire sous-régionale.

### 2.5 Conclusion (30 secondes)
Revenir sur la mission d'IncubaSport : « Ce projet répond exactement à l'ambition du
programme — faire du sport un levier de création d'emplois et d'innovation, en
structurant une filière encore artisanale grâce à la donnée. »

---

## 3. La question piège : « Où allez-vous trouver vos chiffres ? »

Le jury sait que la donnée manque dans le football de formation africain,
contrairement aux championnats européens. **Ne pas éluder la question** — au
contraire, l'anticiper renforce votre crédibilité.

**Réponse structurée en deux temps (stratégie hybride) :**

**Phase 1 — Court terme, collecte humaine simplifiée**
Une application de saisie simple (type formulaire) permettant aux encadreurs des
académies dakaroises d'entrer, après chaque match, les statistiques de base de leurs
joueurs (buts, passes, distance estimée, etc.). Faible barrière technique, adoption
rapide, coût de mise en œuvre minimal.

**Phase 2 — Moyen terme, Computer Vision**
Des outils de vision par ordinateur capables d'extraire automatiquement des
métriques (distance parcourue, vitesse de pointe, heatmaps de placement) à partir de
simples vidéos de matchs filmées au smartphone par les encadreurs. Cela supprime la
saisie manuelle et fiabilise la donnée.

**Phrase de transition à retenir pour le jury :**
> « Le MVP que vous voyez aujourd'hui tourne sur des données synthétiques
> statistiquement réalistes, précisément pour valider l'outil de restitution avant
> d'investir dans la collecte terrain — c'est une démarche produit classique : on
> prouve la valeur de la restitution avant d'industrialiser la collecte. »

---

## 4. Anticipation des questions du jury (Q&A)

| Question probable | Angle de réponse |
|---|---|
| Vos données sont-elles réelles ? | Non, assumé et expliqué : distributions statistiques réalistes par poste (voir §6), pour valider le produit avant la phase de collecte terrain. |
| Comment garantissez-vous la qualité de la saisie manuelle par les encadreurs ? | Formulaire guidé et contraint (listes déroulantes, bornes de valeurs), formation courte des encadreurs, contrôle de cohérence automatique. |
| Combien de temps avant un vrai MVP avec données réelles ? | Phase 1 (formulaire de saisie) déployable en quelques semaines avec 2-3 académies pilotes ; Phase 2 (Computer Vision) en R&D à 6-12 mois. |
| Quelle est la taille du marché ? | Volume de jeunes en formation dans les académies dakaroises et régionales + demande naissante des clubs nord-africains/européens pour des viviers à bas coût. |
| Pourquoi vous et pas un club qui ferait ça en interne ? | Neutralité et mutualisation : un club seul n'a ni les compétences data internes ni l'intérêt à standardiser un outil ouvert à tout un écosystème. |
| Quelle est la barrière à l'entrée pour un concurrent ? | La donnée collectée dans la durée (effet réseau avec les académies) + le score propriétaire calibré au fil du temps. |

---

## 5. Le tableau de bord : guide d'utilisation

### 5.1 Installation

```bash
pip install -r requirements.txt
python generate_data.py      # régénère players_data.csv si besoin
streamlit run app.py
```

Le tableau de bord s'ouvre automatiquement dans le navigateur (généralement sur
`http://localhost:8501`).

### 5.2 Structure de l'application

**Barre latérale (filtres, toujours visible) :**
- Âge (curseur double)
- Poste (Attaquant / Milieu / Défenseur / Gardien)
- Académie
- Score de potentiel minimum

**Page 1 — Vue Superviseur** (page d'accueil)
- 4 indicateurs clés (nombre de joueurs, académies couvertes, âge moyen, score
  moyen)
- Top 5 des talents détectés, avec badge **💎 PÉPITE** pour les joueurs du 90ᵉ
  centile de score
- Deux graphiques : répartition par académie, score moyen par poste
- Table complète exportable/consultable en un clic (`st.dataframe`)

**Page 2 — Fiche Joueur**
- Sélection d'un joueur dans la liste filtrée
- Silhouette anonyme colorée par poste (aucune photo réelle n'est utilisée — voir
  §7 sur ce choix assumé)
- Radar de performance comparant le joueur à la **moyenne des joueurs de son
  poste** sur 5 axes : vitesse, passes réussies, duels gagnés, distance parcourue,
  et une métrique spécifique au poste (finition pour les attaquants, interceptions
  pour les milieux, tacles pour les défenseurs, arrêts pour les gardiens)
- Statistiques brutes détaillées

### 5.3 Conseils pour la démonstration live devant le jury
- Ouvrez l'application **avant** le début du pitch pour éviter tout temps de
  chargement à l'écran.
- Préparez à l'avance le nom d'un joueur "pépite" que vous montrerez en Fiche
  Joueur (repérable via le badge sur la Vue Superviseur).
- Filtrez en direct sur une académie ("Diambars (Saly)" par exemple) pour montrer
  la réactivité du filtre — c'est un bon moyen de prouver l'interactivité sans
  improviser une navigation complexe.
- Gardez la Vue Superviseur comme écran d'ouverture et de clôture de la démo.

---

## 6. Méthodologie de génération des données synthétiques

Pour rester crédible devant un jury technique, les données ne sont **pas
aléatoires** : elles suivent des lois normales dont la moyenne et l'écart-type
varient **par poste**, avec des bornes réalistes (ex : un taux de passes réussies
ne peut pas dépasser 97 %).

- **180 joueurs** répartis sur 8 académies (Dakar, Mbour/Saly, Thiès, Saint-Louis,
  Diourbel)
- Paramètres différenciés par poste pour : vitesse de pointe, distance parcourue,
  passes réussies, duels gagnés, buts, tirs cadrés, et une métrique spécifique au
  poste
- **7 "pépites"** injectées volontairement : des outliers positifs cohérents
  (vitesse, duels et métrique spécifique surélevés de 8 à 20 %), pour simuler les
  jeunes talents hors normes que l'algorithme doit précisément mettre en avant
- **Score de potentiel** calculé par une moyenne pondérée normalisée par poste :
  vitesse (20 %), passes (20 %), duels (20 %), métrique spécifique au poste
  (30 %), proximité de l'âge optimal 17 ans (10 %)

Le détail des formules est commenté directement dans `generate_data.py`.

---

## 7. Choix assumés à mentionner si le jury interroge dessus

- **Silhouettes anonymes plutôt que photos** : choix délibéré à ce stade de MVP,
  pour ne pas manipuler d'images de personnes réelles ou générées par IA sans
  cadre de consentement clair — un vrai sujet à traiter en production (droit à
  l'image des mineurs notamment, puisque les joueurs ont 15-19 ans).
- **Score de potentiel normalisé par poste** plutôt qu'un score unique toutes
  positions confondues : un gardien et un attaquant n'ont pas les mêmes métriques
  de référence, comparer leurs valeurs brutes n'aurait pas de sens.

---

## 8. Charte graphique du tableau de bord

Au moment de la création de ce projet, IncubaSport (lancé le 20 août 2026) ne
disposait pas encore d'une charte graphique publique officiellement diffusée. Le
tableau de bord utilise donc une palette professionnelle **proposée par défaut** :

| Couleur | Hex | Usage |
|---|---|---|
| Vert profond | `#0B6E4F` | Couleur principale (bandeau, graphiques) |
| Or | `#F2A900` | Accent (mise en valeur, badge "pépite") |
| Anthracite | `#0E1B18` | Barre latérale, texte fort |
| Fond clair | `#F7F9F8` | Fond de page |

**Pour appliquer la vraie charte IncubaSport** dès qu'elle vous sera communiquée
(ou si vous récupérez le logo/les couleurs officielles) : il suffit de modifier les
quatre constantes `COLOR_PRIMARY`, `COLOR_ACCENT`, `COLOR_DARK`, `COLOR_BG` en haut
du fichier `app.py` — tout le reste de l'interface s'adapte automatiquement.

---

## 9. Feuille de route (à mentionner si le jury demande "et après ?")

1. **Mois 1-2** : pilote avec 2-3 académies volontaires à Dakar, formulaire de
   saisie simplifié
2. **Mois 3-4** : consolidation base de données réelle, ajustement du score de
   potentiel avec retour terrain des encadreurs
3. **Mois 5-8** : R&D Computer Vision (extraction de métriques depuis vidéos
   smartphone)
4. **Mois 9-12** : ouverture aux clubs partenaires (nord-africains/européens),
   lancement de l'offre SaaS pour les académies

---

## 10. En une phrase pour clore le pitch

> « Ce projet ne vend pas une promesse technologique lointaine : il montre, données
> à l'appui, qu'un recruteur peut aujourd'hui remplacer des heures de visionnage par
> quelques secondes de lecture d'un tableau de bord — et qu'un data analyst sénégalais
> a les compétences pour construire cet outil de bout en bout. »
