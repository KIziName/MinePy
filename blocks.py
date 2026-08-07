import os
#------- БАЗОВЫЕ НАСТРОЙКИ 0.1 ------------
SCREEN_WIDTH = 1280           # ширина окна 
SCREEN_HEIGHT = 720           # высота окна
BLOCK_SIZE = 32               # размер блока

CHUNK_WIDTH = 16              # ширина чанка в блоках
WORLD_HEIGHT = 100            # высота мира в блоках
MAX_STACK = 900               # максимальный размер стопки предметов
BUILD_REACH = 128             # радиус взаимодействия с миром 

GRAVITY = 600.0               # ускорение свободного падения 
PLAYER_SPEED = 200.0          # горизонтальная скорость игрока
JUMP_FORCE = -400.0           # начальная скорость прыжка 

# ---------- Настройки времени суток 1.0 ----------
NIGHT_START = 14000           # начало ночи 
NIGHT_END = 22000             # конец ночи 
DAY_SPEED = 20                # скорость смены времени суток 

#------ Путь к папке сохранений 1.1 -------
APPDATA_DIR = os.environ.get('APPDATA', os.path.expanduser('~'))
APPDATA_PATH = os.path.join(APPDATA_DIR, 'MinePy')
SAVE_FILE_PATH = os.path.join(APPDATA_PATH, 'world_save.json')

# ============================================================
# 2. АТМОСФЕРА И ПОГОДА
# ============================================================
STARS_COUNT = 90                   # количество звёзд на небе
RAIN_PARTICLES = 80                # число капель дождя
SNOW_PARTICLES = 80                # число снежинок
CLOUDS_COUNT = 6                   # количество облаков

PLAYER_WIDTH = 22                  # ширина хитбокса игрока
PLAYER_HEIGHT = 44                 # высота хитбокса игрока
PLAYER_ANIM_SPEED = 21.0           # скорость смены кадров анимации ходьбы
DROPPED_ITEM_PULL_RADIUS = 140     # радиус притяжения выпавших предметов 
WEATHER_TRANSITION_TIME = 5        # длительность плавного перехода (сек)

# ============================================================
# 3. ПАРАМЕТРЫ МОБОВ
# ============================================================
# Слайм
SLIME_WIDTH = 32
SLIME_HEIGHT = 24
SLIME_HP_GREEN = 15
SLIME_HP_BLUE = 25
SLIME_DAMAGE_GREEN = 8
SLIME_DAMAGE_BLUE = 10
SLIME_SPEED_GREEN = 192
SLIME_SPEED_BLUE = 220
SLIME_JUMP_FORCE_MIN = -510         # диапазон силы прыжка
SLIME_JUMP_FORCE_MAX = -690
SLIME_JUMP_COOLDOWN_MIN = 0.3       # задержка между прыжками
SLIME_JUMP_COOLDOWN_MAX = 0.8
SLIME_AGGRO_RANGE = 450             # дистанция агрессии к игроку
SLIME_JUMP_COOLDOWN_AFTER = 0.6
SLIME_JUMP_COOLDOWN_AFTER_MAX = 1.2

# Зомби
ZOMBIE_WIDTH = 24
ZOMBIE_HEIGHT = 44
ZOMBIE_HP = 50
ZOMBIE_DAMAGE = 12
ZOMBIE_SPEED = 130
ZOMBIE_AGGRO_RANGE = 400
ZOMBIE_JUMP_FORCE = -350

# Глаз демона
DEMON_EYE_WIDTH = 28
DEMON_EYE_HEIGHT = 28
DEMON_EYE_HP = 30
DEMON_EYE_DAMAGE = 15
DEMON_EYE_DASH_SPEED = 480           # скорость рывка
DEMON_EYE_DASH_COOLDOWN_MIN = 1.0
DEMON_EYE_DASH_COOLDOWN_MAX = 1.7
DEMON_EYE_ACCEL = 12                 # ускорение при движении к цели
DEMON_EYE_DASH_TIMER_MIN = 0.6
DEMON_EYE_DASH_TIMER_MAX = 1.3

# Скелет
SKELETON_WIDTH = 22
SKELETON_HEIGHT = 42
SKELETON_HP = 40
SKELETON_DAMAGE = 12
SKELETON_SPEED = 160
SKELETON_AGGRO_RANGE = 400
SKELETON_JUMP_FORCE = -350

# Овца
SHEEP_WIDTH = 30
SHEEP_HEIGHT = 24
SHEEP_HP = 15
SHEEP_DAMAGE = 0                
SHEEP_GRAVITY_MULT = 0.3        # пониженная гравитация
SHEEP_MOVE_TIMER_MIN = 1        # интервал смены направления
SHEEP_MOVE_TIMER_MAX = 4
SHEEP_SPEED_MIN = -90
SHEEP_SPEED_MAX = 90

# ============================================================
# 4. ГЕНЕРАЦИЯ ЛАНДШАФТА И РУД
# ============================================================
LAND_HEIGHT_BASE = 40           # базовая высота поверхности
LAND_HEIGHT_AMPLITUDE = 6       # амплитуда первой гармоники
LAND_HEIGHT_FREQ = 0.04         # частота первой гармоники
LAND_HEIGHT_FREQ2 = 0.1         # частота второй гармоники
LAND_HEIGHT_AMPLITUDE2 = 3      # амплитуда второй гармоники

DECORATION_CHANCE = 0.15        # шанс появления травы/цветов на поверхности
GRASS_CHANCE = 0.4              # доля высокой травы среди декораций

TREE_CHANCE = 0.08              # шанс появления дерева на чанк
TREE_MIN_HEIGHT = 4
TREE_MAX_HEIGHT = 6
TREE_LEAF_RADIUS = 2            # радиус кроны

# Руды – шанс и минимальная глубина 
ORE_GOLD_CHANCE = 0.03
ORE_GOLD_MIN_DEPTH = 12
ORE_IRON_CHANCE = 0.06
ORE_IRON_MIN_DEPTH = 10
ORE_COPPER_CHANCE = 0.10
ORE_COPPER_MIN_DEPTH = 7
ORE_COAL_CHANCE = 0.16
ORE_COAL_MIN_DEPTH = 5
DIRT_LAYER_THICKNESS = 5        # толщина слоя земли под травой

# Дополнительные руды 
ORE_SILVER_CHANCE = 0.02
ORE_SILVER_MIN_DEPTH = 15
ORE_PLATINUM_CHANCE = 0.015
ORE_PLATINUM_MIN_DEPTH = 20
ORE_MITHRIL_CHANCE = 0.01
ORE_MITHRIL_MIN_DEPTH = 25
ORE_ADAMANTITE_CHANCE = 0.008
ORE_ADAMANTITE_MIN_DEPTH = 30

# Самые редкие и глубокие руды
ORE_TITAN_CHANCE = 0.006
ORE_TITAN_MIN_DEPTH = 35
ORE_COBALT_CHANCE = 0.005
ORE_COBALT_MIN_DEPTH = 40
ORE_NETHERITE_CHANCE = 0.004
ORE_NETHERITE_MIN_DEPTH = 45
ORE_CRYSTAL_CHANCE = 0.003
ORE_CRYSTAL_MIN_DEPTH = 50


# ИДЕНТИФИКАТОРЫ БЛОКОВ И ПРЕДМЕТОВ
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

# Оружие и инструменты 
ITEM_SWORD_WOOD = 5
ITEM_SWORD_COPPER = 16
ITEM_SWORD_IRON = 17
ITEM_SWORD_GOLD = 28
ITEM_SWORD_DIAMOND = 29
ITEM_PICKAXE_WOOD = 6
ITEM_PICKAXE_COPPER = 18
ITEM_PICKAXE_IRON = 19
ITEM_PICKAXE_GOLD = 30

# Ресурсы
ITEM_GEL = 8
ITEM_COIN = 10
ITEM_TORCH = 13
ITEM_BONE = 21

# Слитки и материалы
ITEM_COPPER_INGOT = 22
ITEM_IRON_INGOT = 23
ITEM_GOLD_INGOT = 31
ITEM_COAL = 32
ITEM_DIAMOND = 33
ITEM_WOOD_SHIELD = 24

# Декорации
BLOCK_TALL_GRASS = 34
BLOCK_FLOWER_RED = 35
BLOCK_FLOWER_YELLOW = 36
BLOCK_FLOWER_BLUE = 37

# Строительные блоки
BLOCK_PLANKS = 38
BLOCK_BRICK = 39
BLOCK_GLASS = 40
BLOCK_SAND = 41
BLOCK_SANDSTONE = 42

# Материалы для крафта
ITEM_STICK = 43
ITEM_LEATHER = 44
ITEM_STRING = 45
ITEM_FEATHER = 46
ITEM_FLINT = 47
ITEM_APPLE = 48
ITEM_BREAD = 49
ITEM_COOKED_MEAT = 50

# Каменные инструменты
ITEM_SWORD_STONE = 51
ITEM_PICKAXE_STONE = 52
ITEM_PICKAXE_DIAMOND = 53

# ---------- Второе расширение 1.2 ----------
BLOCK_SILVER_ORE = 100
BLOCK_PLATINUM_ORE = 101
BLOCK_MITHRIL_ORE = 102
BLOCK_ADAMANTITE_ORE = 103
BLOCK_OBSIDIAN = 104
BLOCK_MARBLE = 105
BLOCK_GLOWSTONE = 106

ITEM_SILVER_INGOT = 107
ITEM_PLATINUM_INGOT = 108
ITEM_MITHRIL_INGOT = 109
ITEM_ADAMANTITE_INGOT = 110

ITEM_SWORD_SILVER = 111
ITEM_PICKAXE_SILVER = 112
ITEM_SWORD_PLATINUM = 113
ITEM_PICKAXE_PLATINUM = 114
ITEM_SWORD_MITHRIL = 115
ITEM_PICKAXE_MITHRIL = 116
ITEM_SWORD_ADAMANTITE = 117
ITEM_PICKAXE_ADAMANTITE = 118

# Мебель и декорации
BLOCK_FENCE = 123
BLOCK_LADDER = 124
BLOCK_ANVIL = 125
BLOCK_FURNACE = 126
BLOCK_CHEST = 127
BLOCK_BOOKSHELF = 128
BLOCK_SNOW = 129
BLOCK_CACTUS = 130
BLOCK_SANDSTONE_SMOOTH = 131

# Еда
ITEM_PIE = 136
ITEM_SOUP = 137
ITEM_MUSHROOM_SOUP = 138
ITEM_COOKED_MUSHROOM = 139

# Лук и стрелы
ITEM_BOW = 140
ITEM_ARROW = 141

# Книги, посуда
ITEM_BOOK = 145
ITEM_PAPER = 146
ITEM_BOWL = 147
ITEM_MUSHROOM = 148
ITEM_WHEAT = 149

# ---------- Третье расширение 1.3 ----------
BLOCK_TITAN_ORE = 200
BLOCK_COBALT_ORE = 201
BLOCK_NETHERITE_ORE = 202
BLOCK_CRYSTAL_ORE = 203

ITEM_TITAN_INGOT = 204
ITEM_COBALT_INGOT = 205
ITEM_NETHERITE_INGOT = 206
ITEM_CRYSTAL_INGOT = 207

ITEM_SWORD_TITAN = 208
ITEM_PICKAXE_TITAN = 209
ITEM_AXE_TITAN = 210
ITEM_SWORD_COBALT = 211
ITEM_PICKAXE_COBALT = 212
ITEM_AXE_COBALT = 213
ITEM_SWORD_NETHERITE = 214
ITEM_PICKAXE_NETHERITE = 215
ITEM_AXE_NETHERITE = 216
ITEM_SWORD_CRYSTAL = 217
ITEM_PICKAXE_CRYSTAL = 218

# Новые виды оружия
ITEM_HAMMER = 223
ITEM_SPEAR = 224
ITEM_CROSSBOW = 225

# Самоцветы
ITEM_RUBY = 226
ITEM_SAPPHIRE = 227
ITEM_EMERALD = 228
ITEM_AMETHYST = 229
ITEM_OPAL = 230
ITEM_AMBER = 231

# Продвинутая еда
ITEM_PIZZA = 241
ITEM_BURGER = 242
ITEM_SUSHI = 243
ITEM_CAKE = 244
ITEM_SALAD = 245
ITEM_FRIED_POTATOES = 246
ITEM_CARROT_JUICE = 247

# Фрукты/овощи
ITEM_BANANA = 248
ITEM_ORANGE = 249
ITEM_CARROT = 250
ITEM_POTATO = 251
ITEM_TOMATO = 252
ITEM_CUCUMBER = 253

# Рыба и снасти
ITEM_FISH_PERCH = 258
ITEM_FISH_SALMON = 259
ITEM_FISH_GOLDFISH = 260
ITEM_FISHING_ROD = 262
ITEM_BAIT = 263

# Архитектурные блоки
BLOCK_DOOR = 264
BLOCK_WINDOW = 265
BLOCK_SHUTTER = 266
BLOCK_PILLAR = 267
BLOCK_STATUE = 268
BLOCK_CARPET = 269
BLOCK_PAINTING = 270
BLOCK_FRAME = 271
BLOCK_SHELF = 272

# Растения
BLOCK_BUSH = 273
BLOCK_FERN = 274
BLOCK_VINE = 275
BLOCK_TULIP_RED = 276
BLOCK_TULIP_YELLOW = 277
BLOCK_DAISY = 278

# Музыкальные инструменты
ITEM_GUITAR = 279
ITEM_FLUTE = 280
ITEM_DRUM = 281
ITEM_HARP = 282

# Фермерство
ITEM_HOE = 283
ITEM_WATERING_CAN = 284
ITEM_FERTILIZER = 285

# Разные материалы
ITEM_LEATHER_STRIP = 286
ITEM_SCALE = 287
ITEM_SHELL = 288
ITEM_FEATHER_BLUE = 289
ITEM_FEATHER_RED = 290
ITEM_FEATHER_GREEN = 291
ITEM_BONE_MEAL = 292
ITEM_WOOL = 293

# Магические книги
ITEM_SPELLBOOK_FIRE = 294
ITEM_SPELLBOOK_ICE = 295
ITEM_SPELLBOOK_HEAL = 296
ITEM_SPELLBOOK_TELEPORT = 297


# ЦВЕТА БЛОКОВ (RGB)
BLOCK_COLORS = {
    BLOCK_GRASS: (76, 175, 80),
    BLOCK_DIRT: (121, 85, 72),
    BLOCK_STONE: (96, 125, 139),
    BLOCK_WOOD: (93, 64, 55),
    BLOCK_LEAVES: (46, 125, 50),
    BLOCK_COPPER_ORE: (216, 112, 64),
    BLOCK_IRON_ORE: (176, 190, 197),
    BLOCK_GOLD_ORE: (255, 215, 0),
    BLOCK_COAL_ORE: (33, 33, 33),
    BLOCK_TALL_GRASS: (76, 175, 80),
    BLOCK_FLOWER_RED: (255, 80, 80),
    BLOCK_FLOWER_YELLOW: (255, 255, 80),
    BLOCK_FLOWER_BLUE: (80, 150, 255),
    BLOCK_PLANKS: (210, 180, 140),
    BLOCK_BRICK: (178, 34, 34),
    BLOCK_GLASS: (200, 230, 255),
    BLOCK_SAND: (238, 214, 175),
    BLOCK_SANDSTONE: (193, 182, 155),
    BLOCK_SILVER_ORE: (180, 200, 210),
    BLOCK_PLATINUM_ORE: (220, 235, 245),
    BLOCK_MITHRIL_ORE: (120, 200, 220),
    BLOCK_ADAMANTITE_ORE: (80, 50, 120),
    BLOCK_OBSIDIAN: (20, 10, 30),
    BLOCK_MARBLE: (220, 220, 230),
    BLOCK_GLOWSTONE: (255, 240, 100),
    BLOCK_FENCE: (160, 120, 80),
    BLOCK_LADDER: (180, 140, 90),
    BLOCK_ANVIL: (80, 80, 80),
    BLOCK_FURNACE: (120, 80, 60),
    BLOCK_CHEST: (180, 140, 70),
    BLOCK_BOOKSHELF: (150, 100, 60),
    BLOCK_SNOW: (240, 250, 255),
    BLOCK_CACTUS: (60, 120, 40),
    BLOCK_SANDSTONE_SMOOTH: (210, 200, 170),
    BLOCK_TITAN_ORE: (100, 150, 200),
    BLOCK_COBALT_ORE: (50, 150, 200),
    BLOCK_NETHERITE_ORE: (80, 40, 100),
    BLOCK_CRYSTAL_ORE: (200, 240, 255),
    BLOCK_DOOR: (160, 120, 80),
    BLOCK_WINDOW: (150, 200, 230),
    BLOCK_SHUTTER: (100, 80, 60),
    BLOCK_PILLAR: (180, 170, 150),
    BLOCK_STATUE: (200, 200, 200),
    BLOCK_CARPET: (200, 80, 80),
    BLOCK_PAINTING: (150, 100, 80),
    BLOCK_FRAME: (120, 80, 50),
    BLOCK_SHELF: (180, 140, 100),
    BLOCK_BUSH: (40, 120, 40),
    BLOCK_FERN: (50, 140, 50),
    BLOCK_VINE: (60, 150, 60),
    BLOCK_TULIP_RED: (255, 50, 50),
    BLOCK_TULIP_YELLOW: (255, 255, 50),
    BLOCK_DAISY: (255, 255, 200),
}

# Список цветов для генерации на поверхности
FLOWER_TYPES = [BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE]

# Коды погоды
WEATHER_CLEAR = 0
WEATHER_RAIN = 1
WEATHER_SNOW = 2

# ============================================================
# 8. ДОПОЛНИТЕЛЬНЫЕ ГРУППЫ ДЛЯ УДОБСТВА 
# ============================================================
# Непроходимые блоки
NON_SOLID_BLOCKS = {
    BLOCK_LEAVES, BLOCK_TALL_GRASS, BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW,
    BLOCK_FLOWER_BLUE, BLOCK_BUSH, BLOCK_FERN, BLOCK_VINE,
    BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY
}

# Блоки, которые можно размещать
PLACEABLE_BLOCKS = {
    BLOCK_DIRT, BLOCK_GRASS, BLOCK_STONE, BLOCK_WOOD,
    BLOCK_LEAVES, BLOCK_COPPER_ORE, BLOCK_IRON_ORE,
    BLOCK_GOLD_ORE, BLOCK_COAL_ORE,
    BLOCK_TALL_GRASS, BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE,
    BLOCK_PLANKS, BLOCK_BRICK, BLOCK_GLASS, BLOCK_SAND, BLOCK_SANDSTONE,
    BLOCK_FENCE, BLOCK_LADDER, BLOCK_ANVIL, BLOCK_FURNACE,
    BLOCK_CHEST, BLOCK_BOOKSHELF, BLOCK_SNOW, BLOCK_CACTUS,
    BLOCK_SANDSTONE_SMOOTH, BLOCK_OBSIDIAN, BLOCK_GLOWSTONE,
    BLOCK_SILVER_ORE, BLOCK_PLATINUM_ORE, BLOCK_MITHRIL_ORE, BLOCK_ADAMANTITE_ORE,
    BLOCK_TITAN_ORE, BLOCK_COBALT_ORE, BLOCK_NETHERITE_ORE, BLOCK_CRYSTAL_ORE,
    BLOCK_DOOR, BLOCK_WINDOW, BLOCK_SHUTTER, BLOCK_PILLAR,
    BLOCK_STATUE, BLOCK_CARPET, BLOCK_PAINTING, BLOCK_FRAME, BLOCK_SHELF,
    BLOCK_BUSH, BLOCK_FERN, BLOCK_VINE,
    BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY
}

# Еда и лечение (восстанавливаемое здоровье)
FOOD_HEAL = {
    ITEM_APPLE: 10, ITEM_BREAD: 20, ITEM_COOKED_MEAT: 35,
    ITEM_PIE: 50, ITEM_SOUP: 30, ITEM_MUSHROOM_SOUP: 35,
    ITEM_COOKED_MUSHROOM: 20, ITEM_PIZZA: 60, ITEM_BURGER: 70,
    ITEM_SUSHI: 50, ITEM_CAKE: 80, ITEM_SALAD: 40,
    ITEM_FRIED_POTATOES: 30, ITEM_CARROT_JUICE: 25
}

# Урон оружия (для быстрого доступа)
WEAPON_DAMAGE = {
    ITEM_SWORD_WOOD: 12,
    ITEM_SWORD_COPPER: 18,
    ITEM_SWORD_IRON: 28,
    ITEM_SWORD_GOLD: 38,
    ITEM_SWORD_DIAMOND: 55,
    ITEM_SWORD_STONE: 16,
    ITEM_SWORD_SILVER: 45,
    ITEM_SWORD_PLATINUM: 55,
    ITEM_SWORD_MITHRIL: 70,
    ITEM_SWORD_ADAMANTITE: 90,
    ITEM_SWORD_TITAN: 100,
    ITEM_SWORD_COBALT: 120,
    ITEM_SWORD_NETHERITE: 150,
    ITEM_SWORD_CRYSTAL: 180,
    ITEM_HAMMER: 200,
    ITEM_SPEAR: 70,
    ITEM_CROSSBOW: 50,
    ITEM_AXE_TITAN: 90,
    ITEM_AXE_COBALT: 110,
    ITEM_AXE_NETHERITE: 140,
}

# ----------Настройки генерации мира 1.4 ---------
WORLD_SEED = None                # если None – случайное зерно, иначе число
WORLD_MAX_X = None               # ограничение по X (в блоках), None – бесконечно

# ---------- Настройки спавна мобов 1.5 ----------
MOB_SPAWN_LIMITS = {
    'Zombie': {'night': 5, 'day': 0},    # максимум на карте
    'Slime': {'night': 5, 'day': 5},
    'DemonEye': {'night': 2, 'day': 0},
    'Skeleton': {'night': 5, 'day': 0},
    'Sheep': {'night': 2, 'day': 6},
}

MOB_SPAWN_RADIUS_MIN = 800           # минимальное расстояние от игрока для спавна
MOB_SPAWN_RADIUS_MAX = 1600          # максимальное расстояние от игрока

# ---------- Настройки сложности 1.6 ----------
DIFFICULTY = {
    'player_damage_multiplier': 1.0,    # множитель урона игрока (от оружия)
    'mob_damage_multiplier': 1.0,       # множитель урона мобов (по игроку)
}

# ---------- Настройки регенерации здоровья 1.7 ----------
REGEN_DELAY = 30.0          # секунд после урона до начала регенерации
REGEN_INTERVAL = 8.0        # интервал между восстановлениями (сек)
REGEN_AMOUNT = 1            # сколько HP восстанавливать за раз

# ---------- Настройки погоды 1.8 ----------
WEATHER_DURATION = {
    'clear': (300, 600),      # (мин, макс) секунд
    'rain': (30, 180),
    'snow': (30, 180),
}
