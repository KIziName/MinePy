import pygame
import math
import random
import threading
import queue
from blocks import *

class GameWorld:
    def __init__(self):
        self.chunk_data = {}
        self.chunk_surfaces = {}
        self.dirty_chunks = set()
        self.land_height_cache = {}

        self.lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.requested = set()
        self.active = True
        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

    def _worker_loop(self):
        while True:
            chunk_x = self.task_queue.get()
            if not self.active:
                self.task_queue.task_done()
                continue
            data = self._generate_chunk_data(chunk_x)
            with self.lock:
                if self.active:
                    self.chunk_data[chunk_x] = data
                    self.dirty_chunks.add(chunk_x)
            self.task_queue.task_done()

    def _generate_chunk_data(self, chunk_x):
        chunk = [[BLOCK_AIR for _ in range(CHUNK_WIDTH)] for _ in range(WORLD_HEIGHT)]
        for local_x in range(CHUNK_WIDTH):
            global_gx = chunk_x * CHUNK_WIDTH + local_x
            ground_h = self._get_land_height(global_gx)

            for gy in range(WORLD_HEIGHT - 1, ground_h - 1, -1):
                if gy == ground_h:
                    chunk[gy][local_x] = BLOCK_GRASS
                    if random.random() < DECORATION_CHANCE:
                        if random.random() < GRASS_CHANCE:
                            chunk[gy][local_x] = BLOCK_TALL_GRASS
                        else:
                            chunk[gy][local_x] = random.choice(FLOWER_TYPES)
                elif gy > ground_h - DIRT_LAYER_THICKNESS:
                    chunk[gy][local_x] = BLOCK_DIRT
                else:
                    r = random.random()
                    if r < ORE_GOLD_CHANCE and gy > ground_h + ORE_GOLD_MIN_DEPTH:
                        chunk[gy][local_x] = BLOCK_GOLD_ORE
                    elif r < ORE_IRON_CHANCE and gy > ground_h + ORE_IRON_MIN_DEPTH:
                        chunk[gy][local_x] = BLOCK_IRON_ORE
                    elif r < ORE_COPPER_CHANCE and gy > ground_h + ORE_COPPER_MIN_DEPTH:
                        chunk[gy][local_x] = BLOCK_COPPER_ORE
                    elif r < ORE_COAL_CHANCE and gy > ground_h + ORE_COAL_MIN_DEPTH:
                        chunk[gy][local_x] = BLOCK_COAL_ORE
                    else:
                        chunk[gy][local_x] = BLOCK_STONE

            if random.random() < TREE_CHANCE and ground_h > 8:
                tree_h = random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT)
                for th in range(tree_h):
                    if ground_h - th >= 0:
                        chunk[ground_h - th][local_x] = BLOCK_WOOD
                top_y = ground_h - tree_h
                for lx in range(-TREE_LEAF_RADIUS, TREE_LEAF_RADIUS + 1):
                    for ly in range(-TREE_LEAF_RADIUS, TREE_LEAF_RADIUS):
                        if abs(lx) == TREE_LEAF_RADIUS and abs(ly) == TREE_LEAF_RADIUS:
                            continue
                        gx_leaf, gy_leaf = local_x + lx, top_y + ly
                        if 0 <= gx_leaf < CHUNK_WIDTH and 0 <= gy_leaf < WORLD_HEIGHT:
                            if chunk[gy_leaf][gx_leaf] == BLOCK_AIR:
                                chunk[gy_leaf][gx_leaf] = BLOCK_LEAVES
        return chunk

    def _get_land_height(self, global_gx):
        if global_gx not in self.land_height_cache:
            h = int(LAND_HEIGHT_BASE
                    - (math.sin(global_gx * LAND_HEIGHT_FREQ) * LAND_HEIGHT_AMPLITUDE
                       + math.cos(global_gx * LAND_HEIGHT_FREQ2) * LAND_HEIGHT_AMPLITUDE2))
            self.land_height_cache[global_gx] = h
        return self.land_height_cache[global_gx]

    def request_chunk(self, chunk_x):
        with self.lock:
            if chunk_x in self.chunk_data or chunk_x in self.requested:
                return
            self.requested.add(chunk_x)
        self.task_queue.put(chunk_x)

    def ensure_chunk(self, chunk_x):
        with self.lock:
            if chunk_x in self.chunk_data:
                return
        data = self._generate_chunk_data(chunk_x)
        with self.lock:
            self.chunk_data[chunk_x] = data
            self.dirty_chunks.add(chunk_x)

    def get_block(self, global_gx, gy):
        if gy < 0 or gy >= WORLD_HEIGHT:
            return BLOCK_AIR
        chunk_x = global_gx // CHUNK_WIDTH
        self.ensure_chunk(chunk_x)
        with self.lock:
            data = self.chunk_data[chunk_x]
        return data[gy][global_gx % CHUNK_WIDTH]

    def set_block(self, global_gx, gy, block_type):
        if 0 <= gy < WORLD_HEIGHT:
            chunk_x = global_gx // CHUNK_WIDTH
            self.ensure_chunk(chunk_x)
            with self.lock:
                data = self.chunk_data[chunk_x]
                data[gy][global_gx % CHUNK_WIDTH] = block_type
                self.dirty_chunks.add(chunk_x)

    def get_chunk_surface(self, chunk_x):
        with self.lock:
            if chunk_x in self.chunk_surfaces and chunk_x not in self.dirty_chunks:
                return self.chunk_surfaces[chunk_x]

        with self.lock:
            data = self.chunk_data.get(chunk_x)
        if data is None:
            return None

        surf = self._render_chunk_data(chunk_x, data)
        with self.lock:
            self.chunk_surfaces[chunk_x] = surf
            self.dirty_chunks.discard(chunk_x)
        return surf

    def _render_chunk_data(self, chunk_x, data):
        surf = pygame.Surface((CHUNK_WIDTH * BLOCK_SIZE, WORLD_HEIGHT * BLOCK_SIZE), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        for gy in range(WORLD_HEIGHT):
            for gx in range(CHUNK_WIDTH):
                b = data[gy][gx]
                if b != BLOCK_AIR:
                    rect = (gx * BLOCK_SIZE, gy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surf, BLOCK_COLORS.get(b, (85, 85, 85)), rect)
                    if b not in (BLOCK_LEAVES, BLOCK_TALL_GRASS, BLOCK_FLOWER_RED,
                                 BLOCK_FLOWER_YELLOW, BLOCK_FLOWER_BLUE):
                        pygame.draw.rect(surf, (20, 20, 20), rect, 1)
        return surf

    def clear(self):
        with self.lock:
            self.active = False
            self.chunk_data.clear()
            self.chunk_surfaces.clear()
            self.dirty_chunks.clear()
            self.land_height_cache.clear()
            self.requested.clear()
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
                self.task_queue.task_done()
            except queue.Empty:
                break
        with self.lock:
            self.active = True

    def load_data(self, chunks_data):
        with self.lock:
            self.active = False
            self.chunk_data.clear()
            self.chunk_surfaces.clear()
            self.dirty_chunks.clear()
            self.requested.clear()
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
                self.task_queue.task_done()
            except queue.Empty:
                break
        with self.lock:
            self.chunk_data = {int(k): v for k, v in chunks_data.items()}
            self.dirty_chunks = set(self.chunk_data.keys())
            self.active = True