import pygame
from sys import exit
from random import randint, choice

pygame.init()

font = pygame.font.Font("font/Pixeltype.ttf", 50)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1 , player_walk_2]
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        # self.player = player_walk[0]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300 :
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0


        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1500), y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.distroy()

    def distroy(self):
        if self.rect.x <= -100:
            self.kill()

def collision_sprite():
    if pygame.sprite.spritecollide(new_player.sprite, obstacle, True):
        obstacle.empty()
        return False
    return True

def display_score():
    global font
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score = font.render(f"{current_time}", False,(64, 64, 64))
    score_rect = score.get_rect(center = (800/2, 50 ))
    window.blit(score, score_rect)
    return current_time
#
# def obstacle_movement(obstacle_rect_list):
#     if obstacle_rect_list :
#         for object_rect in obstacle_rect_list:
#             object_rect.x -= 5
#             if object_rect.bottom == 300:
#                 window.blit(snail, object_rect)
#             else:
#                 window.blit(fly, object_rect)
#         obstacle_list = [obstacle_rect for obstacle_rect in obstacle_rect_list if obstacle_rect.x > 100]
#         return obstacle_rect_list
#     return []
#
# def detect_collision(player_rect, obstacle_rect_list):
#     if obstacle_rect_list:
#         for obstacle_rect in obstacle_rect_list:
#             if player_rect.colliderect(obstacle_rect):
#                 return False
#     return True
#
# def player_animation():
#     global player, player_index
#     if player_rect.bottom < 300:
#         player = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= len(player_walk):
#             player_index = 0
#         player = player_walk[int(player_index)]

window = pygame.display.set_mode((800,400))
pygame.display.set_caption("title")
clock = pygame.time.Clock()
game_active =False
start_time  = 0
score = 0
sky = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

#Groups
new_player = pygame.sprite.GroupSingle()
new_player.add(Player())

obstacle = pygame.sprite.Group()


player_gravity = 0


obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_walk = [player_walk_1 , player_walk_2]
player = player_walk[0]
player_index = 0
player_rect = player.get_rect(midbottom = (80,300))

# obstacles
snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snails = [snail_1, snail_2]
snail_index = 0
snail = snails[0]

fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
flies = [fly_1, fly_2]
fly_index = 0
fly = flies[0]

player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (800/2, 400/2))

game_name = font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

# timer
obstacle_timer = pygame.USEREVENT + 1 #custom event
pygame.time.set_timer(obstacle_timer, 1600)# trigger the event based on the given time
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


game_message = font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        # if game_active:
            # if player_rect.bottom == 300:
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             player_gravity = -20
            #
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         player_gravity -= 20

        if True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                # snail_rect.x = 800
                # player_rect.y = 300

        if game_active:
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(["fly", "snail", "snail"])))
                # if randint(0, 2):
                #     object_obstacle_list = obstacle_rect_list.append(snail.get_rect(midbottom = (randint(900, 1100), 300)))
                # else:
                #     object_obstacle_list = obstacle_rect_list.append(fly.get_rect(midbottom = (randint(900,1100), 210)))

            # if event.type == snail_animation_timer:
            #     if snail_index == 0:
            #         snail_index = 1
            #     else :
            #         snail_index = 0
            #     snail = snails[snail_index]

            # if event.type == fly_animation_timer:
            #     if fly_index == 0:
            #         fly_index = 1
            #     else :
            #         fly_index = 0
            #     fly = flies[fly_index]

    if game_active:
        window.blit(sky, (0, 0))
        window.blit(ground, (0, 300))
        # player_animation()
        # window.blit(player, player_rect)
        new_player.draw(window)
        new_player.update()

        obstacle.draw(window)
        obstacle.update()

        score = display_score()
        game_active = collision_sprite()

        # player_gravity += 1
        # player_rect.y += player_gravity

        # if player_rect.bottom >300:
        #     player_rect.bottom = 300
        # obstacle_movement(obstacle_rect_list)
        # game_active = detect_collision(player_rect, obstacle_rect_list)

    else:
        window.fill((94, 129, 162))
        # obstacle_rect_list = []
        # player_rect.bottom = 300
        window.blit(player_stand, player_stand_rect)
        window.blit(game_name, game_name_rect)
        if score == 0 :
            window.blit(game_message, game_message_rect)
        else:
            show_score = font.render(f"your score: {score}", False, (111, 196, 169))
            show_score_rect = show_score.get_rect(center = (400, 320))
            window.blit(show_score, show_score_rect)



    pygame.display.update()
    clock.tick(60)



        # elif event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("yaa")

        # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

        # if player_rect.colliderect(snail_rect):
    #     print("collide")


        # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print("j")