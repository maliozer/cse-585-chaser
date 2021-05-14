import pygame as pg

import random
import time
import os
import numpy as np
import pandas as pd

from chaser.config import *
from chaser.sprites import *
from chaser.graph import *
from chaser.brain import *

class Game():
    def __init__(self, simulation_id, game_no):
        self.simulation_id=str(simulation_id)
        self.game_no = str(game_no)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1800, 1200)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.runner_track = np.zeros(15).astype(int)
        self.ch1_track = np.zeros(15).astype(int)
        self.ch2_track = np.zeros(15).astype(int)
        self.runner_move_track = np.zeros(1).astype(int)
        self.ch1_move_track = np.zeros(1).astype(int)
        self.ch2_move_track = np.zeros(1).astype(int)

        self.clock = pg.time.Clock()

        self.is_map_possible4c1 = False
        self.is_map_possible4c2 = False

        self.map_checktrace = set()
        self.wall_coordinates = set()

        #runner, chaser1, chaser2
        self.turn = [1, 0, 0]
        self.winner = 0
        self.number_of_turn = 0


        self.graph = Graph()
        self.gameloop()



    def reset(self):
        self.map_checktrace.clear()


    def gameloop(self):
        self.blocksize = random.randint(15,30)
        while(self.is_map_possible4c1 == False or self.is_map_possible4c2 == False):
            self.is_map_possible4c1 = False
            self.is_map_possible4c2 = False
            #n = n -1
            pg.init()
            pg.display.set_caption('Simulation' + self.simulation_id + ' | Game ' + self.game_no)
            self.new(block=self.blocksize)

            self.map_checker(self.player.x, self.player.y, self.chaser1.x, self.chaser1.y, test4 = 1)
            self.reset()

            self.map_checker(self.player.x, self.player.y, self.chaser2.x, self.chaser2.y, test4 = 2)
            self.reset()

            #print(self.is_map_possible4c1, self.is_map_possible4c2)
        self.run()
        #print("Game Over!")

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            X_in, reward = self.get_features()
            movement, d_key = self.get_turn().decision(X_in, reward)
            self.events(movement, d_key)
            self.update()
            self.draw()

    def get_features(self):

        player_no = np.argmax(self.turn)
        agent = self.get_turn()

        #DistanceSignal[3]
        #for chasers -> #[ch to target, opponent to target, me to opponent]
        #for runner -> #[runner to opponent1, runner to opponent2, opponent1 to opponent2]
        dsf1 = self.manhattan_distance2(self.player.x, self.player.y, self.chaser1.x, self.chaser1.y)
        dsf2 = self.manhattan_distance2(self.player.x, self.player.y, self.chaser2.x, self.chaser2.y)
        dsf3 = self.manhattan_distance2(self.chaser1.x, self.chaser1.y, self.chaser2.x, self.chaser2.y)

        input_list = list()

        is_up, is_right, is_down, is_left = 0, 0, 0, 0

        if player_no == 0 or player_no == 1:
            input_list = [dsf1, dsf2, dsf3]
        elif player_no == 2:
            input_list = [dsf2, dsf1, dsf3]

        #Compass[4]
        if player_no == 0:
            if self.player.x < self.chaser1.x:
                is_right += 1
            elif self.player.x > self.chaser1.x:
                is_left += 1
            if self.player.y < self.chaser1.y:
                is_down += 1
            elif self.player.y > self.chaser1.y:
                is_up += 1

            if self.player.x < self.chaser2.x:
                is_right += 1
            elif self.player.x > self.chaser2.x:
                is_left += 1
            if self.player.y < self.chaser2.y:
                is_down += 1
            elif self.player.y > self.chaser2.y:
                is_up += 1

        if player_no == 1 or player_no == 2:
            if self.player.x > agent.x:
                is_right += 1
            elif self.player.x < agent.x:
                is_left += 1
            if self.player.y > agent.y:
                is_down += 1
            elif self.player.y < agent.y:
                is_up += 1

        input_list.append(is_up)
        input_list.append(is_right)
        input_list.append(is_down)
        input_list.append(is_left)

        #vision_inputs
        #nw, n, ne, w , e, sw, s, se
        vision_list = [1,1,1,1,1,1,1,1]

        ch_loc = [(self.chaser1.x, self.chaser1.y),(self.chaser2.x, self.chaser2.y)]
        runner_loc = (self.player.x, self.player.y)

        vision_loc = [(agent.x-1, agent.y-1), (agent.x, agent.y-1), (agent.x+1, agent.y-1), (agent.x-1, agent.y), (agent.x+1, agent.y), (agent.x-1, agent.y+1), (agent.x, agent.y+1), (agent.x+1, agent.y+1)]

        for index, loc in enumerate(vision_loc):
            if loc in self.wall_coordinates:
                vision_list[index] = 0
            else:
                if player_no == 0:
                    for chaser_pos_t1 in ch_loc:
                        if loc == chaser_pos_t1:
                            vision_list[index] += 9

                elif player_no == 1 or player_no == 2:
                    if loc == runner_loc:
                        vision_list[index] += 9

                    else:
                        for chaser_pos_t2 in ch_loc:
                            if loc == chaser_pos_t2:
                                vision_list[index] -= 11

        for v in vision_list: input_list.append(v)

        x_inputs = np.array(input_list)
        x_inputs = x_inputs.reshape(1, x_inputs.shape[0])

        reward = 0

        return x_inputs, reward

    def new(self, block):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.wall_coordinates = set()
        obj_set = set()

        for y in range(8):
            Wall(self, -1, y)
            Wall(self, 13, y)
            obj_set.add((-1, y)) #to avoid collision on map generation
            obj_set.add((13, y))
            self.wall_coordinates.add((-1, y)) #to get vision features
            self.wall_coordinates.add((13, y))

        for x in range(13):
            Wall(self, x, -1)
            Wall(self, x, 8)
            obj_set.add((x, -1))
            obj_set.add((x, 8))
            self.wall_coordinates.add((x, -1))
            self.wall_coordinates.add((x, 8))

        self.player = Player(self, 0, random.randint(0,7), is_free = True, can_move=True)
        self.chaser1 = Player(self, random.randint(11,12), random.randint(0,7), RED)
        self.chaser2 = Player(self, random.randint(11, 12), random.randint(0, 7), BLUE)

        obj_set.add((self.player.x,self.player.y))
        obj_set.add((self.chaser1.x, self.chaser1.y))
        obj_set.add((self.chaser2.x, self.chaser2.y))
        for x in range(block):
            for trial in range(10):
                rnd_x = random.randint(0,12)
                rnd_y = random.randint(0,7)
                next_wall_pos = (rnd_x, rnd_y)
                if(next_wall_pos not in obj_set):
                    Wall(self, rnd_x, rnd_y)
                    obj_set.add((rnd_x,rnd_y))
                    self.wall_coordinates.add((rnd_x, rnd_y))
                    break

    def is_collide(self,x1,y1, obj):
        x2 = obj.x
        y2 = obj.y
        if(abs(x1-x2) + abs(y1-y2) == 0):
            return True
        else:
            return False

    def vision_x(self, player, wall):
        x1 = player.x
        x2 = wall.x
        y1 = player.y
        y2 = wall.y
        return (y1 - y2)

    def vision_y(self, player, wall):
        x1 = player.x
        x2 = wall.x
        y1 = player.y
        y2 = wall.y
        return (x1 - x2)

    def collision_detection(self, player, dx, dy):
        c_x = player.x + dx
        c_y = player.y + dy

        for o_wall in self.walls.sprites():
            v_x = self.vision_x(player, o_wall)
            v_y = self.vision_y(player, o_wall)

            flag = (abs(c_x - o_wall.x) + abs(c_y - o_wall.y) == 0)

            if flag is True:
                # print("Collision detected!!", o_wall.x, o_wall.y)
                return flag

        return flag

    def get_turn(self):
        # catch all events here
        which_agent = self.turn.index(max(self.turn))

        if(which_agent == 0):
            agent = self.player
        elif(which_agent == 1):
            agent = self.chaser1
        elif(which_agent == 2):
            agent = self.chaser2

        return agent

    def set_turn(self):
        which_agent = self.turn.index(max(self.turn))
        if(which_agent == 0):
            self.turn = [0, 1, 0]
        elif(which_agent == 1):
            self.turn = [0, 0, 1]
        elif(which_agent == 2):
            self.turn = [1, 0, 0]

    def events(self, movement, direction_key):
        agent = self.get_turn()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False

            # if event.type == pg.KEYDOWN:
            #    if event.key == pg.K_ESCAPE:
            #        self.playing = False

        x,_ = self.get_features()

        if np.argmax(self.turn) == 0:
            self.runner_track = np.vstack([self.runner_track, x[0]])
            self.runner_move_track = np.append(self.runner_move_track, direction_key)
        elif np.argmax(self.turn) == 1:
            self.ch1_track = np.vstack([self.ch1_track, x[0]])
            self.ch1_move_track = np.append(self.ch1_move_track, direction_key)
        elif np.argmax(self.turn) == 2:
            self.ch2_track = np.vstack([self.ch2_track, x[0]])
            self.ch2_move_track = np.append(self.ch2_move_track, direction_key)

        if movement is not None:
            if movement == 'A':
                if not self.collision_detection(agent, dx=-1, dy=0):
                    agent.move(dx=-1)
            if movement == 'D':
                if not self.collision_detection(agent, dx=1, dy=0):
                    agent.move(dx=1)
            if movement == 'W':
                if not self.collision_detection(agent, dx=0, dy=-1):
                    agent.move(dy=-1)
            if movement == 'S':
                if not self.collision_detection(agent, dx=0, dy=1):
                    agent.move(dy=1)

        # feature debug
        # print(np.argmax(self.turn),"-->", x[0], movement,direction_key)
        self.set_turn()
        self.number_of_turn += 1

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        x1=self.player.x
        y1=self.player.y
        x2=self.chaser1.x
        y2=self.chaser1.y

        zx2=self.chaser2.x
        zy2=self.chaser2.y
        if(self.manhattan_distance2(x1,y1,x2,y2) == 0):
            self.winner = 1
            self.playing = False
            # print("Collision with chaser1 ", self.number_of_turn, self.winner)
        elif(self.manhattan_distance2(x1, y1, zx2, zy2) == 0):
            self.winner = 2
            self.playing = False
            # print("Collision with chaser2 ", self.number_of_turn, self.winner)

    def draw(self):
        # fill background
        self.screen.fill(BGCOLOR)
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def manhattan_distance2(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    def map_checker(self, px,py, cx,cy, test4):
        if(test4 == 1):
            who = self.is_map_possible4c1
        else:
            who = self.is_map_possible4c2

        if(who is not True):
            class CPos():
                def __init__(self,x,y):
                    self.x = x
                    self.y = y
            current_pos = CPos(cx,cy)
            trace = (current_pos.x, current_pos.y)
            self.map_checktrace.add(trace)
            target_distance = self.manhattan_distance2(px, py, cx, cy)
            if target_distance == 1:
                if test4 == 1:
                    self.is_map_possible4c1 = True
                else:
                    self.is_map_possible4c2 = True
                return

            # print(test4, ": --> ", cx, cy)
            if(current_pos.x > 1 and (trace[0] -1, trace[1]) not in self.map_checktrace and who is not True):
                if not self.collision_detection(current_pos, dx=-1, dy=0):
                    self.map_checker(px, py,current_pos.x-1, current_pos.y, test4)

            if(current_pos.x < 12 and (trace[0]+1, trace[1]) not in self.map_checktrace and who is not True):
                if not self.collision_detection(current_pos, dx=1, dy=0):
                    self.map_checker(px, py,current_pos.x+1, current_pos.y, test4)

            if(current_pos.y > 1 and (trace[0], trace[1]-1) not in self.map_checktrace and who is not True):
                if not self.collision_detection(current_pos, dx=0, dy=-1):
                    self.map_checker(px, py,current_pos.x, current_pos.y-1, test4)

            if(current_pos.y < 7 and (trace[0], trace[1]+1) not in self.map_checktrace and who is not True):
                if not self.collision_detection(current_pos, dx=0, dy=1):
                    self.map_checker(px, py, current_pos.x, current_pos.y+1, test4)
            return


