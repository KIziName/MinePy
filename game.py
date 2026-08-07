import pygame
import json
import math
import random
import os
import webbrowser
import time
import sys
import traceback

from blocks import *
from renderer import GameRenderer
from mobs import DroppedItem, Slime, Zombie, DemonEye, Skeleton, Sheep, GameMobManager
from world import GameWorld
from save import SaveManager
from player import GamePlayer
from event_publisher import EventPublisher  

# ------------------- КЛАСС ИНВЕНТАРЯ -------------------
class GameInventory(EventPublisher):  
    def __init__(self):
        super().__init__()  
        self.slots = [{'type': BLOCK_AIR, 'count': 0} for _ in range(40)]
        self.slots[0] = {'type': ITEM_SWORD_WOOD, 'count': 1}
        self.slots[1] = {'type': ITEM_PICKAXE_WOOD, 'count': 1}
        self.slots[2] = {'type': BLOCK_DIRT, 'count': 20}
        self.selected_slot = 0
        self.dragged_slot = None

    def get_selected_item(self):
        return self.slots[self.selected_slot]

    def add_item(self, item_type, count=1):
        try:
            for slot in self.slots:
                if slot['type'] == item_type and slot['count'] < MAX_STACK:
                    add = min(count, MAX_STACK - slot['count'])
                    slot['count'] += add
                    count -= add
                    if count <= 0:
                        self.notify('inventory_updated')
                        return True
            for slot in self.slots:
                if slot['type'] == BLOCK_AIR:
                    slot['type'] = item_type
                    slot['count'] = min(count, MAX_STACK)
                    count -= slot['count']
                    if count <= 0:
                        self.notify('inventory_updated')
                        return True
            self.notify('inventory_updated')
            return False
        except Exception as e:
            print("[Ошибка add_item]", e)
            traceback.print_exc()
            return False

    def can_craft(self, ingredients):
        for itype, count in ingredients:
            total = sum(s['count'] for s in self.slots if s['type'] == itype)
            if total < count:
                return False
        return True

    def can_add_item(self, item_type, count):
        remaining = count
        for slot in self.slots:
            if slot['type'] == item_type:
                remaining -= MAX_STACK - slot['count']
                if remaining <= 0:
                    return True
        for slot in self.slots:
            if slot['type'] == BLOCK_AIR:
                remaining -= MAX_STACK
                if remaining <= 0:
                    return True
        return remaining <= 0

    def craft(self, result, ingredients):
        try:
            if not self.can_craft(ingredients):
                return False
            if not self.can_add_item(result['type'], result['count']):
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
            success = self.add_item(result['type'], result['count'])
            self.notify('inventory_updated')
            return success
        except Exception as e:
            print("[Ошибка craft]", e)
            traceback.print_exc()
            return False

    def swap_slots(self, idx1, idx2):
        self.slots[idx1], self.slots[idx2] = self.slots[idx2], self.slots[idx1]
        self.notify('inventory_updated')

    def get_slot(self, idx):
        return self.slots[idx]

    def to_dict(self):
        return self.slots

    def from_dict(self, data):
        self.slots = data
        self.notify('inventory_updated')


# ------------------- КЛАСС УПРАВЛЕНИЯ ПОГОДОЙ (с изменениями) -------------------
class WeatherManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.weather = WEATHER_CLEAR
        self.weather_alpha = 1.0
        self.transition_time = WEATHER_TRANSITION_TIME
        # Используем длительность для ясной погоды из WEATHER_DURATION
        clear_min, clear_max = WEATHER_DURATION.get('clear', (60, 300))
        self.weather_timer = random.uniform(clear_min, clear_max)
        self.clouds = []
        self.rain_particles = []
        self.snow_particles = []
        self._init_clouds()
        self._init_particles()

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

    def _init_particles(self):
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

    def update(self, dt, screen_width, screen_height):
        try:
            self.screen_width = screen_width
            self.screen_height = screen_height

            self.weather_timer -= dt
            if self.weather_timer <= 0:
                new_weather = random.choice([WEATHER_CLEAR, WEATHER_RAIN, WEATHER_SNOW])
                if new_weather != self.weather:
                    self.weather = new_weather
                    self.weather_alpha = 0.0
                    # Устанавливаем новую длительность в зависимости от погоды
                    if new_weather == WEATHER_CLEAR:
                        duration = WEATHER_DURATION.get('clear', (60, 300))
                    elif new_weather == WEATHER_RAIN:
                        duration = WEATHER_DURATION.get('rain', (30, 180))
                    else:  # WEATHER_SNOW
                        duration = WEATHER_DURATION.get('snow', (30, 120))
                    self.weather_timer = random.uniform(*duration)

            if self.weather_alpha < 1.0:
                self.weather_alpha += dt / self.transition_time
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
        except Exception as e:
            print("[Ошибка weather.update]", e)
            traceback.print_exc()

    def draw_clouds(self, screen):
        try:
            for cloud in self.clouds:
                x, y, w, h = cloud['x'], cloud['y'], cloud['w'], cloud['h']
                pygame.draw.ellipse(screen, (255, 255, 255), (x, y, w, h))
                pygame.draw.ellipse(screen, (255, 255, 255),
                                    (x + w * 0.2, y - h * 0.3, w * 0.6, h * 0.8))
                pygame.draw.ellipse(screen, (255, 255, 255),
                                    (x - w * 0.1, y + h * 0.1, w * 0.3, h * 0.6))
        except Exception as e:
            print("[Ошибка draw_clouds]", e)

    def draw_weather(self, screen):
        try:
            if self.weather == WEATHER_RAIN and self.rain_particles:
                surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                alpha = int(255 * self.weather_alpha)
                for x, y, speed in self.rain_particles:
                    pygame.draw.line(surf, (180, 200, 255, alpha),
                                     (x, y), (x - 2, y + 10), 1)
                screen.blit(surf, (0, 0))
            elif self.weather == WEATHER_SNOW and self.snow_particles:
                surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                alpha = int(255 * self.weather_alpha)
                for x, y, size, speed in self.snow_particles:
                    pygame.draw.circle(surf, (255, 255, 255, alpha),
                                       (int(x), int(y)), int(size))
                screen.blit(surf, (0, 0))
        except Exception as e:
            print("[Ошибка draw_weather]", e)


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
        self.weather = WeatherManager(self.screen_width, self.screen_height)

        self.save_manager = SaveManager(self)
        self.renderer = GameRenderer(self)

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

        self._init_stars()
        self.bg_surfaces = {}
        self._build_background_surfaces()

        self.fps_options = [30, 60, 100, 120]
        self.fps_index = 1
        self.target_fps = self.fps_options[self.fps_index]

    # ---------- инициализация ----------
    def _init_stars(self):
        # Без try/except – ошибка должна быть видна
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
        # Без try/except
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
        try:
            font_name = pygame.font.match_font('arial') or pygame.font.match_font('dejavusans')
            self.font_small = pygame.font.Font(font_name, 13)
            self.font_med = pygame.font.Font(font_name, 18)
            self.font_big = pygame.font.Font(font_name, 32)
            self.font_huge = pygame.font.Font(font_name, 52)
        except Exception as e:
            print("[Ошибка init_fonts]", e)
            traceback.print_exc()

    def is_night(self):
        return NIGHT_START <= (self.day_time % 24000) <= NIGHT_END

    # ---------- переключения ----------
    def toggle_fullscreen(self):
        try:
            self.is_fullscreen = not self.is_fullscreen
            if self.is_fullscreen:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                info = pygame.display.Info()
                self.screen_width, self.screen_height = info.current_w, info.current_h
            else:
                self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.weather = WeatherManager(self.screen_width, self.screen_height)
            self._init_stars()
            self._build_background_surfaces()
            self.renderer.screen = self.screen
            self.renderer.screen_width = self.screen_width
            self.renderer.screen_height = self.screen_height
        except Exception as e:
            print("[Ошибка toggle_fullscreen]", e)
            traceback.print_exc()

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

    # ---------- игровые действия ----------
    def open_github(self):
        try:
            webbrowser.open("https://github.com/KIziName/MinePy")
        except Exception as e:
            print("[Ошибка open_github]", e)

    def start_game(self, is_new=True):
        try:
            if is_new:
                self.reset_game_data()
                self.player.spawn()
            self.game_state = "game"
            self.inventory_open = False
            self.pause_menu_open = False
        except Exception as e:
            print("[Ошибка start_game]", e)
            traceback.print_exc()

    def load_and_start_game(self):
        if self.save_manager.load():
            self.start_game(is_new=False)

    def reset_game_data(self):
        try:
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
            self.weather = WeatherManager(self.screen_width, self.screen_height)
            self._init_stars()
            self._build_background_surfaces()

            if hasattr(self, 'renderer'):
                self.renderer.cleanup()

            self.renderer = GameRenderer(self)
        except Exception as e:
            print("[Ошибка reset_game_data]", e)
            traceback.print_exc()

    def cycle_fps(self):
        # Без try/except
        self.fps_index = (self.fps_index + 1) % len(self.fps_options)
        self.target_fps = self.fps_options[self.fps_index]

    def exit_to_menu(self):
        self.game_state = "menu"
        self.inventory_open = False
        self.pause_menu_open = False

    # ---------- физика ----------
    def update_physics(self, dt):
        if self.game_state != "game":
            return
        if self.inventory_open or self.pause_menu_open:
            return

        try:
            old_day_time = self.day_time
            self.day_time = (self.day_time + DAY_SPEED * dt) % 24000
            if old_day_time > 23000 and self.day_time < 1000:
                self.day_counter += 1
        except Exception as e:
            print("[Ошибка времени суток]", e)

        try:
            self.player.update(self.keys, dt)
        except Exception as e:
            print("[Ошибка обновления игрока]", e)
            traceback.print_exc()

        try:
            self.mob_manager.update(self.player.x, self.player.y,
                                    self.is_night(), self.player, dt)
        except Exception as e:
            print("[Ошибка обновления мобов]", e)
            traceback.print_exc()

        try:
            for item in self.mob_manager.dropped_items[:]:
                if math.hypot(self.player.x - item.x, self.player.y - item.y) < 28:
                    if self.inventory.add_item(item.item_type, item.count):
                        self.mob_manager.dropped_items.remove(item)
        except Exception as e:
            print("[Ошибка сбора предметов]", e)
            traceback.print_exc()

        if self.save_notification_timer > 0:
            self.save_notification_timer -= dt

        try:
            self.weather.update(dt, self.screen_width, self.screen_height)
        except Exception as e:
            print("[Ошибка погоды]", e)
            traceback.print_exc()

    def get_sky_gradient(self, t):
        # Без try/except
        if t < 10000:
            return (30, 80, 200), (135, 206, 250)
        elif t < 12000:
            return (30, 80, 200), (255, 140, 0)
        elif t < 22000:
            return (5, 7, 20), (20, 30, 60)
        else:
            return (5, 7, 20), (255, 180, 100)

    # ---------- обработка событий ----------
    def handle_events(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = False
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event)
        except Exception as e:
            print("[Ошибка handle_events]", e)
            traceback.print_exc()
            pygame.event.clear()

    def _handle_keydown(self, event):
        try:
            if self.game_state == "game":
                if event.key == pygame.K_e:
                    self.toggle_inventory()
                elif event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                                   pygame.K_9, pygame.K_0):
                    if event.key == pygame.K_0:
                        new_slot = 9
                    else:
                        new_slot = event.key - pygame.K_1
                    self.inventory.selected_slot = new_slot
                    self.inventory.notify('selected_slot_changed', slot=new_slot)
            self.keys[event.key] = True
        except Exception as e:
            print("[Ошибка _handle_keydown]", e)

    def _handle_mouse_click(self, event):
        try:
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
                    self.inventory.notify('selected_slot_changed', slot=self.inventory.selected_slot)
            elif event.button == 5:
                if self.game_state == "game" and not self.inventory_open and not self.pause_menu_open:
                    self.inventory.selected_slot = (self.inventory.selected_slot + 1) % 10
                    self.inventory.notify('selected_slot_changed', slot=self.inventory.selected_slot)
        except Exception as e:
            print("[Ошибка _handle_mouse_click]", e)
            traceback.print_exc()

    def check_hotbar_click(self, pos):
        try:
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
                            self.inventory.notify('inventory_updated')
                    else:
                        self.inventory.selected_slot = i
                        self.inventory.notify('selected_slot_changed', slot=i)
                    return True
            return False
        except Exception as e:
            print("[Ошибка check_hotbar_click]", e)
            return False

    def handle_menu_click(self, pos):
        # Без try/except
        for rect, action in self.menu_buttons:
            if rect.collidepoint(pos):
                action()

    def handle_pause_click(self, pos):
        # Без try/except
        for rect, action in self.pause_buttons:
            if rect.collidepoint(pos):
                action()

    def handle_inventory_click(self, pos):
        try:
            if self.check_hotbar_click(pos):
                return

            inv_x, inv_y = 15, 70
            for row in range(3):
                for col in range(10):
                    idx = (row + 1) * 10 + col
                    rect = pygame.Rect(inv_x + 12 + col * 46,
                                       inv_y + 40 + row * 46, 42, 42)
                    if rect.collidepoint(pos):
                        if self.inventory.dragged_slot is None:
                            if self.inventory.get_slot(idx)['type'] != BLOCK_AIR:
                                self.inventory.dragged_slot = idx
                        else:
                            self.inventory.swap_slots(idx, self.inventory.dragged_slot)
                            self.inventory.dragged_slot = None
                            self.inventory.notify('inventory_updated')
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
        except Exception as e:
            print("[Ошибка handle_inventory_click]", e)
            traceback.print_exc()

    def handle_game_click(self, pos, button=1):
        try:
            cam_x = self.player.x - self.screen_width / 2
            cam_y = self.player.y - self.screen_height / 2
            wx, wy = pos[0] + cam_x, pos[1] + cam_y

            if math.hypot(wx - self.player.x, wy - self.player.y) > BUILD_REACH:
                return

            if button == 1:
                self._handle_attack_or_break(wx, wy)
            elif button == 3:
                self._handle_place_or_use(wx, wy)
        except Exception as e:
            print("[Ошибка handle_game_click]", e)
            traceback.print_exc()

    def _handle_attack_or_break(self, wx, wy):
        try:
            self.player.swing_anim = 0.15
            dmg = self.player.get_weapon_damage(self.inventory)

            for mob in self.mob_manager.mobs[:]:
                try:
                    if abs(mob.x - wx) < 30 and abs(mob.y - wy) < 30:
                        mob.hp -= dmg
                        mob.vy = -220
                        mob.vx = 150 if mob.x < self.player.x else -150
                        if mob.hp <= 0:
                            drop_type = None
                            if isinstance(mob, Slime):
                                drop_type, count = ITEM_GEL, random.randint(1, 3)
                            elif isinstance(mob, Zombie):
                                drop_type, count = ITEM_COIN, random.randint(1, 4)
                            elif isinstance(mob, DemonEye):
                                drop_type, count = ITEM_GEL, 1
                            elif isinstance(mob, Skeleton):
                                drop_type, count = ITEM_BONE, random.randint(1, 2)
                            elif isinstance(mob, Sheep):
                                drop_type, count = ITEM_GEL, random.randint(1, 2)
                            if drop_type is not None:
                                self.mob_manager.add_dropped_item(mob.x, mob.y, drop_type, count)
                            self.mob_manager.remove_mob(mob)
                        return
                except Exception as e:
                    print(f"[Ошибка атаки моба]", e)
                    continue

            gx, gy = int(wx // BLOCK_SIZE), int(wy // BLOCK_SIZE)
            b_type = self.world.get_block(gx, gy)
            if b_type != BLOCK_AIR:
                if b_type in NON_SOLID_BLOCKS:
                    if not self.inventory.add_item(b_type, 1):
                        self.mob_manager.add_dropped_item(
                            (gx + 0.5) * BLOCK_SIZE, (gy + 0.5) * BLOCK_SIZE, b_type, 1
                        )
                    self.world.set_block(gx, gy, BLOCK_AIR)
                    return

                drop_item = b_type
                if b_type == BLOCK_STONE and random.random() < 0.2:
                    drop_item = ITEM_FLINT
                elif b_type == BLOCK_LEAVES and random.random() < 0.05:
                    drop_item = ITEM_APPLE
                elif b_type in (BLOCK_COPPER_ORE, BLOCK_IRON_ORE, BLOCK_GOLD_ORE, BLOCK_COAL_ORE,
                                BLOCK_SILVER_ORE, BLOCK_PLATINUM_ORE, BLOCK_MITHRIL_ORE,
                                BLOCK_ADAMANTITE_ORE, BLOCK_TITAN_ORE, BLOCK_COBALT_ORE,
                                BLOCK_NETHERITE_ORE, BLOCK_CRYSTAL_ORE):
                    drop_item = {
                        BLOCK_COPPER_ORE: ITEM_COPPER_INGOT,
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
                        BLOCK_CRYSTAL_ORE: ITEM_CRYSTAL_INGOT
                    }.get(b_type, b_type)
                self.world.set_block(gx, gy, BLOCK_AIR)
                self.mob_manager.add_dropped_item(
                    (gx + 0.5) * BLOCK_SIZE, (gy + 0.5) * BLOCK_SIZE, drop_item, 1
                )
        except Exception as e:
            print("[Ошибка _handle_attack_or_break]", e)
            traceback.print_exc()

    def _handle_place_or_use(self, wx, wy):
        try:
            slot = self.inventory.get_selected_item()

            if slot['type'] in FOOD_HEAL:
                heal = FOOD_HEAL[slot['type']]
                if self.player.hp < self.player.max_hp:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                    slot['count'] -= 1
                    if slot['count'] <= 0:
                        slot['type'] = BLOCK_AIR
                    self.player.notify('health_changed', hp=self.player.hp, max_hp=self.player.max_hp)
                    self.inventory.notify('inventory_updated')
                return

            if slot['type'] in PLACEABLE_BLOCKS and slot['count'] > 0:
                gx, gy = int(wx // BLOCK_SIZE), int(wy // BLOCK_SIZE)
                if self.world.get_block(gx, gy) == BLOCK_AIR:
                    block_rect = pygame.Rect(
                        gx * BLOCK_SIZE, gy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                    )
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
                        self.inventory.notify('inventory_updated')
        except Exception as e:
            print("[Ошибка _handle_place_or_use]", e)
            traceback.print_exc()

    # ---------- методы для отрисовки (обёртки для рендерера) ----------
    def draw_menu(self):
        self.renderer.draw_menu()

    def render(self):
        self.renderer.render()
