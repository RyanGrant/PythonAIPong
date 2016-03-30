"""
Ryan Grant, Michael Holt, Mitch Olson, Stephen Rowley
CSCI 315
Final Project
ai_pong.py
This program allows one user to play pong against an AI Paddle.
"""

import pygame
import pickle
import numpy as np
from backprop import *

testing_input = []
have_new_input = False

class Player():
        def __init__(self):
                self.x, self.y = 16, SCR_HEI/2
                self.speed = 3
                self.padWid, self.padHei = 8, 85
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
 
class AiPaddle():
        def __init__(self, backprop):
                global size_of_spot
                self.x, self.y = SCR_WID-16, SCR_HEI/2
                self.goal_y = self.y
                self.speed = 3
                self.padWid, self.padHei = 8, 85
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
                self.backprop = backprop
                
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (SCR_HEI+92, 16))
                if self.score == 10:
                        print("Player 2 wins!")
                        exit()
       
        def movement(self):
                global have_new_input
                global testing_input
                # We will only move this paddle if new input has been given
                if have_new_input:
                        # Our inputs are way too big, so we scale them down
                        scaled_testing_input = [x/100 for x in testing_input]
                        output = self.backprop.test(scaled_testing_input)
                        # Find which of the spots is the hottest
                        spot_num = np.argmax(output) 
                        self.goal_y = convert_correct_form_to_location(spot_num, size_of_spot)
                        # Reset the input flag to False
                        have_new_input = False
                check_sum = self.y - self.goal_y
                # check to see if the paddle is where it is supposed to be
                if check_sum != 0:
                        if check_sum < 0:
                                self.y += self.speed
                        else:
                                self.y -= self.speed
                """ Key-based movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                        self.y -= self.speed
                elif keys[pygame.K_DOWN]:
                        self.y += self.speed
       
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64 """
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Ball():
        def __init__(self):
                self.x, self.y = SCR_WID/2, SCR_HEI/2
                # The last index below represents the previous y position
                # The first index below represents the eighth previous y postion
                self.y_prev_list = [0,0,0,0,0,0,0,0]
                self.speed_x = -3
                self.speed_y = 3
                self.size = 8
                
        def movement(self):
                self.x += self.speed_x
                # Update previous y values before changing self.y
                for i in range(len(self.y_prev_list)-1):
                        self.y_prev_list[i] = self.y_prev_list[i+1]
                self.y_prev_list[len(self.y_prev_list)-1] = self.y
                self.y += self.speed_y
                
                #wall col
                if self.y <= 0:
                        self.speed_y *= -1
                elif self.y >= SCR_HEI-self.size:
                        self.speed_y *= -1
 
                if self.x <= 0:
                        self.__init__()
                        AiPaddle.score += 1
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        self.speed_x = 3
                        player.score += 1
                        # We move the AI paddle back to a spot so it can hit the ball
                        AiPaddle.y = convert_correct_form_to_location(6, size_of_spot)
                        AiPaddle.goal_y = AiPaddle.y
                ##wall col
                #paddle col
                #player
                for n in range(-self.size, player.padHei):
                        if self.y == player.y + n:
                                if self.x <= player.x + player.padWid:
                                        # Change the ball's direction if it hits player paddle
                                        self.speed_x *= -1
                                        # We want to signify that we have received new input
                                        # so that our AI Paddle knows to test this input
                                        global have_new_input
                                        global testing_input
                                        have_new_input = True
                                        testing_input = [player.y] + self.y_prev_list + [self.y]
                                        break
                        n += 1
                #AiPaddle
                for n in range(-self.size, AiPaddle.padHei):
                        if self.y == AiPaddle.y + n:
                                if self.x >= AiPaddle.x - AiPaddle.padWid:
                                        # Change the ball's direction if it hits AiPaddle paddle
                                        self.speed_x *= -1
                                        break
                        n += 1
                ##paddle col
 
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, 8, 8))


 
def load_data(fileName):
        with open(fileName, 'rb') as f:
                inputs, outputs = pickle.load(f)
        return (inputs, outputs)

"""
convert_out_to_correct_form takes a y position of a paddle and converts it
into its corresponding output within the network
"""
def convert_location_to_correct_form(y_location):
        spot_num = -1
        counter = 0
        current_location = 0
        while current_location < SCR_HEI and spot_num == -1:
                if y_location <= current_location + size_of_spot-1:
                        spot_num = counter
                counter += 1
                current_location += size_of_spot
        if current_location > SCR_HEI:
                spot_num = no_of_outputs-1    # We are at the last (lowest) spot in this case
        return [0]*spot_num + [1] + [0]*((no_of_outputs-1)-spot_num)

"""
convert_correct_form_to_location takes a spot number representing which spot
the paddle should be in and converts it to a corresponding location
"""
def convert_correct_form_to_location(spot_num, size_of_spot):
        return spot_num*size_of_spot
        

SCR_WID, SCR_HEI = 640, 480
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()

'''Initialize the backprop network'''
# Find number of outputs by dividing the height of the screen into the
# number of spots our paddle must cover (64 is height of paddle);
# When testing, we will have the paddle move to the "hottest" output spot
no_of_outputs = (SCR_HEI // 64) + 1
size_of_spot = SCR_HEI / no_of_outputs
# 10 inputs are ball's y position, its previous eight y positions, and the player's paddle position
no_of_inputs = 10
# Start with 10 hidden units
bprop = Backprop(no_of_inputs, 10, no_of_outputs, .01)
"""
# Train the network with our pickled target I/O
inputs_1, outputs_1 = load_data("./pickled_data/training_data_10_inputs.dat")
inputs_2, outputs_2 = load_data("./pickled_data/training_data_10_inputs_2.dat")
# 3rd set of inputs handles when the AI paddle misses and needs to get back on track
inputs_3, outputs_3 = load_data("./pickled_data/training_data_10_inputs_3.dat")
# 4th set of inputs handles a specific pattern the AI Paddle has missed
inputs_4, outputs_4 = load_data("./pickled_data/training_data_10_inputs_4.dat")
# Combine the various sets of inputs and outputs
inputs = inputs_1 + inputs_2 + inputs_3 + inputs_4
outputs = outputs_1 + outputs_2 + outputs_3 + outputs_4
actual_inputs = []
for tupl in inputs:
        actual_inputs.append([tupl[i]/100 for i in range(len(tupl))])

actual_outputs = []
for paddle_location in outputs:
        # spot_num will represent which location the AI paddle should go to,
        # so our output will be a one-hot output with this spot_num as a 1 and
        # everything else as a 0
        actual_output1 = convert_location_to_correct_form(paddle_location)
        actual_outputs.append(actual_output1)
bprop.train(actual_inputs, actual_outputs, niter=20000, eta=1)
# Save network's weights into "./pickled_data/trained_network_#.dat"
bprop.save("./pickled_data/trained_network_3.dat")
"""
"""After network's weights are pickled, we will use below code (instead of above 10 lines)
# trained_network.dat has no training data for when the ball gets by the computer (no training_data_10_input_3.dat)
        # We get into a cycle of losing after one ball misses
        # Only used training_data_10_input.dat and training_data_10_input_2.dat as input
        # Weightscale = 0.01
        # Eta = 1
        # Niter=20000
        # 10 hidden units
        # RMS Error = 0.10
bprop.load("./pickled_data/trained_network.dat")
# trained_network_2.dat has training data for when the ball gets by the computer paddle
        # We get into a cycle of losing after one ball misses
        # Only used training_data_10_input.dat, training_data_10_input_2.dat and training_data_10_input_3.dat as input
        # Weightscale = 0.01
        # Eta = 1
        # Niter=20000
        # 10 hidden units
        # RMS Error = 0.16
# trained_network_3.dat has training data for when the ball gets by the computer and for patterns commonly missed
# Only used training_data_10_input.dat, training_data_10_input_2.dat, training_data_10_input_3.dat and training_data_10_input_4.dat as input
        # Weightscale = 0.01
        # Eta = 1
        # Niter=20000
        # 10 hidden units
        # RMS Error = 0.17
"""
bprop.load("./pickled_data/trained_network_3.dat")

clock = pygame.time.Clock()
FPS = 60

ball = Ball()
player = Player()
AiPaddle = AiPaddle(bprop)
# Making the W&L text show up
wlu_text = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
wlu_blit = wlu_text.render("W&L", 1, (0, 0, 204))



while True:
        #process
        for event in pygame.event.get():
                        # MUST X OUT OF GAME AND HIT "CANCEL" ON POP-UP TO ENTER BELOW IF
                        if event.type == pygame.QUIT:
                                print("Game exited by user")
                                exit()
        ##process
        #logic
        ball.movement()
        player.movement()
        AiPaddle.movement()
        ##logic
        #draw
        screen.fill((255, 255, 255))
        ball.draw()
        player.draw()
        player.scoring()
        AiPaddle.draw()
        AiPaddle.scoring()
        screen.blit(wlu_blit, (SCR_WID//3 + 40, 16))
        ##draw
        #_______
        pygame.display.flip()
        clock.tick(FPS)
