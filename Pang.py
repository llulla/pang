import pygame
import random
#####################################################################
# 기본 초기화 (반드시 해줘야함)
pygame.init() #초기화 반드시 해줘야함

#화면 크기 설정
screen_width = 640  #가로크기
screen_height = 480 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Pang")

#fps
clock = pygame.time.Clock()
#####################################################################

#1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

weapon_to_remove = -1
ball_to_remove = -1

#배경화면
background = pygame.image.load("D:/study_2107/pygames/pygame_basic/background_pang.png")

stage = pygame.image.load("D:/study_2107/pygames/pygame_basic/stage.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load("D:/study_2107/pygames/pygame_basic/pang_char.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width /2) - (character_width/2)
character_y_pos = screen_height - stage_height - character_height

weapon = pygame.image.load("D:/study_2107/pygames/pygame_basic/weapon.png")
weapon_size = weapon.get_rect().size
weapon_widtn = weapon_size[0]

weapons = []
weapon_speed = 10

ball_images=[
    pygame.image.load("D:/study_2107/pygames/pygame_basic/balloon1.png"),
    pygame.image.load("D:/study_2107/pygames/pygame_basic/balloon2.png"),
    pygame.image.load("D:/study_2107/pygames/pygame_basic/balloon3.png"),
    pygame.image.load("D:/study_2107/pygames/pygame_basic/balloon4.png")]

ball_speed_y= [-18, -15, -12, -9]

balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x": 3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
    "to_y": -6, # y축 이동방향,
    "init_spd_y": ball_speed_y[0]})# y 최초 속도


char_x =0
character_speed = 0.1

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) #게임화면 초당 프레임 수
    print("fps : "+str(clock.get_fps()))

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                char_x += character_speed 
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos +(character_width/2) - (weapon_widtn/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_x =0
            # if event.key == pygame.K_SPACE:

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += char_x *dt

    if character_x_pos <0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [ [w[0], w[1]] for w in weapons if w[1] >-480]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
           ball_val["to_x"] = ball_val["to_x"] * -1



        if ball_pos_y >= screen_height-stage_height -ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5
  
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    
    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": -3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": 3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# y 최초 속도

                break


    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update()

pygame.time.delay(1000)
# pygame 종료
pygame.quit()
