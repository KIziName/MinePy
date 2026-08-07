import pygame
import time
import sys
from game import Game

def main():
    game = None
    try:
        pygame.init()

        game = Game()

        while game.running:
            dt = game.clock.tick(game.target_fps) / 1000.0
            if dt > 0.05:
                dt = 0.05

            game.handle_events()

            if game.game_state == "game":
                game.update_physics(dt)

            if game.game_state == "menu":
                game.draw_menu()
            elif game.game_state == "game":
                game.render()

            pygame.display.flip()

            # Счётчик FPS 
            game.fps_counter += 1
            now = time.time()
            if now - game.last_fps_time >= 1.0:
                game.current_fps = game.fps_counter
                game.fps_counter = 0
                game.last_fps_time = now

    except KeyboardInterrupt:
        print("\nВыход по Ctrl+C")
    except Exception as e:
        print("Критическая ошибка в главном цикле:", e)
        import traceback
        traceback.print_exc()
    finally:
        if game is not None:
            if hasattr(game, 'world') and hasattr(game.world, 'stop'):
                game.world.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
