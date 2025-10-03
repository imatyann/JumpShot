import pygame

import game.settings as settings
import game.camera as camera
import game.player as player


def start():
    """起動時に実行される関数"""
    
    #pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.GAME_TITLE)
    clock = pygame.time.Clock()

    # 初期化関数実行
    main_camera = camera.Camera(
        0,
        0
    )

    main_player = player.Player(
        100,
        100
    )

    # 毎秒実行する関数
    running = True
    while running:
        now = pygame.time.get_ticks()

        # 盤面の描画
        screen.fill(settings.BG_COLOR)

        # 操作受け付け
        for event in pygame.event.get():
            # ウィンドウの終了
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()

        if keys[pygame.key.K_d]:
            pass
        elif keys[pygame.key.k_a]:
            pass



        # 描画関数
        # 主人公描画
        player_screen_x, player_screen_y = main_camera.scroll_to_screen(main_player.scroll_x, main_player.scroll_y)
        main_player.draw(screen, player_screen_x, player_screen_y)

        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    pygame.quit()







if __name__ == "__main__":
    start()

