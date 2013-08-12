#!/usr/bin/env python
#-*- coding:utf-8 -*-

# developed by Jeremy Gangnier - http://jergagnier.wix.com/
# no licensing information provided
# code improvements by daniel@basso.inf.br


import os
import pygame as pg

from random import randint
from math import cos, sin, radians


pg.init()


class color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)


class fonts:
    name = 'fonts/BOOKOS.TTF'
    if not os.path.exists(name):
        name = pg.font.get_default_font()
    p = pg.font.Font(name, 20)
    t1 = pg.font.Font(name, 58)
    t2 = pg.font.Font(name, 48)


size = width,height = 800,660
screen = pg.display.set_mode(size)

trans_scr = pg.Surface(size)
trans_scr.set_alpha(150)
trans_scr.set_colorkey(color.black)

paths_img = pg.Surface(size)
paths_img.set_colorkey(color.black)

empty_hex = pg.Surface((101,100)) # Base image for a board piece
empty_hex.set_colorkey(color.black)
for b in range(20):
    points = []
    for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
    pg.draw.polygon(empty_hex,(100,100,175+b*4),points)

start_hex = pg.Surface((101,100))
start_hex.set_colorkey(color.black)
for b in range(20):
    points = []
    for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
    pg.draw.polygon(start_hex,(175+b*4,0,0),points)


class Board:
    def __init__(self):
        """This class handles the game board."""

        self.pieces = []
        self.line1 = [[3,3],10]

        # This list helps significantly in drawing the board pieces
        self.coords = ((250,0,[0,0]),(325,44,[1,0]),(400,88,[2,0]),(475,132,[3,0]),(175,44,[0,1]),(250,88,[1,1]),\
        (325,132,[2,1]),(400,176,[3,1]),(475,220,[4,1]),(100,88,[0,2]),(175,132,[1,2]),(250,176,[2,2]),(325,220,[3,2]),\
        (400,264,[4,2]),(475,308,[5,2]),(25,132,[0,3]),(100,176,[1,3]),(175,220,[2,3]),(250,264,[3,3]),(325,308,[4,3]),\
        (400,352,[5,3]),(475,396,[6,3]),(25,220,[1,4]),(100,264,[2,4]),(175,308,[3,4]),(250,352,[4,4]),(325,396,[5,4]),\
        (400,440,[6,4]),(25,308,[2,5]),(100,352,[3,5]),(175,396,[4,5]),(250,440,[5,5]),(325,484,[6,5]),(25,396,[3,6]),\
        (100,440,[4,6]),(175,484,[5,6]),(250,528,[6,6]))

        for i in self.coords:
            if i[2] != [3,3]:
                self.pieces.append([(empty_hex,[]),(i[0],i[1])])
            else:
                self.pieces.append([(start_hex,1),(i[0],i[1])])

    def add_piece(self,piece,position):
        """Adds a piece to the board."""

        self.pieces.append([piece,position])

    def draw_board(self,surface):
        """Draws the board."""

        for i in self.pieces: surface.blit(i[0][0],i[1])

    def draw_path(self,surface):
        """Draws the current path taken through the board."""

        for i in self.coords:
            if i[2] == self.line1[0]:
                x = 50+cos(radians(self.line1[1]*30-15))*45+i[0]
                y = 50+sin(radians(self.line1[1]*30-15))*45+i[1]
                pg.draw.circle(surface,color.red,(int(round(x)),int(round(y))),5)


def make_piece(hex=1):
    """Creates a new board piece image and possible paths."""

    if hex:
        piece = pg.Surface((101,100))
        piece.set_colorkey(color.black)
        path_img = pg.Surface((101,100))
        path_img.set_colorkey(color.white)
        path_img.set_alpha(254)
        path_img.fill(color.white)
        for b in range(10):
            points = []
            for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
            pg.draw.polygon(piece,(255-b*10,202-b*10,131-b*10),points)
        paths = []
        for i in range(6):
            while 1:
                path_s = randint(1,12)
                path_e = randint(1,12)
                breaker = 1
                for b in paths:
                    if b[0] == path_s or b[1] == path_s or \
                    b[0] == path_e or b[1] == path_e or path_s == path_e:
                        breaker = 0
                        break
                if len(paths) == 0 and path_s == path_e: breaker = 0
                if breaker: break
            paths.append([path_s,path_e])
        for i in paths:
            x1 = 50+cos(radians(i[0]*30-15))*45
            y1 = 50+sin(radians(i[0]*30-15))*45
            x2 = 50+cos(radians(i[1]*30-15))*45
            y2 = 50+sin(radians(i[1]*30-15))*45
            if -1 <= i[0]-i[1] <= 1 and ((i[0] > i[1] and i[0]%2 < i[1]%2) \
            or (i[0] < i[1] and i[0]%2 > i[1]%2)): width = 10
            else: width = 5
            pg.draw.line(path_img,color.black,(x1,y1),(x2,y2),width)

    piece.blit(path_img,(0,0))
    return [piece,paths]

def draw_text(x,y,font,text,colour,surface=screen):
    """Helper function for drawing text."""

    x2,y2 = font.size(text)
    surface.blit(font.render(text,1,colour),(x-x2/2,y-y2/2))

g_board = Board()   # Initialise game board
status = 1
points1 = 0

new_tile = make_piece() # Make the next tile
rep_tile = make_piece() # Make the reserved tile
cont = 1

xy_incs = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]
xy_px_incs = [(75, 44), (0, 88), (-75, 44), (-75, -44), (0, -88), (75, -44)]
xy_inc_map = dict((i + 1, xy_incs[i // 2]) for i in range(12))
xy_px_inc_map = dict((i + 1, xy_px_incs[i // 2]) for i in range(12))

while cont:
    lc = rc = 0
    for event in pg.event.get():
        if event.type == pg.QUIT: cont = 0
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: lc = 1
            if event.button == 3: rc = 1

    if pg.key.get_pressed()[pg.K_ESCAPE]: break
    mx,my = pg.mouse.get_pos()

    if rc and status == 1:  # Rotate tile
        for i in new_tile[1]:
            i[0] = (i[0]+2)%12
            i[1] = (i[1]+2)%12
            if i[0] == 0: i[0] = 12
            if i[1] == 0: i[1] = 12

        piece = pg.Surface((101,100))  # Change the image of the tile
        piece.set_colorkey(color.black)
        path_img = pg.Surface((101,100))
        path_img.set_colorkey(color.white)
        path_img.set_alpha(254)
        path_img.fill(color.white)
        for b in range(10):
            points = []
            for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
            pg.draw.polygon(piece,(255-b*10,202-b*10,131-b*10),points)

        for i in new_tile[1]:   # Redraw the paths
            x1 = 50+cos(radians(i[0]*30-15))*45
            y1 = 50+sin(radians(i[0]*30-15))*45
            x2 = 50+cos(radians(i[1]*30-15))*45
            y2 = 50+sin(radians(i[1]*30-15))*45
            if -1 <= i[0]-i[1] <= 1 and ((i[0] > i[1] and i[0]%2 < i[1]%2) \
            or (i[0] < i[1] and i[0]%2 > i[1]%2)): width = 10
            else: width = 5
            pg.draw.line(path_img,color.black,(x1,y1),(x2,y2),width)
        piece.blit(path_img,(0,0))

        new_tile[0] = piece

    elif lc and status == 1 and 0 < mx < 100 and 530 < my < 630:    # Swap current tile with reserve tile
        new_tile,rep_tile = rep_tile,new_tile

    elif lc and 640 < mx < 760 and 15 < my < 45:    # New game button
        g_board = Board()
        status = 1
        points1 = 0

        new_tile = make_piece()
        rep_tile = make_piece()
        paths_img.fill(color.black)

    elif lc and status == 1:    # Place down new tile and update path
        # Change x,y coordinate
        g_board.line1[0][0] += xy_inc_map[g_board.line1[1]][0]
        g_board.line1[0][1] += xy_inc_map[g_board.line1[1]][1]
        # Complex path changing
        path_update = ((g_board.line1[1] - 1 & ~1) + 7) % 12
        g_board.line1[1] = g_board.line1[1] % 2 + path_update

        for i in range(len(g_board.coords)):
            if g_board.coords[i][2] == g_board.line1[0]: break
        else:
            status = -1
        g_board.pieces[i][0] = new_tile

        del new_tile

    # Update the screen image
    screen.fill(color.white)
    trans_scr.fill(color.black)
    g_board.draw_board(screen)

    for i in g_board.coords:
        if i[2] == g_board.line1[0]:
            x = i[0] + xy_px_inc_map[g_board.line1[1]][0]
            y = i[1] + xy_px_inc_map[g_board.line1[1]][1]
            in_map = 0
            for i in g_board.coords:
                if i[0:2] == (x,y): in_map = 1
            if not in_map: status = -1



    if status == 1: # Not updating path condition
        try: trans_scr.blit(new_tile[0],(x,y))  # Draw transparent tile

        except:
            for i in range(len(g_board.coords)):
                if g_board.coords[i][2] == g_board.line1[0]: break

            current_piece = g_board.pieces[i]

            if current_piece[0][1] != [] and status != -1:
                status = 0

                if current_piece[0][1] == 1: status = -1

                if status == 0:
                    chain = 1
                    points1 += chain
                    for i in current_piece[0][1]:

                        draw_line = 0
                        if g_board.line1[1] == i[0]:
                            g_board.line1[1] = i[1]
                            draw_line = 1
                        elif g_board.line1[1] == i[1]:
                            g_board.line1[1] = i[0]
                            draw_line = 1

                        if draw_line:
                            x1 = 50+cos(radians(i[0]*30-15))*45+current_piece[1][0]
                            y1 = 50+sin(radians(i[0]*30-15))*45+current_piece[1][1]
                            x2 = 50+cos(radians(i[1]*30-15))*45+current_piece[1][0]
                            y2 = 50+sin(radians(i[1]*30-15))*45+current_piece[1][1]
                            pg.draw.line(paths_img,color.red,(x1,y1),(x2,y2),3)

                    for i in g_board.coords:
                        if i[2] == g_board.line1[0]:
                            x = i[0] + xy_px_inc_map[g_board.line1[1]][0]
                            y = i[1] + xy_px_inc_map[g_board.line1[1]][1]

                    for i in range(len(g_board.coords)):
                        if (x,y) == g_board.coords[i][0:2]: break
                    next_piece = g_board.pieces[i]

                    if next_piece[0][1] == []:
                        status = 1
                        new_tile = make_piece()

    elif status == 0:   # Still updating path condition
        # Change x,y coordinate
        g_board.line1[0][0] += xy_inc_map[g_board.line1[1]][0]
        g_board.line1[0][1] += xy_inc_map[g_board.line1[1]][1]
        # Change path end
        path_update = ((g_board.line1[1] - 1 & ~1) + 7) % 12
        g_board.line1[1] = g_board.line1[1] % 2 + path_update

        for i in range(len(g_board.coords)):
            if g_board.coords[i][2] == g_board.line1[0]: break

        current_piece = g_board.pieces[i]

        if current_piece[0][1] != [] and status != -1:
            status = 0

            if current_piece[0][1] == 1: status = -1

            if status == 0: # Award points for chaining
                chain += 1
                points1 += chain
                for i in current_piece[0][1]:
                    draw_line = 0
                    if g_board.line1[1] == i[0]:
                        g_board.line1[1] = i[1]
                        draw_line = 1
                    elif g_board.line1[1] == i[1]:
                        g_board.line1[1] = i[0]
                        draw_line = 1
                    if draw_line:
                        x1 = 50+cos(radians(i[0]*30-15))*45+current_piece[1][0]
                        y1 = 50+sin(radians(i[0]*30-15))*45+current_piece[1][1]
                        x2 = 50+cos(radians(i[1]*30-15))*45+current_piece[1][0]
                        y2 = 50+sin(radians(i[1]*30-15))*45+current_piece[1][1]
                        pg.draw.line(paths_img,color.red,(x1,y1),(x2,y2),3)

                for i in g_board.coords:
                    if i[2] == g_board.line1[0]:
                        x = i[0] + xy_px_inc_map[g_board.line1[1]][0]
                        y = i[1] + xy_px_inc_map[g_board.line1[1]][1]

                for i in range(len(g_board.coords)):
                    if (x,y) == g_board.coords[i][0:2]: break
                next_piece = g_board.pieces[i]

                if next_piece[0][1] == []:  # Done chaining, make next tile
                    status = 1
                    new_tile = make_piece()

    # Finish up drawing
    screen.blit(trans_scr,(0,0))
    screen.blit(paths_img,(0,0))
    screen.blit(rep_tile[0],(0,530))

    p_msg = fonts.p.render('Points: '+str(points1),1,color.black)
    screen.blit(p_msg,(10,10))
    draw_text(700, 30, fonts.p, 'New Game',color.black)
    if 640 < mx < 760 and 15 < my < 45:
        pg.draw.rect(screen,color.black,(640,15,120,30),2)

    g_board.draw_path(screen)

    if status == -1:    # Game ending condition
        screen.blit(fonts.t1.render('Game Over',0,color.black),(150,250))
        screen.blit(fonts.t1.render('Game Over',1,color.white),(150,250))
        if points1 == 1:
            screen.blit(fonts.t2.render('You are a disgrace.',1,color.white),(100,310))
        else:
            screen.blit(fonts.t2.render('You scored '+str(points1)+' points.',1,color.white),(70,310))

    pg.display.flip()
    pg.time.wait(30)


