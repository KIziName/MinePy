import os
# ------------------- КОНСТАНТЫ -------------------
SCREEN_WIDTH = 1280                     # ширина окна в пикселях
SCREEN_HEIGHT = 720                     # высота окна в пикселях
BLOCK_SIZE = 32                         # размер одного блока в пикселях

CHUNK_WIDTH = 16                        # ширина чанка в блоках
WORLD_HEIGHT = 60                       # высота мира в блоках

MAX_STACK = 900                         # макс. предметов в одной ячейке инвентаря
BUILD_REACH = 128                       # дистанция взаимодействия с блоками

# Физика 
GRAVITY = 600.0                         # ускорение свободного падения
PLAYER_SPEED = 200.0                    # горизонтальная скорость игрока
JUMP_FORCE = -400.0                     # начальная скорость прыжка (вверх)

# Пути сохранения
APPDATA_DIR = os.environ.get('APPDATA', os.path.expanduser('~'))
APPDATA_PATH = os.path.join(APPDATA_DIR, 'MinePy')
SAVE_FILE_PATH = os.path.join(APPDATA_PATH, 'world_save.json')

# ------------------- НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ -------------------
STARS_COUNT = 90                        # количество звёзд (ночью)
RAIN_PARTICLES = 80                     # капель дождя
SNOW_PARTICLES = 80                    # снежинок
CLOUDS_COUNT = 6                       # облаков
MAX_MOBS = 7                            # максимум мобов одновременно

# ------------------- НАСТРОЙКИ ИГРОВОЙ МЕХАНИКИ -------------------
PLAYER_WIDTH = 22                       # ширина игрока в пикселях
PLAYER_HEIGHT = 44                      # высота игрока в пикселях
PLAYER_ANIM_SPEED = 21.0                # скорость анимации шага (кадров в секунду)
DROPPED_ITEM_PULL_RADIUS = 140          # радиус притягивания предметов к игроку
WEATHER_CHANGE_INTERVAL_MIN = 30        # минимальная длительность погоды (сек)
WEATHER_CHANGE_INTERVAL_MAX = 120       # максимальная длительность погоды (сек)
WEATHER_TRANSITION_TIME = 3             # время плавного перехода погоды (сек)

# ------------------- НАСТРОЙКИ МОБОВ -------------------
# Слайм
SLIME_WIDTH = 32
SLIME_HEIGHT = 24
SLIME_HP_GREEN = 15
SLIME_HP_BLUE = 25
SLIME_DAMAGE_GREEN = 8
SLIME_DAMAGE_BLUE = 10
SLIME_SPEED_GREEN = 192
SLIME_SPEED_BLUE = 220
SLIME_JUMP_FORCE_MIN = -510
SLIME_JUMP_FORCE_MAX = -690
SLIME_JUMP_COOLDOWN_MIN = 0.3
SLIME_JUMP_COOLDOWN_MAX = 0.8
SLIME_AGGRO_RANGE = 450
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

# Демон-глаз
DEMON_EYE_WIDTH = 28
DEMON_EYE_HEIGHT = 28
DEMON_EYE_HP = 30
DEMON_EYE_DAMAGE = 15
DEMON_EYE_DASH_SPEED = 480
DEMON_EYE_DASH_COOLDOWN_MIN = 1.0
DEMON_EYE_DASH_COOLDOWN_MAX = 1.7
DEMON_EYE_ACCEL = 12
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
SHEEP_GRAVITY_MULT = 0.3
SHEEP_MOVE_TIMER_MIN = 1
SHEEP_MOVE_TIMER_MAX = 4
SHEEP_SPEED_MIN = -90
SHEEP_SPEED_MAX = 90

# ------------------- НАСТРОЙКИ ГЕНЕРАЦИИ МИРА -------------------
LAND_HEIGHT_BASE = 40                   # базовый уровень высоты
LAND_HEIGHT_AMPLITUDE = 6               # амплитуда первой волны
LAND_HEIGHT_FREQ = 0.04                 # частота первой волны
LAND_HEIGHT_FREQ2 = 0.1                 # частота второй волны
LAND_HEIGHT_AMPLITUDE2 = 3              # амплитуда второй волны

DECORATION_CHANCE = 0.15                # шанс появления декора на поверхности
GRASS_CHANCE = 0.4                      # среди декора – шанс травы (иначе цветок)

TREE_CHANCE = 0.08                      # шанс появления дерева
TREE_MIN_HEIGHT = 4                     # минимальная высота дерева
TREE_MAX_HEIGHT = 6                     # максимальная высота дерева
TREE_LEAF_RADIUS = 2                    # радиус кроны

ORE_GOLD_CHANCE = 0.03                  # шанс золотой руды
ORE_GOLD_MIN_DEPTH = 12                 # минимальная глубина залегания
ORE_IRON_CHANCE = 0.06
ORE_IRON_MIN_DEPTH = 10
ORE_COPPER_CHANCE = 0.10
ORE_COPPER_MIN_DEPTH = 7
ORE_COAL_CHANCE = 0.16
ORE_COAL_MIN_DEPTH = 5

DIRT_LAYER_THICKNESS = 5                # толщина слоя земли под травой (в блоках)

# ------------------- БЛОКИ И ПРЕДМЕТЫ -------------------
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

BLOCK_TALL_GRASS = 34
BLOCK_FLOWER_RED = 35
BLOCK_FLOWER_YELLOW = 36
BLOCK_FLOWER_BLUE = 37

# ------------------- ЦВЕТА БЛОКОВ -------------------
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
}

# ------------------- НАЗВАНИЯ ПРЕДМЕТОВ -------------------
ITEM_NAMES = {
    BLOCK_DIRT: "Земля", BLOCK_GRASS: "Трава", BLOCK_STONE: "Камень", BLOCK_WOOD: "Дерево",
    BLOCK_LEAVES: "Листва", BLOCK_COPPER_ORE: "Медн. руда", BLOCK_IRON_ORE: "Жел. руда",
    BLOCK_GOLD_ORE: "Зол. руда", BLOCK_COAL_ORE: "Угл. руда",
    ITEM_SWORD_WOOD: "Дер. меч", ITEM_SWORD_COPPER: "Медн. меч", ITEM_SWORD_IRON: "Жел. меч",
    ITEM_SWORD_GOLD: "Зол. меч", ITEM_SWORD_DIAMOND: "Алм. меч",
    ITEM_PICKAXE_WOOD: "Дер. кирка", ITEM_PICKAXE_COPPER: "Медн. кирка", ITEM_PICKAXE_IRON: "Жел. кирка",
    ITEM_PICKAXE_GOLD: "Зол. кирка", ITEM_GEL: "Гель", ITEM_POTION: "Зелье", ITEM_BIG_POTION: "Б. Зелье",
    ITEM_COIN: "Монета", ITEM_LENS: "Линза", ITEM_TORCH: "Факел", ITEM_BONE: "Кость",
    ITEM_COPPER_INGOT: "Медн. слиток", ITEM_IRON_INGOT: "Жел. слиток", ITEM_GOLD_INGOT: "Зол. слиток",
    ITEM_COAL: "Уголь", ITEM_DIAMOND: "Алмаз", ITEM_WOOD_SHIELD: "Дер. щит", ITEM_IRON_ARMOR: "Жел. броня",
    BLOCK_TALL_GRASS: "Высокая трава",
    BLOCK_FLOWER_RED: "Красный цветок",
    BLOCK_FLOWER_YELLOW: "Жёлтый цветок",
    BLOCK_FLOWER_BLUE: "Синий цветок",
}

# ------------------- ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ -------------------
FLOWER_TYPES = [BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE]

# ------------------- ПОГОДА -------------------
WEATHER_CLEAR = 0
WEATHER_RAIN = 1
WEATHER_SNOW = 2

# ------------------- РЕЦЕПТЫ КРАФТА -------------------
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
