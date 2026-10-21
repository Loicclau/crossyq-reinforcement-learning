"""Bruitages générés à la volée (aucun fichier audio nécessaire)."""
import array
import math
import random

import pygame


def make_sounds():
    """Retourne un dict {nom: Sound}. Dict vide si l'audio est indisponible."""
    try:
        pygame.mixer.init(22050, -16, 1)
        n_rate = 22050

        def tone(f0, f1, dur, vol=0.35, noise=0.0):
            n, ph, a = int(n_rate * dur), 0.0, array.array("h")
            for i in range(n):
                k = i / n
                ph += 2 * math.pi * (f0 + (f1 - f0) * k) / n_rate
                v = math.sin(ph) * (1 - noise) + random.uniform(-1, 1) * noise
                a.append(int(v * (1 - k) ** 1.5 * vol * 32767))
            return pygame.mixer.Sound(buffer=a.tobytes())
        def wail(dur=1.0, vol=0.22):
            """Sirène 'pin-pon' en boucle (le nombre de cycles est ajusté pour boucler sans clic)."""
            n = int(n_rate * dur)

            def freq(i):
                return 700 + 350 * (0.5 - 0.5 * math.cos(2 * math.pi * 2 * i / n))
            total = sum(2 * math.pi * freq(i) / n_rate for i in range(n))
            k = round(total / (2 * math.pi)) * 2 * math.pi / total
            a, ph = array.array("h"), 0.0
            for i in range(n):
                ph += 2 * math.pi * freq(i) * k / n_rate
                a.append(int((math.sin(ph) + 0.35 * math.sin(2 * ph)) / 1.35 * vol * 32767))
            return pygame.mixer.Sound(buffer=a.tobytes())
        return dict(hop=tone(300, 620, .09), coin=tone(880, 1480, .16, .3),
                    splat=tone(200, 50, .25, .5, .6), splash=tone(600, 120, .35, .4, .8),
                    eagle=tone(900, 300, .4, .3), buy=tone(500, 1000, .25, .3), siren=wail())
    except Exception:
        return {}
