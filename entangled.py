from pygame import *
from pygame import _view
from random import *
from math import *

init()

size = width,height = 800,660
screen = display.set_mode(size)

trans_scr = Surface(size)
trans_scr.set_alpha(150)
trans_scr.set_colorkey((0,0,0))

paths_img = Surface(size)
paths_img.set_colorkey((0,0,0))

empty_hex = Surface((101,100)) # Base image for a board piece
empty_hex.set_colorkey((0,0,0))
for b in range(20):
    points = []
    for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
    draw.polygon(empty_hex,(100,100,175+b*4),points)

start_hex = Surface((101,100))
start_hex.set_colorkey((0,0,0))
for b in range(20):
    points = []
    for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
    draw.polygon(start_hex,(175+b*4,0,0),points)

p_font = font.Font('fonts/BOOKOS.ttf',20)
t1_font = font.Font('fonts/BOOKOS.ttf',58)
t2_font = font.Font('fonts/BOOKOS.ttf',48)

class entangled:
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
                draw.circle(surface,(255,0,0),(round(x),round(y)),5)


def make_piece(hex=1):
    """Creates a new board piece image and possible paths."""

    if hex:
        piece = Surface((101,100))
        piece.set_colorkey((0,0,0))
        path_img = Surface((101,100))
        path_img.set_colorkey((255,255,255))
        path_img.set_alpha(254)
        path_img.fill((255,255,255))
        for b in range(10):
            points = []
            for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
            draw.polygon(piece,(255-b*10,202-b*10,131-b*10),points)
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
            draw.line(path_img,(0,0,0),(x1,y1),(x2,y2),width)

    piece.blit(path_img,(0,0))
    return [piece,paths]

def draw_text(x,y,font,text,colour,surface=screen):
    """Helper function for drawing text."""

    x2,y2 = font.size(text)
    surface.blit(font.render(text,1,colour),(x-x2/2,y-y2/2))

g_board = entangled()   # Initialise game board
status = 1
points1 = 0

new_tile = make_piece() # Make the next tile
rep_tile = make_piece() # Make the reserved tile
cont = 1

while cont:
    lc = rc = 0
    for evnt in event.get():
        if evnt.type == QUIT: cont = 0
        elif evnt.type == MOUSEBUTTONDOWN:
            if evnt.button == 1: lc = 1
            if evnt.button == 3: rc = 1

    if key.get_pressed()[K_ESCAPE]: break
    mx,my = mouse.get_pos()

    if rc and status == 1:  # Rotate tile
        for i in new_tile[1]:
            i[0] = (i[0]+2)%12
            i[1] = (i[1]+2)%12
            if i[0] == 0: i[0] = 12
            if i[1] == 0: i[1] = 12

        piece = Surface((101,100))  # Change the image of the tile
        piece.set_colorkey((0,0,0))
        path_img = Surface((101,100))
        path_img.set_colorkey((255,255,255))
        path_img.set_alpha(254)
        path_img.fill((255,255,255))
        for b in range(10):
            points = []
            for i in range(6): points.append((50+cos(radians(i*60))*(50-b),50+sin(radians(i*60))*(50-b)))
            draw.polygon(piece,(255-b*10,202-b*10,131-b*10),points)

        for i in new_tile[1]:   # Redraw the paths
            x1 = 50+cos(radians(i[0]*30-15))*45
            y1 = 50+sin(radians(i[0]*30-15))*45
            x2 = 50+cos(radians(i[1]*30-15))*45
            y2 = 50+sin(radians(i[1]*30-15))*45
            if -1 <= i[0]-i[1] <= 1 and ((i[0] > i[1] and i[0]%2 < i[1]%2) \
            or (i[0] < i[1] and i[0]%2 > i[1]%2)): width = 10
            else: width = 5
            draw.line(path_img,(0,0,0),(x1,y1),(x2,y2),width)
        piece.blit(path_img,(0,0))

        new_tile[0] = piece

    elif lc and status == 1 and 0 < mx < 100 and 530 < my < 630:    # Swap current tile with reserve tile
        new_tile,rep_tile = rep_tile,new_tile

    elif lc and 640 < mx < 760 and 15 < my < 45:    # New game button
        g_board = entangled()
        status = 1
        points1 = 0

        new_tile = make_piece()
        rep_tile = make_piece()
        paths_img.fill((0,0,0))

    elif lc and status == 1:    # Place down new tile and update path

        if g_board.line1[1] in (1,2): x_plus,y_plus = 1,0
        if g_board.line1[1] in (3,4): x_plus,y_plus = 1,1
        if g_board.line1[1] in (5,6): x_plus,y_plus = 0,1
        if g_board.line1[1] in (7,8): x_plus,y_plus = -1,0
        if g_board.line1[1] in (9,10): x_plus,y_plus = -1,-1
        if g_board.line1[1] in (11,12): x_plus,y_plus = 0,-1
        g_board.line1[0][0] += x_plus
        g_board.line1[0][1] += y_plus

        # Complex path changing
        if g_board.line1[1] in (1,2): g_board.line1[1] = g_board.line1[1]%2+7
        elif g_board.line1[1] in (3,4): g_board.line1[1] = g_board.line1[1]%2+9
        elif g_board.line1[1] in (5,6): g_board.line1[1] = g_board.line1[1]%2+11
        elif g_board.line1[1] in (7,8): g_board.line1[1] = g_board.line1[1]%2+1
        elif g_board.line1[1] in (9,10): g_board.line1[1] = g_board.line1[1]%2+3
        elif g_board.line1[1] in (11,12): g_board.line1[1] = g_board.line1[1]%2+5
        else: raise 'WHAAAT'    # (this should never happen)

        for i in range(len(g_board.coords)):
            if g_board.coords[i][2] == g_board.line1[0]: break
        else:
            status = -1
        g_board.pieces[i][0] = new_tile

        del new_tile

    # Update the screen image
    screen.fill((255,255,255))
    trans_scr.fill((0,0,0))
    g_board.draw_board(screen)

    for i in g_board.coords:
        if i[2] == g_board.line1[0]:

            if g_board.line1[1] in (1,2): x_plus,y_plus = 75,44
            if g_board.line1[1] in (3,4): x_plus,y_plus = 0,88
            if g_board.line1[1] in (5,6): x_plus,y_plus = -75,44
            if g_board.line1[1] in (7,8): x_plus,y_plus = -75,-44
            if g_board.line1[1] in (9,10): x_plus,y_plus = 0,-88
            if g_board.line1[1] in (11,12): x_plus,y_plus = 75,-44
            x = i[0]+x_plus
            y = i[1]+y_plus

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
                            draw.line(paths_img,(255,0,0),(x1,y1),(x2,y2),3)

                    for i in g_board.coords:
                        if i[2] == g_board.line1[0]:
                            if g_board.line1[1] in (1,2): x_plus,y_plus = 75,44
                            if g_board.line1[1] in (3,4): x_plus,y_plus = 0,88
                            if g_board.line1[1] in (5,6): x_plus,y_plus = -75,44
                            if g_board.line1[1] in (7,8): x_plus,y_plus = -75,-44
                            if g_board.line1[1] in (9,10): x_plus,y_plus = 0,-88
                            if g_board.line1[1] in (11,12): x_plus,y_plus = 75,-44
                            x = i[0]+x_plus
                            y = i[1]+y_plus

                    for i in range(len(g_board.coords)):
                        if (x,y) == g_board.coords[i][0:2]: break
                    next_piece = g_board.pieces[i]

                    if next_piece[0][1] == []:
                        status = 1
                        new_tile = make_piece()

    elif status == 0:   # Still updating path condition

        # Change x,y coordinate
        if g_board.line1[1] in (1,2): x_plus,y_plus = 1,0
        if g_board.line1[1] in (3,4): x_plus,y_plus = 1,1
        if g_board.line1[1] in (5,6): x_plus,y_plus = 0,1
        if g_board.line1[1] in (7,8): x_plus,y_plus = -1,0
        if g_board.line1[1] in (9,10): x_plus,y_plus = -1,-1
        if g_board.line1[1] in (11,12): x_plus,y_plus = 0,-1
        g_board.line1[0][0] += x_plus
        g_board.line1[0][1] += y_plus

        # Change path end
        if g_board.line1[1] in (1,2): g_board.line1[1] = g_board.line1[1]%2+7
        elif g_board.line1[1] in (3,4): g_board.line1[1] = g_board.line1[1]%2+9
        elif g_board.line1[1] in (5,6): g_board.line1[1] = g_board.line1[1]%2+11
        elif g_board.line1[1] in (7,8): g_board.line1[1] = g_board.line1[1]%2+1
        elif g_board.line1[1] in (9,10): g_board.line1[1] = g_board.line1[1]%2+3
        elif g_board.line1[1] in (11,12): g_board.line1[1] = g_board.line1[1]%2+5
        else: raise 'WHAAAT'

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
                        draw.line(paths_img,(255,0,0),(x1,y1),(x2,y2),3)

                for i in g_board.coords:
                    if i[2] == g_board.line1[0]:
                        if g_board.line1[1] in (1,2): x_plus,y_plus = 75,44
                        if g_board.line1[1] in (3,4): x_plus,y_plus = 0,88
                        if g_board.line1[1] in (5,6): x_plus,y_plus = -75,44
                        if g_board.line1[1] in (7,8): x_plus,y_plus = -75,-44
                        if g_board.line1[1] in (9,10): x_plus,y_plus = 0,-88
                        if g_board.line1[1] in (11,12): x_plus,y_plus = 75,-44
                        x = i[0]+x_plus
                        y = i[1]+y_plus

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

    p_msg = p_font.render('Points: '+str(points1),1,(0,0,0))
    screen.blit(p_msg,(10,10))
    draw_text(700,30,p_font,'New Game',(0,0,0))
    if 640 < mx < 760 and 15 < my < 45:
        draw.rect(screen,(0,0,0),(640,15,120,30),2)

    g_board.draw_path(screen)

    if status == -1:    # Game ending condition
        screen.blit(t1_font.render('Game Over',0,(0,0,0)),(150,250))
        screen.blit(t1_font.render('Game Over',1,(255,255,255)),(150,250))
        if points1 == 1:
            screen.blit(t2_font.render('You are a disgrace.',1,(255,255,255)),(100,310))
        else:
            screen.blit(t2_font.render('You scored '+str(points1)+' points.',1,(255,255,255)),(70,310))

    display.flip()
    time.wait(30)

quit()


