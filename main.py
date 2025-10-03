import pygame

import game.settings as settings
import game.camera as camera
import game.player as player
import game.rect as rect


def start():
    """起動時に実行される関数"""
    
    #pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.GAME_TITLE)
    clock = pygame.time.Clock()

    # 初期化関数実行
    main_camera, main_player, main_rects = reset_all()

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
        speed = settings.CAMERA_SPEED
        if keys[pygame.K_d]:
            main_camera.move_x(speed)
            main_player.move_x(speed)
        elif keys[pygame.K_a]:
            main_camera.move_x(-speed)
            main_player.move_x(-speed)
        
        if keys[pygame.K_SPACE]:
            if main_player.on_ground:
                main_player.jump(10)
                main_player.on_ground = False


        # 描画関数
        # 主人公描画
        player_screen_x, player_screen_y = main_camera.scroll_to_screen(main_player.scroll_x, main_player.scroll_y)
        main_player.draw(screen, player_screen_x, player_screen_y)

        # 壁の描画
        for rect in main_rects:
            rect_screen_x, rect_screen_y = main_camera.scroll_to_screen(rect.scroll_x, rect.scroll_y)
            rect.draw(screen, rect_screen_x, rect_screen_y) 


        #主人公落下
        if main_player.on_ground:
            main_player.fall_speed = 0
        else:
            main_player.move_y(main_player.fall_speed) 
            main_player.fall()
        
        # 主人公判定更新
        if main_player.scroll_y > settings.SCREEN_HEIGHT - 150:
            main_player.on_ground = True
        else:
            main_player.on_ground = False



        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    pygame.quit()

def reset_all():
    """全てリセットし初期設定に戻す関数"""
    main_camera = camera.Camera(
        0,
        0
    )

    main_player = player.Player(
        settings.PLAYER_FIRST_X,
        settings.PLAYER_FIRST_Y,
        True,
        False,
        0
    )

    main_rects = []
    for setting in settings.RECTS:
        main_rect = rect.Rect(
            setting[0],
            setting[1],
            setting[2],
            setting[3],
            settings.RECT_COLOR
        )
        main_rects.append(main_rect)

    return main_camera, main_player, main_rects


if __name__ == "__main__":
    start()

