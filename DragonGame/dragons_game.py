
########
# Sengdao Oudomsihn
# Python Final
# 3 - 12- 2021

# Goal : collect 20 eggs from dragons in order to win the game,
# but at the same time avoid getting hit by fire balls from dragons and collect the eggs under 2 minutes
# Hero has only 5 lives. If looses all the lives then the hero loses the game.


import pygame, random,time
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Declare the constant 
WIDTH = 1400
HEIGHT = 820
background_file = 'dungeon.png'
dragon_asleep = 'dragon-asleep.png'
dragon_awake = 'dragon-awake.png'
hero_file = 'hero.png'
egg_lair1 = 'one-egg.png'
egg_lair2 = 'two-eggs.png'
egg_lair3 = 'three-eggs.png'
WALL_FILENAME  = 'wall.jpg'
fire_file = 'fireblast1.png'
sound_file = 'Dragon_Sound_ Effects.mp3'
TIME_LIMIT = 120
SCORE_COLOR = (0, 0, 0)
EGG_TARGET = 20
HERO_START = (100,400)
LIVES = 5
EGG_HIDE_TIME = 2
FPS = 24
Fire_vel = 34
Fire_prob = 0.7 / FPS
MOVE_PIXEL = 30
COOLDOWN = FPS / 2.0


# Declare the variables for score, timer, and live
score = 0
score_font = pygame.font.SysFont('Noto Serif', size = 40)
timer = 0
timer_font = pygame.font.SysFont('Noto Serif', size = 35)
live_font = pygame.font.SysFont('Noto Serif', size = 35)
winner_font = pygame.font.SysFont('Noto Serif', size = 50)

#time remaining
ms_remaining = TIME_LIMIT * 1000
sound = pygame.mixer.Sound(sound_file)

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(x, y)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x_move, y_move):
        self.rect = self.rect.move(x_move, y_move)
        if pygame.sprite.spritecollideany(self, vert_wall_grp) != None:
            self.rect = self.rect.move(-x_move, 0)
        if pygame.sprite.spritecollideany(self, horiz_wall_grp) != None:
            self.rect = self.rect.move(0, -y_move)
    

#  Create dragons.
class Dragon(pygame.sprite.Sprite):
    def __init__(self, x, y, image, number_of_eggs): 
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(x, y)
        self.eggs_count = number_of_eggs
        self.cooldown = 0
        self.eggs = pygame.sprite.Group()

        # crete eggs in the loop so dragon can keep laying unlimited eggs
        for i in range(number_of_eggs):
            self.eggs.add(Egg(x-number_of_eggs, y + number_of_eggs, egg_image1))
            self.eggs.add(Egg(x-number_of_eggs, y + number_of_eggs, egg_image2))  
    def update(self):
        if len(self.eggs) == 0:
            self.eggs.add(Egg(self.rect.x - 100, self.rect.y + 50, egg_image1))
            self.eggs.add(Egg(self.rect.x - 100, self.rect.y + 100, egg_image2))

            for e in range(self.eggs_count):
                self.eggs.add(Egg(self.rect.x-100, self.rect.y + 300, egg_image1))
                self.eggs.add(Egg(self.rect.x -100, self.rect.y + 100, egg_image2))
    
    def update(self, move_x, move_y):
        
        self.cooldown = max(0, self.cooldown - 1)
        self.move(move_x, move_y)

    def move(self, move_x, move_y):
        self.rect = self.rect.move(move_x, move_y)

    def in_bounds_left(self):
        return self.rect.left >= 0 

    def in_bounds_right(self):
        return self.rect.right <= WIDTH

    def shoot(self):
        
        if self.cooldown == 0:
            self.cooldown = COOLDOWN
            return Fire(self.rect.left, self.rect.centery, -Fire_vel, fire_image)
            # Otherwise fire from the bottom of the ship.
        else:
            return None
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.eggs.draw(surface)

class Fire(pygame.sprite.Sprite): 
    def __init__(self, x, y, vel, img):

        super(Fire, self).__init__()
        self.vel   = vel
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect  = self.rect.move(x, y)
    
    def in_bounds(self):
        # check horizontal bounds.
        return self.rect.left > 0 and self.rect.right < WIDTH

    def update(self):
        # dragons breath out fire ballhorizontally.
        self.rect = self.rect.move(self.vel, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    

# # # Create egg lairs of dragons.
class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(x, y)
    
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
       
# Walls
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (w, h))
        self.rect  = self.image.get_rect()
        self.rect  = self.rect.move(x, y)

    # Draw the wall.
    def draw(self, surface):
        surface.blit(self.image, self.rect)


clock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH, HEIGHT))
# Set window title.
pygame.display.set_caption('Dragon Game')

# imaport background
bg = pygame.image.load(background_file).convert_alpha()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# import heroes
hero1_image = pygame.image.load(hero_file).convert_alpha()
#hero2_image = pygame.image.load(hero2_file).convert_alpha()

#import dragon
asleep_dragon_image = pygame.image.load(dragon_asleep).convert_alpha()
awaken_dragon_image = pygame.image.load(dragon_awake).convert_alpha()
awaken_dragon_image2 = pygame.image.load(dragon_awake).convert_alpha()
# Scale the awaken-dragon
awaken_dragon_image = pygame.transform.scale2x(awaken_dragon_image)

# import eggs
egg_image1 = pygame.image.load(egg_lair1).convert_alpha()
egg_image2 = pygame.image.load(egg_lair3).convert_alpha()
egg_image3 = pygame.image.load(egg_lair2).convert_alpha()

fire_image = pygame.image.load(fire_file).convert_alpha()
fire_image = pygame.transform.scale(fire_image, (100, 50))

# Create player 
# I declare my heroes as Jon Snow brothers :) :)
jon_snow1 = Player(HERO_START[0], HERO_START[1], hero1_image)
#jon_snow2 = Player(HERO_START[0], HERO_START[1], hero2_image)

# Build the wall so the heroes can't escape :):) Got this chunk of code from Player_class_2020021
wall_img  = pygame.image.load(WALL_FILENAME).convert()

left_wall  = Wall(-30, 0, 30, HEIGHT, wall_img)
right_wall = Wall(WIDTH, 0, 100, HEIGHT, wall_img)
vert_wall_grp = pygame.sprite.Group(left_wall, right_wall)

top_wall    = Wall(0, -100, WIDTH, 100, wall_img)
bottom_wall = Wall(0, HEIGHT, WIDTH, 100, wall_img)
horiz_wall_grp = pygame.sprite.Group(top_wall, bottom_wall)
                        #######


# # Life count 
lives_count = pygame.image.load('life-count.png')   
# Eggs count 
score_count = pygame.image.load('egg-count.png')
# Create dragons
dragon1 = Dragon(1100, 100, asleep_dragon_image,1)
dragon2 = Dragon(800, 200, awaken_dragon_image,1)
dragon3 = Dragon(1100, 600, awaken_dragon_image2,1)

# Fire list
fire_grp = pygame.sprite.Group()
egg_grp = pygame.sprite.Group()


for l in range(LIVES):
    # Create a variable to tell if we are running the game.
    running = True

    # Game loop.
    while(running):
    
        clock.tick(FPS)

        #Draw background
        win.blit(bg,(0, 0))

        # Respond to quit signal from O/S.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Move the hero 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            jon_snow1.move(MOVE_PIXEL, 0)
        elif keys[pygame.K_LEFT]:
            jon_snow1.move(-MOVE_PIXEL, 0)
        elif keys[pygame.K_UP]:
            jon_snow1.move(0, -MOVE_PIXEL)
        elif keys[pygame.K_DOWN]:
            jon_snow1.move(0, MOVE_PIXEL)

        # remaining timer is added in the loop
        ms_remaining = ms_remaining - clock.get_time()
        running = running and ms_remaining > 0

        # live of the hero display
        lives_image = live_font.render(str(LIVES - l), True, (255, 0, 0))
        win.blit(lives_image, (80, 20))

        # Draw heroes on the screen
        jon_snow1.draw(win)

        #update dragons from the Dragon class 
        dragon1.update(0, 0)
        dragon2.update(0, 0)
        dragon3.update(0, 0)

        # Draw dragons on the screen
        dragon1.draw(win)
        dragon2.draw(win)
        dragon3.draw(win)

        # Dragons breath out fires with sound effect
        if random.random() < Fire_prob:
            new_fire = dragon1.shoot()
            if new_fire != None:
                fire_grp.add(new_fire)
                sound.play()
        if random.random() < Fire_prob:
            new_fire = dragon2.shoot()
            if new_fire != None:
                fire_grp.add(new_fire)
                sound.play()
        if random.random() < Fire_prob:
            new_fire = dragon3.shoot()
            if new_fire != None:
                fire_grp.add(new_fire)
                sound.play()

        # draw and update fire from the class
        fire_grp.update()
        fire_grp.draw(win)
    
        # hero and fire collision
        hero_hits = pygame.sprite.spritecollide(jon_snow1, fire_grp, True)
        if len(hero_hits) > 0:
            running = False

        # collect the assigned number of eggs in order to win the game
        if score >= EGG_TARGET:
            running = False
            winer_img = winner_font.render('YOU WON', True, (255, 0, 0))
            win.blit(winer_img, (WIDTH, HEIGHT))
            pygame.display.flip()
            time.sleep(3)
            pygame.quit()

        # Keep laying eggs
        if random.random() < 0.005:
            x = random.randint(1000, 1100)
            y = random.randint(200, HEIGHT)
            egg_grp.add(Egg(x, y, egg_image1))
        if random.random() < 0.005:
            x = random.randint(900, 1100)
            y = random.randint(200, HEIGHT)
            egg_grp.add(Egg(x, y, egg_image3))

        egg_grp.draw(win)

        # check for frog and egg collision
        #collide jon snow1 with eggs
        egg_dragon_collision = pygame.sprite.spritecollide(jon_snow1, dragon1.eggs, True)
        score = score + len(egg_dragon_collision)
        egg_dragon_collision = pygame.sprite.spritecollide(jon_snow1, dragon2.eggs, True)
        score = score + len(egg_dragon_collision)
        egg_dragon_collision = pygame.sprite.spritecollide(jon_snow1, dragon3.eggs, True)
        score = score + len(egg_dragon_collision)

        egg_dragon_collision = pygame.sprite.spritecollide(jon_snow1, egg_grp, True)
        score = score + len(egg_dragon_collision)



        # Draw score and lives count
        win.blit(lives_count, (20, 20))
        win.blit(score_count, (20, 70))


        # Update time and score
        score = score + len(egg_dragon_collision)
        text_image = score_font.render(str(score), True, (255, 0, 0))
        win.blit(text_image, (80, 75))
        # Time
        timer_img = timer_font.render(str(ms_remaining / 1000), True, (255, 0, 0))
        win.blit(timer_img, (20, 130))

        pygame.display.flip()


win.blit(bg,(0, 0))
# Flip the display
pygame.display.flip()

pygame.time.delay(2000)

# Tell pygame to quit.
pygame.quit()