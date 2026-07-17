import gc  # Сборщик мусора вызывается ТОЛЬКО при сбросе/выходе в меню
import json
import math
import os
import random
import time
import webbrowser
import customtkinter as ctk

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
BLOCK_SIZE = 32

CHUNK_WIDTH = 16
WORLD_HEIGHT = 60

MAX_STACK = 9999
BUILD_REACH = BLOCK_SIZE * 5.5

GRAVITY = -0.85
PLAYER_SPEED = 5.2
JUMP_FORCE = 11.5

# Настройки FPS
TARGET_FPS = 45
TARGET_FRAME_TIME_MS = 1000 / TARGET_FPS  # ~22.22 мс на кадр

# Путь к папке AppData
APPDATA_DIR = os.environ.get('APPDATA', os.path.expanduser('~'))
APPDATA_PATH = os.path.join(APPDATA_DIR, 'MinePy')
SAVE_FILE_PATH = os.path.join(APPDATA_PATH, 'world_save.json')

# --- БЛОКИ И ПРЕДМЕТЫ ---
BLOCK_AIR = 0
BLOCK_DIRT = 1
BLOCK_GRASS = 2
BLOCK_STONE = 3
BLOCK_WOOD = 4
BLOCK_LEAVES = 11
BLOCK_COPPER_ORE = 14
BLOCK_IRON_ORE = 15
BLOCK_GOLD_ORE = 26
BLOCK_COAL_ORE = 27

ITEM_SWORD_WOOD = 5
ITEM_SWORD_COPPER = 16
ITEM_SWORD_IRON = 17
ITEM_SWORD_GOLD = 28
ITEM_SWORD_DIAMOND = 29

ITEM_PICKAXE_WOOD = 6
ITEM_PICKAXE_COPPER = 18
ITEM_PICKAXE_IRON = 19
ITEM_PICKAXE_GOLD = 30

ITEM_AXE = 7
ITEM_GEL = 8
ITEM_POTION = 9
ITEM_BIG_POTION = 20
ITEM_COIN = 10
ITEM_LENS = 12
ITEM_TORCH = 13
ITEM_BONE = 21

ITEM_COPPER_INGOT = 22
ITEM_IRON_INGOT = 23
ITEM_GOLD_INGOT = 31
ITEM_COAL = 32
ITEM_DIAMOND = 33

ITEM_WOOD_SHIELD = 24
ITEM_IRON_ARMOR = 25

ITEM_ICONS = {
    BLOCK_AIR: " ",
    BLOCK_DIRT: "🟫",
    BLOCK_GRASS: "🟩",
    BLOCK_STONE: "⬛",
    BLOCK_WOOD: "🪵",
    BLOCK_LEAVES: "🍃",
    BLOCK_COPPER_ORE: "🥉",
    BLOCK_IRON_ORE: "🥈",
    BLOCK_GOLD_ORE: "🥇",
    BLOCK_COAL_ORE: "🖤",
    ITEM_SWORD_WOOD: "🗡️",
    ITEM_SWORD_COPPER: "🗡️",
    ITEM_SWORD_IRON: "⚔️",
    ITEM_SWORD_GOLD: "🔱",
    ITEM_SWORD_DIAMOND: "💎",
    ITEM_PICKAXE_WOOD: "⛏️",
    ITEM_PICKAXE_COPPER: "⛏️",
    ITEM_PICKAXE_IRON: "🛠️",
    ITEM_PICKAXE_GOLD: "🛠️",
    ITEM_AXE: "🪓",
    ITEM_GEL: "💧",
    ITEM_POTION: "🧪",
    ITEM_BIG_POTION: "🧫",
    ITEM_COIN: "🪙",
    ITEM_LENS: "👁️",
    ITEM_TORCH: "🔦",
    ITEM_BONE: "🦴",
    ITEM_COPPER_INGOT: "🟧",
    ITEM_IRON_INGOT: "⬜",
    ITEM_GOLD_INGOT: "🟨",
    ITEM_COAL: "⬛",
    ITEM_DIAMOND: "💎",
    ITEM_WOOD_SHIELD: "🛡️",
    ITEM_IRON_ARMOR: "🎽"
}

BLOCK_COLORS = {
    BLOCK_GRASS: "#4CAF50",
    BLOCK_DIRT: "#795548",
    BLOCK_STONE: "#607D8B",
    BLOCK_WOOD: "#5D4037",
    BLOCK_LEAVES: "#2E7D32",
    BLOCK_COPPER_ORE: "#D87040",
    BLOCK_IRON_ORE: "#B0BEC5",
    BLOCK_GOLD_ORE: "#FFD700",
    BLOCK_COAL_ORE: "#212121"
}

CRAFTING_RECIPES = [
    ({'type': ITEM_TORCH, 'count': 4}, [(BLOCK_WOOD, 1), (ITEM_COAL, 1)]),
    ({'type': ITEM_POTION, 'count': 1}, [(ITEM_GEL, 2), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_BIG_POTION, 'count': 1}, [(ITEM_POTION, 2), (ITEM_LENS, 1)]),
    ({'type': ITEM_COPPER_INGOT, 'count': 1}, [(BLOCK_COPPER_ORE, 3)]),
    ({'type': ITEM_IRON_INGOT, 'count': 1}, [(BLOCK_IRON_ORE, 3)]),
    ({'type': ITEM_GOLD_INGOT, 'count': 1}, [(BLOCK_GOLD_ORE, 3)]),
    ({'type': ITEM_SWORD_WOOD, 'count': 1}, [(BLOCK_WOOD, 7)]),
    ({'type': ITEM_SWORD_COPPER, 'count': 1}, [(ITEM_COPPER_INGOT, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_IRON, 'count': 1}, [(ITEM_IRON_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_GOLD, 'count': 1}, [(ITEM_GOLD_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_DIAMOND, 'count': 1}, [(ITEM_DIAMOND, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_WOOD_SHIELD, 'count': 1}, [(BLOCK_WOOD, 10), (ITEM_BONE, 2)]),
    ({'type': ITEM_IRON_ARMOR, 'count': 1}, [(ITEM_IRON_INGOT, 12), (ITEM_COIN, 5)]),
]


class DroppedItem:
    def __init__(self, x, y, item_type, count=1):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.count = count
        self.vy = random.uniform(2, 4)
        self.vx = random.uniform(-1.5, 1.5)
        self.bob_angle = random.uniform(0, 360)

    def update(self, player_x, player_y, get_block_func):
        self.bob_angle += 0.1
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)

        if dist < 140:
            speed = 2.0 if dist > 30 else 4.0
            self.vx += (dx / dist) * speed
            self.vy += (dy / dist) * speed

        self.vy += GRAVITY * 0.4
        self.x += self.vx
        self.y += self.vy

        gx = int(self.x // BLOCK_SIZE)
        gy = int((self.y - 8) // BLOCK_SIZE)

        if get_block_func(gx, gy) != BLOCK_AIR:
            self.y = (gy + 1) * BLOCK_SIZE + 8
            self.vy = 0
            self.vx *= 0.8

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'item_type': self.item_type, 'count': self.count}

    @staticmethod
    def from_dict(data):
        return DroppedItem(data['x'], data['y'], data['item_type'], data['count'])


class Slime:
    def __init__(self, x, y, is_blue=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 32
        self.h = 24
        self.is_blue = is_blue
        self.hp = 25 if is_blue else 15
        self.max_hp = self.hp
        self.damage = 12 if is_blue else 7
        self.speed = 4.0 if is_blue else 3.2
        self.color = "#1E88E5" if is_blue else "#4CAF50"
        self.is_grounded = False
        self.jump_cooldown = random.randint(20, 50)

    def update(self, player_x, player_y, get_block_func):
        dist_x = player_x - self.x
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        if self.is_grounded and self.jump_cooldown <= 0 and abs(dist_x) < 450:
            self.vy = random.uniform(8.5, 11.5)
            self.vx = self.speed if dist_x > 0 else -self.speed
            self.is_grounded = False
            self.jump_cooldown = random.randint(35, 75)

        self.vy += GRAVITY
        self.x += self.vx

        if self.check_collision(get_block_func):
            self.x -= self.vx
            self.vx = 0

        self.y += self.vy
        if self.check_collision(get_block_func):
            if self.vy < 0:
                self.is_grounded = True
                self.vx = 0
            self.y -= self.vy
            self.vy = 0

    def check_collision(self, get_block_func):
        left = int((self.x - self.w / 2) // BLOCK_SIZE)
        right = int((self.x + self.w / 2) // BLOCK_SIZE)
        bottom = int((self.y - self.h / 2) // BLOCK_SIZE)
        top = int((self.y + self.h / 2) // BLOCK_SIZE)

        for gx in range(left, right + 1):
            for gy in range(bottom, top + 1):
                b = get_block_func(gx, gy)
                if b != BLOCK_AIR and b != BLOCK_LEAVES:
                    return True
        return False

    def to_dict(self):
        return {'type': 'Slime', 'x': self.x, 'y': self.y, 'hp': self.hp, 'is_blue': self.is_blue}


class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 24
        self.h = 44
        self.hp = 45
        self.max_hp = 45
        self.damage = 14
        self.speed = 2.2
        self.is_grounded = False

    def update(self, player_x, player_y, get_block_func):
        dist_x = player_x - self.x
        if abs(dist_x) < 600:
            self.vx = self.speed if dist_x > 0 else -self.speed

        self.vy += GRAVITY
        self.x += self.vx
        if self.check_collision(get_block_func):
            self.x -= self.vx
            if self.is_grounded:
                self.vy = 9.5
                self.is_grounded = False

        self.y += self.vy
        if self.check_collision(get_block_func):
            if self.vy < 0:
                self.is_grounded = True
            self.y -= self.vy
            self.vy = 0

    def check_collision(self, get_block_func):
        left = int((self.x - self.w / 2) // BLOCK_SIZE)
        right = int((self.x + self.w / 2) // BLOCK_SIZE)
        bottom = int((self.y - self.h / 2) // BLOCK_SIZE)
        top = int((self.y + self.h / 2) // BLOCK_SIZE)

        for gx in range(left, right + 1):
            for gy in range(bottom, top + 1):
                b = get_block_func(gx, gy)
                if b != BLOCK_AIR and b != BLOCK_LEAVES:
                    return True
        return False

    def to_dict(self):
        return {'type': 'Zombie', 'x': self.x, 'y': self.y, 'hp': self.hp}


class DemonEye:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 28
        self.h = 28
        self.hp = 30
        self.max_hp = 30
        self.damage = 12
        self.dash_timer = random.randint(40, 80)

    def update(self, player_x, player_y, get_block_func):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)
        self.dash_timer -= 1

        if self.dash_timer <= 0 and dist > 0:
            self.vx = (dx / dist) * 8.0
            self.vy = (dy / dist) * 8.0
            self.dash_timer = random.randint(60, 100)
        else:
            self.vx *= 0.95
            self.vy *= 0.95
            if dist > 0:
                self.vx += (dx / dist) * 0.2
                self.vy += (dy / dist) * 0.2

        self.x += self.vx
        self.y += self.vy

    def to_dict(self):
        return {'type': 'DemonEye', 'x': self.x, 'y': self.y, 'hp': self.hp}


class Skeleton:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 22
        self.h = 42
        self.hp = 35
        self.max_hp = 35
        self.damage = 18
        self.speed = 2.8
        self.is_grounded = False

    def update(self, player_x, player_y, get_block_func):
        dist_x = player_x - self.x
        if abs(dist_x) < 550:
            self.vx = self.speed if dist_x > 0 else -self.speed

        self.vy += GRAVITY
        self.x += self.vx
        if self.check_collision(get_block_func):
            self.x -= self.vx
            if self.is_grounded:
                self.vy = 10.0
                self.is_grounded = False

        self.y += self.vy
        if self.check_collision(get_block_func):
            if self.vy < 0:
                self.is_grounded = True
            self.y -= self.vy
            self.vy = 0

    def check_collision(self, get_block_func):
        left = int((self.x - self.w / 2) // BLOCK_SIZE)
        right = int((self.x + self.w / 2) // BLOCK_SIZE)
        bottom = int((self.y - self.h / 2) // BLOCK_SIZE)
        top = int((self.y + self.h / 2) // BLOCK_SIZE)

        for gx in range(left, right + 1):
            for gy in range(bottom, top + 1):
                b = get_block_func(gx, gy)
                if b != BLOCK_AIR and b != BLOCK_LEAVES:
                    return True
        return False

    def to_dict(self):
        return {'type': 'Skeleton', 'x': self.x, 'y': self.y, 'hp': self.hp}


class MinePyGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MinePy: Expanded Universe (2D)")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.is_fullscreen = False

        self.game_state = "menu"
        self.chunks = {}
        self.mobs = []
        self.dropped_items = []
        self.reset_game_data()

        self.show_main_menu()
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)

    def toggle_fullscreen_mode(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

        self.update_idletasks()
        SCREEN_WIDTH = self.winfo_width()
        SCREEN_HEIGHT = self.winfo_height()

        if self.game_state == "game":
            self.canvas.config(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
            if self.pause_menu_open:
                self.setup_pause_menu()
                self.pause_window.place(relx=0.5, rely=0.5, anchor="center")
        elif self.game_state == "menu":
            self.show_main_menu()

    def reset_game_data(self):
        self.inventory_open = False
        self.pause_menu_open = False
        self.swing_anim = 0
        self.day_time = 3000

        self.fps_counter = 0
        self.current_fps = 0
        self.last_fps_time = time.time()

        self.inventory = [{'type': BLOCK_AIR, 'count': 0} for _ in range(40)]
        self.inventory[0] = {'type': ITEM_SWORD_WOOD, 'count': 1}
        self.inventory[1] = {'type': ITEM_PICKAXE_WOOD, 'count': 1}

        self.selected_slot = 0
        self.dragged_slot = None
        self.mouse_x = 0
        self.mouse_y = 0

        self.hp = 100
        self.max_hp = 100
        self.invulnerable_timer = 0

        self.player_x = 0
        self.player_y = 0
        self.player_vx = 0
        self.player_vy = 0
        self.player_w = 20
        self.player_h = 42

        self.facing_right = True
        self.anim_frame = 0
        self.is_grounded = False

        self.keys = {}
        self.chunks.clear()
        self.mobs.clear()
        self.dropped_items.clear()
        self.spawn_timer = 0

        gc.collect()

    def save_world(self):
        if not os.path.exists(APPDATA_PATH):
            os.makedirs(APPDATA_PATH)

        mobs_data = [m.to_dict() for m in self.mobs]
        items_data = [i.to_dict() for i in self.dropped_items]
        chunks_data = {str(k): v for k, v in self.chunks.items()}

        save_data = {
            'player_x': self.player_x,
            'player_y': self.player_y,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'day_time': self.day_time,
            'inventory': self.inventory,
            'selected_slot': self.selected_slot,
            'chunks': chunks_data,
            'mobs': mobs_data,
            'dropped_items': items_data
        }

        try:
            with open(SAVE_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print("Сцена мира успешно сохранена!")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_world(self):
        if not os.path.exists(SAVE_FILE_PATH):
            return False

        try:
            with open(SAVE_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.player_x = data['player_x']
            self.player_y = data['player_y']
            self.hp = data['hp']
            self.max_hp = data['max_hp']
            self.day_time = data['day_time']
            self.inventory = data['inventory']
            self.selected_slot = data['selected_slot']

            self.chunks = {int(k): v for k, v in data['chunks'].items()}

            self.mobs.clear()
            for md in data['mobs']:
                m_type = md['type']
                if m_type == 'Slime':
                    m = Slime(md['x'], md['y'], md.get('is_blue', False))
                elif m_type == 'Zombie':
                    m = Zombie(md['x'], md['y'])
                elif m_type == 'DemonEye':
                    m = DemonEye(md['x'], md['y'])
                elif m_type == 'Skeleton':
                    m = Skeleton(md['x'], md['y'])

                m.hp = md['hp']
                self.mobs.append(m)

            self.dropped_items = [
                DroppedItem.from_dict(item_data)
                for item_data in data['dropped_items']
            ]

            return True
        except Exception as e:
            print(f"Ошибка загрузки сохранения: {e}")
            return False

    def is_night(self):
        return 11000 <= (self.day_time % 24000) <= 23000

    def get_land_height(self, global_gx):
        sin_wave = math.sin(global_gx * 0.04) * 6
        cos_wave = math.cos(global_gx * 0.1) * 3
        return int(22 + sin_wave + cos_wave)

    def get_chunk(self, chunk_x):
        if chunk_x in self.chunks:
            return self.chunks[chunk_x]

        chunk = [
            [BLOCK_AIR for _ in range(CHUNK_WIDTH)]
            for _ in range(WORLD_HEIGHT)
        ]

        for local_x in range(CHUNK_WIDTH):
            global_gx = chunk_x * CHUNK_WIDTH + local_x
            ground_h = self.get_land_height(global_gx)

            for gy in range(ground_h):
                if gy == ground_h - 1:
                    chunk[gy][local_x] = BLOCK_GRASS
                elif gy > ground_h - 6:
                    chunk[gy][local_x] = BLOCK_DIRT
                else:
                    r = random.random()
                    if r < 0.03 and gy < ground_h - 12:
                        chunk[gy][local_x] = BLOCK_GOLD_ORE
                    elif r < 0.06 and gy < ground_h - 10:
                        chunk[gy][local_x] = BLOCK_IRON_ORE
                    elif r < 0.10 and gy < ground_h - 7:
                        chunk[gy][local_x] = BLOCK_COPPER_ORE
                    elif r < 0.16 and gy < ground_h - 5:
                        chunk[gy][local_x] = BLOCK_COAL_ORE
                    else:
                        chunk[gy][local_x] = BLOCK_STONE

            if random.random() < 0.12 and ground_h < WORLD_HEIGHT - 8:
                tree_h = random.randint(4, 6)
                for th in range(tree_h):
                    chunk[ground_h + th][local_x] = BLOCK_WOOD

                top_y = ground_h + tree_h
                for lx in range(-2, 3):
                    for ly in range(-2, 2):
                        if abs(lx) == 2 and abs(ly) == 2:
                            continue
                        gx_leaf = local_x + lx
                        gy_leaf = top_y + ly
                        if 0 <= gx_leaf < CHUNK_WIDTH and 0 <= gy_leaf < WORLD_HEIGHT:
                            if chunk[gy_leaf][gx_leaf] == BLOCK_AIR:
                                chunk[gy_leaf][gx_leaf] = BLOCK_LEAVES

        self.chunks[chunk_x] = chunk
        return chunk

    def get_block(self, global_gx, gy):
        if gy < 0 or gy >= WORLD_HEIGHT:
            return BLOCK_AIR
        chunk = self.get_chunk(global_gx // CHUNK_WIDTH)
        return chunk[gy][global_gx % CHUNK_WIDTH]

    def set_block(self, global_gx, gy, block_type):
        if 0 <= gy < WORLD_HEIGHT:
            chunk = self.get_chunk(global_gx // CHUNK_WIDTH)
            chunk[gy][global_gx % CHUNK_WIDTH] = block_type

    def open_github(self):
        webbrowser.open("https://github.com/KIziName/MinePy")

    def show_main_menu(self):
        self.game_state = "menu"
        for w in self.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#0b132b")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="написанно на Python 3.14", font=("Arial", 16, "italic"), text_color="#8d99ae"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            frame, text="MinePy 2D", font=("Impact", 64), text_color="#FFD700"
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            frame, text="Автор: KIziName | Версия: 0.1", font=("Arial", 14, "bold"), text_color="#e0e1dd"
        ).pack(pady=(0, 5))

        ctk.CTkButton(
            frame, text="GitHub: MinePy", font=("Arial", 13, "underline"),
            fg_color="transparent", hover_color="#1c2541", text_color="#4cc9f0", command=self.open_github
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            frame, text="НОВАЯ ИГРА", font=("Arial", 18, "bold"),
            width=260, height=45, fg_color="#2e7d32", hover_color="#1b5e20", command=self.start_game
        ).pack(pady=5)

        save_exists = os.path.exists(SAVE_FILE_PATH)
        load_btn_color = "#1565C0" if save_exists else "#3a506b"
        btn_state = "normal" if save_exists else "disabled"

        ctk.CTkButton(
            frame, text="ЗАГРУЗИТЬ МИР", font=("Arial", 16, "bold"),
            width=260, height=40, fg_color=load_btn_color, hover_color="#0D47A1",
            state=btn_state, command=self.load_and_start_game
        ).pack(pady=5)

        fs_text = "🗔 Оконный режим" if self.is_fullscreen else "📺 Полноэкранный режим"
        ctk.CTkButton(
            frame, text=fs_text, font=("Arial", 15, "bold"),
            width=260, height=40, fg_color="#ffb703", text_color="#000000", hover_color="#fb8500",
            command=self.toggle_fullscreen_mode
        ).pack(pady=5)

        ctk.CTkButton(
            frame, text="ВЫХОД", font=("Arial", 16), fg_color="#d32f2f", hover_color="#9a0007",
            width=260, height=40, command=self.destroy
        ).pack(pady=10)

        gc.collect()

    def load_and_start_game(self):
        if self.load_world():
            self.start_game(is_new=False)

    def start_game(self, is_new=True):
        if is_new:
            self.reset_game_data()
            self.spawn_player()

        self.game_state = "game"
        for w in self.winfo_children():
            w.destroy()

        self.canvas = ctk.CTkCanvas(
            self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#5c94fc", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.hotbar_frame = ctk.CTkFrame(
            self, fg_color="#1c2541", corner_radius=8, border_width=2, border_color="#3a506b"
        )
        self.hotbar_frame.place(x=15, y=15)

        self.hotbar_slots = []
        for i in range(10):
            btn = ctk.CTkButton(
                self.hotbar_frame, text=" ", width=46, height=46, corner_radius=6,
                font=("Arial", 16), fg_color="#0b132b", border_width=2, border_color="#3a506b"
            )
            btn.pack(side="left", padx=2, pady=4)
            btn.bind("<Button-1>", lambda e, idx=i: self.start_drag(idx))
            self.hotbar_slots.append(btn)

        self.inv_window = ctk.CTkFrame(
            self, width=580, height=420, fg_color="#0b132b", corner_radius=12,
            border_width=3, border_color="#FFD700"
        )
        self.inv_buttons = {}

        self.pause_window = ctk.CTkFrame(
            self, width=320, height=280, fg_color="#0b132b", corner_radius=12,
            border_width=3, border_color="#3a506b"
        )
        self.setup_pause_menu()

        self.update_ui()
        self.game_loop()

    def setup_pause_menu(self):
        for w in self.pause_window.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.pause_window, text="ПАУЗА", font=("Impact", 28), text_color="#FFD700"
        ).pack(pady=10)

        ctk.CTkButton(
            self.pause_window, text="Продолжить", fg_color="#2e7d32", hover_color="#1b5e20",
            font=("Arial", 15), command=self.toggle_pause_menu
        ).pack(pady=4, padx=20, fill="x")

        fs_text = "🗔 Оконный режим" if self.is_fullscreen else "📺 Полноэкранный режим"
        ctk.CTkButton(
            self.pause_window, text=fs_text, fg_color="#ffb703", text_color="#000000", hover_color="#fb8500",
            font=("Arial", 15, "bold"), command=self.toggle_fullscreen_mode
        ).pack(pady=4, padx=20, fill="x")

        ctk.CTkButton(
            self.pause_window, text="Сохранить мир", fg_color="#1565C0", hover_color="#0D47A1",
            font=("Arial", 15), command=self.save_world
        ).pack(pady=4, padx=20, fill="x")

        ctk.CTkButton(
            self.pause_window, text="Главное меню", fg_color="#d32f2f", hover_color="#9a0007",
            font=("Arial", 15), command=self.show_main_menu
        ).pack(pady=4, padx=20, fill="x")

    def toggle_inventory(self):
        if self.pause_menu_open:
            return

        self.inventory_open = not self.inventory_open
        if self.inventory_open:
            self.inv_window.place(x=15, y=75)
            self.render_inventory()
        else:
            self.inv_window.place_forget()

    def toggle_pause_menu(self):
        if self.inventory_open:
            self.toggle_inventory()

        self.pause_menu_open = not self.pause_menu_open
        if self.pause_menu_open:
            self.pause_window.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.pause_window.place_forget()

    def render_inventory(self):
        for w in self.inv_window.winfo_children():
            w.destroy()
        self.inv_buttons.clear()

        ctk.CTkLabel(
            self.inv_window, text="ИНВЕНТАРЬ И КРАФТ", font=("Arial", 14, "bold"), text_color="#FFD700"
        ).pack(pady=5)

        inv_grid = ctk.CTkFrame(self.inv_window, fg_color="#1c2541", corner_radius=8)
        inv_grid.pack(padx=10, pady=5)

        for row in range(3):
            for col in range(10):
                slot_idx = (row + 1) * 10 + col
                item = self.inventory[slot_idx]

                icon = ITEM_ICONS.get(item['type'], " ")
                count = f"\n{item['count']}" if item['count'] > 1 else ""
                display_text = f"{icon}{count}" if item['type'] != BLOCK_AIR else " "

                btn = ctk.CTkButton(
                    inv_grid, text=display_text, width=46, height=46, font=("Arial", 14, "bold"),
                    fg_color="#0b132b", hover_color="#1f4068", border_width=2, border_color="#3a506b"
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                btn.bind("<Button-1>", lambda e, idx=slot_idx: self.start_drag(idx))
                self.inv_buttons[slot_idx] = btn

        craft_frame = ctk.CTkScrollableFrame(
            self.inv_window, fg_color="#1c2541", corner_radius=8, height=140
        )
        craft_frame.pack(padx=10, pady=5, fill="x")

        for result, ingredients in CRAFTING_RECIPES:
            icon = ITEM_ICONS.get(result['type'], "?")
            req_text = " + ".join([
                f"{count} {ITEM_ICONS.get(itype, '')}"
                for itype, count in ingredients
            ])

            can_craft = self.can_craft(ingredients)
            btn_color = "#2e7d32" if can_craft else "#3a506b"

            line_frame = ctk.CTkFrame(craft_frame, fg_color="transparent")
            line_frame.pack(fill="x", pady=2)

            btn = ctk.CTkButton(
                line_frame, text=f"{icon} x{result['count']}  ({req_text})", font=("Arial", 12), height=28,
                fg_color=btn_color, command=lambda r=result, ing=ingredients: self.craft_item(r, ing)
            )
            btn.pack(side="left", fill="x", expand=True)

    def can_craft(self, ingredients):
        for itype, count in ingredients:
            total = sum(slot['count'] for slot in self.inventory if slot['type'] == itype)
            if total < count:
                return False
        return True

    def craft_item(self, result, ingredients):
        if not self.can_craft(ingredients):
            return

        for itype, count in ingredients:
            needed = count
            for slot in self.inventory:
                if slot['type'] == itype:
                    take = min(needed, slot['count'])
                    slot['count'] -= take
                    needed -= take
                    if slot['count'] <= 0:
                        slot['type'] = BLOCK_AIR
                    if needed <= 0:
                        break

        self.add_to_inventory(result['type'], result['count'])
        self.render_inventory()

    def on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_mouse_drag(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def start_drag(self, slot_idx):
        if self.inventory[slot_idx]['type'] != BLOCK_AIR:
            self.dragged_slot = slot_idx
            if slot_idx < 10:
                self.selected_slot = slot_idx
            self.update_ui()

    def get_slot_under_mouse(self):
        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty()

        for idx, btn in enumerate(self.hotbar_slots):
            bx = btn.winfo_rootx() - root_x
            by = btn.winfo_rooty() - root_y
            if bx <= self.mouse_x <= bx + 46 and by <= self.mouse_y <= by + 46:
                return idx

        if self.inventory_open:
            for idx, btn in self.inv_buttons.items():
                bx = btn.winfo_rootx() - root_x
                by = btn.winfo_rooty() - root_y
                if bx <= self.mouse_x <= bx + 46 and by <= self.mouse_y <= by + 46:
                    return idx

        return None

    def on_mouse_release(self, event):
        if self.dragged_slot is not None:
            target_slot = self.get_slot_under_mouse()

            if target_slot is not None:
                self.inventory[target_slot], self.inventory[self.dragged_slot] = (
                    self.inventory[self.dragged_slot],
                    self.inventory[target_slot]
                )
            else:
                item = self.inventory[self.dragged_slot]
                if item['type'] != BLOCK_AIR:
                    self.dropped_items.append(
                        DroppedItem(self.player_x, self.player_y + 10, item['type'], item['count'])
                    )
                    self.inventory[self.dragged_slot] = {'type': BLOCK_AIR, 'count': 0}

            self.dragged_slot = None
            if self.inventory_open:
                self.render_inventory()
            self.update_ui()

    def update_ui(self):
        for i in range(10):
            item = self.inventory[i]
            btn = self.hotbar_slots[i]

            border_c = "#FFD700" if i == self.selected_slot else "#3a506b"
            width = 3 if i == self.selected_slot else 1

            icon = ITEM_ICONS.get(item['type'], " ")
            cnt = f"\n{item['count']}" if item['count'] > 1 else ""
            txt = f"{icon}{cnt}" if item['type'] != BLOCK_AIR else " "

            btn.configure(text=txt, border_color=border_c, border_width=width)

    def add_to_inventory(self, item_type, count=1):
        for slot in self.inventory:
            if slot['type'] == item_type and slot['count'] < MAX_STACK:
                add = min(count, MAX_STACK - slot['count'])
                slot['count'] += add
                count -= add
                if count <= 0:
                    self.update_ui()
                    return True

        for slot in self.inventory:
            if slot['type'] == BLOCK_AIR:
                slot['type'] = item_type
                slot['count'] = min(count, MAX_STACK)
                count -= slot['count']
                if count <= 0:
                    self.update_ui()
                    return True

        return False

    def get_player_weapon_damage(self):
        slot = self.inventory[self.selected_slot]
        itype = slot['type']

        if itype == ITEM_SWORD_WOOD:
            return 12
        if itype == ITEM_SWORD_COPPER:
            return 18
        if itype == ITEM_SWORD_IRON:
            return 28
        if itype == ITEM_SWORD_GOLD:
            return 38
        if itype == ITEM_SWORD_DIAMOND:
            return 55

        return 6

    def on_canvas_click(self, event):
        if self.inventory_open or self.pause_menu_open:
            return

        cam_x = self.player_x - SCREEN_WIDTH / 2
        cam_y = self.player_y - SCREEN_HEIGHT / 2
        wx = event.x + cam_x
        wy = (SCREEN_HEIGHT - event.y) + cam_y

        if math.hypot(wx - self.player_x, wy - self.player_y) > BUILD_REACH:
            return

        self.swing_anim = 8
        slot = self.inventory[self.selected_slot]

        if slot['type'] in [ITEM_POTION, ITEM_BIG_POTION]:
            heal_amount = 40 if slot['type'] == ITEM_POTION else 80
            if self.hp < self.max_hp:
                self.hp = min(self.max_hp, self.hp + heal_amount)
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                self.update_ui()
            return

        dmg = self.get_player_weapon_damage()

        for mob in self.mobs[:]:
            if abs(mob.x - wx) < 30 and abs(mob.y - wy) < 30:
                mob.hp -= dmg
                mob.vy = 4.0

                if mob.hp <= 0:
                    if isinstance(mob, Slime):
                        drop = DroppedItem(mob.x, mob.y, ITEM_GEL, random.randint(1, 3))
                    elif isinstance(mob, Zombie):
                        drop = DroppedItem(mob.x, mob.y, ITEM_COIN, random.randint(1, 4))
                    elif isinstance(mob, DemonEye):
                        drop = DroppedItem(mob.x, mob.y, ITEM_LENS, 1)
                    elif isinstance(mob, Skeleton):
                        drop = DroppedItem(mob.x, mob.y, ITEM_BONE, random.randint(1, 2))

                    self.dropped_items.append(drop)
                    self.mobs.remove(mob)
                return

        gx = int(wx // BLOCK_SIZE)
        gy = int(wy // BLOCK_SIZE)
        b_type = self.get_block(gx, gy)

        if b_type != BLOCK_AIR:
            self.set_block(gx, gy, BLOCK_AIR)
            drop_item = b_type
            if b_type == BLOCK_COAL_ORE:
                drop_item = ITEM_COAL

            drop_x = (gx + 0.5) * BLOCK_SIZE
            drop_y = (gy + 0.5) * BLOCK_SIZE
            self.dropped_items.append(DroppedItem(drop_x, drop_y, drop_item, 1))

    def on_right_click(self, event):
        if self.inventory_open or self.pause_menu_open:
            return

        cam_x = self.player_x - SCREEN_WIDTH / 2
        cam_y = self.player_y - SCREEN_HEIGHT / 2
        wx = event.x + cam_x
        wy = (SCREEN_HEIGHT - event.y) + cam_y

        if math.hypot(wx - self.player_x, wy - self.player_y) > BUILD_REACH:
            return

        gx = int(wx // BLOCK_SIZE)
        gy = int(wy // BLOCK_SIZE)
        slot = self.inventory[self.selected_slot]

        placeable = [
            BLOCK_DIRT, BLOCK_GRASS, BLOCK_STONE, BLOCK_WOOD,
            BLOCK_LEAVES, BLOCK_COPPER_ORE, BLOCK_IRON_ORE,
            BLOCK_GOLD_ORE, BLOCK_COAL_ORE
        ]

        if slot['type'] in placeable and slot['count'] > 0:
            if self.get_block(gx, gy) == BLOCK_AIR:
                self.set_block(gx, gy, slot['type'])
                slot['count'] -= 1
                if slot['count'] <= 0:
                    slot['type'] = BLOCK_AIR
                self.update_ui()

    def spawn_player(self):
        self.player_x = 0
        ground_h = self.get_land_height(0)
        self.player_y = (ground_h + 3) * BLOCK_SIZE
        self.player_vx = 0
        self.player_vy = 0

    def spawn_mobs_dynamically(self):
        self.spawn_timer += 1
        if self.spawn_timer > 120:
            self.spawn_timer = 0

            if len(self.mobs) < 7:
                offset = random.choice([-1, 1]) * random.randint(450, 750)
                sx = self.player_x + offset
                gx = int(sx // BLOCK_SIZE)
                sy = (self.get_land_height(gx) + 3) * BLOCK_SIZE

                if self.is_night():
                    r = random.random()
                    if r < 0.4:
                        self.mobs.append(Zombie(sx, sy))
                    elif r < 0.7:
                        self.mobs.append(DemonEye(sx, sy + 100))
                    else:
                        self.mobs.append(Skeleton(sx, sy))
                else:
                    is_blue_slime = random.random() < 0.35
                    self.mobs.append(Slime(sx, sy, is_blue=is_blue_slime))

    def get_sky_color(self):
        t = self.day_time % 24000
        if t < 10000:
            return "#5c94fc"
        elif t < 12000:
            return "#E07A5F"
        elif t < 22000:
            return "#050714"
        else:
            return "#F4A261"

    def update_physics(self):
        if self.inventory_open or self.pause_menu_open:
            return

        self.day_time = (self.day_time + 2) % 24000

        if self.swing_anim > 0:
            self.swing_anim -= 1

        self.player_vx = 0

        if self.keys.get("a") or self.keys.get("left"):
            self.player_vx = -PLAYER_SPEED
            self.facing_right = False

        if self.keys.get("d") or self.keys.get("right"):
            self.player_vx = PLAYER_SPEED
            self.facing_right = True

        jump_key = self.keys.get("w") or self.keys.get("space") or self.keys.get("up")
        if jump_key and self.is_grounded:
            self.player_vy = JUMP_FORCE
            self.is_grounded = False

        self.player_vy += GRAVITY

        self.player_x += self.player_vx
        if self.check_player_collision():
            self.player_x -= self.player_vx

        self.player_y += self.player_vy
        if self.check_player_collision():
            if self.player_vy < 0:
                self.is_grounded = True
            self.player_y -= self.player_vy
            self.player_vy = 0

        if self.player_vx != 0:
            self.anim_frame += 0.35

        for mob in self.mobs[:]:
            mob.update(self.player_x, self.player_y, self.get_block)

            if self.invulnerable_timer == 0:
                if abs(self.player_x - mob.x) < 22 and abs(self.player_y - mob.y) < 26:
                    self.hp -= mob.damage
                    self.invulnerable_timer = 25
                    self.player_vy = 7
                    self.player_vx = 8 if self.player_x > mob.x else -8

                    if self.hp <= 0:
                        self.spawn_player()
                        self.hp = self.max_hp

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

        for item in self.dropped_items[:]:
            item.update(self.player_x, self.player_y, self.get_block)
            if math.hypot(self.player_x - item.x, self.player_y - item.y) < 28:
                if self.add_to_inventory(item.item_type, item.count):
                    self.dropped_items.remove(item)

        self.spawn_mobs_dynamically()

    def check_player_collision(self):
        left = int((self.player_x - self.player_w / 2) // BLOCK_SIZE)
        right = int((self.player_x + self.player_w / 2) // BLOCK_SIZE)
        bottom = int((self.player_y - self.player_h / 2) // BLOCK_SIZE)
        top = int((self.player_y + self.player_h / 2) // BLOCK_SIZE)

        for gx in range(left, right + 1):
            for gy in range(bottom, top + 1):
                b = self.get_block(gx, gy)
                if b != BLOCK_AIR and b != BLOCK_LEAVES:
                    return True
        return False

    def render(self):
        if self.game_state != "game":
            return

        sky_c = self.get_sky_color()
        self.canvas.configure(bg=sky_c)
        self.canvas.delete("all")

        cam_x = self.player_x - SCREEN_WIDTH / 2
        cam_y = self.player_y - SCREEN_HEIGHT / 2

        t = self.day_time
        sun_angle = ((t % 24000) / 24000.0) * math.pi * 2 - math.pi / 2
        sun_x = SCREEN_WIDTH / 2 + math.cos(sun_angle) * (SCREEN_WIDTH * 0.45)
        sun_y = SCREEN_HEIGHT / 2 + math.sin(sun_angle) * (SCREEN_HEIGHT * 0.4)

        if sun_y < SCREEN_HEIGHT - 100:
            if 0 <= t < 12000:
                self.canvas.create_oval(
                    sun_x - 25, sun_y - 25, sun_x + 25, sun_y + 25,
                    fill="#FFD700", outline="#FFA000", width=3
                )
            else:
                self.canvas.create_oval(
                    sun_x - 20, sun_y - 20, sun_x + 20, sun_y + 20,
                    fill="#ECEFF1", outline="#CFD8DC", width=2
                )

        curr_cam_gx = int(cam_x // BLOCK_SIZE)
        curr_cam_gy = int(cam_y // BLOCK_SIZE)

        start_gx = curr_cam_gx - 1
        end_gx = curr_cam_gx + int(SCREEN_WIDTH // BLOCK_SIZE) + 2
        start_gy = max(0, curr_cam_gy - 1)
        end_gy = min(WORLD_HEIGHT, curr_cam_gy + int(SCREEN_HEIGHT // BLOCK_SIZE) + 2)

        for gy in range(start_gy, end_gy):
            for gx in range(start_gx, end_gx):
                b_type = self.get_block(gx, gy)
                if b_type != BLOCK_AIR:
                    sx = gx * BLOCK_SIZE - cam_x
                    sy = SCREEN_HEIGHT - ((gy + 1) * BLOCK_SIZE - cam_y)
                    color = BLOCK_COLORS.get(b_type, "#555")
                    outline = "#1a1a1a" if b_type != BLOCK_LEAVES else "#1B5E20"

                    self.canvas.create_rectangle(
                        sx, sy, sx + BLOCK_SIZE, sy + BLOCK_SIZE,
                        fill=color, outline=outline
                    )

        for item in self.dropped_items:
            sx = item.x - cam_x
            bob_y = math.sin(item.bob_angle) * 4
            sy = SCREEN_HEIGHT - (item.y - cam_y) + bob_y

            self.canvas.create_oval(
                sx - 10, sy - 10, sx + 10, sy + 10,
                fill="#FFFFFF", outline=""
            )
            icon = ITEM_ICONS.get(item.item_type, "❓")
            self.canvas.create_text(sx, sy, text=icon, font=("Arial", 16))

        for mob in self.mobs:
            sx = mob.x - cam_x
            sy = SCREEN_HEIGHT - (mob.y - cam_y)

            if isinstance(mob, Slime):
                self.canvas.create_oval(
                    sx - 16, sy - 12, sx + 16, sy + 12,
                    fill=mob.color, outline="#ffffff", width=2
                )
            elif isinstance(mob, Zombie):
                self.canvas.create_rectangle(
                    sx - 12, sy - 22, sx + 12, sy + 22,
                    fill="#388E3C", outline="#1B5E20", width=2
                )
                self.canvas.create_rectangle(
                    sx - 10, sy - 20, sx + 10, sy - 8,
                    fill="#5D4037"
                )
            elif isinstance(mob, DemonEye):
                self.canvas.create_oval(
                    sx - 14, sy - 14, sx + 14, sy + 14,
                    fill="#ECEFF1", outline="#D32F2F", width=2
                )
                self.canvas.create_oval(
                    sx - 6, sy - 6, sx + 6, sy + 6,
                    fill="#D32F2F"
                )
            elif isinstance(mob, Skeleton):
                self.canvas.create_rectangle(
                    sx - 11, sy - 21, sx + 11, sy + 21,
                    fill="#E0E0E0", outline="#9E9E9E", width=2
                )

            bar_w = 30
            hp_pct = max(0, mob.hp / mob.max_hp)

            self.canvas.create_rectangle(
                sx - bar_w / 2, sy - mob.h / 2 - 10,
                sx + bar_w / 2, sy - mob.h / 2 - 6,
                fill="#333"
            )
            if hp_pct > 0:
                self.canvas.create_rectangle(
                    sx - bar_w / 2, sy - mob.h / 2 - 10,
                    sx - bar_w / 2 + (bar_w * hp_pct), sy - mob.h / 2 - 6,
                    fill="#76FF03"
                )

        px = self.player_x - cam_x
        py = SCREEN_HEIGHT - (self.player_y - cam_y)

        if self.invulnerable_timer % 4 < 2:
            face_dir = 1 if self.facing_right else -1
            leg_step = math.sin(self.anim_frame) * 6 if self.is_grounded and self.player_vx != 0 else 0

            self.canvas.create_line(
                px - 4, py + 8, px - 4 + leg_step, py + 21,
                fill="#0D47A1", width=5
            )
            self.canvas.create_line(
                px + 4, py + 8, px + 4 - leg_step, py + 21,
                fill="#1565C0", width=5
            )
            self.canvas.create_rectangle(
                px - 9, py - 6, px + 9, py + 8,
                fill="#1976D2", outline="#0D47A1"
            )
            self.canvas.create_oval(
                px - 9, py - 23, px + 9, py - 6,
                fill="#FFCC80", outline="#E65100"
            )

            swing_off = (10 - self.swing_anim) * 2 if self.swing_anim > 0 else 0
            tool_x = px + ((12 + swing_off) * face_dir)
            tool_y = py - 4 + swing_off

            self.canvas.create_line(
                px + (4 * face_dir), py, tool_x, tool_y,
                fill="#795548", width=4
            )

            curr_item = self.inventory[self.selected_slot]['type']
            if curr_item != BLOCK_AIR:
                self.canvas.create_text(
                    tool_x, tool_y - 8,
                    text=ITEM_ICONS.get(curr_item, ""),
                    font=("Arial", 16)
                )

        hp_x = SCREEN_WIDTH - 220
        hp_y = 25
        hp_pct = max(0, self.hp / self.max_hp)

        self.canvas.create_rectangle(
            hp_x, hp_y, hp_x + 180, hp_y + 22,
            fill="#1c2541", outline="#3a506b", width=2
        )
        if hp_pct > 0:
            self.canvas.create_rectangle(
                hp_x + 2, hp_y + 2, hp_x + 2 + (176 * hp_pct), hp_y + 20,
                fill="#e63946", outline=""
            )
        self.canvas.create_text(
            hp_x + 90, hp_y + 11,
            text=f"❤️ {self.hp} / {self.max_hp}",
            fill="#ffffff",
            font=("Arial", 11, "bold")
        )

        if self.dragged_slot is not None:
            item = self.inventory[self.dragged_slot]
            self.canvas.create_text(
                self.mouse_x, self.mouse_y,
                text=ITEM_ICONS.get(item['type'], ""),
                font=("Arial", 22)
            )

        fps_color = "#76FF03" if self.current_fps >= 30 else "#FF5252"
        self.canvas.create_rectangle(
            530, 20, 620, 50,
            fill="#0b132b", outline="#3a506b", width=2
        )
        self.canvas.create_text(
            575, 35,
            text=f"FPS: {self.current_fps}",
            fill=fps_color,
            font=("Arial", 12, "bold")
        )

    def game_loop(self):
        if self.game_state == "game":
            frame_start_time = time.time()

            self.fps_counter += 1
            if frame_start_time - self.last_fps_time >= 1.0:
                self.current_fps = self.fps_counter
                self.fps_counter = 0
                self.last_fps_time = frame_start_time

            self.update_physics()
            self.render()

            # Вычисляем время работы и высчитываем точный остаток до 45 FPS (~22.22 мс)
            elapsed_ms = (time.time() - frame_start_time) * 1000.0
            target_delay = max(1, int(round(TARGET_FRAME_TIME_MS - elapsed_ms)))
        else:
            target_delay = 50

        self.after(target_delay, self.game_loop)

    def on_key_press(self, event):
        key = event.keysym.lower()
        self.keys[key] = True

        if self.game_state == "game":
            if key == "e":
                self.toggle_inventory()
            elif key == "escape":
                self.toggle_pause_menu()
            elif key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                self.selected_slot = 9 if key == "0" else int(key) - 1
                self.update_ui()

    def on_key_release(self, event):
        self.keys[event.keysym.lower()] = False


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MinePyGame()
    app.mainloop()