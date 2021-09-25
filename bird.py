import pygame as pg
import sys, random

pg.init()
pg.mixer.pre_init(frequency= 44100, size = 16, channels = 1, buffer = 516)
# make the sound better, so you had better set "pg.mixer.pre_init()" up. You don't need to care what's inside.
screen = pg.display.set_mode((380,600))
clock = pg.time.Clock()

# game image
red_bird1 = pg.image.load("flappy-bird-assets-master/sprites/redbird-downflap.png").convert_alpha()
red_bird2 = pg.image.load("flappy-bird-assets-master/sprites/redbird-midflap.png").convert_alpha()
red_bird3 = pg.image.load("flappy-bird-assets-master/sprites/redbird-upflap.png").convert_alpha()
bird_frame = [red_bird1,red_bird2,red_bird3]
bird_index = 0
bird_surface = bird_frame[bird_index]
bird_rect = bird_surface.get_rect(center = (60,250))
BIRDANIMATE = pg.USEREVENT +1
pg.time.set_timer(BIRDANIMATE, 200)
# pg.USEREVENT +1 因為不想與pg.USEREVENT搞混所以 + 1

bg = pg.image.load("flappy-bird-assets-master/sprites/background-day.png").convert()
bg = pg.transform.scale(bg, (380,600))

base =pg.image.load("flappy-bird-assets-master/sprites/base.png").convert()
base2 =pg.image.load("flappy-bird-assets-master/sprites/base.png").convert()
base = pg.transform.scale(base, (380,100))
base2 = pg.transform.scale(base2, (380,100))

pipe_surface = pg.image.load("flappy-bird-assets-master\sprites\pipe-red.png").convert()
pipe_surface = pg.transform.scale(pipe_surface,(65,380))
pipe_list = [] # each pipe position
SPAWNPIPE = pg.USEREVENT 
pg.time.set_timer(SPAWNPIPE, 1500)
# pg.time.set_timer()的毫秒決定pipe之間的距離。

message = pg.image.load("flappy-bird-assets-master/sprites/message.png").convert_alpha()
message_rect = message.get_rect(center = (190, 300))

# font and score
score = 0 
record_score = 0
font = pg.font.Font("04B_19.TTF", 40)

# render_font_score= font.render("Score" + render_font,True,(255,255,255))
# font_score_rect = render_font_score.get_rect(center=(190,50))

# base move
pos = 0
def base_move():
    global pos        
    screen.blit(base,(pos,520))
    screen.blit(base2,(pos + 380,520))
    pos -= 2
    if pos == -380:
        pos = 0

# create pipe 
def create_pipe():
    midtop_y = random.choice(pipe_top)
    pipe_rect_bottom = pipe_surface.get_rect(midtop=(400,midtop_y))
    pipe_rect_top = pipe_surface.get_rect(midbottom=(400,midtop_y -180))
    return [pipe_rect_bottom, pipe_rect_top]
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
        if pipe.centerx < -100:
            pipes.remove(pipe)
    return pipes
# !!!important: return 新的list  
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600: 
            screen.blit(pipe_surface, pipe)
        else: 
            flip_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            
# 兩個有rect的物體，才能測試是否有碰撞
def check_collide(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.y > 650 or bird_rect.y < -50:
        drop_sound.play()
        return False

    return True
        
def rotate(bird_surface):
    # bird_movement 從哪裡get到的??? 為何可從while中get到 bird_movement 卻不用寫在rotate()中???
    bird_surface = pg.transform.rotozoom(bird_surface, -bird_movement*5, 1)
    return bird_surface

#遊戲中的score 
def game_score(font):
    render_font= font.render(str(int(score)),True,(255,255,255))

    font_rect = render_font.get_rect(center=(190,70))
    return render_font, font_rect
#遊戲開始畫面的score 
def get_score(font):
    Score_font = font.render("Score " + str(int(score)), True, (255,255,255))
    Score_font_rect = Score_font.get_rect(center= (190,70))
    return Score_font,Score_font_rect
def score_record(font):
    Record_font = font.render("Record "+ str(int(record_score)), True, (255,255,255))
    Record_font_rect = Record_font.get_rect(center= (190,520))
    return Record_font,Record_font_rect
def compare_score(score,record_score):
    if score >= record_score:
        record_score = score
    return record_score

# BGM
flap_sound = pg.mixer.Sound("flappy-bird-assets-master/audio/wing.wav")
death_sound = pg.mixer.Sound("flappy-bird-assets-master/audio/hit.wav")
score_sound = pg.mixer.Sound("flappy-bird-assets-master/audio/point.wav")
drop_sound = pg.mixer.Sound("flappy-bird-assets-master/audio/die.wav")
# game variable
gravity = 0.15
bird_movement = 0
pipe_top = [300, 380, 450, 250]
play_game = False
score_sound_coundown = 100

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        #必須先寫 event.type 再寫 event.key 字母a就是K_a、K_SPACE...
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # !!! important: 跳起來時也遵守等加速度運動，bird_movement等於0時 v=0 在最高點，然後往下墜
                bird_movement = 0
                bird_movement -= 5
                if play_game == True:
                    flap_sound.play()
        #每1.2秒就創建一個pipe 
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == pg.MOUSEBUTTONDOWN:
            play_game = True
            # !!!important 重新開始，所有pipe_list要歸零，bird回到原位,bird_movement = 0
            pipe_list.clear()
            bird_rect.center = (60,250)
            bird_movement = 0
            score = 0
        if event.type == BIRDANIMATE:
            bird_index +=1
            if bird_index >= len(bird_frame):
                bird_index = 0
            bird_surface = bird_frame[bird_index]

    if play_game == True:
        screen.blit(bg, (0,0))
        # !!!important:  pipe_list = move_pipe(pipe_list) 新的list覆蓋舊的list
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        base_move()
        # player()
        # 重力加速度，為"等加速度"，因此寫兩層程式 bird_movement += gravity ,bird_rect.centery += bird_movement; 
        # "跳起來"時也呈現"等加速度"，到最高點要掉下前的bird_movement == 0，如同再有重力的地點往上跳，起跳快，停在半空中後，往下掉。
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # rotate bird 
        # ???為何rotate()中一定要放red_bird1，不能到了def rotate: global red_bird
        rotated_red_bird1 = rotate(bird_surface)
        screen.blit(rotated_red_bird1,bird_rect)

        # score
        render_font, font_rect = game_score(font)
        screen.blit(render_font, font_rect)
        # when variable "score" get the "full number", play "score_sound"
        # 因為score要加100次才會等於1(整數)，所以設定score_sound_coundown = 100, 當它為0時 score_sound.play()
        score += 0.01
        score_sound_coundown -= 1
        if score_sound_coundown <= 0:
            score_sound.play()
            score_sound_coundown = 100

        # record_score唯有等到比第一局分數高的score，record_score 才會改變。
        record_score = compare_score(score, record_score)

        # colliderect
        play_game = check_collide(pipe_list)
    else:
        screen.blit(bg, (0,0))
        screen.blit(message, message_rect)

        Score_font, Score_font_rect = get_score(font)
        screen.blit(Score_font, Score_font_rect)
        Record_font,Record_font_rect = score_record(font)
        screen.blit(Record_font,Record_font_rect)
        

    pg.display.flip()
    clock.tick(120)



# centerx/ centery
# flappy bird 是因為重力加速度而掉下去，

 
# pygame.transform.flip(Surface, xbool左右, ybool 上下) )
# (flip vertically and horizontally) 左右或上下翻轉

# event.type == KEYDOWN or KEYUP 之後 
# event.key == K_a(字母)、K_SPACE...
# event.unicode 有意義的英文字 

# 每幾豪秒就觸發pg.USEREVENT
# something = pg.USEREVENT 
# pg.time.set_timer(something, 1200)
# if event.type == something:

# append vs. extend
# x = [1, 2, 3]
# x.append([4, 5]) >>> [1, 2, 3, [4, 5]]
# x.extend([4, 5]) >>> [1, 2, 3, 4, 5]  "extend" concatenate the first list with another list


# List 和 for loop ，新的list 覆蓋舊的list
# Players = []
# while True:
#   Players.append(50)
#   Players = minus(Players)
# 
# def minus(Players):
#   global Players
#   for player in Players:
#       player -= 5 
#       return Players (新的list)
# print out >>>
# 1. [50]
# 2. [45,50]
# 3. [40,45,50]...


# !!!important
# while loop 中有定義的"變數"，在while中呼叫function時，def 中有這個變數出現，則會取while中的這個變數，而非while外的

# int() 能讓原本float的值，"將小數捨去"
