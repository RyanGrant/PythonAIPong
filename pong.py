import pygame
import pickle

global_training_input = []
global_training_output = []

class Player():
        def __init__(self):
                self.x, self.y = 16, SCR_HEI/2
                self.speed = 3
                self.padWid, self.padHei = 8, 64
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (32, 16))
                if self.score == 10:
                        print("player 1 wins!")
                        exit()
       
        def movement(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                        self.y -= self.speed
                elif keys[pygame.K_s]:
                        self.y += self.speed
       
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Enemy():
        def __init__(self):
                self.x, self.y = SCR_WID-16, SCR_HEI/2
                self.speed = 3
                self.padWid, self.padHei = 8, 64
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (SCR_HEI+92, 16))
                if self.score == 10:
                        print("Player 2 wins!")
                        exit()
       
        def movement(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                        self.y -= self.speed
                elif keys[pygame.K_DOWN]:
                        self.y += self.speed
       
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Ball():
        def __init__(self):
                self.x, self.y = SCR_WID/2, SCR_HEI/2
                self.speed_x = -3
                self.speed_y = 3
                self.size = 8
                
        def movement(self):
                self.x += self.speed_x
                self.y += self.speed_y
                
                #wall col
                if self.y <= 0:
                        self.speed_y *= -1
                elif self.y >= SCR_HEI-self.size:
                        self.speed_y *= -1
 
                if self.x <= 0:
                        self.__init__()
                        enemy.score += 1
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        self.speed_x = 3
                        player.score += 1
                ##wall col
                #paddle col
                #player
                for n in range(-self.size, player.padHei):
                        if self.y == player.y + n:
                                if self.x <= player.x + player.padWid:
                                        # Change the ball's direction if it hits player paddle
                                        self.speed_x *= -1
                                        # Also save the player's and ball's y position (TRAINING INPUT)
                                        global global_training_input
                                        global_training_input.append((player.y, self.y))
                                        break
                        n += 1
                #enemy
                for n in range(-self.size, enemy.padHei):
                        if self.y == enemy.y + n:
                                if self.x >= enemy.x - enemy.padWid:
                                        # Change the ball's direction if it hits enemy paddle
                                        self.speed_x *= -1
                                        # Also save the enemy's position (TRAINING OUTPUT)
                                        global global_training_output
                                        global_training_output.append(enemy.y)
                                        break
                        n += 1
                ##paddle col
 
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, 8, 8))
 
SCR_WID, SCR_HEI = 640, 480
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60
 
ball = Ball()
player = Player()
enemy = Enemy()
# Making the W&L text show up
wlu_text = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
wlu_blit = wlu_text.render("W&L", 1, (0, 0, 204))


def save_data(fileName):
        global global_training_output
        global global_training_input
        with open(fileName, 'wb') as f:
                pickle.dump((global_training_input, global_training_output), f)
 
def load_data(fileName):
        with open(fileName, 'rb') as f:
                inputs, outputs = pickle.load(f)
        return (inputs, outputs)

while True:
        #process
        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                print("Game exited by user")
                                save_data("training_data.dat")
                                exit()
        ##process
        #logic
        ball.movement()
        player.movement()
        enemy.movement()
        ##logic
        #draw
        screen.fill((255, 255, 255))
        ball.draw()
        player.draw()
        player.scoring()
        enemy.draw()
        enemy.scoring()
        screen.blit(wlu_blit, (SCR_WID//3 + 40, 16))
        ##draw
        #_______
        pygame.display.flip()
        clock.tick(FPS)
