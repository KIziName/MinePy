import pygame
import time
import sys
from game import Game

def main():
    game = Game()

    try:
        while game.running:
            dt = game.clock.tick(game.target_fps) / 1000.0
            if dt > 0.05:
                dt = 0.05

            # 1. Обработка событий (ввод, мышь, выход)
            game.handle_events()

            # 2. Обновление игровой логики (физика, мобы, погода)
            if game.game_state == "game":
                game.update_physics(dt)

            # 3. Отрисовка в зависимости от состояния
            if game.game_state == "menu":
                game.draw_menu()
            elif game.game_state == "game":
                game.render()

            # 4. Переключение буферов
            pygame.display.flip()

            # Счётчик FPS (не влияет на логику)
            game.fps_counter += 1
            now = time.time()
            if now - game.last_fps_time >= 1.0:
                game.current_fps = game.fps_counter
                game.fps_counter = 0
                game.last_fps_time = now

    except Exception as e:
        print("Критическая ошибка в главном цикле:", e)
        import traceback
        traceback.print_exc()
    finally:
        game.world.stop()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()