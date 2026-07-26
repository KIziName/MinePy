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

# ------------------- ДОПОЛНИТЕЛЬНЫЕ БЛОКИ (из первого расширения) -------------------
BLOCK_PLANKS = 38
BLOCK_BRICK = 39
BLOCK_GLASS = 40
BLOCK_SAND = 41
BLOCK_SANDSTONE = 42

# ------------------- ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ (из первого расширения) -------------------
ITEM_STICK = 43
ITEM_LEATHER = 44
ITEM_STRING = 45
ITEM_FEATHER = 46
ITEM_FLINT = 47
ITEM_APPLE = 48
ITEM_BREAD = 49
ITEM_COOKED_MEAT = 50

ITEM_SWORD_STONE = 51
ITEM_PICKAXE_STONE = 52
ITEM_PICKAXE_DIAMOND = 53

ITEM_GOLD_ARMOR = 54
ITEM_DIAMOND_ARMOR = 55

# ------------------- НОВЫЕ РУДЫ (второе расширение) -------------------
BLOCK_SILVER_ORE = 100
BLOCK_PLATINUM_ORE = 101
BLOCK_MITHRIL_ORE = 102
BLOCK_ADAMANTITE_ORE = 103
BLOCK_OBSIDIAN = 104
BLOCK_MARBLE = 105
BLOCK_GLOWSTONE = 106

# ------------------- НОВЫЕ СЛИТКИ -------------------
ITEM_SILVER_INGOT = 107
ITEM_PLATINUM_INGOT = 108
ITEM_MITHRIL_INGOT = 109
ITEM_ADAMANTITE_INGOT = 110

# ------------------- НОВЫЕ ИНСТРУМЕНТЫ -------------------
ITEM_SWORD_SILVER = 111
ITEM_PICKAXE_SILVER = 112
ITEM_SWORD_PLATINUM = 113
ITEM_PICKAXE_PLATINUM = 114
ITEM_SWORD_MITHRIL = 115
ITEM_PICKAXE_MITHRIL = 116
ITEM_SWORD_ADAMANTITE = 117
ITEM_PICKAXE_ADAMANTITE = 118

# ------------------- НОВАЯ БРОНЯ -------------------
ITEM_SILVER_ARMOR = 119
ITEM_PLATINUM_ARMOR = 120
ITEM_MITHRIL_ARMOR = 121
ITEM_ADAMANTITE_ARMOR = 122

# ------------------- НОВЫЕ БЛОКИ ДЛЯ СТРОИТЕЛЬСТВА -------------------
BLOCK_FENCE = 123
BLOCK_LADDER = 124
BLOCK_ANVIL = 125
BLOCK_FURNACE = 126
BLOCK_CHEST = 127
BLOCK_BOOKSHELF = 128
BLOCK_SNOW = 129
BLOCK_CACTUS = 130
BLOCK_SANDSTONE_SMOOTH = 131

# ------------------- НОВЫЕ ЗЕЛЬЯ -------------------
ITEM_POTION_REGENERATION = 132
ITEM_POTION_STRENGTH = 133
ITEM_POTION_SPEED = 134
ITEM_POTION_JUMP = 135

# ------------------- НОВАЯ ЕДА -------------------
ITEM_PIE = 136
ITEM_SOUP = 137
ITEM_MUSHROOM_SOUP = 138
ITEM_COOKED_MUSHROOM = 139

# ------------------- ЛУК И СТРЕЛЫ -------------------
ITEM_BOW = 140
ITEM_ARROW = 141

# ------------------- НОВЫЕ РЕСУРСЫ ДЛЯ КРАФТА -------------------
ITEM_SPIDER_EYE = 142
ITEM_WOLF_FANG = 143
ITEM_DRAGON_SCALE = 144
ITEM_BOOK = 145
ITEM_PAPER = 146
ITEM_BOWL = 147
ITEM_MUSHROOM = 148
ITEM_WHEAT = 149

# ------------------- РУДЫ (ТИТАН, КОБАЛЬТ, НЕЗЕРИТ, ХРУСТАЛЬ) -------------------
BLOCK_TITAN_ORE = 200
BLOCK_COBALT_ORE = 201
BLOCK_NETHERITE_ORE = 202
BLOCK_CRYSTAL_ORE = 203

# ------------------- СЛИТКИ (второе расширение) -------------------
ITEM_TITAN_INGOT = 204
ITEM_COBALT_INGOT = 205
ITEM_NETHERITE_INGOT = 206
ITEM_CRYSTAL_INGOT = 207

# ------------------- ИНСТРУМЕНТЫ из новых материалов -------------------
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

# ------------------- БРОНЯ новых материалов -------------------
ITEM_TITAN_ARMOR = 219
ITEM_COBALT_ARMOR = 220
ITEM_NETHERITE_ARMOR = 221
ITEM_CRYSTAL_ARMOR = 222

# ------------------- ДРУГОЕ ОРУЖИЕ -------------------
ITEM_HAMMER = 223
ITEM_SPEAR = 224
ITEM_CROSSBOW = 225

# ------------------- САМОЦВЕТЫ -------------------
ITEM_RUBY = 226
ITEM_SAPPHIRE = 227
ITEM_EMERALD = 228
ITEM_AMETHYST = 229
ITEM_OPAL = 230
ITEM_AMBER = 231

# ------------------- МАГИЧЕСКИЕ ПОСОХИ -------------------
ITEM_STAFF_FIRE = 232
ITEM_STAFF_ICE = 233
ITEM_STAFF_LIGHTNING = 234
ITEM_STAFF_HEALING = 235

# ------------------- УКРАШЕНИЯ -------------------
ITEM_RING_STRENGTH = 236
ITEM_RING_PROTECTION = 237
ITEM_AMULET_REGENERATION = 238
ITEM_AMULET_SPEED = 239
ITEM_NECKLACE_JUMP = 240

# ------------------- ЕДА (второе расширение) -------------------
ITEM_PIZZA = 241
ITEM_BURGER = 242
ITEM_SUSHI = 243
ITEM_CAKE = 244
ITEM_SALAD = 245
ITEM_FRIED_POTATOES = 246
ITEM_CARROT_JUICE = 247

# ------------------- ФРУКТЫ/ОВОЩИ -------------------
ITEM_BANANA = 248
ITEM_ORANGE = 249
ITEM_CARROT = 250
ITEM_POTATO = 251
ITEM_TOMATO = 252
ITEM_CUCUMBER = 253

# ------------------- НОВЫЕ ЗЕЛЬЯ (второе расширение) -------------------
ITEM_POTION_NIGHT_VISION = 254
ITEM_POTION_INVISIBILITY = 255
ITEM_POTION_WATER_BREATHING = 256
ITEM_POTION_HASTE = 257

# ------------------- РЫБА и РЫБАЛКА -------------------
ITEM_FISH_PERCH = 258
ITEM_FISH_SALMON = 259
ITEM_FISH_GOLDFISH = 260
ITEM_FISH_PUFFER = 261
ITEM_FISHING_ROD = 262
ITEM_BAIT = 263

# ------------------- ДЕКОРАТИВНЫЕ БЛОКИ -------------------
BLOCK_DOOR = 264
BLOCK_WINDOW = 265
BLOCK_SHUTTER = 266
BLOCK_PILLAR = 267
BLOCK_STATUE = 268
BLOCK_CARPET = 269
BLOCK_PAINTING = 270
BLOCK_FRAME = 271
BLOCK_SHELF = 272

# ------------------- РАСТЕНИЯ -------------------
BLOCK_BUSH = 273
BLOCK_FERN = 274
BLOCK_VINE = 275
BLOCK_TULIP_RED = 276
BLOCK_TULIP_YELLOW = 277
BLOCK_DAISY = 278

# ------------------- МУЗЫКАЛЬНЫЕ ИНСТРУМЕНТЫ -------------------
ITEM_GUITAR = 279
ITEM_FLUTE = 280
ITEM_DRUM = 281
ITEM_HARP = 282

# ------------------- ФЕРМЕРСКИЕ ИНСТРУМЕНТЫ -------------------
ITEM_HOE = 283
ITEM_WATERING_CAN = 284
ITEM_FERTILIZER = 285

# ------------------- РЕСУРСЫ (второе расширение) -------------------
ITEM_LEATHER_STRIP = 286
ITEM_SCALE = 287
ITEM_SHELL = 288
ITEM_FEATHER_BLUE = 289
ITEM_FEATHER_RED = 290
ITEM_FEATHER_GREEN = 291
ITEM_BONE_MEAL = 292
ITEM_WOOL = 293

# ------------------- КНИГИ ЗАКЛИНАНИЙ -------------------
ITEM_SPELLBOOK_FIRE = 294
ITEM_SPELLBOOK_ICE = 295
ITEM_SPELLBOOK_HEAL = 296
ITEM_SPELLBOOK_TELEPORT = 297

# ------------------- СВИТКИ -------------------
ITEM_SCROLL_TELEPORT = 298

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
    # новые блоки
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
    # новые
    BLOCK_PLANKS: "Доски",
    BLOCK_BRICK: "Кирпич",
    BLOCK_GLASS: "Стекло",
    BLOCK_SAND: "Песок",
    BLOCK_SANDSTONE: "Песчаник",
    ITEM_STICK: "Палка",
    ITEM_LEATHER: "Кожа",
    ITEM_STRING: "Нить",
    ITEM_FEATHER: "Перо",
    ITEM_FLINT: "Кремень",
    ITEM_APPLE: "Яблоко",
    ITEM_BREAD: "Хлеб",
    ITEM_COOKED_MEAT: "Жареное мясо",
    ITEM_SWORD_STONE: "Каменный меч",
    ITEM_PICKAXE_STONE: "Каменная кирка",
    ITEM_PICKAXE_DIAMOND: "Алмазная кирка",
    ITEM_GOLD_ARMOR: "Золотая броня",
    ITEM_DIAMOND_ARMOR: "Алмазная броня",
    BLOCK_SILVER_ORE: "Серебр. руда",
    BLOCK_PLATINUM_ORE: "Платин. руда",
    BLOCK_MITHRIL_ORE: "Мифр. руда",
    BLOCK_ADAMANTITE_ORE: "Адамант. руда",
    BLOCK_OBSIDIAN: "Обсидиан",
    BLOCK_MARBLE: "Мрамор",
    BLOCK_GLOWSTONE: "Светокамень",
    ITEM_SILVER_INGOT: "Серебр. слиток",
    ITEM_PLATINUM_INGOT: "Платин. слиток",
    ITEM_MITHRIL_INGOT: "Мифр. слиток",
    ITEM_ADAMANTITE_INGOT: "Адамант. слиток",
    ITEM_SWORD_SILVER: "Серебр. меч",
    ITEM_PICKAXE_SILVER: "Серебр. кирка",
    ITEM_SWORD_PLATINUM: "Платин. меч",
    ITEM_PICKAXE_PLATINUM: "Платин. кирка",
    ITEM_SWORD_MITHRIL: "Мифр. меч",
    ITEM_PICKAXE_MITHRIL: "Мифр. кирка",
    ITEM_SWORD_ADAMANTITE: "Адамант. меч",
    ITEM_PICKAXE_ADAMANTITE: "Адамант. кирка",
    ITEM_SILVER_ARMOR: "Серебр. броня",
    ITEM_PLATINUM_ARMOR: "Платин. броня",
    ITEM_MITHRIL_ARMOR: "Мифр. броня",
    ITEM_ADAMANTITE_ARMOR: "Адамант. броня",
    BLOCK_FENCE: "Забор",
    BLOCK_LADDER: "Лестница",
    BLOCK_ANVIL: "Наковальня",
    BLOCK_FURNACE: "Печь",
    BLOCK_CHEST: "Сундук",
    BLOCK_BOOKSHELF: "Книжн. полка",
    BLOCK_SNOW: "Снег",
    BLOCK_CACTUS: "Кактус",
    BLOCK_SANDSTONE_SMOOTH: "Глад. песчаник",
    ITEM_POTION_REGENERATION: "Зелье регена",
    ITEM_POTION_STRENGTH: "Зелье силы",
    ITEM_POTION_SPEED: "Зелье скорости",
    ITEM_POTION_JUMP: "Зелье прыжка",
    ITEM_PIE: "Пирог",
    ITEM_SOUP: "Суп",
    ITEM_MUSHROOM_SOUP: "Гриб. суп",
    ITEM_COOKED_MUSHROOM: "Жар. гриб",
    ITEM_BOW: "Лук",
    ITEM_ARROW: "Стрела",
    ITEM_SPIDER_EYE: "Глаз паука",
    ITEM_WOLF_FANG: "Клык волка",
    ITEM_DRAGON_SCALE: "Чешуя дракона",
    ITEM_BOOK: "Книга",
    ITEM_PAPER: "Бумага",
    ITEM_BOWL: "Миска",
    ITEM_MUSHROOM: "Гриб",
    ITEM_WHEAT: "Пшеница",
    BLOCK_TITAN_ORE: "Титановая руда",
    BLOCK_COBALT_ORE: "Кобальтовая руда",
    BLOCK_NETHERITE_ORE: "Незеритовая руда",
    BLOCK_CRYSTAL_ORE: "Хрустальная руда",
    ITEM_TITAN_INGOT: "Титановый слиток",
    ITEM_COBALT_INGOT: "Кобальтовый слиток",
    ITEM_NETHERITE_INGOT: "Незеритовый слиток",
    ITEM_CRYSTAL_INGOT: "Хрустальный слиток",
    ITEM_SWORD_TITAN: "Титановый меч",
    ITEM_PICKAXE_TITAN: "Титановая кирка",
    ITEM_AXE_TITAN: "Титановый топор",
    ITEM_SWORD_COBALT: "Кобальтовый меч",
    ITEM_PICKAXE_COBALT: "Кобальтовая кирка",
    ITEM_AXE_COBALT: "Кобальтовый топор",
    ITEM_SWORD_NETHERITE: "Незеритовый меч",
    ITEM_PICKAXE_NETHERITE: "Незеритовая кирка",
    ITEM_AXE_NETHERITE: "Незеритовый топор",
    ITEM_SWORD_CRYSTAL: "Хрустальный меч",
    ITEM_PICKAXE_CRYSTAL: "Хрустальная кирка",
    ITEM_TITAN_ARMOR: "Титановая броня",
    ITEM_COBALT_ARMOR: "Кобальтовая броня",
    ITEM_NETHERITE_ARMOR: "Незеритовая броня",
    ITEM_CRYSTAL_ARMOR: "Хрустальная броня",
    ITEM_HAMMER: "Молот",
    ITEM_SPEAR: "Копьё",
    ITEM_CROSSBOW: "Арбалет",
    ITEM_RUBY: "Рубин",
    ITEM_SAPPHIRE: "Сапфир",
    ITEM_EMERALD: "Изумруд",
    ITEM_AMETHYST: "Аметист",
    ITEM_OPAL: "Опал",
    ITEM_AMBER: "Янтарь",
    ITEM_STAFF_FIRE: "Посох огня",
    ITEM_STAFF_ICE: "Посох льда",
    ITEM_STAFF_LIGHTNING: "Посох молнии",
    ITEM_STAFF_HEALING: "Посох лечения",
    ITEM_RING_STRENGTH: "Кольцо силы",
    ITEM_RING_PROTECTION: "Кольцо защиты",
    ITEM_AMULET_REGENERATION: "Амулет регенерации",
    ITEM_AMULET_SPEED: "Амулет скорости",
    ITEM_NECKLACE_JUMP: "Ожерелье прыжка",
    ITEM_PIZZA: "Пицца",
    ITEM_BURGER: "Бургер",
    ITEM_SUSHI: "Суши",
    ITEM_CAKE: "Торт",
    ITEM_SALAD: "Салат",
    ITEM_FRIED_POTATOES: "Жареная картошка",
    ITEM_CARROT_JUICE: "Морковный сок",
    ITEM_BANANA: "Банан",
    ITEM_ORANGE: "Апельсин",
    ITEM_CARROT: "Морковь",
    ITEM_POTATO: "Картофель",
    ITEM_TOMATO: "Помидор",
    ITEM_CUCUMBER: "Огурец",
    ITEM_POTION_NIGHT_VISION: "Зелье ночного зрения",
    ITEM_POTION_INVISIBILITY: "Зелье невидимости",
    ITEM_POTION_WATER_BREATHING: "Зелье водного дыхания",
    ITEM_POTION_HASTE: "Зелье ускорения",
    ITEM_FISH_PERCH: "Окунь",
    ITEM_FISH_SALMON: "Лосось",
    ITEM_FISH_GOLDFISH: "Золотая рыбка",
    ITEM_FISH_PUFFER: "Фугу",
    ITEM_FISHING_ROD: "Удочка",
    ITEM_BAIT: "Наживка",
    BLOCK_DOOR: "Дверь",
    BLOCK_WINDOW: "Окно",
    BLOCK_SHUTTER: "Ставни",
    BLOCK_PILLAR: "Колонна",
    BLOCK_STATUE: "Статуя",
    BLOCK_CARPET: "Ковёр",
    BLOCK_PAINTING: "Картина",
    BLOCK_FRAME: "Рамка",
    BLOCK_SHELF: "Полка",
    BLOCK_BUSH: "Куст",
    BLOCK_FERN: "Папоротник",
    BLOCK_VINE: "Лиана",
    BLOCK_TULIP_RED: "Красный тюльпан",
    BLOCK_TULIP_YELLOW: "Жёлтый тюльпан",
    BLOCK_DAISY: "Ромашка",
    ITEM_GUITAR: "Гитара",
    ITEM_FLUTE: "Флейта",
    ITEM_DRUM: "Барабан",
    ITEM_HARP: "Арфа",
    ITEM_HOE: "Мотыга",
    ITEM_WATERING_CAN: "Лейка",
    ITEM_FERTILIZER: "Удобрение",
    ITEM_LEATHER_STRIP: "Кожаная полоса",
    ITEM_SCALE: "Чешуя",
    ITEM_SHELL: "Панцирь",
    ITEM_FEATHER_BLUE: "Синее перо",
    ITEM_FEATHER_RED: "Красное перо",
    ITEM_FEATHER_GREEN: "Зелёное перо",
    ITEM_BONE_MEAL: "Костная мука",
    ITEM_WOOL: "Шерсть",
    ITEM_SPELLBOOK_FIRE: "Книга огня",
    ITEM_SPELLBOOK_ICE: "Книга льда",
    ITEM_SPELLBOOK_HEAL: "Книга лечения",
    ITEM_SPELLBOOK_TELEPORT: "Книга телепортации",
    ITEM_SCROLL_TELEPORT: "Свиток телепортации",
}

# ------------------- ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ -------------------
FLOWER_TYPES = [BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE]

# ------------------- ПОГОДА -------------------
WEATHER_CLEAR = 0
WEATHER_RAIN = 1
WEATHER_SNOW = 2

# ------------------- РЕЦЕПТЫ КРАФТА (полный список) -------------------
CRAFTING_RECIPES = [
    # Базовые (старые)
    ({'type': ITEM_TORCH, 'count': 4}, [(BLOCK_WOOD, 1), (ITEM_COAL, 1)]),
    ({'type': ITEM_POTION, 'count': 1}, [(ITEM_GEL, 2), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_BIG_POTION, 'count': 1}, [(ITEM_POTION, 2), (ITEM_LENS, 1)]),
    ({'type': ITEM_COPPER_INGOT, 'count': 1}, [(BLOCK_COPPER_ORE, 3)]),
    ({'type': ITEM_IRON_INGOT, 'count': 1}, [(BLOCK_IRON_ORE, 3)]),
    ({'type': ITEM_GOLD_INGOT, 'count': 1}, [(BLOCK_GOLD_ORE, 3)]),
    ({'type': ITEM_SWORD_WOOD, 'count': 1}, [(BLOCK_WOOD, 7)]),
    ({'type': ITEM_PICKAXE_WOOD, 'count': 1}, [(BLOCK_WOOD, 5)]),
    ({'type': ITEM_SWORD_COPPER, 'count': 1}, [(ITEM_COPPER_INGOT, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_IRON, 'count': 1}, [(ITEM_IRON_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_GOLD, 'count': 1}, [(ITEM_GOLD_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_DIAMOND, 'count': 1}, [(ITEM_DIAMOND, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_WOOD_SHIELD, 'count': 1}, [(BLOCK_WOOD, 10), (ITEM_BONE, 2)]),
    ({'type': ITEM_IRON_ARMOR, 'count': 1}, [(ITEM_IRON_INGOT, 12), (ITEM_COIN, 5)]),
    # Первое расширение
    ({'type': ITEM_STICK, 'count': 4}, [(BLOCK_WOOD, 2)]),
    ({'type': BLOCK_PLANKS, 'count': 4}, [(BLOCK_WOOD, 1)]),
    ({'type': ITEM_SWORD_STONE, 'count': 1}, [(BLOCK_STONE, 2), (ITEM_STICK, 1)]),
    ({'type': ITEM_PICKAXE_STONE, 'count': 1}, [(BLOCK_STONE, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_PICKAXE_DIAMOND, 'count': 1}, [(ITEM_DIAMOND, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_GOLD_ARMOR, 'count': 1}, [(ITEM_GOLD_INGOT, 8)]),
    ({'type': ITEM_DIAMOND_ARMOR, 'count': 1}, [(ITEM_DIAMOND, 8)]),
    ({'type': BLOCK_GLASS, 'count': 1}, [(BLOCK_SAND, 1)]),
    ({'type': BLOCK_BRICK, 'count': 1}, [(BLOCK_STONE, 4)]),
    ({'type': BLOCK_SANDSTONE, 'count': 1}, [(BLOCK_SAND, 2)]),
    ({'type': ITEM_APPLE, 'count': 1}, [(BLOCK_LEAVES, 3)]),
    ({'type': ITEM_BREAD, 'count': 1}, [(ITEM_APPLE, 2), (ITEM_GEL, 1)]),
    ({'type': ITEM_COOKED_MEAT, 'count': 1}, [(ITEM_GEL, 3), (ITEM_COAL, 1)]),
    # Второе расширение (слитки, инструменты, броня, зелья, еда, блоки)
    ({'type': ITEM_SILVER_INGOT, 'count': 1}, [(BLOCK_SILVER_ORE, 3)]),
    ({'type': ITEM_PLATINUM_INGOT, 'count': 1}, [(BLOCK_PLATINUM_ORE, 3)]),
    ({'type': ITEM_MITHRIL_INGOT, 'count': 1}, [(BLOCK_MITHRIL_ORE, 3)]),
    ({'type': ITEM_ADAMANTITE_INGOT, 'count': 1}, [(BLOCK_ADAMANTITE_ORE, 3)]),
    ({'type': ITEM_SWORD_SILVER, 'count': 1}, [(ITEM_SILVER_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_SILVER, 'count': 1}, [(ITEM_SILVER_INGOT, 4), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_PLATINUM, 'count': 1}, [(ITEM_PLATINUM_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_PLATINUM, 'count': 1}, [(ITEM_PLATINUM_INGOT, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_MITHRIL, 'count': 1}, [(ITEM_MITHRIL_INGOT, 10), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_MITHRIL, 'count': 1}, [(ITEM_MITHRIL_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_ADAMANTITE, 'count': 1}, [(ITEM_ADAMANTITE_INGOT, 12), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_ADAMANTITE, 'count': 1}, [(ITEM_ADAMANTITE_INGOT, 7), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SILVER_ARMOR, 'count': 1}, [(ITEM_SILVER_INGOT, 10)]),
    ({'type': ITEM_PLATINUM_ARMOR, 'count': 1}, [(ITEM_PLATINUM_INGOT, 12)]),
    ({'type': ITEM_MITHRIL_ARMOR, 'count': 1}, [(ITEM_MITHRIL_INGOT, 14)]),
    ({'type': ITEM_ADAMANTITE_ARMOR, 'count': 1}, [(ITEM_ADAMANTITE_INGOT, 16)]),
    ({'type': BLOCK_FENCE, 'count': 8}, [(BLOCK_WOOD, 2), (ITEM_STICK, 4)]),
    ({'type': BLOCK_LADDER, 'count': 6}, [(BLOCK_WOOD, 3)]),
    ({'type': BLOCK_ANVIL, 'count': 1}, [(ITEM_IRON_INGOT, 6)]),
    ({'type': BLOCK_FURNACE, 'count': 1}, [(BLOCK_STONE, 8), (ITEM_COAL, 1)]),
    ({'type': BLOCK_CHEST, 'count': 1}, [(BLOCK_WOOD, 8)]),
    ({'type': BLOCK_BOOKSHELF, 'count': 1}, [(BLOCK_WOOD, 6), (ITEM_BOOK, 3)]),
    ({'type': BLOCK_SNOW, 'count': 4}, [(BLOCK_GRASS, 1)]),
    ({'type': BLOCK_SANDSTONE_SMOOTH, 'count': 1}, [(BLOCK_SANDSTONE, 1)]),
    ({'type': BLOCK_OBSIDIAN, 'count': 1}, [(BLOCK_STONE, 2), (ITEM_COAL, 1)]),
    ({'type': BLOCK_GLOWSTONE, 'count': 1}, [(BLOCK_GLASS, 1), (ITEM_COAL, 1)]),
    ({'type': ITEM_POTION_REGENERATION, 'count': 1}, [(ITEM_POTION, 1), (ITEM_GEL, 2), (ITEM_SPIDER_EYE, 1)]),
    ({'type': ITEM_POTION_STRENGTH, 'count': 1}, [(ITEM_POTION, 1), (ITEM_WOLF_FANG, 1)]),
    ({'type': ITEM_POTION_SPEED, 'count': 1}, [(ITEM_POTION, 1), (ITEM_FEATHER, 2), (ITEM_LENS, 1)]),
    ({'type': ITEM_POTION_JUMP, 'count': 1}, [(ITEM_POTION, 1), (ITEM_GEL, 3)]),
    ({'type': ITEM_PIE, 'count': 1}, [(ITEM_APPLE, 3), (ITEM_GEL, 2), (ITEM_WHEAT, 2)]),
    ({'type': ITEM_SOUP, 'count': 1}, [(ITEM_APPLE, 2), (ITEM_GEL, 1), (ITEM_BOWL, 1)]),
    ({'type': ITEM_MUSHROOM_SOUP, 'count': 1}, [(ITEM_MUSHROOM, 2), (ITEM_BOWL, 1)]),
    ({'type': ITEM_COOKED_MUSHROOM, 'count': 1}, [(ITEM_MUSHROOM, 1), (ITEM_COAL, 1)]),
    ({'type': ITEM_BOW, 'count': 1}, [(ITEM_STICK, 3), (ITEM_STRING, 3)]),
    ({'type': ITEM_ARROW, 'count': 8}, [(ITEM_STICK, 1), (ITEM_FEATHER, 1), (ITEM_FLINT, 1)]),
    ({'type': ITEM_PAPER, 'count': 3}, [(BLOCK_WOOD, 1)]),
    ({'type': ITEM_BOOK, 'count': 1}, [(ITEM_LEATHER, 1), (ITEM_FEATHER, 2), (ITEM_PAPER, 3)]),
    ({'type': ITEM_TORCH, 'count': 8}, [(ITEM_STICK, 1), (BLOCK_GLOWSTONE, 1)]),
    # Третье расширение (огромное)
    ({'type': ITEM_TITAN_INGOT, 'count': 1}, [(BLOCK_TITAN_ORE, 3)]),
    ({'type': ITEM_COBALT_INGOT, 'count': 1}, [(BLOCK_COBALT_ORE, 3)]),
    ({'type': ITEM_NETHERITE_INGOT, 'count': 1}, [(BLOCK_NETHERITE_ORE, 3)]),
    ({'type': ITEM_CRYSTAL_INGOT, 'count': 1}, [(BLOCK_CRYSTAL_ORE, 3)]),
    ({'type': ITEM_SWORD_TITAN, 'count': 1}, [(ITEM_TITAN_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_TITAN, 'count': 1}, [(ITEM_TITAN_INGOT, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_AXE_TITAN, 'count': 1}, [(ITEM_TITAN_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_COBALT, 'count': 1}, [(ITEM_COBALT_INGOT, 8), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_COBALT, 'count': 1}, [(ITEM_COBALT_INGOT, 5), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_AXE_COBALT, 'count': 1}, [(ITEM_COBALT_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_NETHERITE, 'count': 1}, [(ITEM_NETHERITE_INGOT, 10), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_NETHERITE, 'count': 1}, [(ITEM_NETHERITE_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_AXE_NETHERITE, 'count': 1}, [(ITEM_NETHERITE_INGOT, 7), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SWORD_CRYSTAL, 'count': 1}, [(ITEM_CRYSTAL_INGOT, 6), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_PICKAXE_CRYSTAL, 'count': 1}, [(ITEM_CRYSTAL_INGOT, 4), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_TITAN_ARMOR, 'count': 1}, [(ITEM_TITAN_INGOT, 14)]),
    ({'type': ITEM_COBALT_ARMOR, 'count': 1}, [(ITEM_COBALT_INGOT, 14)]),
    ({'type': ITEM_NETHERITE_ARMOR, 'count': 1}, [(ITEM_NETHERITE_INGOT, 16)]),
    ({'type': ITEM_CRYSTAL_ARMOR, 'count': 1}, [(ITEM_CRYSTAL_INGOT, 12)]),
    ({'type': ITEM_HAMMER, 'count': 1}, [(ITEM_IRON_INGOT, 10), (BLOCK_WOOD, 2)]),
    ({'type': ITEM_SPEAR, 'count': 1}, [(ITEM_IRON_INGOT, 6), (ITEM_STICK, 3)]),
    ({'type': ITEM_CROSSBOW, 'count': 1}, [(ITEM_IRON_INGOT, 4), (ITEM_STICK, 2), (ITEM_STRING, 2)]),
    ({'type': ITEM_RUBY, 'count': 1}, [(ITEM_COPPER_INGOT, 2), (ITEM_GEL, 1)]),
    ({'type': ITEM_SAPPHIRE, 'count': 1}, [(ITEM_IRON_INGOT, 2), (ITEM_LENS, 1)]),
    ({'type': ITEM_EMERALD, 'count': 1}, [(ITEM_GOLD_INGOT, 2), (ITEM_APPLE, 1)]),
    ({'type': ITEM_AMETHYST, 'count': 1}, [(ITEM_SILVER_INGOT, 2), (ITEM_GEL, 2)]),
    ({'type': ITEM_OPAL, 'count': 1}, [(ITEM_PLATINUM_INGOT, 2), (ITEM_LENS, 2)]),
    ({'type': ITEM_AMBER, 'count': 1}, [(ITEM_GOLD_INGOT, 2), (ITEM_GEL, 3)]),
    ({'type': ITEM_STAFF_FIRE, 'count': 1}, [(ITEM_RUBY, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_STAFF_ICE, 'count': 1}, [(ITEM_SAPPHIRE, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_STAFF_LIGHTNING, 'count': 1}, [(ITEM_AMETHYST, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_STAFF_HEALING, 'count': 1}, [(ITEM_EMERALD, 3), (ITEM_STICK, 2)]),
    ({'type': ITEM_RING_STRENGTH, 'count': 1}, [(ITEM_RUBY, 2), (ITEM_IRON_INGOT, 1)]),
    ({'type': ITEM_RING_PROTECTION, 'count': 1}, [(ITEM_SAPPHIRE, 2), (ITEM_IRON_INGOT, 1)]),
    ({'type': ITEM_AMULET_REGENERATION, 'count': 1}, [(ITEM_EMERALD, 2), (ITEM_GOLD_INGOT, 1)]),
    ({'type': ITEM_AMULET_SPEED, 'count': 1}, [(ITEM_AMBER, 2), (ITEM_GOLD_INGOT, 1)]),
    ({'type': ITEM_NECKLACE_JUMP, 'count': 1}, [(ITEM_OPAL, 2), (ITEM_GOLD_INGOT, 1)]),
    ({'type': ITEM_PIZZA, 'count': 1}, [(ITEM_WHEAT, 2), (ITEM_TOMATO, 2), (ITEM_GEL, 1)]),
    ({'type': ITEM_BURGER, 'count': 1}, [(ITEM_WHEAT, 2), (ITEM_COOKED_MEAT, 1), (ITEM_TOMATO, 1)]),
    ({'type': ITEM_SUSHI, 'count': 1}, [(ITEM_FISH_SALMON, 2), (ITEM_WHEAT, 1)]),
    ({'type': ITEM_CAKE, 'count': 1}, [(ITEM_WHEAT, 3), (ITEM_APPLE, 2), (ITEM_GEL, 2)]),
    ({'type': ITEM_SALAD, 'count': 1}, [(ITEM_CARROT, 2), (ITEM_CUCUMBER, 2), (ITEM_TOMATO, 1)]),
    ({'type': ITEM_FRIED_POTATOES, 'count': 1}, [(ITEM_POTATO, 3), (ITEM_COAL, 1)]),
    ({'type': ITEM_CARROT_JUICE, 'count': 1}, [(ITEM_CARROT, 3), (ITEM_GEL, 1)]),
    ({'type': ITEM_BANANA, 'count': 1}, [(ITEM_APPLE, 1), (ITEM_GEL, 1)]),
    ({'type': ITEM_ORANGE, 'count': 1}, [(ITEM_APPLE, 1), (ITEM_LENS, 1)]),
    ({'type': ITEM_CARROT, 'count': 2}, [(BLOCK_GRASS, 1)]),
    ({'type': ITEM_POTATO, 'count': 2}, [(BLOCK_DIRT, 1)]),
    ({'type': ITEM_TOMATO, 'count': 2}, [(ITEM_APPLE, 1), (ITEM_GEL, 1)]),
    ({'type': ITEM_CUCUMBER, 'count': 2}, [(ITEM_APPLE, 1), (ITEM_WATERING_CAN, 1)]),
    ({'type': ITEM_POTION_NIGHT_VISION, 'count': 1}, [(ITEM_POTION, 1), (BLOCK_GLOWSTONE, 1)]),
    ({'type': ITEM_POTION_INVISIBILITY, 'count': 1}, [(ITEM_POTION, 1), (ITEM_AMETHYST, 1)]),
    ({'type': ITEM_POTION_WATER_BREATHING, 'count': 1}, [(ITEM_POTION, 1), (ITEM_FISH_PUFFER, 1)]),
    ({'type': ITEM_POTION_HASTE, 'count': 1}, [(ITEM_POTION, 1), (ITEM_COBALT_INGOT, 1)]),
    ({'type': ITEM_FISH_PERCH, 'count': 1}, [(ITEM_GEL, 2), (ITEM_APPLE, 1)]),
    ({'type': ITEM_FISH_SALMON, 'count': 1}, [(ITEM_GEL, 3), (ITEM_ORANGE, 1)]),
    ({'type': ITEM_FISH_GOLDFISH, 'count': 1}, [(ITEM_GOLD_INGOT, 1), (ITEM_GEL, 1)]),
    ({'type': ITEM_FISH_PUFFER, 'count': 1}, [(ITEM_GEL, 4), (ITEM_POTION, 1)]),
    ({'type': ITEM_FISHING_ROD, 'count': 1}, [(ITEM_STICK, 2), (ITEM_STRING, 2)]),
    ({'type': ITEM_BAIT, 'count': 4}, [(ITEM_GEL, 1)]),
    ({'type': BLOCK_DOOR, 'count': 1}, [(BLOCK_WOOD, 6)]),
    ({'type': BLOCK_WINDOW, 'count': 1}, [(BLOCK_GLASS, 4), (BLOCK_WOOD, 2)]),
    ({'type': BLOCK_SHUTTER, 'count': 1}, [(BLOCK_WOOD, 4)]),
    ({'type': BLOCK_PILLAR, 'count': 1}, [(BLOCK_STONE, 4)]),
    ({'type': BLOCK_STATUE, 'count': 1}, [(BLOCK_STONE, 6), (ITEM_GOLD_INGOT, 1)]),
    ({'type': BLOCK_CARPET, 'count': 1}, [(ITEM_WOOL, 4)]),
    ({'type': BLOCK_PAINTING, 'count': 1}, [(BLOCK_WOOD, 2), (ITEM_WOOL, 1), (ITEM_GEL, 1)]),
    ({'type': BLOCK_FRAME, 'count': 1}, [(BLOCK_WOOD, 2), (BLOCK_GLASS, 1)]),
    ({'type': BLOCK_SHELF, 'count': 1}, [(BLOCK_WOOD, 3)]),
    ({'type': BLOCK_BUSH, 'count': 1}, [(BLOCK_LEAVES, 2)]),
    ({'type': BLOCK_FERN, 'count': 1}, [(BLOCK_GRASS, 1), (ITEM_GEL, 1)]),
    ({'type': BLOCK_VINE, 'count': 2}, [(BLOCK_LEAVES, 1), (ITEM_STRING, 1)]),
    ({'type': BLOCK_TULIP_RED, 'count': 1}, [(BLOCK_FLOWER_RED, 1), (ITEM_GEL, 1)]),
    ({'type': BLOCK_TULIP_YELLOW, 'count': 1}, [(BLOCK_FLOWER_YELLOW, 1), (ITEM_GEL, 1)]),
    ({'type': BLOCK_DAISY, 'count': 1}, [(BLOCK_FLOWER_RED, 1), (BLOCK_FLOWER_YELLOW, 1)]),
    ({'type': ITEM_GUITAR, 'count': 1}, [(BLOCK_WOOD, 4), (ITEM_STRING, 3)]),
    ({'type': ITEM_FLUTE, 'count': 1}, [(ITEM_STICK, 4), (ITEM_GOLD_INGOT, 1)]),
    ({'type': ITEM_DRUM, 'count': 1}, [(BLOCK_WOOD, 3), (ITEM_LEATHER, 2)]),
    ({'type': ITEM_HARP, 'count': 1}, [(BLOCK_WOOD, 5), (ITEM_STRING, 4)]),
    ({'type': ITEM_HOE, 'count': 1}, [(ITEM_IRON_INGOT, 2), (ITEM_STICK, 1)]),
    ({'type': ITEM_WATERING_CAN, 'count': 1}, [(ITEM_IRON_INGOT, 3), (ITEM_GEL, 2)]),
    ({'type': ITEM_FERTILIZER, 'count': 2}, [(ITEM_BONE_MEAL, 1), (ITEM_GEL, 1)]),
    ({'type': ITEM_LEATHER_STRIP, 'count': 2}, [(ITEM_LEATHER, 1)]),
    ({'type': ITEM_SCALE, 'count': 1}, [(ITEM_FISH_SALMON, 1), (ITEM_IRON_INGOT, 1)]),
    ({'type': ITEM_SHELL, 'count': 1}, [(ITEM_FISH_PUFFER, 1), (BLOCK_STONE, 1)]),
    ({'type': ITEM_FEATHER_BLUE, 'count': 1}, [(ITEM_FEATHER, 1), (ITEM_SAPPHIRE, 1)]),
    ({'type': ITEM_FEATHER_RED, 'count': 1}, [(ITEM_FEATHER, 1), (ITEM_RUBY, 1)]),
    ({'type': ITEM_FEATHER_GREEN, 'count': 1}, [(ITEM_FEATHER, 1), (ITEM_EMERALD, 1)]),
    ({'type': ITEM_BONE_MEAL, 'count': 2}, [(ITEM_BONE, 1)]),
    ({'type': ITEM_WOOL, 'count': 2}, [(ITEM_STRING, 2)]),
    ({'type': ITEM_SPELLBOOK_FIRE, 'count': 1}, [(ITEM_BOOK, 1), (ITEM_RUBY, 3)]),
    ({'type': ITEM_SPELLBOOK_ICE, 'count': 1}, [(ITEM_BOOK, 1), (ITEM_SAPPHIRE, 3)]),
    ({'type': ITEM_SPELLBOOK_HEAL, 'count': 1}, [(ITEM_BOOK, 1), (ITEM_EMERALD, 3)]),
    ({'type': ITEM_SPELLBOOK_TELEPORT, 'count': 1}, [(ITEM_BOOK, 1), (ITEM_AMETHYST, 3)]),
    ({'type': ITEM_SCROLL_TELEPORT, 'count': 1}, [(ITEM_SPELLBOOK_TELEPORT, 1), (ITEM_FEATHER, 1)]),
]