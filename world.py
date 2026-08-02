import pygame
import math
import random
import threading
import queue
import numpy as np

from blocks import *  

class GameWorld:
    def __init__(self):
        self.chunk_data = {}          # chunk_x -> np.ndarray (H, W)
        self.chunk_surfaces = {}
        self.dirty_chunks = set()
        self.land_height_cache = {}

        self.lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.requested = set()

        self.running = True
        self.worker = threading.Thread(target=self._worker_loop, daemon=False)
        self.worker.start()

    def _worker_loop(self):
        while self.running:
            try:
                chunk_x = self.task_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            if chunk_x is None:
                self.task_queue.task_done()
                break
            try:
                with self.lock:
                    if chunk_x in self.chunk_data:
                        self.task_queue.task_done()
                        continue
                data = self._generate_chunk_data(chunk_x)   # np.ndarray (H, W)
                with self.lock:
                    if self.running and chunk_x not in self.chunk_data:
                        self.chunk_data[chunk_x] = data
                        self.dirty_chunks.add(chunk_x)
                        self.requested.discard(chunk_x)
            except Exception as e:
                print(f"Ошибка в потоке генерации чанка {chunk_x}: {e}")
                import traceback
                traceback.print_exc()
            finally:
                self.task_queue.task_done()

    def stop(self):
        with self.lock:
            self.running = False
        self.task_queue.put(None)
        if self.worker.is_alive():
            self.worker.join(timeout=1.0)

    def _get_land_height(self, global_gx):
        if global_gx not in self.land_height_cache:
            h = int(
                LAND_HEIGHT_BASE
                - (math.sin(global_gx * LAND_HEIGHT_FREQ) * LAND_HEIGHT_AMPLITUDE
                   + math.cos(global_gx * LAND_HEIGHT_FREQ2) * LAND_HEIGHT_AMPLITUDE2)
            )
            self.land_height_cache[global_gx] = h
        return self.land_height_cache[global_gx]

    # ---------- ГЕНЕРАЦИЯ ЧАНКА (NumPy) ----------
    def _generate_chunk_data(self, chunk_x):
        # Создаём пустой чанк (воздух) - форма (WORLD_HEIGHT, CHUNK_WIDTH)
        chunk = np.full((WORLD_HEIGHT, CHUNK_WIDTH), BLOCK_AIR, dtype=np.int16)

        # 1. Базовый ландшафт (заполняем СНИЗУ ВВЕРХ, как в старой версии)
        for local_x in range(CHUNK_WIDTH):
            global_gx = chunk_x * CHUNK_WIDTH + local_x
            ground_h = self._get_land_height(global_gx)  # верхняя граница земли

            # Трава на поверхности (ground_h)
            chunk[ground_h, local_x] = BLOCK_GRASS

            # Земля (слой ниже травы)
            soil_top = ground_h + 1
            soil_bottom = min(WORLD_HEIGHT, ground_h + DIRT_LAYER_THICKNESS)
            if soil_top < soil_bottom:
                chunk[soil_top:soil_bottom, local_x] = BLOCK_DIRT

            # Камень (всё, что ниже земли)
            if soil_bottom < WORLD_HEIGHT:
                chunk[soil_bottom:, local_x] = BLOCK_STONE

        # 2. Генерация руд (векторизованно) - только на камне (который теперь внизу)
        depths = WORLD_HEIGHT - np.arange(WORLD_HEIGHT)[:, None]  # форма (H, W)
        rand = np.random.random((WORLD_HEIGHT, CHUNK_WIDTH))
        stone_mask = (chunk == BLOCK_STONE)

        ores = [
            (ORE_GOLD_CHANCE, ORE_GOLD_MIN_DEPTH, BLOCK_GOLD_ORE),
            (ORE_IRON_CHANCE, ORE_IRON_MIN_DEPTH, BLOCK_IRON_ORE),
            (ORE_COPPER_CHANCE, ORE_COPPER_MIN_DEPTH, BLOCK_COPPER_ORE),
            (ORE_COAL_CHANCE, ORE_COAL_MIN_DEPTH, BLOCK_COAL_ORE),
            (ORE_SILVER_CHANCE, ORE_SILVER_MIN_DEPTH, BLOCK_SILVER_ORE),
            (ORE_PLATINUM_CHANCE, ORE_PLATINUM_MIN_DEPTH, BLOCK_PLATINUM_ORE),
            (ORE_MITHRIL_CHANCE, ORE_MITHRIL_MIN_DEPTH, BLOCK_MITHRIL_ORE),
            (ORE_ADAMANTITE_CHANCE, ORE_ADAMANTITE_MIN_DEPTH, BLOCK_ADAMANTITE_ORE),
            (ORE_TITAN_CHANCE, ORE_TITAN_MIN_DEPTH, BLOCK_TITAN_ORE),
            (ORE_COBALT_CHANCE, ORE_COBALT_MIN_DEPTH, BLOCK_COBALT_ORE),
            (ORE_NETHERITE_CHANCE, ORE_NETHERITE_MIN_DEPTH, BLOCK_NETHERITE_ORE),
            (ORE_CRYSTAL_CHANCE, ORE_CRYSTAL_MIN_DEPTH, BLOCK_CRYSTAL_ORE),
        ]

        for chance, min_depth, block_id in ores:
            mask = stone_mask & (depths >= min_depth) & (rand < chance)
            chunk[mask] = block_id
            stone_mask = stone_mask & ~mask

        # 3. Декорации (трава/цветы) на поверхности
        for local_x in range(CHUNK_WIDTH):
            global_gx = chunk_x * CHUNK_WIDTH + local_x
            ground_h = self._get_land_height(global_gx)

            if random.random() < DECORATION_CHANCE:
                if random.random() < GRASS_CHANCE:
                    chunk[ground_h, local_x] = BLOCK_TALL_GRASS
                else:
                    chunk[ground_h, local_x] = random.choice(FLOWER_TYPES)

        # 4. Деревья
        for local_x in range(CHUNK_WIDTH):
            global_gx = chunk_x * CHUNK_WIDTH + local_x
            ground_h = self._get_land_height(global_gx)

            if random.random() < TREE_CHANCE and ground_h > 8:
                tree_h = random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT)
                # Ствол (растёт вверх от ground_h)
                for th in range(tree_h):
                    y = ground_h - th
                    if y >= 0:
                        chunk[y, local_x] = BLOCK_WOOD

                top_y = ground_h - tree_h
                # Листва
                for lx in range(-TREE_LEAF_RADIUS, TREE_LEAF_RADIUS + 1):
                    for ly in range(-TREE_LEAF_RADIUS, TREE_LEAF_RADIUS + 1):
                        if abs(lx) == TREE_LEAF_RADIUS and abs(ly) == TREE_LEAF_RADIUS:
                            continue
                        tx = local_x + lx
                        ty = top_y + ly
                        if 0 <= tx < CHUNK_WIDTH and 0 <= ty < WORLD_HEIGHT:
                            if chunk[ty, tx] == BLOCK_AIR:
                                chunk[ty, tx] = BLOCK_LEAVES

        return chunk   # np.ndarray (H, W)

    # ---------- ДОСТУП К БЛОКАМ ----------
    def request_chunk(self, chunk_x):
        with self.lock:
            if not self.running:
                return
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
            if self.running and chunk_x not in self.chunk_data:
                self.chunk_data[chunk_x] = data
                self.dirty_chunks.add(chunk_x)
                self.requested.discard(chunk_x)

    def get_block(self, global_gx, gy):
        if gy < 0 or gy >= WORLD_HEIGHT:
            return BLOCK_AIR
        chunk_x = global_gx // CHUNK_WIDTH
        self.ensure_chunk(chunk_x)
        with self.lock:
            data = self.chunk_data.get(chunk_x)
            if data is None:
                return BLOCK_AIR
            return int(data[gy, global_gx % CHUNK_WIDTH])

    def set_block(self, global_gx, gy, block_type):
        if 0 <= gy < WORLD_HEIGHT:
            chunk_x = global_gx // CHUNK_WIDTH
            self.ensure_chunk(chunk_x)
            with self.lock:
                data = self.chunk_data.get(chunk_x)
                if data is not None:
                    data[gy, global_gx % CHUNK_WIDTH] = block_type
                    self.dirty_chunks.add(chunk_x)

    # ---------- ОТРИСОВКА ЧАНКА ----------
    def get_chunk_surface(self, chunk_x):
        with self.lock:
            if not self.running:
                return None
            if chunk_x in self.chunk_surfaces and chunk_x not in self.dirty_chunks:
                return self.chunk_surfaces[chunk_x]
        with self.lock:
            data = self.chunk_data.get(chunk_x)
        if data is None:
            return None
        surf = self._render_chunk_data(chunk_x, data)
        with self.lock:
            if self.running:
                self.chunk_surfaces[chunk_x] = surf
                self.dirty_chunks.discard(chunk_x)
        return surf

    def _render_chunk_data(self, chunk_x, data):
        surf = pygame.Surface(
            (CHUNK_WIDTH * BLOCK_SIZE, WORLD_HEIGHT * BLOCK_SIZE), pygame.SRCALPHA
        )
        surf.fill((0, 0, 0, 0))
        for gy in range(WORLD_HEIGHT):
            for gx in range(CHUNK_WIDTH):
                b = int(data[gy, gx])
                if b != BLOCK_AIR:
                    rect = (gx * BLOCK_SIZE, gy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surf, BLOCK_COLORS.get(b, (85, 85, 85)), rect)
                    if b not in NON_SOLID_BLOCKS:
                        pygame.draw.rect(surf, (20, 20, 20), rect, 1)
        return surf

    # ---------- ЗАГРУЗКА / ОЧИСТКА ----------
    def clear(self):
        self.stop()
        with self.lock:
            self.chunk_data.clear()
            self.chunk_surfaces.clear()
            self.dirty_chunks.clear()
            self.land_height_cache.clear()
            self.requested.clear()
        self.task_queue = queue.Queue()
        self.running = True
        self.worker = threading.Thread(target=self._worker_loop, daemon=False)
        self.worker.start()

    def load_data(self, chunks_data):
        self.stop()
        with self.lock:
            self.chunk_data.clear()
            self.chunk_surfaces.clear()
            self.dirty_chunks.clear()
            self.land_height_cache.clear()
            self.requested.clear()

            for chunk_key, raw_data in chunks_data.items():
                chunk_x = int(chunk_key)
                arr = np.array(raw_data, dtype=np.int16)
                # Если сохранённый чанк имеет форму (CHUNK_WIDTH, WORLD_HEIGHT) -> транспонируем
                if arr.shape == (CHUNK_WIDTH, WORLD_HEIGHT):
                    arr = arr.T
                elif arr.shape != (WORLD_HEIGHT, CHUNK_WIDTH):
                    if arr.size == WORLD_HEIGHT * CHUNK_WIDTH:
                        arr = arr.reshape((WORLD_HEIGHT, CHUNK_WIDTH))
                    else:
                        continue
                self.chunk_data[chunk_x] = arr
                self.dirty_chunks.add(chunk_x)

        self.task_queue = queue.Queue()
        self.running = True
        self.worker = threading.Thread(target=self._worker_loop, daemon=False)
        self.worker.start()