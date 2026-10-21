"""Le monde : les rangées (herbe, route, rivière, rails, nénuphars) et leur génération."""
import random

from settings import (COL_MAX, WRAP, ZT, LOG_H, CAR_COLORS, TRAILERS,
                      GRASS_C, ROAD_C, RAIL_C, LOG_C, PAD_C, LOG1_CHANCE_START, LOG1_CHANCE_END)
from utils import difficulty


def ground_z(row):
    """Hauteur sur laquelle se tient le joueur pour une rangée donnée."""
    if row is None:
        return 0
    if row.kind == "river":
        return ZT["river"] + LOG_H
    if row.kind == "pads":
        return ZT["pads"] + 2
    return ZT[row.kind]


def ground_color(row):
    k = row.kind
    if k == "grass":
        return GRASS_C[row.y % 2]
    if k == "road":
        return ROAD_C[row.y % 2]
    if k == "rail":
        return RAIL_C
    if k == "river":
        return LOG_C
    return PAD_C


class Row:
    def __init__(self, y, kind, seed, direction):
        self.y = y
        self.kind = kind
        self.seed = seed
        self.dir = direction
        self.speed = 0.0
        self.shift = 0.0
        self.trees = {}
        self.coins = set()
        self.pads = set()
        self.items = []     # véhicules
        self.logs = []      # (centre, longueur)
        self.state = "idle"
        self.timer = 0.0
        self.front = 0.0
        self.cops = []             # voitures de police en cours de passage
        self.cop_state = None      # None | clearing | active | restoring
        self.idle = (2.0, 5.0)     # pause entre deux trains (s)
        self.warn = 1.4            # durée de l'avertissement (s)

    def train_extent(self):
        a = self.front
        b = self.front - self.dir * 16
        return min(a, b), max(a, b)

    def update(self, dt, rng):
        if self.kind in ("road", "river"):
            self.shift += self.dir * self.speed * dt
            if self.cops:
                for c in self.cops:
                    c["x"] += self.dir * c["spd"] * dt
                self.cops = [c for c in self.cops if abs(c["x"]) < 26]
        elif self.kind == "rail":
            self.timer -= dt
            if self.state == "idle" and self.timer <= 0:
                self.state, self.timer = "warn", self.warn
            elif self.state == "warn" and self.timer <= 0:
                self.state = "pass"
                self.front = -34.0 if self.dir > 0 else 34.0
            elif self.state == "pass":
                self.front += self.dir * 30 * dt
                if (self.dir > 0 and self.front > 42) or (self.dir < 0 and self.front < -42):
                    self.state, self.timer = "idle", rng.uniform(*self.idle)


class World:
    EASY = {"grass": 3.0, "road": 4.0, "river": 2.2, "rail": 1.0, "pads": 1.0}
    HARD = {"grass": 1.1, "road": 4.6, "river": 3.4, "rail": 1.9, "pads": 1.4}
    LIMITS = {"grass": 2, "road": 4, "river": 3, "rail": 1, "pads": 3}

    def __init__(self):
        self.rng = random.Random()
        self.rows = {}
        self.last, self.run = "grass", 0
        self.reach = set(range(-COL_MAX, COL_MAX + 1))   # colonnes atteignables sur la dernière rangée
        for y in range(-16, 2):
            self.rows[y] = self.make(y, "grass", start=True)
        self.top = 2

    def pick(self):
        """Choisit le type de la prochaine rangée (pondéré par la difficulté)."""
        r = self.rng
        d = difficulty(self.top)
        kinds = list(self.EASY)
        weights = [self.EASY[k] + (self.HARD[k] - self.EASY[k]) * d for k in kinds]
        while True:
            k = r.choices(kinds, weights)[0]
            if k == self.last and self.run >= self.LIMITS[k]:
                continue
            return k

    def make(self, y, kind, start=False):
        r = self.rng
        row = Row(y, kind, r.randint(0, 999), r.choice((-1, 1)))
        d = difficulty(y)
        m = 1 + 0.9 * d                      # multiplicateur de vitesse
        if kind == "grass":
            for c in range(-COL_MAX, COL_MAX + 1):
                if c == 0 and y <= 1:
                    continue
                p = (0.1 if y < -1 else 0.0) if start else 0.2 + 0.12 * d
                if r.random() < p:
                    row.trees[c] = (r.randint(1, 3), r.randint(0, 2))
            if not start and r.random() < 0.12 - 0.06 * d:
                free = [c for c in range(-COL_MAX, COL_MAX + 1) if c not in row.trees]
                if free:
                    row.coins.add(r.choice(free))
        elif kind == "road":
            row.speed = r.uniform(1.6, 3.8) * m
            n = min(5, 2 + int(round(2 * d)) + r.choice((0, 1)))     # 2-3 au début, 4-5 plus loin
            jit = 1.2 - 0.5 * d
            sp, o = WRAP / n, r.uniform(0, WRAP)
            for i in range(n):
                truck = r.random() < min(0.15 + 0.30 * d, 0.45 if n < 5 else 0.3)
                row.items.append(dict(off=(o + i * sp + r.uniform(-jit, jit)) % WRAP,
                                      len=3.2 if truck else 1.5, truck=truck,
                                      color=r.choice(CAR_COLORS), color2=r.choice(TRAILERS)))
        elif kind == "river":
            row.speed = r.uniform(0.7, 1.6) * m
            prev = self.rows.get(y - 1)
            if prev is not None and prev.kind == "river" and prev.dir == row.dir:
                # deux rivières voisines dans le même sens : vitesses nettement différentes
                gap, lo_s, hi_s = 0.55 * m, 0.6 * m, 1.8 * m
                options = []
                if prev.speed - gap >= lo_s:
                    options.append(r.uniform(lo_s, prev.speed - gap))
                if prev.speed + gap <= hi_s:
                    options.append(r.uniform(prev.speed + gap, hi_s))
                row.speed = r.choice(options) if options else prev.speed + gap
            pos, centers = r.uniform(0, 2), []
            while pos < WRAP - 3:
                p1 = LOG1_CHANCE_START + (LOG1_CHANCE_END - LOG1_CHANCE_START) * d      # bûche d'1 case
                if r.random() < p1:
                    ln = 1
                else:
                    ln = r.choice((2, 2, 3, 3, 4) if r.random() > d else (2, 2, 2, 3))
                centers.append([pos + ln / 2, ln])
                pos += ln + r.uniform(1.0 + 0.7 * d, 2.2 + 0.9 * d)
            scale = WRAP / pos
            row.logs = [(c * scale, ln) for c, ln in centers]
        elif kind == "pads":
            prev = self.rows.get(y - 1)
            if prev is not None and prev.kind == "pads":
                cols = set(prev.pads)
                for c in range(-COL_MAX, COL_MAX + 1):
                    if r.random() < 0.25:
                        cols.add(c)
            else:
                cols = {c for c in range(-COL_MAX, COL_MAX + 1) if r.random() < 0.55}
                while len(cols) < 3:
                    cols.add(r.randint(-COL_MAX, COL_MAX))
            row.pads = cols
        elif kind == "rail":
            row.timer = r.uniform(0.5, 3.5)
            row.idle = (max(0.6, 2.0 - 1.4 * d), max(1.6, 5.0 - 3.0 * d))
            row.warn = max(0.9, 1.4 - 0.5 * d)
        return row

    def generate(self, y_max):
        """Génère les rangées jusqu'à y_max."""
        while self.top <= y_max:
            k = self.pick()
            self.run = self.run + 1 if k == self.last else 1
            self.last = k
            row = self.make(self.top, k)
            self.ensure_passable(row)
            self.rows[self.top] = row
            self.top += 1

    # ---- garantie que la map est toujours franchissable ----
    def standable(self, row, c):
        if row.kind == "grass":
            return c not in row.trees
        if row.kind == "pads":
            return c in row.pads
        return True

    def spread(self, row, cells):
        """Colonnes atteignables sur la rangée en se déplaçant latéralement."""
        if row.kind not in ("grass", "pads"):
            return set(range(-COL_MAX, COL_MAX + 1))     # route / rails / rivière : on circule librement
        out, stack = set(cells), list(cells)
        while stack:
            c = stack.pop()
            for n in (c - 1, c + 1):
                if -COL_MAX <= n <= COL_MAX and n not in out and self.standable(row, n):
                    out.add(n)
                    stack.append(n)
        return out

    def ensure_passable(self, row):
        """Si le joueur ne peut pas entrer dans cette rangée depuis la précédente,
        on ouvre un passage (on retire un arbre ou on ajoute un nénuphar)."""
        enter = {c for c in self.reach if self.standable(row, c)}
        if not enter:
            c = self.rng.choice(sorted(self.reach))
            if row.kind == "grass":
                row.trees.pop(c, None)
            elif row.kind == "pads":
                row.pads.add(c)
            enter = {c}
        self.reach = self.spread(row, enter)

    def prune(self, y_min):
        """Supprime les rangées derrière la caméra."""
        for y in [y for y in self.rows if y < y_min]:
            del self.rows[y]
