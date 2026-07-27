import pygame
import json
import math
import random
import os
import webbrowser
import time
import sys

from blocks import *
from renderer import GameRenderer  # <-- добавлен импорт класса
from mobs import DroppedItem, Slime, Zombie, DemonEye, Skeleton, Sheep
from world import GameWorld
from save import SaveManager

# ------------------- ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ -------------------
class GamePlayer:
    def __init__(self, world):
        self.world = world
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.w, self.h = PLAYER_WIDTH, PLAYER_HEIGHT
        self.facing_right = True
        self.anim_frame = 0
        self.is_grounded = False
        self.hp = 100
        self.max_hp = 100
        self.invulnerable_timer = 0.0
        self.swing_anim = 0.0
        self.damage_bonus = 0
        self.speed_bonus = 0
        self.jump_bonus = 0
        self.night_vision = False
        self.invisible = False
        self.water_breathing = False
        self.haste = False

    def spawn(self):
        ground_h = self.world._get_land_height(0)
        self.x = 0
        self.y = (ground_h - 2) * BLOCK_SIZE
        self.vx = self.vy = 0
        self.is_grounded = False
        self.hp = self.max_hp
        self.invulnerable_timer = 0.0

        attempts = 200
        while self._check_collision() and attempts > 0:
            self.y -= 1
            attempts -= 1
        if attempts == 0:
            self.y = (ground_h - 10) * BLOCK_SIZE

    def update(self, keys, dt):
        self.vx = 0
        speed = PLAYER_SPEED + self.speed_bonus
        if keys.get(pygame.K_a) or keys.get(pygame.K_LEFT):
            self.vx = -speed
            self.facing_right = False
        if keys.get(pygame.K_d) or keys.get(pygame.K_RIGHT):
            self.vx = speed
            self.facing_right = True

        jump_force = JUMP_FORCE - self.jump_bonus
        if (keys.get(pygame.K_w) or keys.get(pygame.K_SPACE) or keys.get(pygame.K_UP)) and self.is_grounded:
            self.vy = jump_force
            self.is_grounded = False

        self.vy += GRAVITY * dt

        self.x += self.vx * dt
        if self._check_collision():
            self.x -= self.vx * dt

        self.y += self.vy * dt
        if self._check_collision():
            if self.vy > 0:
                self.is_grounded = True
            self.y -= self.vy * dt
            self.vy = 0

        if self.vx != 0:
            self.anim_frame += PLAYER_ANIM_SPEED * dt

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        if self.swing_anim > 0:
            self.swing_anim -= dt

        if self.damage_bonus > 0:
            self.damage_bonus = max(0, self.damage_bonus - dt * 10)
        if self.speed_bonus > 0:
            self.speed_bonus = max(0, self.speed_bonus - dt * 10)
        if self.jump_bonus > 0:
            self.jump_bonus = max(0, self.jump_bonus - dt * 10)
        if self.night_vision:
            self.night_vision = False
        if self.invisible:
            self.invisible = False
        if self.water_breathing:
            self.water_breathing = False
        if self.haste:
            self.haste = False

    def _check_collision(self):
        left = int((self.x - self.w/2) // BLOCK_SIZE)
        right = int((self.x + self.w/2) // BLOCK_SIZE)
        top = int((self.y - self.h/2) // BLOCK_SIZE)
        bottom = int((self.y + self.h/2) // BLOCK_SIZE)
        for gx in range(left, right + 1):
            for gy in range(top, bottom + 1):
                b = self.world.get_block(gx, gy)
                if b != BLOCK_AIR and b not in (BLOCK_LEAVES, BLOCK_TALL_GRASS, BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE,
                                                 BLOCK_BUSH, BLOCK_FERN, BLOCK_VINE, BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY):
                    return True
        return False

    def take_damage(self, damage, knockback_x=0):
        if self.invulnerable_timer <= 0:
            self.hp -= damage
            self.invulnerable_timer = 0.4
            self.vx = knockback_x
            self.vy = -250
            if self.hp <= 0:
                self.hp = self.max_hp
                self.spawn()

    def get_weapon_damage(self, inventory):
        itype = inventory.get_selected_item()['type']
        if itype == ITEM_SWORD_WOOD: return 12
        if itype == ITEM_SWORD_COPPER: return 18
        if itype == ITEM_SWORD_IRON: return 28
        if itype == ITEM_SWORD_GOLD: return 38
        if itype == ITEM_SWORD_DIAMOND: return 55
        if itype == ITEM_SWORD_STONE: return 16
        if itype == ITEM_SWORD_SILVER: return 45
        if itype == ITEM_SWORD_PLATINUM: return 55
        if itype == ITEM_SWORD_MITHRIL: return 70
        if itype == ITEM_SWORD_ADAMANTITE: return 90
        if itype == ITEM_SWORD_TITAN: return 100
        if itype == ITEM_SWORD_COBALT: return 120
        if itype == ITEM_SWORD_NETHERITE: return 150
        if itype == ITEM_SWORD_CRYSTAL: return 180
        if itype == ITEM_HAMMER: return 200
        if itype == ITEM_SPEAR: return 70
        if itype == ITEM_CROSSBOW: return 50
        if itype == ITEM_AXE_TITAN: return 90
        if itype == ITEM_AXE_COBALT: return 110
        if itype == ITEM_AXE_NETHERITE: return 140
        return 6


class GameInventory:
    def __init__(self):
        self.slots = [{'type': BLOCK_AIR, 'count': 0} for _ in range(40)]
        self.slots[0] = {'type': ITEM_SWORD_WOOD, 'count': 1}
        self.slots[1] = {'type': ITEM_PICKAXE_WOOD, 'count': 1}
        self.slots[2] = {'type': BLOCK_DIRT, 'count': 20}
        self.selected_slot = 0
        self.dragged_slot = None

    def get_selected_item(self):
        return self.slots[self.selected_slot]

    def add_item(self, item_type, count=1):
        for slot in self.slots:
            if slot['type'] == item_type and slot['count'] < MAX_STACK:
                add = min(count, MAX_STACK - slot['count'])
                slot['count'] += add
                count -= add
                if count <= 0:
                    return True
        for slot in self.slots:
            if slot['type'] == BLOCK_AIR:
                slot['type'] = item_type
                slot['count'] = min(count, MAX_STACK)
                count -= slot['count']
                if count <= 0:
                    return True
        return False

    def can_craft(self, ingredients):
        for itype, count in ingredients:
            total = sum(s['count'] for s in self.slots if s['type'] == itype)
            if total < count:
                return False
        return True

    def craft(self, result, ingredients):
        if not self.can_craft(ingredients):
            return False
        for itype, count in ingredients:
            needed = count
            for slot in self.slots:
                if slot['type'] == itype:
                    take = min(needed, slot['count'])
                    slot['count'] -= take
                    needed -= take
                    if slot['count'] <= 0:
                        slot['type'] = BLOCK_AIR
                    if needed <= 0:
                        break
        return self.add_item(result['type'], result['count'])

    def swap_slots(self, idx1, idx2):
        self.slots[idx1], self.slots[idx2] = self.slots[idx2], self.slots[idx1]

    def get_slot(self, idx):
        return self.slots[idx]

    def to_dict(self):
        return self.slots

    def from_dict(self, data):
        self.slots = data


class GameMobManager:
    def __init__(self, world):
        self.world = world
        self.mobs = []
        self.dropped_items = []
        self.spawn_timer = 0.0

    def update(self, player_x, player_y, is_night, player, dt):
        for mob in self.mobs[:]:
            mob.update(player_x, player_y, self.world.get_block, dt)
            if player.invulnerable_timer <= 0:
                if abs(player_x - mob.x) < 22 and abs(player_y - mob.y) < 26:
                    player.take_damage(mob.damage, 8 if player_x > mob.x else -8)

        for item in self.dropped_items[:]:
            item.update(player_x, player_y, self.world.get_block, dt)

        self.spawn_timer += dt
        if self.spawn_timer >= 2.0:
            self.spawn_timer = 0.0
            if len(self.mobs) < MAX_MOBS:
                offset = random.choice([-1, 1]) * random.randint(450, 750)
                sx = player_x + offset
                gx = int(sx // BLOCK_SIZE)
                sy = (self.world._get_land_height(gx) - 2) * BLOCK_SIZE

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

                self.mobs.append(mob)

    def add_dropped_item(self, x, y, item_type, count=1):
        self.dropped_items.append(DroppedItem(x, y, item_type, count))

    def remove_mob(self, mob):
        if mob in self.mobs:
            self.mobs.remove(mob)

    def clear(self):
        self.mobs.clear()
        self.dropped_items.clear()
        self.spawn_timer = 0.0

    def to_dict(self):
        return [m.to_dict() for m in self.mobs], [i.to_dict() for i in self.dropped_items]

    def from_dict(self, mobs_data, items_data):
        self.mobs.clear()
        for md in mobs_data:
            m_type = md['type']
            if m_type == 'Slime':
                m = Slime(md['x'], md['y'], md.get('is_blue', False))
            elif m_type == 'Zombie':
                m = Zombie(md['x'], md['y'])
            elif m_type == 'DemonEye':
                m = DemonEye(md['x'], md['y'])
            elif m_type == 'Skeleton':
                m = Skeleton(md['x'], md['y'])
            elif m_type == 'Sheep':
                m = Sheep(md['x'], md['y'])
            else:
                continue
            m.hp = md['hp']
            self.mobs.append(m)
        self.dropped_items = [DroppedItem.from_dict(it) for it in items_data]


# ------------------- ОСНОВНОЙ КЛАСС GAME -------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MinePy 2D")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = False

        self.init_fonts()
        self.game_state = "menu"

        self.world = GameWorld()
        self.player = GamePlayer(self.world)
        self.inventory = GameInventory()
        self.mob_manager = GameMobManager(self.world)

        # Менеджер сохранения
        self.save_manager = SaveManager(self)

        # Рендерер (создаём после инициализации всех компонентов)
        self.renderer = GameRenderer(self)   # <-- добавлено

        self.day_time = 3000
        self.day_counter = 0
        self.save_notification_timer = 0.0
        self.inventory_open = False
        self.pause_menu_open = False
        self.keys = {}
        self.mouse_x, self.mouse_y = 0, 0

        self.fps_counter = 0
        self.current_fps = 0
        self.last_fps_time = time.time()

        self.menu_buttons = []
        self.pause_buttons = []

        # Погода
        self.weather = WEATHER_CLEAR
        self.weather_timer = 0.0
        self.weather_alpha = 1.0
        self.weather_transition_time = WEATHER_TRANSITION_TIME

        self._init_weather_particles()
        self._init_clouds()
        self._init_stars()

        # Кеширование фона
        self.bg_surfaces = {}
        self._build_background_surfaces()

        # FPS SELECTION
        self.fps_options = [30, 60, 100, 120]
        self.fps_index = 1
        self.target_fps = self.fps_options[self.fps_index]

    def _init_clouds(self):
        self.clouds = []
        for _ in range(CLOUDS_COUNT):
            self.clouds.append({
                'x': random.randint(0, self.screen_width * 2),
                'y': random.randint(-200, 100),
                'w': random.randint(200, 400),
                'h': random.randint(40, 80),
                'speed': random.uniform(10, 30)
            })

    def _init_weather_particles(self):
        self.rain_particles = []
        for _ in range(RAIN_PARTICLES):
            x = random.randint(0, self.screen_width)
            y = random.randint(-self.screen_height, self.screen_height)
            speed = random.uniform(300, 500)
            self.rain_particles.append((x, y, speed))

        self.snow_particles = []
        for _ in range(SNOW_PARTICLES):
            x = random.randint(0, self.screen_width)
            y = random.randint(-self.screen_height, self.screen_height)
            size = random.uniform(2, 5)
            speed = random.uniform(50, 120)
            self.snow_particles.append((x, y, size, speed))

    def _init_stars(self):
        self.stars = []
        for _ in range(STARS_COUNT):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.uniform(1, 3)
            brightness = random.uniform(0.3, 1.0)
            twinkle_speed = random.uniform(0.5, 2.0)
            phase = random.uniform(0, 6.28)
            self.stars.append([x, y, size, brightness, twinkle_speed, phase])

    def _build_background_surfaces(self):
        self.bg_surfaces.clear()
        intervals = {
            'day': 0,
            'sunset': 11000,
            'night': 17000,
            'sunrise': 23000
        }
        for key, t in intervals.items():
            surf = pygame.Surface((self.screen_width, self.screen_height))
            top_color, bottom_color = self.get_sky_gradient(t)
            for y in range(self.screen_height):
                blend = y / self.screen_height
                r = int(top_color[0] + (bottom_color[0] - top_color[0]) * blend)
                g = int(top_color[1] + (bottom_color[1] - top_color[1]) * blend)
                b = int(top_color[2] + (bottom_color[2] - top_color[2]) * blend)
                pygame.draw.line(surf, (r, g, b), (0, y), (self.screen_width, y))
            self.bg_surfaces[key] = surf

    def init_fonts(self):
        font_name = pygame.font.match_font('arial') or pygame.font.match_font('dejavusans')
        self.font_small = pygame.font.Font(font_name, 13)
        self.font_med = pygame.font.Font(font_name, 18)
        self.font_big = pygame.font.Font(font_name, 32)
        self.font_huge = pygame.font.Font(font_name, 52)

    def is_night(self):
        return 11000 <= (self.day_time % 24000) <= 23000

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.screen_width, self.screen_height = info.current_w, info.current_h
        else:
            self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self._init_weather_particles()
        self._init_clouds()
        self._init_stars()
        self._build_background_surfaces()

        self.renderer.screen = self.screen
        self.renderer.screen_width = self.screen_width
        self.renderer.screen_height = self.screen_height

    def toggle_inventory(self):
        if self.pause_menu_open:
            return
        self.inventory_open = not self.inventory_open
        if not self.inventory_open:
            self.inventory.dragged_slot = None

    def toggle_pause(self):
        if self.inventory_open:
            self.inventory_open = False
        self.pause_menu_open = not self.pause_menu_open

    def open_github(self):
        webbrowser.open("https://github.com/KIziName/MinePy")

    def start_game(self, is_new=True):
        if is_new:
            self.reset_game_data()
            self.player.spawn()
        self.game_state = "game"
        self.inventory_open = False
        self.pause_menu_open = False

    def load_and_start_game(self):
        if self.save_manager.load():
            self.start_game(is_new=False)

    def reset_game_data(self):
        self.inventory_open = False
        self.pause_menu_open = False
        self.day_time = 3000
        self.day_counter = 0
        self.save_notification_timer = 0.0
        self.keys.clear()
        self.world.clear()
        self.mob_manager.clear()
        self.inventory = GameInventory()
        self.player = GamePlayer(self.world)
        self.player.spawn()
        self.weather = WEATHER_CLEAR
        self.weather_timer = 0.0
        self.weather_alpha = 1.0
        self._init_weather_particles()
        self._init_clouds()
        self._init_stars()
        self._build_background_surfaces()

    def cycle_fps(self):
        self.fps_index = (self.fps_index + 1) % len(self.fps_options)
        self.target_fps = self.fps_options[self.fps_index]

    def exit_to_menu(self):
        self.game_state = "menu"
        self.inventory_open = False
        self.pause_menu_open = False
        
    def draw_menu(self):
        self.renderer.draw_menu()

    def render(self):
        self.renderer.render()

    # ------------------- UPDATE -------------------
    def update_physics(self, dt):
        if self.game_state != "game":
            return
        if self.inventory_open or self.pause_menu_open:
            return

        old_day_time = self.day_time
        self.day_time = (self.day_time + 120 * dt) % 24000
        if old_day_time > 23000 and self.day_time < 1000:
            self.day_counter += 1

        self.player.update(self.keys, dt)
        self.mob_manager.update(self.player.x, self.player.y, self.is_night(), self.player, dt)

        for item in self.mob_manager.dropped_items[:]:
            if math.hypot(self.player.x - item.x, self.player.y - item.y) < 28:
                if self.inventory.add_item(item.item_type, item.count):
                    self.mob_manager.dropped_items.remove(item)

        if self.save_notification_timer > 0:
            self.save_notification_timer -= dt

        # Погода
        self.weather_timer -= dt
        if self.weather_timer <= 0:
            new_weather = random.choice([WEATHER_CLEAR, WEATHER_RAIN, WEATHER_SNOW])
            if new_weather != self.weather:
                self.weather = new_weather
                self.weather_alpha = 0.0
            self.weather_timer = random.uniform(WEATHER_CHANGE_INTERVAL_MIN, WEATHER_CHANGE_INTERVAL_MAX)

        if self.weather_alpha < 1.0:
            self.weather_alpha += dt / self.weather_transition_time
            if self.weather_alpha > 1.0:
                self.weather_alpha = 1.0

        if self.weather == WEATHER_RAIN and self.weather_alpha > 0:
            for i, (x, y, speed) in enumerate(self.rain_particles):
                y += speed * dt
                if y > self.screen_height + 20:
                    y = random.randint(-30, -10)
                    x = random.randint(0, self.screen_width)
                self.rain_particles[i] = (x, y, speed)
        elif self.weather == WEATHER_SNOW and self.weather_alpha > 0:
            for i, (x, y, size, speed) in enumerate(self.snow_particles):
                y += speed * dt
                x += math.sin(y * 0.01) * 0.5
                if y > self.screen_height + 20:
                    y = random.randint(-30, -10)
                    x = random.randint(0, self.screen_width)
                self.snow_particles[i] = (x, y, size, speed)

        for cloud in self.clouds:
            cloud['x'] += cloud['speed'] * dt
            if cloud['x'] > self.screen_width + 400:
                cloud['x'] = -400 - cloud['w']
                cloud['y'] = random.randint(-200, 100)
                cloud['w'] = random.randint(200, 400)
                cloud['h'] = random.randint(40, 80)
                cloud['speed'] = random.uniform(10, 30)

    def get_sky_gradient(self, t):
        if t < 10000:
            return (30, 80, 200), (135, 206, 250)
        elif t < 12000:
            return (30, 80, 200), (255, 140, 0)
        elif t < 22000:
            return (5, 7, 20), (20, 30, 60)
        else:
            return (5, 7, 20), (255, 180, 100)

    # ------------------- ОБРАБОТКА СОБЫТИЙ -------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.game_state == "game":
                    if event.key == pygame.K_e:
                        self.toggle_inventory()
                    elif event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                       pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                        if event.key == pygame.K_0:
                            self.inventory.selected_slot = 9
                        else:
                            self.inventory.selected_slot = event.key - pygame.K_1
                self.keys[event.key] = True

            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_state == "menu":
                        self.handle_menu_click(event.pos)
                    elif self.game_state == "game":
                        if self.pause_menu_open:
                            self.handle_pause_click(event.pos)
                        elif self.inventory_open:
                            self.handle_inventory_click(event.pos)
                        else:
                            if not self.check_hotbar_click(event.pos):
                                self.handle_game_click(event.pos, button=1)
                elif event.button == 3:
                    if self.game_state == "game" and not self.inventory_open and not self.pause_menu_open:
                        self.handle_game_click(event.pos, button=3)
                elif event.button == 4:
                    if self.game_state == "game" and not self.inventory_open and not self.pause_menu_open:
                        self.inventory.selected_slot = (self.inventory.selected_slot - 1) % 10
                elif event.button == 5:
                    if self.game_state == "game" and not self.inventory_open and not self.pause_menu_open:
                        self.inventory.selected_slot = (self.inventory.selected_slot + 1) % 10

    def check_hotbar_click(self, pos):
        bar_x, bar_y = 15, 15
        for i in range(10):
            rect = pygame.Rect(bar_x + i * 48, bar_y, 44, 44)
            if rect.collidepoint(pos):
                if self.inventory_open:
                    if self.inventory.dragged_slot is None:
                        if self.inventory.get_slot(i)['type'] != BLOCK_AIR:
                            self.inventory.dragged_slot = i
                    else:
                        self.inventory.swap_slots(i, self.inventory.dragged_slot)
                        self.inventory.dragged_slot = None
                else:
                    self.inventory.selected_slot = i
                return True
        return False

    def handle_menu_click(self, pos):
        for rect, action in self.menu_buttons:
            if rect.collidepoint(pos):
                action()

    def handle_pause_click(self, pos):
        for rect, action in self.pause_buttons:
            if rect.collidepoint(pos):
                action()

    def handle_inventory_click(self, pos):
        if self.check_hotbar_click(pos):
            return

        inv_x, inv_y = 15, 70
        for row in range(3):
            for col in range(10):
                idx = (row + 1) * 10 + col
                rect = pygame.Rect(inv_x + 12 + col * 46, inv_y + 40 + row * 46, 42, 42)
                if rect.collidepoint(pos):
                    if self.inventory.dragged_slot is None:
                        if self.inventory.get_slot(idx)['type'] != BLOCK_AIR:
                            self.inventory.dragged_slot = idx
                    else:
                        self.inventory.swap_slots(idx, self.inventory.dragged_slot)
                        self.inventory.dragged_slot = None
                    return

        craft_y = inv_y + 185
        for result, ingredients in CRAFTING_RECIPES:
            rect = pygame.Rect(inv_x + 12, craft_y, 466, 24)
            if rect.collidepoint(pos):
                self.inventory.craft(result, ingredients)
                return
            craft_y += 27

        if not (inv_x <= pos[0] <= inv_x + 490 and inv_y <= pos[1] <= inv_y + 360):
            self.toggle_inventory()

    def handle_game_click(self, pos, button=1):
        cam_x = self.player.x - self.screen_width / 2
        cam_y = self.player.y - self.screen_height / 2
        wx, wy = pos[0] + cam_x, pos[1] + cam_y

        if math.hypot(wx - self.player.x, wy - self.player.y) > BUILD_REACH:
            return

        if button == 1:
            self.player.swing_anim = 0.15
            slot = self.inventory.get_selected_item()

            # --- Использование зелий и еды (левый клик) ---
            if slot['type'] in (ITEM_POTION, ITEM_BIG_POTION, ITEM_POTION_REGENERATION,
                                ITEM_POTION_STRENGTH, ITEM_POTION_SPEED, ITEM_POTION_JUMP,
                                ITEM_POTION_NIGHT_VISION, ITEM_POTION_INVISIBILITY,
                                ITEM_POTION_WATER_BREATHING, ITEM_POTION_HASTE):
                heal = 0
                if slot['type'] == ITEM_POTION:
                    heal = 40
                elif slot['type'] == ITEM_BIG_POTION:
                    heal = 80
                elif slot['type'] == ITEM_POTION_REGENERATION:
                    heal = 30
                elif slot['type'] == ITEM_POTION_STRENGTH:
                    self.player.damage_bonus = 30
                elif slot['type'] == ITEM_POTION_SPEED:
                    self.player.speed_bonus = 150
                elif slot['type'] == ITEM_POTION_JUMP:
                    self.player.jump_bonus = 150
                elif slot['type'] == ITEM_POTION_NIGHT_VISION:
                    self.player.night_vision = True
                elif slot['type'] == ITEM_POTION_INVISIBILITY:
                    self.player.invisible = True
                elif slot['type'] == ITEM_POTION_WATER_BREATHING:
                    self.player.water_breathing = True
                elif slot['type'] == ITEM_POTION_HASTE:
                    self.player.haste = True
                if heal > 0:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Еда ---
            if slot['type'] in (ITEM_APPLE, ITEM_BREAD, ITEM_COOKED_MEAT, ITEM_PIE, ITEM_SOUP,
                                ITEM_MUSHROOM_SOUP, ITEM_COOKED_MUSHROOM,
                                ITEM_PIZZA, ITEM_BURGER, ITEM_SUSHI, ITEM_CAKE,
                                ITEM_SALAD, ITEM_FRIED_POTATOES, ITEM_CARROT_JUICE):
                heal = {
                    ITEM_APPLE: 10, ITEM_BREAD: 20, ITEM_COOKED_MEAT: 35,
                    ITEM_PIE: 50, ITEM_SOUP: 30, ITEM_MUSHROOM_SOUP: 35, ITEM_COOKED_MUSHROOM: 20,
                    ITEM_PIZZA: 60, ITEM_BURGER: 70, ITEM_SUSHI: 50, ITEM_CAKE: 80,
                    ITEM_SALAD: 40, ITEM_FRIED_POTATOES: 30, ITEM_CARROT_JUICE: 25,
                }.get(slot['type'], 20)
                if self.player.hp < self.player.max_hp:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                    slot['count'] -= 1
                    if slot['count'] <= 0:
                        slot['type'] = BLOCK_AIR
                return

            # --- Посохи (левый клик) ---
            if slot['type'] in (ITEM_STAFF_FIRE, ITEM_STAFF_ICE, ITEM_STAFF_LIGHTNING, ITEM_STAFF_HEALING):
                dmg = {
                    ITEM_STAFF_FIRE: 30,
                    ITEM_STAFF_ICE: 25,
                    ITEM_STAFF_LIGHTNING: 40,
                    ITEM_STAFF_HEALING: 50,
                }.get(slot['type'], 0)
                if slot['type'] == ITEM_STAFF_HEALING:
                    self.player.hp = min(self.player.max_hp, self.player.hp + 50)
                else:
                    target = None
                    min_dist = 200
                    for mob in self.mob_manager.mobs:
                        dist = math.hypot(mob.x - self.player.x, mob.y - self.player.y)
                        if dist < min_dist:
                            min_dist = dist
                            target = mob
                    if target:
                        target.hp -= dmg
                        target.vy = -300
                        if target.hp <= 0:
                            self.mob_manager.remove_mob(target)
                return

            # --- Украшения (левый клик) ---
            if slot['type'] in (ITEM_RING_STRENGTH, ITEM_RING_PROTECTION,
                                ITEM_AMULET_REGENERATION, ITEM_AMULET_SPEED,
                                ITEM_NECKLACE_JUMP):
                self.player.damage_bonus += 10
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Свиток телепортации ---
            if slot['type'] == ITEM_SCROLL_TELEPORT:
                self.player.x += random.randint(-500, 500)
                self.player.y += random.randint(-500, 500)
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Удар по мобу ---
            dmg = self.player.get_weapon_damage(self.inventory)
            for mob in self.mob_manager.mobs[:]:
                if abs(mob.x - wx) < 30 and abs(mob.y - wy) < 30:
                    mob.hp -= dmg
                    mob.vy = -220
                    if mob.hp <= 0:
                        drop_type = None
                        if isinstance(mob, Slime):
                            drop_type, count = ITEM_GEL, random.randint(1, 3)
                        elif isinstance(mob, Zombie):
                            drop_type, count = ITEM_COIN, random.randint(1, 4)
                        elif isinstance(mob, DemonEye):
                            drop_type, count = ITEM_LENS, 1
                        elif isinstance(mob, Skeleton):
                            drop_type, count = ITEM_BONE, random.randint(1, 2)
                        elif isinstance(mob, Sheep):
                            drop_type, count = ITEM_GEL, random.randint(1, 2)
                        if drop_type is not None:
                            self.mob_manager.add_dropped_item(mob.x, mob.y, drop_type, count)
                        self.mob_manager.remove_mob(mob)
                    return

            # --- Разрушение блока ---
            gx, gy = int(wx // BLOCK_SIZE), int(wy // BLOCK_SIZE)
            b_type = self.world.get_block(gx, gy)
            if b_type != BLOCK_AIR:
                if b_type in (BLOCK_TALL_GRASS, BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE,
                              BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY, BLOCK_BUSH, BLOCK_FERN, BLOCK_VINE):
                    if not self.inventory.add_item(b_type, 1):
                        self.mob_manager.add_dropped_item((gx + 0.5) * BLOCK_SIZE, (gy + 0.5) * BLOCK_SIZE, b_type, 1)
                    self.world.set_block(gx, gy, BLOCK_AIR)
                    return
                drop_item = b_type
                if b_type == BLOCK_STONE and random.random() < 0.2:
                    drop_item = ITEM_FLINT
                elif b_type == BLOCK_LEAVES and random.random() < 0.05:
                    drop_item = ITEM_APPLE
                elif b_type in (BLOCK_COPPER_ORE, BLOCK_IRON_ORE, BLOCK_GOLD_ORE, BLOCK_COAL_ORE,
                                BLOCK_SILVER_ORE, BLOCK_PLATINUM_ORE, BLOCK_MITHRIL_ORE, BLOCK_ADAMANTITE_ORE,
                                BLOCK_TITAN_ORE, BLOCK_COBALT_ORE, BLOCK_NETHERITE_ORE, BLOCK_CRYSTAL_ORE):
                    drop_item = {BLOCK_COPPER_ORE: ITEM_COPPER_INGOT,
                                 BLOCK_IRON_ORE: ITEM_IRON_INGOT,
                                 BLOCK_GOLD_ORE: ITEM_GOLD_INGOT,
                                 BLOCK_COAL_ORE: ITEM_COAL,
                                 BLOCK_SILVER_ORE: ITEM_SILVER_INGOT,
                                 BLOCK_PLATINUM_ORE: ITEM_PLATINUM_INGOT,
                                 BLOCK_MITHRIL_ORE: ITEM_MITHRIL_INGOT,
                                 BLOCK_ADAMANTITE_ORE: ITEM_ADAMANTITE_INGOT,
                                 BLOCK_TITAN_ORE: ITEM_TITAN_INGOT,
                                 BLOCK_COBALT_ORE: ITEM_COBALT_INGOT,
                                 BLOCK_NETHERITE_ORE: ITEM_NETHERITE_INGOT,
                                 BLOCK_CRYSTAL_ORE: ITEM_CRYSTAL_INGOT}.get(b_type, b_type)
                self.world.set_block(gx, gy, BLOCK_AIR)
                self.mob_manager.add_dropped_item((gx + 0.5) * BLOCK_SIZE, (gy + 0.5) * BLOCK_SIZE, drop_item, 1)

        elif button == 3:
            gx, gy = int(wx // BLOCK_SIZE), int(wy // BLOCK_SIZE)
            slot = self.inventory.get_selected_item()

            # --- ЕДА (правая кнопка) ---
            if slot['type'] in (ITEM_APPLE, ITEM_BREAD, ITEM_COOKED_MEAT, ITEM_PIE, ITEM_SOUP,
                                ITEM_MUSHROOM_SOUP, ITEM_COOKED_MUSHROOM,
                                ITEM_PIZZA, ITEM_BURGER, ITEM_SUSHI, ITEM_CAKE,
                                ITEM_SALAD, ITEM_FRIED_POTATOES, ITEM_CARROT_JUICE):
                heal = {
                    ITEM_APPLE: 10, ITEM_BREAD: 20, ITEM_COOKED_MEAT: 35,
                    ITEM_PIE: 50, ITEM_SOUP: 30, ITEM_MUSHROOM_SOUP: 35, ITEM_COOKED_MUSHROOM: 20,
                    ITEM_PIZZA: 60, ITEM_BURGER: 70, ITEM_SUSHI: 50, ITEM_CAKE: 80,
                    ITEM_SALAD: 40, ITEM_FRIED_POTATOES: 30, ITEM_CARROT_JUICE: 25,
                }.get(slot['type'], 20)
                if self.player.hp < self.player.max_hp:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                    slot['count'] -= 1
                    if slot['count'] <= 0:
                        slot['type'] = BLOCK_AIR
                return

            # --- Зелья (правая кнопка) ---
            if slot['type'] in (ITEM_POTION, ITEM_BIG_POTION, ITEM_POTION_REGENERATION,
                                ITEM_POTION_STRENGTH, ITEM_POTION_SPEED, ITEM_POTION_JUMP,
                                ITEM_POTION_NIGHT_VISION, ITEM_POTION_INVISIBILITY,
                                ITEM_POTION_WATER_BREATHING, ITEM_POTION_HASTE):
                heal = 0
                if slot['type'] == ITEM_POTION:
                    heal = 40
                elif slot['type'] == ITEM_BIG_POTION:
                    heal = 80
                elif slot['type'] == ITEM_POTION_REGENERATION:
                    heal = 30
                elif slot['type'] == ITEM_POTION_STRENGTH:
                    self.player.damage_bonus = 30
                elif slot['type'] == ITEM_POTION_SPEED:
                    self.player.speed_bonus = 150
                elif slot['type'] == ITEM_POTION_JUMP:
                    self.player.jump_bonus = 150
                elif slot['type'] == ITEM_POTION_NIGHT_VISION:
                    self.player.night_vision = True
                elif slot['type'] == ITEM_POTION_INVISIBILITY:
                    self.player.invisible = True
                elif slot['type'] == ITEM_POTION_WATER_BREATHING:
                    self.player.water_breathing = True
                elif slot['type'] == ITEM_POTION_HASTE:
                    self.player.haste = True
                if heal > 0:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Посохи (правая кнопка) ---
            if slot['type'] in (ITEM_STAFF_FIRE, ITEM_STAFF_ICE, ITEM_STAFF_LIGHTNING, ITEM_STAFF_HEALING):
                dmg = {
                    ITEM_STAFF_FIRE: 30,
                    ITEM_STAFF_ICE: 25,
                    ITEM_STAFF_LIGHTNING: 40,
                    ITEM_STAFF_HEALING: 50,
                }.get(slot['type'], 0)
                if slot['type'] == ITEM_STAFF_HEALING:
                    self.player.hp = min(self.player.max_hp, self.player.hp + 50)
                else:
                    target = None
                    min_dist = 200
                    for mob in self.mob_manager.mobs:
                        dist = math.hypot(mob.x - self.player.x, mob.y - self.player.y)
                        if dist < min_dist:
                            min_dist = dist
                            target = mob
                    if target:
                        target.hp -= dmg
                        target.vy = -300
                        if target.hp <= 0:
                            self.mob_manager.remove_mob(target)
                return

            # --- Украшения ---
            if slot['type'] in (ITEM_RING_STRENGTH, ITEM_RING_PROTECTION,
                                ITEM_AMULET_REGENERATION, ITEM_AMULET_SPEED,
                                ITEM_NECKLACE_JUMP):
                self.player.damage_bonus += 10
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Свиток телепортации ---
            if slot['type'] == ITEM_SCROLL_TELEPORT:
                self.player.x += random.randint(-500, 500)
                self.player.y += random.randint(-500, 500)
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                return

            # --- Размещение блоков ---
            placeable = [BLOCK_DIRT, BLOCK_GRASS, BLOCK_STONE, BLOCK_WOOD,
                         BLOCK_LEAVES, BLOCK_COPPER_ORE, BLOCK_IRON_ORE,
                         BLOCK_GOLD_ORE, BLOCK_COAL_ORE,
                         BLOCK_TALL_GRASS, BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW,
                         BLOCK_FLOWER_BLUE,
                         BLOCK_PLANKS, BLOCK_BRICK, BLOCK_GLASS, BLOCK_SAND, BLOCK_SANDSTONE,
                         BLOCK_FENCE, BLOCK_LADDER, BLOCK_ANVIL, BLOCK_FURNACE,
                         BLOCK_CHEST, BLOCK_BOOKSHELF, BLOCK_SNOW, BLOCK_CACTUS,
                         BLOCK_SANDSTONE_SMOOTH, BLOCK_OBSIDIAN, BLOCK_GLOWSTONE,
                         BLOCK_SILVER_ORE, BLOCK_PLATINUM_ORE, BLOCK_MITHRIL_ORE, BLOCK_ADAMANTITE_ORE,
                         BLOCK_TITAN_ORE, BLOCK_COBALT_ORE, BLOCK_NETHERITE_ORE, BLOCK_CRYSTAL_ORE,
                         BLOCK_DOOR, BLOCK_WINDOW, BLOCK_SHUTTER, BLOCK_PILLAR,
                         BLOCK_STATUE, BLOCK_CARPET, BLOCK_PAINTING, BLOCK_FRAME, BLOCK_SHELF,
                         BLOCK_BUSH, BLOCK_FERN, BLOCK_VINE,
                         BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY]
            if slot['type'] in placeable and slot['count'] > 0:
                if self.world.get_block(gx, gy) == BLOCK_AIR:
                    block_rect = pygame.Rect(gx * BLOCK_SIZE, gy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    player_rect = pygame.Rect(
                        self.player.x - self.player.w / 2,
                        self.player.y - self.player.h / 2,
                        self.player.w,
                        self.player.h
                    )
                    if not block_rect.colliderect(player_rect):
                        self.world.set_block(gx, gy, slot['type'])
                        slot['count'] -= 1
                        if slot['count'] <= 0:
                            slot['type'] = BLOCK_AIR
