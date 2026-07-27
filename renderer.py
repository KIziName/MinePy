import pygame
import math
import time
import sys
from blocks import *
from mobs import Slime, Zombie, DemonEye, Skeleton, Sheep

# ----------------------------------------------------------------------
# УТИЛИТЫ (иконки, облака, погода)
# ----------------------------------------------------------------------

def draw_item_icon(surface, item_type, x, y, size=32):
    """Детализированная отрисовка предметов (включая мечи и кирки)."""
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

    # ======== МЕЧИ ========
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

    # ======== КИРКИ ========
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

    # ======== ЗЕЛЬЯ ========
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

    # ======== СЛИТКИ ========
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

    # ======== РЕСУРСЫ ========
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
    else:
        # fallback для неизвестных предметов
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


# ------------------- ПОГОДА -------------------
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


# ----------------------------------------------------------------------
# ОСНОВНОЙ КЛАСС РЕНДЕРИНГА (перенесён из game.py)
# ----------------------------------------------------------------------

class GameRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height
        self.font_small = game.font_small
        self.font_med = game.font_med
        self.font_big = game.font_big
        self.font_huge = game.font_huge

    def render(self):
        """Главный метод отрисовки всего игрового состояния."""
        if self.game.game_state != "game":
            return

        # --- Фон ---
        t = self.game.day_time % 24000
        if t < 10000:
            bg = self.game.bg_surfaces['day']
        elif t < 12000:
            bg = self.game.bg_surfaces['sunset']
        elif t < 22000:
            bg = self.game.bg_surfaces['night']
        else:
            bg = self.game.bg_surfaces['sunrise']
        self.screen.blit(bg, (0, 0))

        # --- Звёзды ---
        if self.game.is_night():
            moon_x = self.screen_width - 100
            moon_y = 100
            moon_radius = 40
            now = time.time()
            for star in self.game.stars:
                x, y, size, brightness, twinkle_speed, phase = star
                dist = math.hypot(x - moon_x, y - moon_y)
                if dist < moon_radius * 2:
                    factor = max(0, (dist - moon_radius) / moon_radius)
                    brightness *= factor
                alpha = int(255 * brightness * (0.7 + 0.3 * math.sin(now * twinkle_speed + phase)))
                if alpha > 0:
                    star_surf = pygame.Surface((int(size*2)+2, int(size*2)+2), pygame.SRCALPHA)
                    pygame.draw.circle(star_surf, (255, 255, 255, alpha), (int(size)+1, int(size)+1), int(size))
                    self.screen.blit(star_surf, (int(x-size-1), int(y-size-1)))

        # --- Облака ---
        render_clouds(self.screen, self.game.clouds, self.screen_width, self.screen_height)

        # --- Солнце ---
        sun_angle = ((t % 24000) / 24000.0) * math.pi * 2 - math.pi / 2
        sun_x = self.screen_width / 2 + math.cos(sun_angle) * (self.screen_width * 0.45)
        sun_y = self.screen_height / 2 + math.sin(sun_angle) * (self.screen_height * 0.4)
        if sun_y < self.screen_height - 100:
            col = (255, 215, 0) if 0 <= t < 12000 else (236, 239, 241)
            pygame.draw.circle(self.screen, col, (int(sun_x), int(sun_y)), 22)

        self.draw_moon(self.screen_width - 100, 100, 35)

        # --- Чанки (мировые блоки) ---
        cam_x = self.game.player.x - self.screen_width / 2
        cam_y = self.game.player.y - self.screen_height / 2
        start_chunk = int(cam_x // (CHUNK_WIDTH * BLOCK_SIZE)) - 1
        end_chunk = int((cam_x + self.screen_width) // (CHUNK_WIDTH * BLOCK_SIZE)) + 2
        for cx in range(start_chunk, end_chunk):
            self.game.world.request_chunk(cx)
            surf = self.game.world.get_chunk_surface(cx)
            if surf is not None:
                x = cx * CHUNK_WIDTH * BLOCK_SIZE - cam_x
                y = -cam_y
                self.screen.blit(surf, (x, y))

        # --- Выпавшие предметы ---
        for item in self.game.mob_manager.dropped_items:
            sx = item.x - cam_x
            sy = item.y - cam_y + math.sin(item.bob_angle) * 4
            draw_item_icon(self.screen, item.item_type, int(sx - 12), int(sy - 12), size=24)

        # --- Мобы ---
        for mob in self.game.mob_manager.mobs:
            sx, sy = mob.x - cam_x, mob.y - cam_y
            if isinstance(mob, Slime):
                pygame.draw.ellipse(self.screen, mob.color, (sx-16, sy-12, 32, 24), 0)
                pygame.draw.ellipse(self.screen, (255,255,255), (sx-16, sy-12, 32, 24), 2)
            elif isinstance(mob, Zombie):
                pygame.draw.rect(self.screen, (56, 142, 60), (sx-12, sy-22, 24, 44), 0)
                pygame.draw.rect(self.screen, (93, 64, 55), (sx-10, sy-20, 20, 12))
            elif isinstance(mob, DemonEye):
                pygame.draw.circle(self.screen, (236, 239, 241), (int(sx), int(sy)), 14)
                pygame.draw.circle(self.screen, (211, 47, 47), (int(sx), int(sy)), 6)
            elif isinstance(mob, Skeleton):
                pygame.draw.rect(self.screen, (224, 224, 224), (sx-11, sy-21, 22, 42), 0)
            elif isinstance(mob, Sheep):
                pygame.draw.ellipse(self.screen, (255, 255, 255), (sx-15, sy-10, 30, 22), 0)
                pygame.draw.ellipse(self.screen, (200, 200, 200), (sx-15, sy-10, 30, 22), 2)

            bar_w = 30
            hp_pct = max(0, mob.hp / mob.max_hp)
            pygame.draw.rect(self.screen, (50,50,50), (sx - bar_w//2, sy - mob.h//2 - 10, bar_w, 4))
            if hp_pct > 0:
                pygame.draw.rect(self.screen, (118, 255, 3), (sx - bar_w//2, sy - mob.h//2 - 10, bar_w * hp_pct, 4))

        # --- Игрок ---
        px, py = self.game.player.x - cam_x, self.game.player.y - cam_y
        self.draw_player(px, py)

        # --- HP ---
        hp_x, hp_y = self.screen_width - 220, 20
        hp_pct = max(0, self.game.player.hp / self.game.player.max_hp)
        pygame.draw.rect(self.screen, (28, 37, 65), (hp_x, hp_y, 180, 22), 0)
        pygame.draw.rect(self.screen, (58, 80, 107), (hp_x, hp_y, 180, 22), 2)
        if hp_pct > 0:
            pygame.draw.rect(self.screen, (230, 57, 70), (hp_x+2, hp_y+2, 176*hp_pct, 18))
        hp_text = self.font_small.render(f"HP: {self.game.player.hp} / {self.game.player.max_hp}", True, (255,255,255))
        self.screen.blit(hp_text, (hp_x+45, hp_y+4))

        # --- FPS ---
        fps_color = (118, 255, 3) if self.game.current_fps >= 30 else (255, 82, 82)
        pygame.draw.rect(self.screen, (11, 19, 43), (self.screen_width // 2 - 45, 15, 90, 26), 0)
        pygame.draw.rect(self.screen, (58, 80, 107), (self.screen_width // 2 - 45, 15, 90, 26), 2)
        fps_text = self.font_small.render(f"FPS: {self.game.current_fps}", True, fps_color)
        self.screen.blit(fps_text, (self.screen_width // 2 - 25, 20))

        self.draw_hotbar()

        # --- Погода ---
        render_weather(self.screen, self.game.weather, self.game.rain_particles, self.game.snow_particles,
                       alpha=self.game.weather_alpha, width=self.screen_width, height=self.screen_height)

        # --- Инвентарь / пауза ---
        if self.game.inventory_open:
            self.draw_inventory()
        if self.game.pause_menu_open:
            self.draw_pause()

        # --- Уведомление о сохранении ---
        if self.game.save_notification_timer > 0:
            msg_surf = self.font_med.render("✓ Мир успешно сохранен!", True, (118, 255, 3))
            rect_w, rect_h = msg_surf.get_width() + 30, 36
            rect_x = self.screen_width // 2 - rect_w // 2
            rect_y = self.screen_height - 60
            pygame.draw.rect(self.screen, (11, 19, 43), (rect_x, rect_y, rect_w, rect_h), 0, 4)
            pygame.draw.rect(self.screen, (118, 255, 3), (rect_x, rect_y, rect_w, rect_h), 2, 4)
            self.screen.blit(msg_surf, (rect_x + 15, rect_y + 8))

        # --- Перетаскиваемый предмет ---
        if self.game.inventory.dragged_slot is not None:
            item = self.game.inventory.get_slot(self.game.inventory.dragged_slot)
            if item['type'] != BLOCK_AIR:
                draw_item_icon(self.screen, item['type'], self.game.mouse_x - 16, self.game.mouse_y - 16, size=32)

    # ---------- Вспомогательные методы отрисовки ----------
    def draw_hotbar(self):
        bar_x, bar_y = 15, 15
        for i in range(10):
            x, y = bar_x + i*48, bar_y
            item = self.game.inventory.get_slot(i)
            color = (11, 19, 43) if i != self.game.inventory.selected_slot else (255, 215, 0)
            pygame.draw.rect(self.screen, color, (x, y, 44, 44), 0)
            pygame.draw.rect(self.screen, (58, 80, 107), (x, y, 44, 44), 2 if i != self.game.inventory.selected_slot else 3)
            if item['type'] != BLOCK_AIR:
                draw_item_icon(self.screen, item['type'], x + 6, y + 6, size=32)
                if item['count'] > 1:
                    cnt = self.font_small.render(str(item['count']), True, (255,255,255))
                    self.screen.blit(cnt, (x + 22, y + 25))

    def draw_inventory(self):
        inv_w, inv_h = 490, 360
        inv_x, inv_y = 15, 70

        s = pygame.Surface((inv_w, inv_h))
        s.set_alpha(225)
        s.fill((11, 19, 43))
        self.screen.blit(s, (inv_x, inv_y))
        pygame.draw.rect(self.screen, (255, 215, 0), (inv_x, inv_y, inv_w, inv_h), 2)

        title = self.font_med.render("ИНВЕНТАРЬ И КРАФТ", True, (255, 215, 0))
        self.screen.blit(title, (inv_x + 160, inv_y + 10))

        for row in range(3):
            for col in range(10):
                idx = (row+1)*10 + col
                x, y = inv_x + 12 + col*46, inv_y + 40 + row*46
                item = self.game.inventory.get_slot(idx)
                is_selected = (self.game.inventory.dragged_slot == idx)
                bg_col = (28, 37, 65) if not is_selected else (58, 80, 107)
                pygame.draw.rect(self.screen, bg_col, (x, y, 42, 42), 0)
                pygame.draw.rect(self.screen, (58, 80, 107), (x, y, 42, 42), 1)
                if item['type'] != BLOCK_AIR and not is_selected:
                    draw_item_icon(self.screen, item['type'], x + 5, y + 5, size=32)
                    if item['count'] > 1:
                        cnt = self.font_small.render(str(item['count']), True, (255,255,255))
                        self.screen.blit(cnt, (x + 22, y + 24))

        craft_y = inv_y + 185
        for result, ingredients in CRAFTING_RECIPES:
            can_craft = self.game.inventory.can_craft(ingredients)
            color = (46, 125, 50) if can_craft else (38, 50, 56)
            rect = pygame.Rect(inv_x + 12, craft_y, 466, 24)
            pygame.draw.rect(self.screen, color, rect, 0)
            pygame.draw.rect(self.screen, (255,255,255), rect, 1)
            res_name = ITEM_NAMES.get(result['type'], "Предмет")
            req_text = " + ".join([f"{count}x {ITEM_NAMES.get(itype, '')}" for itype, count in ingredients])
            label = f"{res_name} (x{result['count']}) <-- [{req_text}]"
            text = self.font_small.render(label, True, (255,255,255))
            self.screen.blit(text, (inv_x + 20, craft_y + 4))
            craft_y += 27

    def draw_pause(self):
        # Затемнение
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(180)
        s.fill((0,0,0))
        self.screen.blit(s, (0,0))

        # Окно паузы
        box_w, box_h = 220, 200
        box_x = self.screen_width // 2 - box_w // 2
        box_y = self.screen_height // 2 - box_h // 2
        pygame.draw.rect(self.screen, (11, 19, 43), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(self.screen, (58, 80, 107), (box_x, box_y, box_w, box_h), 2)

        self.game.pause_buttons = []
        btn_y = box_y + 20
        btn_texts = [
            ("Продолжить", self.game.toggle_pause, (46, 125, 50), (27, 94, 32)),
            ("Главное меню", self.game.exit_to_menu, (211, 47, 47), (154, 0, 7)),
            (f"FPS: {self.game.target_fps}", self.game.cycle_fps, (100, 100, 100), (70, 70, 70)),
            ("Сохранить мир", self.game.save_manager.save, (21, 101, 192), (13, 71, 161))
        ]
        for text, action, color, hover_color in btn_texts:
            rect = pygame.Rect(box_x + 20, btn_y, box_w - 40, 30)
            is_hover = rect.collidepoint((self.game.mouse_x, self.game.mouse_y))
            draw_color = hover_color if is_hover else color
            self.game.pause_buttons.append((rect, action))
            pygame.draw.rect(self.screen, draw_color, rect, 0)
            pygame.draw.rect(self.screen, (255,255,255), rect, 1)
            txt = self.font_med.render(text, True, (255,255,255))
            self.screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + 6))
            btn_y += 35

    def draw_menu(self):
        """Отрисовка главного меню."""
        self.screen.fill((11, 19, 43))
        title = self.font_huge.render("MinePy 2D", True, (255, 215, 0))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 60))
        sub = self.font_small.render("Версия: 0.2", True, (141, 153, 174))
        self.screen.blit(sub, (self.screen_width // 2 - sub.get_width() // 2, 120))

        self.game.menu_buttons = []
        btn_y = 155
        btn_data = [
            ("GitHub: MinePy", self.game.open_github, (0, 0, 0, 0), (28, 37, 65)),
            ("НОВАЯ ИГРА", self.game.start_game, (46, 125, 50), (27, 94, 32)),
            ("ЗАГРУЗИТЬ МИР", self.game.load_and_start_game, (21, 101, 192), (13, 71, 161)),
            ("Полный экран", self.game.toggle_fullscreen, (255, 183, 3), (251, 133, 0)),
            ("ВЫХОД", sys.exit, (211, 47, 47), (154, 0, 7))
        ]
        for text, action, color, hover_color in btn_data:
            if text == "GitHub: MinePy":
                rect = pygame.Rect(self.screen_width // 2 - 130, btn_y, 260, 30)
                is_hover = rect.collidepoint((self.game.mouse_x, self.game.mouse_y))
                self.game.menu_buttons.append((rect, action))
                txt = self.font_med.render(text, True, (76, 201, 240) if is_hover else (0, 180, 216))
                self.screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + 4))
                btn_y += 40
            else:
                rect = pygame.Rect(self.screen_width // 2 - 130, btn_y, 260, 42)
                is_hover = rect.collidepoint((self.game.mouse_x, self.game.mouse_y))
                self.game.menu_buttons.append((rect, action))
                draw_color = hover_color if is_hover else color
                pygame.draw.rect(self.screen, draw_color, rect, 0)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                txt = self.font_med.render(text, True, (255, 255, 255))
                self.screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + 9))
                btn_y += 52
        author = self.font_small.render("Автор: KIziName", True, (224, 225, 221))
        self.screen.blit(author, (self.screen_width // 2 - author.get_width() // 2, self.screen_height - 35))

    def draw_player(self, px, py):
        """Отрисовка игрока."""
        if self.game.player.invulnerable_timer > 0:
            if int(time.time() * 10) % 2 == 0:
                return

        face_dir = 1 if self.game.player.facing_right else -1
        leg_step = math.sin(self.game.player.anim_frame) * 5 if self.game.player.is_grounded and self.game.player.vx != 0 else 0

        pygame.draw.rect(self.screen, (21, 101, 192), (px - 6 + leg_step, py + 8, 5, 14))
        pygame.draw.rect(self.screen, (13, 71, 161), (px + 1 - leg_step, py + 8, 5, 14))
        pygame.draw.rect(self.screen, (198, 40, 40), (px - 7, py - 8, 14, 16), 0, 2)
        pygame.draw.circle(self.screen, (255, 204, 128), (int(px), int(py - 14)), 8)
        pygame.draw.arc(self.screen, (121, 85, 72), (px - 8, py - 22, 16, 12), 0, math.pi, 4)

        eye_x = px + (3 * face_dir)
        pygame.draw.circle(self.screen, (33, 33, 33), (int(eye_x), int(py - 15)), 2)

        hand_x = px + (6 * face_dir)
        hand_y = py - 2
        swing_progress = self.game.player.swing_anim / 0.15 if self.game.player.swing_anim > 0 else 0
        swing_angle = (1 - swing_progress) * 80 if self.game.player.swing_anim > 0 else 0
        if not self.game.player.facing_right:
            swing_angle = -swing_angle

        curr_item = self.game.inventory.get_selected_item()['type']
        if curr_item != BLOCK_AIR:
            item_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            draw_item_icon(item_surf, curr_item, 0, 0, size=32)
            if not self.game.player.facing_right:
                item_surf = pygame.transform.flip(item_surf, True, False)
            rotated_item = pygame.transform.rotate(item_surf, -swing_angle if self.game.player.facing_right else swing_angle)
            item_rect = rotated_item.get_rect(center=(hand_x + (8 * face_dir), hand_y))
            self.screen.blit(rotated_item, item_rect)

        pygame.draw.circle(self.screen, (255, 204, 128), (int(hand_x), int(hand_y)), 3)

    def draw_moon(self, cx, cy, radius=30):
        if not self.game.is_night():
            return
        phase = (self.game.day_counter % 8) / 8.0
        moon_color = (220, 220, 240)
        pygame.draw.circle(self.screen, moon_color, (cx, cy), radius)
        if 0.05 < phase < 0.95:
            offset = radius * (1 - 2 * phase)
            shadow_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surf, (0, 0, 0, 200), (radius + offset, radius), radius)
            self.screen.blit(shadow_surf, (cx - radius, cy - radius), special_flags=pygame.BLEND_RGBA_SUB)