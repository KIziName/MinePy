import json
import os
import traceback
from blocks import SAVE_FILE_PATH, APPDATA_PATH

class SaveManager:
    def __init__(self, game):
        self.game = game

    def save(self):
        try:
            world = self.game.world
            player = self.game.player
            inventory = self.game.inventory
            mob_manager = self.game.mob_manager

            mobs_data, items_data = mob_manager.to_dict()

            with world.lock:
                chunks_data = {str(k): v.tolist() for k, v in world.chunk_data.items()}

            save_data = {
                'player_x': player.x,
                'player_y': player.y,
                'hp': player.hp,
                'max_hp': player.max_hp,
                'day_time': self.game.day_time,
                'day_counter': self.game.day_counter,
                'inventory': inventory.to_dict(),
                'selected_slot': inventory.selected_slot,
                'chunks': chunks_data,
                'mobs': mobs_data,
                'dropped_items': items_data
            }

            if not os.path.exists(APPDATA_PATH):
                os.makedirs(APPDATA_PATH)

            with open(SAVE_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=None, separators=(',', ':'))

            self.game.save_notification_timer = 2.0
            print("[Сохранение] Мир успешно сохранён")
        except (OSError, json.JSONEncodeError, TypeError, KeyError) as e:
            print(f"[Ошибка сохранения] {e}")
            traceback.print_exc()

    def load(self):
        if not os.path.exists(SAVE_FILE_PATH):
            return False
        try:
            with open(SAVE_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            player = self.game.player
            player.x = data.get('player_x', 0)
            player.y = data.get('player_y', 200)
            player.hp = data.get('hp', player.max_hp)
            player.max_hp = data.get('max_hp', 100)
            self.game.day_time = data.get('day_time', 3000)
            self.game.day_counter = data.get('day_counter', 0)

            inventory = self.game.inventory
            inv_data = data.get('inventory')
            if inv_data and isinstance(inv_data, list) and len(inv_data) == 40:
                inventory.from_dict(inv_data)
            else:
                print("[Загрузка] Инвентарь повреждён, создан новый")
                from game import GameInventory
                new_inv = GameInventory()
                self.game.inventory = new_inv
                # Обновляем ссылку в рендерере, если он существует
                if hasattr(self.game, 'renderer') and self.game.renderer is not None:
                    self.game.renderer.inventory_slots = new_inv.slots[:]
                inventory = new_inv

            inventory.selected_slot = data.get('selected_slot', 0)
            inventory.notify('selected_slot_changed', slot=inventory.selected_slot)

            world = self.game.world
            chunks_data = data.get('chunks', {})
            world.load_data(chunks_data)

            mob_manager = self.game.mob_manager
            mobs_data = data.get('mobs', [])
            items_data = data.get('dropped_items', [])
            mob_manager.from_dict(mobs_data, items_data)

            self.game._build_background_surfaces()
            print("[Загрузка] Мир успешно загружен")
            return True
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"[Ошибка загрузки] {e}")
            traceback.print_exc()
            return False
        except Exception as e:
            # На всякий случай ловим всё остальное (например, ошибки в from_dict)
            print(f"[Неожиданная ошибка загрузки] {e}")
            traceback.print_exc()
            return False