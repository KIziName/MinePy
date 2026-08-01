import pygame
import math
import random

from blocks import * 


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
        speed = PLAYER_SPEED

        if keys.get(pygame.K_a) or keys.get(pygame.K_LEFT):
            self.vx = -speed
            self.facing_right = False
        if keys.get(pygame.K_d) or keys.get(pygame.K_RIGHT):
            self.vx = speed
            self.facing_right = True

        if (keys.get(pygame.K_w) or keys.get(pygame.K_SPACE) or keys.get(pygame.K_UP)) and self.is_grounded:
            self.vy = JUMP_FORCE
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

        # Защита от падения в пустоту
        if self.y > (WORLD_HEIGHT + 10) * BLOCK_SIZE:
            self.spawn()

    def _check_collision(self):
        left = int((self.x - self.w / 2) // BLOCK_SIZE)
        right = int((self.x + self.w / 2) // BLOCK_SIZE)
        top = int((self.y - self.h / 2) // BLOCK_SIZE)
        bottom = int((self.y + self.h / 2) // BLOCK_SIZE)

        for gx in range(left, right + 1):
            for gy in range(top, bottom + 1):
                b = self.world.get_block(gx, gy)
                if b != BLOCK_AIR and b not in NON_SOLID_BLOCKS:
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
        return WEAPON_DAMAGE.get(itype, 6)