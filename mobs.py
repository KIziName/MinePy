import math
import random
import traceback

from blocks import *
from event_publisher import EventPublisher  

# ---------- БАЗОВЫЙ КЛАСС МОБА ----------
class Mob:
    def __init__(self, x, y, w, h, hp, damage, speed=0):
        self.x, self.y = x, y
        self.vx, self.vy = 0.0, 0.0
        self.w, self.h = w, h
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.speed = speed
        self.is_grounded = False

    def check_collision(self, get_block_func):
        left = int((self.x - self.w / 2) // BLOCK_SIZE)
        right = int((self.x + self.w / 2) // BLOCK_SIZE)
        top = int((self.y - self.h / 2) // BLOCK_SIZE)
        bottom = int((self.y + self.h / 2) // BLOCK_SIZE)
        for gx in range(left, right + 1):
            for gy in range(top, bottom + 1):
                b = get_block_func(gx, gy)
                if b != BLOCK_AIR and b not in NON_SOLID_BLOCKS:
                    return True
        return False

    def apply_gravity(self, dt, gravity_mult=1.0):
        self.vy += GRAVITY * gravity_mult * dt

    def move_x(self, dt, get_block_func):
        self.x += self.vx * dt
        if self.check_collision(get_block_func):
            self.x -= self.vx * dt
            self.vx = 0

    def move_y(self, dt, get_block_func):
        self.y += self.vy * dt
        if self.check_collision(get_block_func):
            if self.vy > 0:
                self.is_grounded = True
            self.y -= self.vy * dt
            self.vy = 0

    def update(self, player_x, player_y, get_block_func, dt):
        try:
            self.update_ai(player_x, player_y, get_block_func, dt)
        except Exception as e:
            print(f"[Ошибка AI моба {self.__class__.__name__}]", e)
            traceback.print_exc()
        try:
            self.apply_gravity(dt)
        except Exception as e:
            print("[Ошибка гравитации]", e)
        try:
            self.move_x(dt, get_block_func)
        except Exception as e:
            print("[Ошибка move_x]", e)
        try:
            self.move_y(dt, get_block_func)
        except Exception as e:
            print("[Ошибка move_y]", e)

    def update_ai(self, player_x, player_y, get_block_func, dt):
        pass

    def to_dict(self):
        try:
            return {
                'type': self.__class__.__name__,
                'x': self.x,
                'y': self.y,
                'hp': self.hp
            }
        except Exception as e:
            print("[Ошибка to_dict]", e)
            return {}

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError("from_dict должен быть переопределён в дочернем классе")


# ------------------- СЛАЙМ -------------------
class Slime(Mob):
    def __init__(self, x, y, is_blue=False):
        w, h = SLIME_WIDTH, SLIME_HEIGHT
        hp = SLIME_HP_BLUE if is_blue else SLIME_HP_GREEN
        damage = SLIME_DAMAGE_BLUE if is_blue else SLIME_DAMAGE_GREEN
        super().__init__(x, y, w, h, hp, damage)
        self.is_blue = is_blue
        self.speed = SLIME_SPEED_BLUE if is_blue else SLIME_SPEED_GREEN
        self.color = (30, 136, 229) if is_blue else (76, 175, 80)
        self.jump_cooldown = random.uniform(SLIME_JUMP_COOLDOWN_MIN, SLIME_JUMP_COOLDOWN_MAX)

    def update_ai(self, player_x, player_y, get_block_func, dt):
        try:
            dist_x = player_x - self.x
            if self.jump_cooldown > 0:
                self.jump_cooldown -= dt

            if self.is_grounded and self.jump_cooldown <= 0 and abs(dist_x) < SLIME_AGGRO_RANGE:
                self.vy = random.uniform(SLIME_JUMP_FORCE_MIN, SLIME_JUMP_FORCE_MAX)
                self.vx = self.speed if dist_x > 0 else -self.speed
                self.is_grounded = False
                self.jump_cooldown = random.uniform(
                    SLIME_JUMP_COOLDOWN_AFTER, SLIME_JUMP_COOLDOWN_AFTER_MAX
                )
        except Exception as e:
            print("[Ошибка update_ai слайма]", e)
            traceback.print_exc()

    def to_dict(self):
        d = super().to_dict()
        d['is_blue'] = self.is_blue
        return d

    @classmethod
    def from_dict(cls, data):
        try:
            slime = cls(data['x'], data['y'], data.get('is_blue', False))
            slime.hp = data['hp']
            return slime
        except Exception as e:
            print("[Ошибка Slime.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- ЗОМБИ -------------------
class Zombie(Mob):
    def __init__(self, x, y):
        super().__init__(x, y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT, ZOMBIE_HP, ZOMBIE_DAMAGE)
        self.speed = ZOMBIE_SPEED

    def update_ai(self, player_x, player_y, get_block_func, dt):
        try:
            dist_x = player_x - self.x
            if abs(dist_x) < ZOMBIE_AGGRO_RANGE:
                self.vx = self.speed if dist_x > 0 else -self.speed
            else:
                self.vx = 0
        except Exception as e:
            print("[Ошибка update_ai зомби]", e)
            traceback.print_exc()

    def move_x(self, dt, get_block_func):
        self.x += self.vx * dt
        if self.check_collision(get_block_func):
            self.x -= self.vx * dt
            if self.is_grounded:
                self.vy = ZOMBIE_JUMP_FORCE
                self.is_grounded = False
            self.vx = 0

    @classmethod
    def from_dict(cls, data):
        try:
            z = cls(data['x'], data['y'])
            z.hp = data['hp']
            return z
        except Exception as e:
            print("[Ошибка Zombie.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- ГЛАЗ ДЕМОНА -------------------
class DemonEye(Mob):
    def __init__(self, x, y):
        super().__init__(
            x, y, DEMON_EYE_WIDTH, DEMON_EYE_HEIGHT,
            DEMON_EYE_HP, DEMON_EYE_DAMAGE
        )
        self.dash_timer = random.uniform(
            DEMON_EYE_DASH_TIMER_MIN, DEMON_EYE_DASH_TIMER_MAX
        )

    def update_ai(self, player_x, player_y, get_block_func, dt):
        try:
            dx, dy = player_x - self.x, player_y - self.y
            dist = math.hypot(dx, dy)

            self.dash_timer -= dt
            if self.dash_timer <= 0 and dist > 0:
                speed = DEMON_EYE_DASH_SPEED
                self.vx = (dx / dist) * speed
                self.vy = (dy / dist) * speed
                self.dash_timer = random.uniform(
                    DEMON_EYE_DASH_COOLDOWN_MIN, DEMON_EYE_DASH_COOLDOWN_MAX
                )
            else:
                self.vx *= 0.95
                self.vy *= 0.95
                if dist > 0:
                    accel = DEMON_EYE_ACCEL
                    self.vx += (dx / dist) * accel * dt
                    self.vy += (dy / dist) * accel * dt
        except Exception as e:
            print("[Ошибка update_ai глаза демона]", e)
            traceback.print_exc()

    def apply_gravity(self, dt, gravity_mult=1.0):
        pass

    def move_y(self, dt, get_block_func):
        self.y += self.vy * dt

    @classmethod
    def from_dict(cls, data):
        try:
            d = cls(data['x'], data['y'])
            d.hp = data['hp']
            return d
        except Exception as e:
            print("[Ошибка DemonEye.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- СКЕЛЕТ -------------------
class Skeleton(Mob):
    def __init__(self, x, y):
        super().__init__(x, y, SKELETON_WIDTH, SKELETON_HEIGHT, SKELETON_HP, SKELETON_DAMAGE)
        self.speed = SKELETON_SPEED

    def update_ai(self, player_x, player_y, get_block_func, dt):
        try:
            dist_x = player_x - self.x
            if abs(dist_x) < SKELETON_AGGRO_RANGE:
                self.vx = self.speed if dist_x > 0 else -self.speed
            else:
                self.vx = 0
        except Exception as e:
            print("[Ошибка update_ai скелета]", e)
            traceback.print_exc()

    def move_x(self, dt, get_block_func):
        self.x += self.vx * dt
        if self.check_collision(get_block_func):
            self.x -= self.vx * dt
            if self.is_grounded:
                self.vy = SKELETON_JUMP_FORCE
                self.is_grounded = False
            self.vx = 0

    @classmethod
    def from_dict(cls, data):
        try:
            s = cls(data['x'], data['y'])
            s.hp = data['hp']
            return s
        except Exception as e:
            print("[Ошибка Skeleton.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- ОВЦА -------------------
class Sheep(Mob):
    def __init__(self, x, y):
        super().__init__(x, y, SHEEP_WIDTH, SHEEP_HEIGHT, SHEEP_HP, SHEEP_DAMAGE)
        self.color = (255, 255, 255)
        self.move_timer = random.uniform(0, 2)

    def update_ai(self, player_x, player_y, get_block_func, dt):
        try:
            self.move_timer -= dt
            if self.move_timer <= 0:
                self.vx = random.uniform(SHEEP_SPEED_MIN, SHEEP_SPEED_MAX)
                self.move_timer = random.uniform(SHEEP_MOVE_TIMER_MIN, SHEEP_MOVE_TIMER_MAX)
        except Exception as e:
            print("[Ошибка update_ai овцы]", e)
            traceback.print_exc()

    def apply_gravity(self, dt, gravity_mult=1.0):
        self.vy += GRAVITY * SHEEP_GRAVITY_MULT * dt

    @classmethod
    def from_dict(cls, data):
        try:
            sh = cls(data['x'], data['y'])
            sh.hp = data['hp']
            return sh
        except Exception as e:
            print("[Ошибка Sheep.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- ВЫПАВШИЙ ПРЕДМЕТ -------------------
class DroppedItem:
    def __init__(self, x, y, item_type, count=1):
        self.x, self.y = x, y
        self.item_type = item_type
        self.count = count
        self.vy = random.uniform(-120, -240)
        self.vx = random.uniform(-90, 90)
        self.bob_angle = random.uniform(0, 360)

    def update(self, player_x, player_y, get_block_func, dt):
        try:
            self.bob_angle += 0.1 * dt

            dx, dy = player_x - self.x, player_y - self.y
            dist = math.hypot(dx, dy)

            if dist < DROPPED_ITEM_PULL_RADIUS and dist > 0:
                speed = 120.0 if dist > 30 else 240.0
                self.vx += (dx / dist) * speed * dt
                self.vy += (dy / dist) * speed * dt

            self.vy += GRAVITY * 0.4 * dt
            self.x += self.vx * dt
            self.y += self.vy * dt

            gx = int(self.x // BLOCK_SIZE)
            gy = int((self.y + 8) // BLOCK_SIZE)
            if get_block_func(gx, gy) != BLOCK_AIR:
                self.y = gy * BLOCK_SIZE - 8
                self.vy = 0
                self.vx *= 0.8
        except Exception as e:
            print("[Ошибка обновления выпавшего предмета]", e)
            traceback.print_exc()

    def to_dict(self):
        try:
            return {
                'type': 'DroppedItem',
                'x': self.x,
                'y': self.y,
                'item_type': self.item_type,
                'count': self.count
            }
        except Exception as e:
            print("[Ошибка DroppedItem.to_dict]", e)
            return {}

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(data['x'], data['y'], data['item_type'], data['count'])
        except Exception as e:
            print("[Ошибка DroppedItem.from_dict]", e)
            traceback.print_exc()
            return None


# ------------------- КЛАСС УПРАВЛЕНИЯ МОБАМИ -------------------
class GameMobManager(EventPublisher):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.mobs = []
        self.dropped_items = []
        self.spawn_timer = 0.0

    def update(self, player_x, player_y, is_night, player, dt):
        try:
            for mob in self.mobs[:]:
                try:
                    mob.update(player_x, player_y, self.world.get_block, dt)
                    if player.invulnerable_timer <= 0:
                        if abs(player_x - mob.x) < 22 and abs(player_y - mob.y) < 26:
                            player.take_damage(mob.damage, 8 if player_x > mob.x else -8)
                except Exception as e:
                    print(f"[Ошибка обновления моба {mob}]", e)
                    traceback.print_exc()
                    if mob in self.mobs:
                        self.remove_mob(mob)

            for mob in self.mobs[:]:
                if mob.y > (WORLD_HEIGHT + 20) * BLOCK_SIZE:
                    self.remove_mob(mob)

            for item in self.dropped_items[:]:
                item.update(player_x, player_y, self.world.get_block, dt)

            self.spawn_timer += dt
            if self.spawn_timer >= 2.0:
                self.spawn_timer = 0.0

                total_limit = 20
                if MOB_SPAWN_LIMITS:
                    total_limit = 0
                    for limits in MOB_SPAWN_LIMITS.values():
                        if is_night:
                            total_limit += limits.get('night', 0)
                        else:
                            total_limit += limits.get('day', 0)
                    if total_limit == 0:
                        total_limit = 20

                if len(self.mobs) < total_limit:
                    radius_min = MOB_SPAWN_RADIUS_MIN
                    radius_max = MOB_SPAWN_RADIUS_MAX
                    if radius_min is None:
                        radius_min = 450
                    if radius_max is None:
                        radius_max = 750

                    offset = random.choice([-1, 1]) * random.randint(radius_min, radius_max)
                    sx = player_x + offset
                    gx = int(sx // BLOCK_SIZE)
                    sy = (self.world.get_land_height(gx) - 2) * BLOCK_SIZE
                    if sy < 0:
                        sy = 0

                    if is_night:
                        r = random.random()
                        if r < 0.4:
                            mob = Zombie(sx, sy)
                        elif r < 0.7:
                            mob = DemonEye(sx, sy - 100)
                        else:
                            mob = Skeleton(sx, sy)
                    else:
                        if random.random() < 0.4:
                            mob = Sheep(sx, sy)
                        else:
                            is_blue = random.random() < 0.35
                            mob = Slime(sx, sy, is_blue)

                    attempts = 100
                    while mob.check_collision(self.world.get_block) and attempts > 0:
                        mob.y -= 1
                        attempts -= 1

                    if attempts > 0:
                        self.mobs.append(mob)
        except Exception as e:
            print("[Ошибка update моб-менеджера]", e)
            traceback.print_exc()

    def add_dropped_item(self, x, y, item_type, count=1):
        try:
            self.dropped_items.append(DroppedItem(x, y, item_type, count))
        except Exception as e:
            print("[Ошибка add_dropped_item]", e)

    def remove_mob(self, mob):
        try:
            if mob in self.mobs:
                mob_type = type(mob).__name__
                self.mobs.remove(mob)
                self.notify('mob_killed', mob_type=mob_type, x=mob.x, y=mob.y)
        except Exception as e:
            print("[Ошибка remove_mob]", e)

    # Метод clear удалён – он больше не используется, т.к. мы создаём новый менеджер при сбросе.

    def to_dict(self):
        try:
            mobs_data = [m.to_dict() for m in self.mobs]
            items_data = [i.to_dict() for i in self.dropped_items]
            return mobs_data, items_data
        except Exception as e:
            print("[Ошибка to_dict]", e)
            return [], []

    def from_dict(self, mobs_data, items_data):
        self.mobs.clear()
        mob_classes = {
            'Slime': Slime,
            'Zombie': Zombie,
            'DemonEye': DemonEye,
            'Skeleton': Skeleton,
            'Sheep': Sheep
        }
        for md in mobs_data:
            cls = mob_classes.get(md['type'])
            if cls is None:
                continue
            m = cls.from_dict(md)
            if m is not None:
                self.mobs.append(m)
        self.dropped_items = [DroppedItem.from_dict(it) for it in items_data if it is not None]