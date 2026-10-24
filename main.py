#!/usr/bin/env python3
"""
FROGGY ROAD - point d'entrée.   Lancement :  python3 main.py

Contrôles :  flèches / ZQSD / WASD  (ESPACE = avancer)
             P = pause, R = rejouer, ECHAP = quitter
             C = changer de personnage (écran titre, déblocage avec les pièces)

Installation :  pip install pygame-ce   (ou)   pip install pygame
"""
import sys

import pygame

from settings import W, H, FPS
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Crossy Road")
    try:
        screen = pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)
    except (pygame.error, AttributeError):
        screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    game = Game(screen)
    while True:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.shutdown()
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                game.key(e.key)
        game.update(dt)
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
