"""Les données du joueur (position, saut en cours, direction)."""


class Player:
    def __init__(self):
        self.x = 0.0
        self.y = 0
        self.max_y = 0       # rangée la plus lointaine atteinte = le score
        self.lift = 0.0      # hauteur du saut (visuel)
        self.hop = None      # saut en cours : [x0, y0, x1, y1, progression 0..1]
        self.queue = None    # prochain saut mémorisé pendant un saut
        self.face = (0, 1)   # direction regardée
        self.ride = None     # bûche portée : dict(row, idx, k, off) -> case 'off' de la bûche idx
        self.snap = 0.0      # écart restant à résorber après l'atterrissage (recalage doux)
        self.hop_follow = None   # saut latéral sur une bûche : la cible suit la bûche
