import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load('assets/character/white64x128.png').convert_alpha()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom = (50,650))
        self.movement_horizontal = 0
        self.gravity = 0
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement_horizontal = -5
        elif keys[pygame.K_d]:
                self.movement_horizontal = 5
        else:
            self.movement_horizontal = 0
        self.rect.x += self.movement_horizontal
        
        if keys[pygame.K_SPACE] and self.rect.bottom >= 650:
            self.gravity = -22

    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 650:
            self.rect.bottom = 650
    
    def update(self):
        self.player_input()
        self.apply_gravity()

class Background(pygame.sprite.Sprite):
    def __init__(self):  
        super().__init__()
        self.image = pygame.image.load('assets/Background/Background0.png')
        self.rect = self.image.get_rect(bottomleft = (0,720))

    def camera_movement(self):
        global follow_cam
        keys = pygame.key.get_pressed()
        if follow_cam:
            if keys[pygame.K_a]:
                self.rect.x += 5
            elif keys[pygame.K_d]:
                self.rect.x -= 5
            else:
                self.rect.x += 0


# Initialising
pygame.init()
clock = pygame.time.Clock()

# Screen vars
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('Fish Game')

# World vars
ground = 650

# Player assign to sprite group
player = pygame.sprite.GroupSingle(Player())

# Background assign to sprite group
bg = pygame.sprite.GroupSingle(Background())

# Player cam follow state
follow_cam = False
camera_x = 0

# Gameplay loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Update player and camera
    player.update()        
    camera_x = max(0, player.sprite.rect.x - screen_width // 2)
    
    # Player draw and functions
    screen.fill((95,95,95))

   
    #Camera follow
    if player.sprite.rect.midbottom[0] >= screen_width // 2 and not follow_cam:
        follow_cam = True
    elif player.sprite.rect.midbottom[0] < screen_width// 2 and follow_cam:
        follow_cam = False

    if follow_cam: 
        bg.sprite.camera_movement()
        bg.draw(screen)
        for sprite in player:
            screen.blit(sprite.image,(sprite.rect.x - camera_x, sprite.rect.y))
    else:
        bg.draw(screen)
        player.draw(screen)

    

    # screen.blit(bg,bg_rect)
    # player.draw(screen)
    
    # Display update and frame rate
    pygame.display.update()
    clock.tick(60)

