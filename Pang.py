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
weapon_height = weapon_size[1]
weapon_x_pos = character_x_pos
weapon_y_pos = screen_height - stage_height

balloon1 = pygame.image.load("D:/study_2107/pygames/pygame_basic/balloon1.png")
balloon1_size = balloon1.get_rect().size
balloon1_width = balloon1_size[0]
balloon1_height = balloon1_size[1]
# balloon1_x_pos = random.randint()

char_x =0
character_speed = 0.1

go_weap=0
weap_y =0
weap_speed = 5
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
            if event.key == pygame.K_RIGHT:
                char_x += character_speed 
            if event.key == pygame.K_SPACE:
                    weap_y -= weap_speed
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_x =0
            if event.key == pygame.K_SPACE:
                go_weap = character_x_pos
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += char_x *dt

    weapon_y_pos += weap_y * dt

    # 4. 충돌 처리
    if character_x_pos <0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if weapon_y_pos < -480:
        weapon_y_pos = screen_height - stage_height
        weap_y = 0

    # 5. 화면에 그리기
    screen.blit(background, (0,0))
    screen.blit(weapon, (go_weap, weapon_y_pos))
    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update() # 게임화면 다시 그리기


pygame.time.delay(1000)
# pygame 종료
pygame.quit()
