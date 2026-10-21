"""Petites fonctions mathématiques réutilisables (sans dépendance au jeu)."""
from settings import WRAP, DIFF_RANGE


def shade(c, f):
    """Éclaircit / assombrit une couleur RGB d'un facteur f."""
    return tuple(max(0, min(255, int(v * f))) for v in c)


def pd(a, b):
    """Distance signée sur la boucle de période WRAP."""
    return ((a - b + WRAP / 2) % WRAP) - WRAP / 2


def difficulty(y):
    """Difficulté 0..1 qui croît avec la distance (progression douce)."""
    t = min(1.0, max(0.0, y) / DIFF_RANGE)
    return t * t * (3 - 2 * t) * 0.35 + t * 0.65


def creep_speed(max_y):
    """Vitesse de l'aigle (avancée de la caméra, rangées/s)."""
    return 0.30 + 0.60 * difficulty(max_y)
