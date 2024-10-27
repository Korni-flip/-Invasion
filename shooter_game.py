#баги
#1 если не стрилять то если пройдёт больше 3 пришельцов поражение ни защетаеться
#2 полсе поражения от счёта то показоно будет Пропущено: 2 а не 3
#подключение библиотек
from pygame import *
mixer.init()
font.init()
from random import randint
from time  import time as timer
lost = 0
score = 0
metiar = 0
potrons = 5
false = True
#
finish = False
#класы
#ласс родитель для игроков
class Game_sprite(sprite.Sprite):
#основы
    def __init__(self,image2,x,y,sprint,razmer_x,razmer_y):
        super().__init__()
        self.image = transform.scale(image.load(image2),(razmer_x, razmer_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprint = sprint
    def show(self):
        windows.blit(self.image,(self.rect.x,self.rect.y))
#для игрока
class Player(Game_sprite):
#передвежение для игрока
    def tuda_sida(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.sprint
        if keys_pressed[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.sprint
    def fire(self):
        pul_1 = Bullet('bullet.png',self.rect.centerx,self.rect.top,7,5,10)
#добавление в групу
        puli.add(pul_1)
class UFO(Game_sprite):
#вараг
    def update(self):
        global lost
        self.rect.y += self.sprint
        if self.rect.y > 550:
            self.rect.x = randint(0,500)
            self.rect.y = -30
            lost += 1
class Bullet(Game_sprite):
#выстрел
    def update(self):
        self.rect.y -= self.sprint
        if self.rect.y == -20:
            self.kill()
class metiarit(Game_sprite):
    def update(self):
        global metiar
        self.rect.y += self.sprint
        if self.rect.y > 550:
            self.rect.x = randint(0,500)
            self.rect.y = -30
#стандартные размеры спрайтов
razmer_x = 65
razmer_y = 65
#FPS
clock = time.Clock()
fps = 60
#окно
windows = display.set_mode((700, 500))
display.set_caption('pygame window')
#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
excep = True
#музыка
# mixer.music.load('space.ogg')
# mixer.music.play()
fire_music = mixer.Sound('fire.ogg')
#обекты
#Игрок
player = Player('rocket.png',0,420,7,65,80)
#групы
puli = sprite.Group()
ufos = sprite.Group()
metiarits = sprite.Group()
#энело
for i in range(5):
    ufo_1 = UFO('ufo.png',randint(0,500),-250,randint(1,3),90,65)
    ufos.add(ufo_1)
#метиариты
for i in range(3):
    metiarit_1 = metiarit('asteroid.png',randint(0,500),-250,randint(1,5),90,65)
    metiarits.add(metiarit_1)
#шрифт
font2 = font.SysFont('Arial', 35)
font3 = font.SysFont('Arial', 70)
#игровой цикл
#время пошло
while excep != False:
#цикл
    for i in event.get():
        if i.type == QUIT:
            excep = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if potrons != 0 and false == True:
                    potrons -= 1
                    player.fire()
                    fire_music.play()
                if potrons == 0 and false == True:
                    time_start = timer()
                    false = False
    if false == False:
        time_stop = timer()
        total = int(time_stop-time_start)
        if total == 1:
            potrons = 5
            false = True
    if finish != True:
        windows.blit(background,(0, 0))
        sprites_list = sprite.groupcollide(ufos, puli, True, True)
        for i in sprites_list:
            ufo_1 = UFO('ufo.png',randint(0,500),-30,randint(1,4),90,65)
            ufos.add(ufo_1)
            score += 1
        if sprite.spritecollide(player, metiarits, False):
            metiar += 1
            sprite.spritecollide(player, metiarits, True)
#счёт
#счёт пропушеных
        lost_text = font2.render('Пропущено:' , True , (255, 255, 255))
        lost_text_chislo = font2.render(str(lost) , True , (255, 255, 255))
        windows.blit(lost_text , (0 , 0))
        windows.blit(lost_text_chislo , (190 , 0))
#счёт сбитых
        score_text = font2.render('Счёт:' , True , (255, 255, 255))
        score_text_chislo = font2.render(str(score) , True , (255, 255, 255))
        windows.blit(score_text , (0 , 30))
        windows.blit(score_text_chislo , (85 , 30))
#счёт поподания метиорита в корабль
        metiarit_chislo = font2.render(str(metiar) , True , (255, 0, 0))
        windows.blit(metiarit_chislo , (670 , 0))
#игрок
        player.show()
        player.tuda_sida()
#пуля
        puli.draw(windows)
        puli.update()
#энело
        ufos.draw(windows)
        ufos.update()
#метиариты
        metiarits.draw(windows)
        metiarits.update()
#выбор события
#поражени
        if sprite.spritecollide(player, ufos, False) or lost == 3 or metiar == 3:
            Game_over = font3.render('Game over' , True , (255, 0, 0))
            windows.blit(Game_over , (200 , 250))
            finish = True
#победа
        if score == 7:
            Win = font3.render('Win' , True , (0, 255, 0))
            windows.blit(Win , (200 , 250))
            finish = True
#FPS
        display.update()
        clock.tick(fps)