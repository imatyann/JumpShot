import pygame
import math
import random

import game.settings as settings
import game.camera as camera
import game.player as player
import game.rect as rect
import game.board as board
import game.goal as goal
import game.reticle as reticle
import game.bullet as bullet
import game.exchange as exchange
import game.teresa as teresa
import game.key as key


def start():
    """起動時に実行される関数"""
    
    #pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.GAME_TITLE)
    clock = pygame.time.Clock()

    # 初期化関数実行
    main_camera, main_player, main_rects, main_board, main_goal, main_reticle, bullets, exchange_bullet, teresas, last_summon_time, interval, main_key  = reset_all()


    # 毎秒実行する関数
    running = True
    while running:
        now = pygame.time.get_ticks()

        # マウスの位置を確保
        player_center_scroll_x = main_player.scroll_x + main_player.width / 2
        player_center_scroll_y = main_player.scroll_y + main_player.height / 2
        
        mouse_scroll_x, mouse_scroll_y = main_camera.screen_to_scroll(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) 
        vx, vy = mouse_scroll_x - player_center_scroll_x, mouse_scroll_y - player_center_scroll_y
        length = math.hypot(vx, vy)
        dx, dy = (vx/length, vy/length) if length != 0 else (0, 0)

        # 盤面の描画
        screen.fill(settings.BG_COLOR)

        # =========================操作受け付け=====================================
        for event in pygame.event.get():
            # ウィンドウの終了
            if event.type == pygame.QUIT:
                running = False
            # 左クリックで弾を発射
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets.append(new_bullet(player_center_scroll_x, player_center_scroll_y, dx, dy))
                elif event.button == 3:
                    if exchange_bullet.is_in_screen == False:
                        exchange_bullet.summon(player_center_scroll_x,player_center_scroll_y, dx, dy)
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not esc_was_down:
                # ここだけ1回実行される
                if main_board.status == "play":
                    main_board.status = "pause"
                elif main_board.status == "pause":
                    main_board.status = "play"
                esc_was_down = True
        else:
            esc_was_down = False


        # 左右に主人公とカメラを移動
        speed = settings.CAMERA_SPEED
        if main_board.status == "play":    
            if keys[pygame.K_d]:
                if main_player.touch_right == False:
                    main_camera.move_x(speed)
                    main_player.move_x(speed)

            elif keys[pygame.K_a]:
                if main_player.touch_left == False:
                    main_camera.move_x(-speed)
                    main_player.move_x(-speed)
                    

            # ジャンプ
            if keys[pygame.K_SPACE]:
                if main_player.on_ground:
                    main_player.jump(10)
                    main_player.on_ground = False

            if keys[pygame.K_0]:
                print(main_player.scroll_x, main_player.scroll_y)
                
            
                


        # Rキーでリセット
        if keys[pygame.K_r]:
            main_camera, main_player, main_rects, main_board, main_goal, main_reticle, bullets, exchange_bullet, teresas, last_summon_time, interval, main_key = reset_all()

        # ============================描画関数============================

        # 壁の描画
        for rect in main_rects:
            rect_screen_x, rect_screen_y = main_camera.scroll_to_screen(rect.scroll_x, rect.scroll_y)
            rect.draw(screen, rect_screen_x, rect_screen_y) 

        # ゴールの描画
        goal_screen_x, goal_screen_y = main_camera.scroll_to_screen(main_goal.scroll_x, main_goal.scroll_y)
        main_goal.draw(screen, goal_screen_x, goal_screen_y)

        # 鍵の描画
        if main_key.is_draw == True:
            key_screen_x, key_screen_y = main_camera.scroll_to_screen(main_key.scroll_x, main_key.scroll_y)
            main_key.draw(screen, key_screen_x, key_screen_y)
            if main_key.touch(main_player.scroll_x, main_player.scroll_y, main_player.width, main_player.height):
                main_key.is_draw = False
                main_player.have_key = True
        

        # レティクルの描画
        reticle_end_scroll_x = player_center_scroll_x + 600*dx
        reticle_end_scroll_y = player_center_scroll_y + 600*dy
        
        reticle_first_screen_x, reticle_first_screen_y = main_camera.scroll_to_screen(player_center_scroll_x, player_center_scroll_y)
        reticle_end_screen_x, reticle_end_screen_y = main_camera.scroll_to_screen(reticle_end_scroll_x, reticle_end_scroll_y)

        main_reticle.draw(screen, reticle_first_screen_x, reticle_first_screen_y, reticle_end_screen_x, reticle_end_screen_y)
        
        # ========================テレサ===========================
        # 召喚関数
        if main_board.status == "play":
            if now >= last_summon_time + interval:
                last_summon_time = now
                interval = random.random() * settings.TERESA_MAX_SUMMON_TIME
                teresas.append(new_teresa(main_camera.scroll_x))


        # 敵を進ませて描画する
        # テレサ
        teresas_before = teresas[:]

        for main_teresa in teresas:
            main_teresa_screen_x, main_teresa_screen_y = main_camera.scroll_to_screen(main_teresa.scroll_x, main_teresa.scroll_y)
            if main_player.have_key:
                main_teresa.color = settings.TERESA_HIGH_COLOR
                main_teresa_speed = settings.TERESA_HIGH_SPEED
            else:
                main_teresa.color = settings.TERESA_COLOR
                main_teresa_speed = settings.TERESA_SPEED

            main_teresa.draw(screen,main_teresa_screen_x,main_teresa_screen_y)
            teresa_vx, teresa_vy = player_center_scroll_x - main_teresa.scroll_x, player_center_scroll_y - main_teresa.scroll_y
            teresa_length = math.hypot(teresa_vx, teresa_vy)    

            main_teresa.direction_x, main_teresa.direction_y =  (teresa_vx/teresa_length, teresa_vy/teresa_length) if teresa_length != 0 else (0, 0)
            if main_board.status == "play":
                main_teresa.move_front(main_teresa_speed)

            teresas_before = teresas[:]

        #============================弾=========================

        # 弾を進ませて描画する
        for main_bullet in bullets:
            main_bullet_screen_x, main_bullet_screen_y = main_camera.scroll_to_screen(main_bullet.scroll_x, main_bullet.scroll_y)

            main_bullet.draw(screen,main_bullet_screen_x,main_bullet_screen_y)
            main_bullet.move_front(settings.BULLET_SPEED)

        # 敵と弾の衝突判定
        teresas = [
            t for t in teresas
            if all(not t.attacking(b.scroll_x, b.scroll_y, b.radius) for b in bullets)
        ]

        bullets = [
            b for b in bullets
            if all(not t.attacking(b.scroll_x, b.scroll_y, b.radius) for t in teresas_before)
            and all(not rect.include(b.scroll_x, b.scroll_y) for rect in main_rects)
            and -100 <= b.scroll_x <= main_camera.screen_to_scroll(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)[0] + 100
            and -100 <= b.scroll_y <= main_camera.screen_to_scroll(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)[1]
        ]


        # 特殊弾を進ませて描画する
        exchange_screen_x, exchange_screen_y = main_camera.scroll_to_screen(exchange_bullet.scroll_x, exchange_bullet.scroll_y)
        if exchange_bullet.is_in_screen == True:
            exchange_bullet.draw(screen,exchange_screen_x,exchange_screen_y)
            exchange_bullet.move_front(settings.EXCHANGE_SPEED)
            
            exchange_attacking = False
            for main_teresa in teresas:
                if main_teresa.attacking(exchange_bullet.scroll_x, exchange_bullet.scroll_y, exchange_bullet.radius):
                    exchange_attacking = True
                    teresas.remove(main_teresa)
                    break

            if not (all(not rect.include(exchange_bullet.scroll_x, exchange_bullet.scroll_y) for rect in main_rects) and not exchange_attacking):
                # 弾方向に応じて召喚場所を決める
                if exchange_bullet.direction_x  > 0:
                    summon_player_x = exchange_bullet.scroll_x - main_player.width
                    summon_camera_x = exchange_bullet.scroll_x - settings.SCREEN_WIDTH/2
                else:
                    summon_player_x = exchange_bullet.scroll_x
                    summon_camera_x = exchange_bullet.scroll_x - settings.SCREEN_WIDTH/2
                if exchange_bullet.direction_y > 0:
                    summon_player_y = exchange_bullet.scroll_y - main_player.height
                    summon_camera_y = main_camera.scroll_y
                else:
                    summon_player_y = exchange_bullet.scroll_y
                    summon_camera_y = main_camera.scroll_y
                
                main_player.summon(summon_player_x, summon_player_y)
                main_camera.summon(summon_camera_x , summon_camera_y)
                exchange_bullet.is_in_screen = False



            if not ((-100 <= exchange_bullet.scroll_x <= main_camera.screen_to_scroll(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)[0] + 100)
            and (-100 <= exchange_bullet.scroll_y <= main_camera.screen_to_scroll(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)[1])):
                exchange_bullet.is_in_screen = False

        # ===========================主人公========================
        # 主人公描画
        player_screen_x, player_screen_y = main_camera.scroll_to_screen(main_player.scroll_x, main_player.scroll_y)
        main_player.draw(screen, player_screen_x, player_screen_y)

        #主人公落下
        if main_board.status == "play":
            if main_player.on_ground:
                main_player.fall_speed = 0
            else:
                main_player.move_y(main_player.fall_speed) 
                main_player.fall()

        # 主人公判定更新
        main_player_right = main_player.scroll_x + main_player.width
        main_player_left = main_player.scroll_x
        main_player_upper = main_player.scroll_y
        main_player_bottom = main_player.scroll_y + main_player.height
        
        # 右接触判定 
        main_player.touch_right = False
        for rect in main_rects:
            if ((main_player_right >= rect.scroll_x) and (main_player_right <= rect.scroll_x + 6)) and ((main_player_bottom >= rect.scroll_y) and (main_player_upper <= rect.scroll_y + rect.height)):
                main_player.touch_right = True
                break

        # 左接触判定
        main_player.touch_left = False
        for rect in main_rects:
            if ((main_player_left <= rect.scroll_x + rect.width) and (main_player_left >= rect.scroll_x + rect.width - 6)) and ((main_player_bottom >= rect.scroll_y) and (main_player_upper <= rect.scroll_y + rect.height)):
                main_player.touch_left = True
                break

        # 下接触判定
        main_player.touch_foot = False
        for rect in main_rects:
            if ((main_player_bottom >= rect.scroll_y) and (main_player_bottom <= rect.scroll_y + 20)) and ((main_player_right >= rect.scroll_x) and (main_player_left <= rect.scroll_x + rect.width)):
                main_player.touch_foot = True
                break

        # 上接触判定
        main_player.touch_head= False
        for rect in main_rects:
            if ((main_player_upper <= rect.scroll_y + rect.height) and (main_player_upper >= rect.scroll_y + rect.height - 6)) and ((main_player_right >= rect.scroll_x) and (main_player_left <= rect.scroll_x + rect.width)):
                main_player.touch_head = True
                break
    
        if main_player.touch_foot:
            main_player.on_ground = True
        else:
            main_player.on_ground = False

        if main_player.touch_head:
            main_player.fall_speed = 1

        # 死亡判定
        # 落下判定
        if main_player.scroll_y >= settings.DEADLINE:
            main_board.status = "gameover"
        
        for teresa in teresas:
            if teresa.attacking_rect(main_player.scroll_x, main_player.scroll_y, main_player.width, main_player.height):
                main_board.status = "gameover"
                break



        # ゴール判定
        if main_player.conflict_rect(main_goal.scroll_x, main_goal.scroll_y, main_goal.width, main_goal.height) and main_player.have_key == True:
            main_board.status = "goal"
            

        if main_board.status == "gameover":
            gameover(screen)

        if main_board.status == "goal":
            goal_function(screen)
        


        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    pygame.quit()

def reset_all():
    """全てリセットし初期設定に戻す関数"""
    main_camera = camera.Camera(
        settings.CAMERA_FIRST_X,
        settings.CAMERA_FIRST_Y
    )

    main_player = player.Player(
        settings.PLAYER_FIRST_X,
        settings.PLAYER_FIRST_Y,
        True,
        0,
        False,
        False,
        False,
        False,
        settings.PLAYER_WIDTH,
        settings.PLAYER_HEIGHT,
        False
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
    
    main_board = board.Board(
        "play"
    )

    main_goal = goal.Goal(
        settings.GOAL_FIRST_X,
        settings.GOAL_FIRST_Y,
        settings.GOAL_WIDTH,
        settings.GOAL_HEIGHT,
        settings.GOAL_COLOR,
        settings.GOAL_BG_COLOR
    )

    main_reticle = reticle.Reticle(
        settings.RETICLE_WIDTH,
        settings.RETICLE_COLOR
    )

    bullets = []

    exchange_bullet = exchange.Exchange(
        settings.EXCHANGE_COLOR,
        settings.EXCHANGE_RADIUS,
        0,
        0,
        0,
        0,
        False
    )

    teresas = []

    last_summon_time = 0
    interval = random.random() * settings.TERESA_MAX_SUMMON_TIME

    main_key = key.Key(
        settings.KEY_FIRST_X,
        settings.KEY_FIRST_Y,
        True,
        settings.KEY_COLOR,
        settings.KEY_WIDTH,
        settings.KEY_HEIGHT
    )
    
    return main_camera, main_player, main_rects, main_board, main_goal, main_reticle, bullets, exchange_bullet, teresas, last_summon_time, interval, main_key

def new_bullet(scroll_x, scroll_y, direction_x, direction_y):
    main_bullet = bullet.Bullet(
        settings.BULLET_COLOR,
        settings.BULLET_RADIUS,
        scroll_x,
        scroll_y,
        direction_x,
        direction_y
    )
    return main_bullet

def new_teresa(camera_x):
    main_teresa = teresa.Teresa(
            camera_x + settings.SCREEN_WIDTH,
            settings.SCREEN_HEIGHT * random.random(),
            settings.TERESA_RADIUS,
            settings.TERESA_COLOR,
            0,
            0
    )
    return main_teresa


def gameover(screen):
    font = pygame.font.Font(None, 96)
    surf = font.render("GAMEOVER", True, (255,0,0))
    rect = surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(surf, rect)

def goal_function(screen):
    font = pygame.font.Font(None, 96)
    surf = font.render("GOAL!!", True, (255,0,0))
    rect = surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(surf, rect)


if __name__ == "__main__":
    start()

