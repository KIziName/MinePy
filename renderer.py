import pygame
import math
from blocks import *

def draw_item_icon(surface, item_type, x, y, size=32):
    """Детализированная отрисовка предметов (включая мечи и кирки)"""
    if item_type in BLOCK_COLORS:
        if item_type == BLOCK_TALL_GRASS:
            pygame.draw.rect(surface, (76, 175, 80), (x+6, y+4, 20, 24))
            pygame.draw.line(surface, (50, 120, 50), (x+8, y+20), (x+16, y+4), 2)
            pygame.draw.line(surface, (50, 120, 50), (x+16, y+20), (x+24, y+4), 2)
            return
        elif item_type in (BLOCK_FLOWER_RED, BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE,
                           BLOCK_TULIP_RED, BLOCK_TULIP_YELLOW, BLOCK_DAISY):
            col = BLOCK_COLORS[item_type]
            cx, cy = x + size//2, y + size//2
            pygame.draw.circle(surface, col, (cx, cy-4), 6)
            pygame.draw.line(surface, (50, 150, 50), (cx, cy+2), (cx, cy+10), 2)
            return
        # Для остальных блоков рисуем квадрат с цветом
        pygame.draw.rect(surface, BLOCK_COLORS.get(item_type, (85,85,85)), (x+2, y+2, size-4, size-4))
        pygame.draw.rect(surface, (20,20,20), (x+2, y+2, size-4, size-4), 1)
        return

    cx, cy = x + size // 2, y + size // 2

    # ======== СТАРЫЕ МЕЧИ И КИРКИ ========
    if item_type in (ITEM_SWORD_WOOD, ITEM_SWORD_COPPER, ITEM_SWORD_IRON, ITEM_SWORD_GOLD, ITEM_SWORD_DIAMOND,
                     ITEM_SWORD_STONE, ITEM_SWORD_SILVER, ITEM_SWORD_PLATINUM, ITEM_SWORD_MITHRIL, ITEM_SWORD_ADAMANTITE,
                     ITEM_SWORD_TITAN, ITEM_SWORD_COBALT, ITEM_SWORD_NETHERITE, ITEM_SWORD_CRYSTAL):
        colors = {
            ITEM_SWORD_WOOD: (141,110,99), ITEM_SWORD_COPPER: (216,112,64),
            ITEM_SWORD_IRON: (220,235,245), ITEM_SWORD_GOLD: (255,215,0),
            ITEM_SWORD_DIAMOND: (0,229,255), ITEM_SWORD_STONE: (158,158,158),
            ITEM_SWORD_SILVER: (180,200,210), ITEM_SWORD_PLATINUM: (220,235,245),
            ITEM_SWORD_MITHRIL: (120,200,220), ITEM_SWORD_ADAMANTITE: (80,50,120),
            ITEM_SWORD_TITAN: (100,150,200), ITEM_SWORD_COBALT: (50,150,200),
            ITEM_SWORD_NETHERITE: (80,40,100), ITEM_SWORD_CRYSTAL: (200,240,255),
        }
        col = colors.get(item_type, (255,255,255))
        pygame.draw.line(surface, col, (x+8, y+size-8), (x+size-5, y+5), 4)
        pygame.draw.line(surface, (255,255,255), (x+10, y+size-10), (x+size-7, y+7), 1)
        pygame.draw.line(surface, (100,100,100), (x+7, y+size-13), (x+13, y+size-7), 3)
        pygame.draw.line(surface, (121,85,72), (x+5, y+size-5), (x+8, y+size-8), 3)
        pygame.draw.circle(surface, (200,200,200), (x+4, y+size-4), 2)

    elif item_type in (ITEM_PICKAXE_WOOD, ITEM_PICKAXE_COPPER, ITEM_PICKAXE_IRON, ITEM_PICKAXE_GOLD,
                       ITEM_PICKAXE_STONE, ITEM_PICKAXE_DIAMOND,
                       ITEM_PICKAXE_SILVER, ITEM_PICKAXE_PLATINUM, ITEM_PICKAXE_MITHRIL, ITEM_PICKAXE_ADAMANTITE,
                       ITEM_PICKAXE_TITAN, ITEM_PICKAXE_COBALT, ITEM_PICKAXE_NETHERITE, ITEM_PICKAXE_CRYSTAL):
        colors = {
            ITEM_PICKAXE_WOOD: (141,110,99), ITEM_PICKAXE_COPPER: (216,112,64),
            ITEM_PICKAXE_IRON: (220,235,245), ITEM_PICKAXE_GOLD: (255,215,0),
            ITEM_PICKAXE_STONE: (158,158,158), ITEM_PICKAXE_DIAMOND: (0,229,255),
            ITEM_PICKAXE_SILVER: (180,200,210), ITEM_PICKAXE_PLATINUM: (220,235,245),
            ITEM_PICKAXE_MITHRIL: (120,200,220), ITEM_PICKAXE_ADAMANTITE: (80,50,120),
            ITEM_PICKAXE_TITAN: (100,150,200), ITEM_PICKAXE_COBALT: (50,150,200),
            ITEM_PICKAXE_NETHERITE: (80,40,100), ITEM_PICKAXE_CRYSTAL: (200,240,255),
        }
        col = colors.get(item_type, (255,255,255))
        pygame.draw.line(surface, (101,67,33), (x+5, y+size-5), (x+size-8, y+8), 3)
        head_pts = [(x+size-16, y+4), (x+size-4, y+4), (x+size-4, y+16)]
        pygame.draw.lines(surface, col, False, head_pts, 4)
        pygame.draw.circle(surface, col, (x+size-4, y+4), 3)

    # ======== ТОПОРЫ ========
    elif item_type in (ITEM_AXE_TITAN, ITEM_AXE_COBALT, ITEM_AXE_NETHERITE):
        colors = {
            ITEM_AXE_TITAN: (100,150,200),
            ITEM_AXE_COBALT: (50,150,200),
            ITEM_AXE_NETHERITE: (80,40,100),
        }
        col = colors[item_type]
        pygame.draw.line(surface, (101,67,33), (x+5, y+size-5), (x+size-8, y+8), 3)
        pygame.draw.polygon(surface, col, [(x+size-14, y+4), (x+size-4, y+10), (x+size-4, y+20)])

    # ======== МОЛОТ, КОПЬЁ, АРБАЛЕТ ========
    elif item_type == ITEM_HAMMER:
        pygame.draw.rect(surface, (150,150,150), (x+8, y+8, size-16, size-16), 0)
        pygame.draw.line(surface, (101,67,33), (x+size//2, y+size-8), (x+size//2, y+size-4), 3)
    elif item_type == ITEM_SPEAR:
        pygame.draw.line(surface, (101,67,33), (x+5, y+size-5), (x+size-5, y+5), 3)
        pygame.draw.polygon(surface, (200,200,200), [(x+size-5, y+5), (x+size-2, y+8), (x+size-8, y+8)])
    elif item_type == ITEM_CROSSBOW:
        pygame.draw.rect(surface, (121,85,72), (x+6, y+10, size-12, size-12), 0)
        pygame.draw.arc(surface, (80,60,40), (x+4, y+8, size-8, size-12), 0, math.pi, 3)

    # ======== ЗЕЛЬЯ (старые и новые) ========
    elif item_type in (ITEM_POTION, ITEM_BIG_POTION, ITEM_POTION_REGENERATION,
                       ITEM_POTION_STRENGTH, ITEM_POTION_SPEED, ITEM_POTION_JUMP,
                       ITEM_POTION_NIGHT_VISION, ITEM_POTION_INVISIBILITY,
                       ITEM_POTION_WATER_BREATHING, ITEM_POTION_HASTE):
        colors = {
            ITEM_POTION: (229,57,53),
            ITEM_BIG_POTION: (156,39,176),
            ITEM_POTION_REGENERATION: (46,125,50),
            ITEM_POTION_STRENGTH: (211,47,47),
            ITEM_POTION_SPEED: (0,188,212),
            ITEM_POTION_JUMP: (255,183,77),
            ITEM_POTION_NIGHT_VISION: (0,100,200),
            ITEM_POTION_INVISIBILITY: (200,200,200),
            ITEM_POTION_WATER_BREATHING: (0,200,255),
            ITEM_POTION_HASTE: (255,200,0),
        }
        col = colors.get(item_type, (200,200,200))
        pygame.draw.circle(surface, col, (cx, cy+3), 7)
        pygame.draw.rect(surface, (200,200,200), (cx-3, cy-8, 6, 5))

    # ======== СЛИТКИ (все) ========
    elif item_type in (ITEM_COPPER_INGOT, ITEM_IRON_INGOT, ITEM_GOLD_INGOT,
                       ITEM_SILVER_INGOT, ITEM_PLATINUM_INGOT, ITEM_MITHRIL_INGOT, ITEM_ADAMANTITE_INGOT,
                       ITEM_TITAN_INGOT, ITEM_COBALT_INGOT, ITEM_NETHERITE_INGOT, ITEM_CRYSTAL_INGOT):
        colors = {
            ITEM_COPPER_INGOT: (216,112,64), ITEM_IRON_INGOT: (207,216,220),
            ITEM_GOLD_INGOT: (255,215,0), ITEM_SILVER_INGOT: (180,200,210),
            ITEM_PLATINUM_INGOT: (220,235,245), ITEM_MITHRIL_INGOT: (120,200,220),
            ITEM_ADAMANTITE_INGOT: (80,50,120), ITEM_TITAN_INGOT: (100,150,200),
            ITEM_COBALT_INGOT: (50,150,200), ITEM_NETHERITE_INGOT: (80,40,100),
            ITEM_CRYSTAL_INGOT: (200,240,255),
        }
        pygame.draw.polygon(surface, colors[item_type], [(x+6, y+20), (x+10, y+10), (x+22, y+10), (x+26, y+20)])

    # ======== САМОЦВЕТЫ ========
    elif item_type in (ITEM_RUBY, ITEM_SAPPHIRE, ITEM_EMERALD, ITEM_AMETHYST, ITEM_OPAL, ITEM_AMBER):
        colors = {
            ITEM_RUBY: (255,50,50), ITEM_SAPPHIRE: (50,50,255),
            ITEM_EMERALD: (50,255,50), ITEM_AMETHYST: (200,50,200),
            ITEM_OPAL: (200,200,255), ITEM_AMBER: (255,200,50),
        }
        pygame.draw.circle(surface, colors[item_type], (cx, cy), 8)
        pygame.draw.circle(surface, (255,255,255), (cx-2, cy-2), 3)

    # ======== ПОСОХИ ========
    elif item_type in (ITEM_STAFF_FIRE, ITEM_STAFF_ICE, ITEM_STAFF_LIGHTNING, ITEM_STAFF_HEALING):
        color = {
            ITEM_STAFF_FIRE: (255,100,0), ITEM_STAFF_ICE: (0,150,255),
            ITEM_STAFF_LIGHTNING: (255,255,0), ITEM_STAFF_HEALING: (0,255,100),
        }[item_type]
        pygame.draw.line(surface, (101,67,33), (x+8, y+size-8), (x+size-8, y+8), 4)
        pygame.draw.circle(surface, color, (x+size-8, y+8), 6)

    # ======== УКРАШЕНИЯ ========
    elif item_type in (ITEM_RING_STRENGTH, ITEM_RING_PROTECTION):
        pygame.draw.circle(surface, (200,200,0), (cx, cy), 7, 2)
        pygame.draw.circle(surface, (255,215,0), (cx, cy), 3)
    elif item_type in (ITEM_AMULET_REGENERATION, ITEM_AMULET_SPEED, ITEM_NECKLACE_JUMP):
        pygame.draw.line(surface, (200,200,0), (cx, y+4), (cx, y+20), 2)
        pygame.draw.circle(surface, (255,215,0), (cx, y+20), 5)

    # ======== ЕДА ========
    elif item_type in (ITEM_APPLE, ITEM_BREAD, ITEM_COOKED_MEAT, ITEM_PIE, ITEM_SOUP,
                       ITEM_MUSHROOM_SOUP, ITEM_COOKED_MUSHROOM,
                       ITEM_PIZZA, ITEM_BURGER, ITEM_SUSHI, ITEM_CAKE,
                       ITEM_SALAD, ITEM_FRIED_POTATOES, ITEM_CARROT_JUICE):
        if item_type == ITEM_APPLE:
            pygame.draw.circle(surface, (255,0,0), (cx, cy), 8)
            pygame.draw.line(surface, (139,69,19), (cx, cy-8), (cx, cy-12), 2)
        elif item_type == ITEM_BREAD:
            pygame.draw.ellipse(surface, (210,180,140), (x+6, y+10, size-12, size-16))
            pygame.draw.line(surface, (139,69,19), (x+10, y+10), (x+22, y+10), 1)
            pygame.draw.line(surface, (139,69,19), (x+10, y+16), (x+22, y+16), 1)
        elif item_type == ITEM_COOKED_MEAT:
            pygame.draw.ellipse(surface, (139,69,19), (x+6, y+10, size-12, size-16))
            pygame.draw.ellipse(surface, (205,133,63), (x+8, y+12, size-16, size-20))
        elif item_type == ITEM_PIE:
            pygame.draw.circle(surface, (210,180,140), (cx, cy), 8)
            pygame.draw.line(surface, (139,69,19), (cx-6, cy), (cx+6, cy), 2)
        elif item_type == ITEM_SOUP:
            pygame.draw.ellipse(surface, (255,200,100), (x+6, y+8, size-12, size-16))
            pygame.draw.ellipse(surface, (200,180,80), (x+8, y+10, size-16, size-20))
        elif item_type == ITEM_MUSHROOM_SOUP:
            pygame.draw.ellipse(surface, (200,180,150), (x+6, y+8, size-12, size-16))
            pygame.draw.circle(surface, (120,80,60), (cx, cy-2), 4)
        elif item_type == ITEM_COOKED_MUSHROOM:
            pygame.draw.ellipse(surface, (160,120,70), (x+6, y+10, size-12, size-16))
            pygame.draw.circle(surface, (80,60,40), (cx, cy-2), 4)
        elif item_type == ITEM_PIZZA:
            pygame.draw.circle(surface, (210,180,140), (cx, cy), 8)
            pygame.draw.line(surface, (200,50,50), (cx-6, cy), (cx+6, cy), 2)
            pygame.draw.line(surface, (200,50,50), (cx, cy-6), (cx, cy+6), 2)
        elif item_type == ITEM_BURGER:
            pygame.draw.ellipse(surface, (210,180,140), (x+6, y+10, size-12, size-16))
            pygame.draw.ellipse(surface, (139,69,19), (x+8, y+12, size-16, size-20))
            pygame.draw.ellipse(surface, (50,200,50), (x+10, y+14, size-20, size-16))
        elif item_type == ITEM_SUSHI:
            pygame.draw.ellipse(surface, (200,200,200), (x+6, y+10, size-12, size-16))
            pygame.draw.ellipse(surface, (255,100,100), (x+10, y+12, size-20, size-12))
        elif item_type == ITEM_CAKE:
            pygame.draw.rect(surface, (255,200,200), (x+6, y+8, size-12, size-16))
            pygame.draw.circle(surface, (255,50,50), (x+10, y+8), 3)
            pygame.draw.circle(surface, (255,50,50), (x+size-10, y+8), 3)
        elif item_type == ITEM_SALAD:
            pygame.draw.ellipse(surface, (50,200,50), (x+6, y+10, size-12, size-16))
            pygame.draw.circle(surface, (200,50,50), (x+10, y+12), 4)
            pygame.draw.circle(surface, (200,200,50), (x+20, y+12), 4)
        elif item_type == ITEM_FRIED_POTATOES:
            for i in range(3):
                pygame.draw.ellipse(surface, (200,180,100), (x+8+i*6, y+10, 8, 12))
        elif item_type == ITEM_CARROT_JUICE:
            pygame.draw.rect(surface, (255,150,50), (x+10, y+8, size-20, size-16))
            pygame.draw.rect(surface, (200,100,0), (x+12, y+10, size-24, size-20))

    # ======== ФРУКТЫ/ОВОЩИ ========
    elif item_type in (ITEM_BANANA, ITEM_ORANGE, ITEM_CARROT, ITEM_POTATO, ITEM_TOMATO, ITEM_CUCUMBER):
        if item_type == ITEM_BANANA:
            pygame.draw.ellipse(surface, (255,255,100), (x+8, y+10, size-16, size-12))
        elif item_type == ITEM_ORANGE:
            pygame.draw.circle(surface, (255,200,50), (cx, cy), 8)
        elif item_type == ITEM_CARROT:
            pygame.draw.polygon(surface, (255,150,50), [(x+10, y+6), (x+22, y+6), (x+16, y+26)])
        elif item_type == ITEM_POTATO:
            pygame.draw.ellipse(surface, (180,150,100), (x+8, y+10, size-16, size-12))
        elif item_type == ITEM_TOMATO:
            pygame.draw.circle(surface, (255,50,50), (cx, cy), 8)
            pygame.draw.line(surface, (50,200,50), (cx, cy-8), (cx, cy-12), 2)
        elif item_type == ITEM_CUCUMBER:
            pygame.draw.ellipse(surface, (50,200,50), (x+8, y+12, size-16, size-10))

    # ======== ЛУК И СТРЕЛЫ ========
    elif item_type == ITEM_BOW:
        pygame.draw.arc(surface, (121,85,72), (x+4, y+6, size-8, size-12), 0, math.pi, 3)
        pygame.draw.line(surface, (101,67,33), (x+6, y+8), (x+size-6, y+8), 2)
    elif item_type == ITEM_ARROW:
        pygame.draw.line(surface, (121,85,72), (x+4, y+size//2), (x+size-4, y+size//2), 2)
        pygame.draw.polygon(surface, (200,200,200), [(x+size-4, y+size//2), (x+size-10, y+size//2-4), (x+size-10, y+size//2+4)])

    # ======== РЫБА ========
    elif item_type in (ITEM_FISH_PERCH, ITEM_FISH_SALMON, ITEM_FISH_GOLDFISH, ITEM_FISH_PUFFER):
        colors = {
            ITEM_FISH_PERCH: (200,200,100),
            ITEM_FISH_SALMON: (255,150,150),
            ITEM_FISH_GOLDFISH: (255,215,0),
            ITEM_FISH_PUFFER: (100,200,100),
        }
        pygame.draw.ellipse(surface, colors[item_type], (x+6, y+10, size-12, size-16))
        pygame.draw.polygon(surface, (200,200,200), [(x+size-6, y+14), (x+size-2, y+10), (x+size-2, y+18)])

    # ======== УДОЧКА И НАЖИВКА ========
    elif item_type == ITEM_FISHING_ROD:
        pygame.draw.line(surface, (101,67,33), (x+4, y+size-4), (x+size-4, y+4), 3)
        pygame.draw.line(surface, (200,200,200), (x+size-4, y+4), (x+size-2, y+8), 2)
    elif item_type == ITEM_BAIT:
        pygame.draw.circle(surface, (150,100,50), (cx, cy), 5)

    # ======== МУЗЫКАЛЬНЫЕ ИНСТРУМЕНТЫ ========
    elif item_type in (ITEM_GUITAR, ITEM_FLUTE, ITEM_DRUM, ITEM_HARP):
        if item_type == ITEM_GUITAR:
            pygame.draw.ellipse(surface, (160,120,80), (x+8, y+12, size-16, size-16))
            pygame.draw.line(surface, (101,67,33), (x+16, y+6), (x+16, y+size-6), 3)
        elif item_type == ITEM_FLUTE:
            pygame.draw.line(surface, (200,180,150), (x+6, y+16), (x+size-6, y+16), 4)
            for i in range(4):
                pygame.draw.circle(surface, (0,0,0), (x+8+i*5, y+16), 1)
        elif item_type == ITEM_DRUM:
            pygame.draw.ellipse(surface, (200,200,200), (x+8, y+10, size-16, size-12))
            pygame.draw.rect(surface, (160,120,80), (x+12, y+10, size-24, 4))
        elif item_type == ITEM_HARP:
            pygame.draw.arc(surface, (160,120,80), (x+6, y+6, size-12, size-12), 0, math.pi, 3)
            for i in range(5):
                pygame.draw.line(surface, (200,200,200), (x+8+i*4, y+6), (x+8+i*4, y+size-6), 1)

    # ======== ФЕРМЕРСКИЕ ИНСТРУМЕНТЫ ========
    elif item_type in (ITEM_HOE, ITEM_WATERING_CAN, ITEM_FERTILIZER):
        if item_type == ITEM_HOE:
            pygame.draw.line(surface, (101,67,33), (x+5, y+size-5), (x+size-8, y+8), 3)
            pygame.draw.rect(surface, (150,150,150), (x+size-14, y+6, 8, 8))
        elif item_type == ITEM_WATERING_CAN:
            pygame.draw.rect(surface, (150,150,150), (x+8, y+12, size-16, size-14))
            pygame.draw.rect(surface, (100,100,100), (x+size-10, y+8, 6, 8))
            for i in range(4):
                pygame.draw.circle(surface, (0,0,255), (x+10+i*4, y+14), 1)
        elif item_type == ITEM_FERTILIZER:
            pygame.draw.rect(surface, (100,80,50), (x+8, y+10, size-16, size-16))

    # ======== РЕСУРСЫ (кожа, нить, перья, костная мука, шерсть и т.д.) ========
    elif item_type in (ITEM_LEATHER, ITEM_STRING, ITEM_FEATHER, ITEM_FLINT, ITEM_STICK,
                       ITEM_GEL, ITEM_COIN, ITEM_COAL, ITEM_DIAMOND, ITEM_TORCH,
                       ITEM_BONE, ITEM_LENS, ITEM_SPIDER_EYE, ITEM_WOLF_FANG,
                       ITEM_DRAGON_SCALE, ITEM_BOOK, ITEM_PAPER, ITEM_BOWL,
                       ITEM_MUSHROOM, ITEM_WHEAT, ITEM_LEATHER_STRIP, ITEM_SCALE,
                       ITEM_SHELL, ITEM_FEATHER_BLUE, ITEM_FEATHER_RED, ITEM_FEATHER_GREEN,
                       ITEM_BONE_MEAL, ITEM_WOOL):
        if item_type == ITEM_GEL:
            pygame.draw.circle(surface, (66,165,245), (cx, cy), 7)
        elif item_type == ITEM_COIN:
            pygame.draw.circle(surface, (255,215,0), (cx, cy), 6)
        elif item_type == ITEM_COAL:
            pygame.draw.circle(surface, (33,33,33), (cx, cy), 7)
        elif item_type == ITEM_DIAMOND:
            pygame.draw.polygon(surface, (0,229,255), [(cx, y+6), (x+24, cy), (cx, y+26), (x+8, cy)])
        elif item_type == ITEM_TORCH:
            pygame.draw.rect(surface, (121,85,72), (cx-2, cy-2, 4, 12))
            pygame.draw.circle(surface, (255,112,67), (cx, cy-4), 4)
        elif item_type == ITEM_STICK:
            pygame.draw.line(surface, (121,85,72), (x+8, y+24), (x+24, y+8), 4)
        elif item_type == ITEM_LEATHER:
            pygame.draw.rect(surface, (139,69,19), (x+6, y+10, size-12, size-16), 0)
        elif item_type == ITEM_STRING:
            pygame.draw.line(surface, (200,200,200), (x+6, y+10), (x+26, y+10), 2)
            pygame.draw.line(surface, (200,200,200), (x+6, y+16), (x+26, y+16), 2)
        elif item_type == ITEM_FEATHER:
            pygame.draw.polygon(surface, (255,255,255), [(x+8, y+24), (x+24, y+24), (x+16, y+6)])
        elif item_type == ITEM_FLINT:
            pygame.draw.polygon(surface, (50,50,50), [(x+6, y+20), (x+26, y+20), (x+16, y+6)])
        elif item_type == ITEM_BONE:
            pygame.draw.rect(surface, (220,220,220), (x+10, y+8, size-20, size-16))
        elif item_type == ITEM_LENS:
            pygame.draw.circle(surface, (200,230,255), (cx, cy), 7)
            pygame.draw.circle(surface, (255,255,255), (cx-2, cy-2), 3)
        elif item_type == ITEM_SPIDER_EYE:
            pygame.draw.circle(surface, (200,0,0), (cx, cy), 6)
            pygame.draw.circle(surface, (0,0,0), (cx-2, cy-2), 2)
        elif item_type == ITEM_WOLF_FANG:
            pygame.draw.polygon(surface, (255,255,255), [(x+10, y+6), (x+18, y+6), (x+14, y+24)])
        elif item_type == ITEM_DRAGON_SCALE:
            pygame.draw.polygon(surface, (255,200,100), [(x+6, y+6), (x+26, y+6), (x+16, y+26)])
        elif item_type == ITEM_BOOK:
            pygame.draw.rect(surface, (150,50,20), (x+6, y+6, size-12, size-12), 0)
            pygame.draw.line(surface, (200,200,200), (x+12, y+6), (x+12, y+size-6), 2)
        elif item_type == ITEM_PAPER:
            pygame.draw.rect(surface, (240,235,200), (x+6, y+8, size-12, size-16), 0)
            pygame.draw.line(surface, (200,190,160), (x+10, y+12), (x+22, y+12), 1)
        elif item_type == ITEM_BOWL:
            pygame.draw.ellipse(surface, (200,180,150), (x+6, y+10, size-12, size-16), 2)
        elif item_type == ITEM_MUSHROOM:
            pygame.draw.ellipse(surface, (160,120,70), (x+8, y+10, size-16, size-16), 0)
            pygame.draw.ellipse(surface, (200,180,160), (x+10, y+8, size-20, size-12), 0)
        elif item_type == ITEM_WHEAT:
            pygame.draw.line(surface, (200,180,100), (x+12, y+6), (x+20, y+6), 2)
            pygame.draw.line(surface, (200,180,100), (x+12, y+10), (x+20, y+10), 2)
            pygame.draw.line(surface, (200,180,100), (x+12, y+14), (x+20, y+14), 2)
            pygame.draw.line(surface, (100,80,50), (x+16, y+6), (x+16, y+26), 2)
        elif item_type == ITEM_LEATHER_STRIP:
            pygame.draw.rect(surface, (139,69,19), (x+6, y+12, size-12, 8))
        elif item_type == ITEM_SCALE:
            pygame.draw.ellipse(surface, (200,200,200), (x+8, y+10, size-16, size-12))
        elif item_type == ITEM_SHELL:
            pygame.draw.ellipse(surface, (180,160,140), (x+8, y+10, size-16, size-12))
        elif item_type in (ITEM_FEATHER_BLUE, ITEM_FEATHER_RED, ITEM_FEATHER_GREEN):
            colors = {ITEM_FEATHER_BLUE: (50,50,255), ITEM_FEATHER_RED: (255,50,50), ITEM_FEATHER_GREEN: (50,255,50)}
            pygame.draw.polygon(surface, colors[item_type], [(x+8, y+24), (x+24, y+24), (x+16, y+6)])
        elif item_type == ITEM_BONE_MEAL:
            pygame.draw.rect(surface, (220,220,200), (x+8, y+10, size-16, size-16))
        elif item_type == ITEM_WOOL:
            pygame.draw.ellipse(surface, (200,200,200), (x+8, y+10, size-16, size-12))

    # ======== КНИГИ ЗАКЛИНАНИЙ И СВИТКИ ========
    elif item_type in (ITEM_SPELLBOOK_FIRE, ITEM_SPELLBOOK_ICE, ITEM_SPELLBOOK_HEAL, ITEM_SPELLBOOK_TELEPORT):
        colors = {
            ITEM_SPELLBOOK_FIRE: (255,100,0),
            ITEM_SPELLBOOK_ICE: (0,150,255),
            ITEM_SPELLBOOK_HEAL: (0,255,100),
            ITEM_SPELLBOOK_TELEPORT: (200,50,200),
        }
        pygame.draw.rect(surface, colors[item_type], (x+6, y+6, size-12, size-12), 0)
        pygame.draw.rect(surface, (200,200,200), (x+8, y+8, size-16, size-16), 1)
    elif item_type == ITEM_SCROLL_TELEPORT:
        pygame.draw.rect(surface, (240,230,200), (x+6, y+8, size-12, size-16))
        pygame.draw.line(surface, (200,100,50), (x+10, y+12), (x+22, y+12), 1)
        pygame.draw.line(surface, (200,100,50), (x+10, y+16), (x+22, y+16), 1)

    # ======== БРОНЯ ========
    elif item_type in (ITEM_IRON_ARMOR, ITEM_GOLD_ARMOR, ITEM_DIAMOND_ARMOR,
                       ITEM_SILVER_ARMOR, ITEM_PLATINUM_ARMOR, ITEM_MITHRIL_ARMOR,
                       ITEM_ADAMANTITE_ARMOR, ITEM_TITAN_ARMOR, ITEM_COBALT_ARMOR,
                       ITEM_NETHERITE_ARMOR, ITEM_CRYSTAL_ARMOR):
        colors = {
            ITEM_IRON_ARMOR: (207,216,220), ITEM_GOLD_ARMOR: (255,215,0),
            ITEM_DIAMOND_ARMOR: (0,229,255), ITEM_SILVER_ARMOR: (180,200,210),
            ITEM_PLATINUM_ARMOR: (220,235,245), ITEM_MITHRIL_ARMOR: (120,200,220),
            ITEM_ADAMANTITE_ARMOR: (80,50,120), ITEM_TITAN_ARMOR: (100,150,200),
            ITEM_COBALT_ARMOR: (50,150,200), ITEM_NETHERITE_ARMOR: (80,40,100),
            ITEM_CRYSTAL_ARMOR: (200,240,255),
        }
        col = colors.get(item_type, (200,200,200))
        pygame.draw.rect(surface, col, (x+6, y+6, size-12, size-12), 0)
        pygame.draw.rect(surface, (20,20,20), (x+6, y+6, size-12, size-12), 2)

    else:
        # fallback
        pygame.draw.circle(surface, (180,180,180), (cx, cy), 6)


# ------------------- ОБЛАКА ------------------
def render_clouds(screen, clouds, width, height):
    for cloud in clouds:
        x = cloud['x']
        y = cloud['y']
        w = cloud['w']
        h = cloud['h']
        pygame.draw.ellipse(screen, (255, 255, 255), (x, y, w, h))
        pygame.draw.ellipse(screen, (255, 255, 255), (x + w*0.2, y - h*0.3, w*0.6, h*0.8))
        pygame.draw.ellipse(screen, (255, 255, 255), (x - w*0.1, y + h*0.1, w*0.3, h*0.6))


# ------------------- ПОГОДА  -------------------
def render_weather(screen, weather, rain_particles, snow_particles, alpha=1.0, width=None, height=None):
    """Рисует дождь и снег с прозрачностью alpha (0..1)."""
    if weather == WEATHER_RAIN and rain_particles:
        surf = pygame.Surface((width or SCREEN_WIDTH, height or SCREEN_HEIGHT), pygame.SRCALPHA)
        for x, y, speed in rain_particles:
            pygame.draw.line(surf, (180, 200, 255, int(255 * alpha)), (x, y), (x - 2, y + 10), 1)
        screen.blit(surf, (0, 0))
    elif weather == WEATHER_SNOW and snow_particles:
        surf = pygame.Surface((width or SCREEN_WIDTH, height or SCREEN_HEIGHT), pygame.SRCALPHA)
        for x, y, size in snow_particles:
            pygame.draw.circle(surf, (255, 255, 255, int(255 * alpha)), (int(x), int(y)), int(size))
        screen.blit(surf, (0, 0))