## TODO LIST:
# let user change background color of test text

import pygame, sys, time
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(300,1)

RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (70, 70, 70)
DISPLAY_SIZE = (1024, 768)
SELECTOR_SIZE = (500, DISPLAY_SIZE[1] - 40)

screen = pygame.display.set_mode(DISPLAY_SIZE)
basefont = pygame.font.Font(None, 24)
lorem = file("lorem_ipsum.txt")
filetext = []
for line in lorem:
    filetext.append(line.strip())
lorem.close()

class Data(object):
    def __init__(self):
        self.name = None
        self.size = 25
        self.font = pygame.font.Font(self.name, self.size)
        self.index = 0
        self.fontlist = pygame.font.get_fonts()
        self.select_font = False
        self.highlight = 0
        self.antialias = True
        self.sel_bump = 0
        self.color = [255, 255, 255]
        self.sel_color = 0

d = Data()

def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and d.select_font == True:
                for i in range(len(d.fontlist)):
                    if d.fontlist[i] == d.overfont:
                        d.index = i
            if event.button == 4 and d.select_font: # mwheel up
                d.highlight -= 1
            if event.button == 5 and d.select_font: # mwheel down
                d.highlight += 1
        if event.type == KEYDOWN:
            if event.key == K_r:
                d.sel_color = 0
            if event.key == K_g:
                d.sel_color = 1
            if event.key == K_b:
                d.sel_color = 2
            if event.key == K_PAGEDOWN and d.select_font:
                d.highlight += 20
            if event.key == K_PAGEUP and d.select_font:
                d.highlight -= 20
            if event.key == K_DOWN:
                if d.select_font:
                    d.highlight += 1
                else:
                    if d.color[d.sel_color] > 0:
                        d.color[d.sel_color] -= 1
            if event.key == K_UP:
                if d.select_font:
                    d.highlight -= 1
                else:
                    if d.color[d.sel_color] < 255:
                        d.color[d.sel_color] += 1
            if event.key == K_ESCAPE and not d.select_font:
                pygame.quit()
            if event.key == K_ESCAPE and d.select_font:
                d.select_font = False
            if event.key == K_MINUS:
                d.size -= 1
            if event.key == K_EQUALS:
                d.size += 1
            if event.key == K_F1:
                if d.index > 0:
                    d.index -= 1
            if event.key == K_F2:
                if d.index < len(d.fontlist):
                    d.index += 1
            if event.key == K_F3:
                if d.select_font == False:
                    d.select_font = True
                    d.sel_buff = 0
                elif d.select_font == True: d.select_font = False
            if event.key == K_F4:
                if d.antialias == False: d.antialias = True
                elif d.antialias == True: d.antialias = False

def draw_topdata():
    if d.sel_color == 0:
        color = "Red"
        printcolor = RED
    if d.sel_color == 1:
        color = "Green"
        printcolor = GREEN
    if d.sel_color == 2:
        color = "Blue"
        printcolor = BLUE
    helpstr = "+/-: font size    F1/F2: prev/next font    F3: font selector    F4: antialias"
    help2str = "    antialias: " + str(d.antialias)
    help3str = "(r)ed,(g)reen,(b)lue: choose color    up/down: change selected color value"
    help4str = "selected color:" + color + "    RGB values:" + str(d.color)
    text = basefont.render("Font: " + str(d.name) + ", " + str(d.size) + help2str, 1, WHITE)
    text2 = basefont.render(helpstr, 1, WHITE)
    text3 = basefont.render(help3str, 1, WHITE)
    text4 = basefont.render(help4str, 1, WHITE, printcolor)
    sr = screen.get_rect()
    dest = text.get_rect()
    dest.centerx = sr.centerx
    dest.top += 10
    screen.blit(text, dest)
    dest = text2.get_rect()
    dest.centerx = sr.centerx
    dest.top += 30
    screen.blit(text2, dest)
    dest = text3.get_rect()
    dest.centerx = sr.centerx
    dest.top += 50
    screen.blit(text3, dest)
    dest = text4.get_rect()
    dest.centerx = sr.centerx
    dest.top += 70
    screen.blit(text4, dest)
    
def draw_test():
        font = d.fontlist[d.index]
        d.name = font
        font = pygame.font.match_font(font)
        d.font = pygame.font.Font(font, d.size)
        surf = pygame.surface.Surface(DISPLAY_SIZE)
        buffer = (((len(filetext)+1) * d.size) / 2) * -1
        for line in filetext:
            text = d.font.render(line, d.antialias, d.color)
            dest = text.get_rect()
            dest.center = surf.get_rect().center
            dest.top += buffer
            buffer += d.size + 4
            surf.blit(text, dest)
        dest = surf.get_rect()
        dest.center = screen.get_rect().center
        screen.blit(surf, dest)
        
def draw_font_selector_bg():
    surf = pygame.surface.Surface(SELECTOR_SIZE)
    surf.fill(GREY)
    screen.blit(surf, (0,0))
        
def draw_font_selector():
    amount = 20
    draw_font_selector_bg()
    max_index = len(d.fontlist) - 1
    if d.highlight < 0: d.highlight = 0
    if d.highlight >= max_index: d.highlight = max_index - 1
    visible_indices = []
    for num in range(amount):
        sum = d.sel_bump + num
        if sum < max_index:
            visible_indices.append(sum)
    #d.VI = visible_indices
    if d.highlight < visible_indices[0]:
        diff = abs(d.highlight - visible_indices[0])
        d.sel_bump -= diff
    if d.highlight > visible_indices[-1]:
        if d.sel_bump <= (max_index - amount):
            diff = abs(d.highlight - visible_indices[-1])
            d.sel_bump += diff
    d.index = d.highlight
    
    left, top = 20, 20
    for i in visible_indices:
        font = pygame.font.Font(d.matched_fontlist[i], 20)
        if i == d.highlight:
            text = font.render(str(i) + " - " + d.fontlist[i], d.antialias, WHITE, BLUE)
        else:
            text = font.render(str(i) + " - " + d.fontlist[i], d.antialias, WHITE)
        dest = (left, top)
        top += 35
        screen.blit(text, dest)


def draw():
    screen.fill(BLACK)
    draw_test()
    draw_topdata()
    if d.select_font:
        draw_font_selector()
    pygame.display.update()

def main():
    while True:
        draw()
        events()
        
def build_font_list():
    t = []
    for font in d.fontlist:
        font = pygame.font.match_font(font)
        t.append(font)
    d.matched_fontlist = t
    
build_font_list()        
main()
        