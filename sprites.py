"""Éléments dessinés directement en 2D (espace écran) : pièce et aigle."""
import math

import pygame


def draw_coin(s, cx, cy, t):
    wd = max(3, abs(math.cos(t * 5)) * 14)
    pygame.draw.ellipse(s, (196, 138, 20), (cx - wd / 2 - 2, cy - 12, wd + 4, 24))
    pygame.draw.ellipse(s, (255, 214, 62), (cx - wd / 2, cy - 10, wd, 20))
    if wd > 8:
        pygame.draw.ellipse(s, (255, 240, 150), (cx - wd / 4, cy - 5, wd / 2, 10))


def draw_eagle(s, x, y, t):
    flap = math.sin(t * 20)
    wing = (92, 62, 38)
    pygame.draw.polygon(s, wing, [(x - 8, y), (x - 95, y - 34 + flap * 22), (x - 70, y + 6), (x - 30, y + 16)])
    pygame.draw.polygon(s, wing, [(x + 8, y), (x + 95, y - 34 + flap * 22), (x + 70, y + 6), (x + 30, y + 16)])
    pygame.draw.ellipse(s, (122, 82, 48), (x - 24, y - 12, 48, 58))
    pygame.draw.circle(s, (246, 246, 246), (int(x), int(y - 14)), 15)
    pygame.draw.polygon(s, (250, 190, 40), [(x - 6, y - 10), (x + 6, y - 10), (x, y + 6)])
    pygame.draw.circle(s, (20, 20, 20), (int(x - 6), int(y - 18)), 2)
    pygame.draw.circle(s, (20, 20, 20), (int(x + 6), int(y - 18)), 2)
    pygame.draw.polygon(s, (250, 190, 40), [(x - 10, y + 44), (x - 4, y + 44), (x - 7, y + 56)])
    pygame.draw.polygon(s, (250, 190, 40), [(x + 4, y + 44), (x + 10, y + 44), (x + 7, y + 56)])
