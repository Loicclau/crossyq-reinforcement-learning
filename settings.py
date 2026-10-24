"""Toutes les constantes du jeu : tailles, couleurs, skins, réglages de difficulté.
Pour équilibrer ou personnaliser le jeu, c'est ici qu'on commence."""
import math
from pathlib import Path

# --- écran et projection isométrique ---
W, H = 560, 760
S = 44.0                    # taille d'une unité monde (px)

# --- caméra ---
# YAW_DEG = angle de rotation de la vue.
#   45 = ancienne vue très diagonale | 0 = vue de face parfaite (routes horizontales)
#   15 à 25 = rendu proche du vrai Crossy Road
YAW_DEG = 22
_K, _T = 1.2247, 0.5774     # échelle et inclinaison (30°) : identiques à l'ancienne vue
_yaw = math.radians(YAW_DEG)
AX = S * _K * math.cos(_yaw)   # 1 colonne (x)  -> décalage horizontal écran
AY = S * _K * math.sin(_yaw)   # 1 rangée (y)   -> décalage horizontal écran
BX = AY * _T                   # 1 colonne (x)  -> décalage vertical écran
BY = AX * _T                   # 1 rangée (y)   -> décalage vertical écran
LEAD = 2.0                  # le joueur est affiché LEAD rangées devant la caméra
OX = W / 2 - LEAD * AY
OY = H * 0.60 + LEAD * BY
FPS = 60

# --- gameplay ---
HOP_T = 0.13                # durée d'un saut (s)
WRAP = 22.0                 # période des véhicules / troncs (cases)
COL_MAX = 4                 # colonnes jouables : -4 .. 4
Z_BOT = -50                 # bas des dalles de terrain
LOG_H = 9                   # hauteur des troncs au-dessus de l'eau
DIFF_RANGE = 250.0          # rangées pour atteindre la difficulté maximale
LEVEL_STEP = 25             # une rangée-palier "Niveau N" toutes les 25 rangées

SAVE_FILE = Path.home() / ".froggy_road.json"

# --- hauteur (z) du sol de chaque type de rangée ---
ZT = {"grass": 10, "road": 4, "river": -2, "pads": -2, "rail": 5}

# --- couleurs ---
GRASS_C = [(132, 208, 84), (120, 194, 74)]
ROAD_C = [(94, 98, 110), (86, 90, 102)]
WATER_C = [(88, 184, 240), (78, 172, 232)]
RAIL_C = (158, 148, 136)
LOG_C = (146, 100, 60)
PAD_C = (72, 172, 86)
CAR_COLORS = [(228, 70, 70), (70, 130, 230), (244, 204, 64), (84, 194, 114),
              (236, 236, 240), (166, 96, 206), (244, 144, 56)]
TRAILERS = [(232, 232, 238), (96, 156, 226), (240, 184, 64), (124, 204, 144)]
FOLIAGE = [(76, 168, 66), (60, 150, 78), (100, 184, 64)]
WINDOW = (52, 72, 104)

# --- personnages (skins) ---
SKINS = [
    dict(name="Grenouille", price=0, body=(242, 138, 50), foot=(212, 104, 30), belly=(255, 228, 164), acc=None),
    dict(name="Lapin", price=10, body=(236, 236, 244), foot=(196, 196, 210), belly=(255, 190, 208), acc="ears"),
    dict(name="Canard", price=20, body=(252, 218, 70), foot=(240, 150, 40), belly=(255, 244, 170), acc="beak"),
    dict(name="Robot", price=30, body=(150, 170, 196), foot=(104, 120, 146), belly=(210, 226, 244), acc="ant"),
    dict(name="Poulet", price=40, style="chicken", body=(250, 250, 252), foot=(248, 200, 40), belly=(250, 250, 252),
         acc=None, wing=(224, 228, 238), comb=(222, 48, 48), beak=(246, 160, 42), eye=(22, 22, 28)),
]
CHICKEN_SCALE = 0.76          # taille du poulet (1.0 = taille précédente ; plus petit = plus compact)

# --- bordures latérales (zone hors des colonnes jouables) ---
SIDE_DARKEN = {"grass": 0.86, "road": 0.78, "rail": 0.84, "river": 0.88, "pads": 0.88}
FOAM_COLOR = (240, 250, 255)     # particules blanches de l'eau

# --- arbres ---
TRUNK_H = 18                     # hauteur du tronc (px) : plus grand = tronc plus visible

# --- voie ferrée ---
RAIL_SIGNAL_X = -0.5             # panneau des trains : -0.5 = entre les colonnes 0 et -1

# --- caméra : douceur du suivi (plus petit = plus lent et plus fluide) ---
CAM_SMOOTH_Y = 3.2
CAM_SMOOTH_X = 2.2

# --- voiture de police (rare, très rapide) ---
COP_INTERVAL_START = (22.0, 45.0)  # délai (s) entre deux polices au début de la partie
COP_INTERVAL_END = (12.0, 26.0)    # ... et à difficulté maximale (rangée ~250) : plus fréquent, mais toujours rare
COP_MIN_SCORE = 6                # n'apparaît qu'à partir de cette rangée
COP_SPEED = 9.5                  # vitesse de base (cases/s), augmente un peu avec la difficulté

# --- bûches : le joueur se cale sur la case de bûche la plus proche ---
LOG_SNAP_SPEED = 18.0            # vitesse du recalage (plus grand = plus rapide)

# --- bûches d'une seule case : rares au début, de plus en plus fréquentes quand le jeu devient dur ---
LOG1_CHANCE_START = 0.03         # probabilité par bûche au début de la partie
LOG1_CHANCE_END = 0.28           # ... à difficulté maximale (rangée ~250)

# --- petites voitures (1 case environ) : voies dédiées, rares au début, un peu plus rapides ---
SMALL_LANE_START = 0.04          # part des routes qui sont des voies de petites voitures (début)
SMALL_LANE_END = 0.22            # ... à difficulté maximale
SMALL_SPEED_MUL = 1.12           # elles roulent environ 25 % plus vite
SMALL_SPEED_MAX = 6.8            # plafond de vitesse (cases/s)

# --- bûches : la bûche s'enfonce un peu quand le joueur atterrit dessus, puis remonte ---
LOG_DIP_DEPTH = 5.0              # profondeur de l'enfoncement (px)
LOG_DIP_TIME = 0.5               # durée totale (s)

# --- génération du monde : sections, zones de repos, arbres, vitesse des bûches ---
ROAD_RUN_MIN = 4                 # une section de routes compte au moins 4 rangées
ROAD_RUN_MAX_HARD = 8            # ... et jusqu'à 8 à difficulté maximale (4 au début)
REST_START = 75                  # première rangée où une zone de repos (herbe) peut apparaître
REST_PEAK = 100                  # rangée où elle est la plus probable
REST_GAP = 55                    # écart minimal (rangées) entre deux zones de repos
REST_LEN = (4, 5)                # longueur d'une zone de repos
TREE_CENTER_FACTOR = 0.75        # arbres sur les colonnes centrales (-1..1) : multipliés par ce facteur
LOG_SPEED = (0.8, 1.85)          # vitesse de base des bûches (avant : 0.7 - 1.6), puis x difficulté
CUT_LOG_START = 0.06             # part des rivières en "bûches coupées" (petits morceaux) au début
CUT_LOG_END = 0.40               # ... à difficulté maximale
