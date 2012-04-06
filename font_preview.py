import pygame, sys
from pygame.locals import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (70, 70, 70)
DISPLAY_SIZE = (1024, 768)
SELECTOR_SIZE = (300, DISPLAY_SIZE[1] - 40)

screen = pygame.display.set_mode(DISPLAY_SIZE)
basefont = pygame.font.Font(None, 24)
lorem = file("lorem_ipsum/lorem_ipsum.txt")
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
        self.sel_buff = 0
        self.rects = []
        self.overfont = None

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
        if event.type == KEYDOWN:
            if event.key == K_PAGEDOWN:
                d.sel_buff -= 700
            if event.key == K_PAGEUP:
                d.sel_buff += 700
            if event.key == K_ESCAPE:
                pygame.quit()
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
                if d.select_font == False: d.select_font = True
                elif d.select_font == True: d.select_font = False

def draw_topdata():
    helpstr = "+/-: font size  F1/F2: prev/next font   F3: font selector"
    mousestr = "  mpos: " + str(pygame.mouse.get_pos()) + "  over font: " + str(d.overfont)
    text = basefont.render("Font: " + str(d.name) + ", " + str(d.size), 1, WHITE)
    tr = text.get_rect()
    sr = screen.get_rect()
    tr.centerx = sr.centerx
    tr.top += 10
    screen.blit(text, tr)
    text2 = basefont.render(helpstr + mousestr, 1, WHITE)
    dest = text2.get_rect()
    dest.centerx = sr.centerx
    dest.top += 30
    screen.blit(text2, dest)
    
def draw_test():
        font = d.fontlist[d.index]
        d.name = font
        font = pygame.font.match_font(font)
        d.font = pygame.font.Font(font, d.size)
        surf = pygame.surface.Surface(DISPLAY_SIZE)
        buffer = (((len(filetext)+1) * d.size) / 2) * -1
        for line in filetext:
            text = d.font.render(line, 1, WHITE)
            dest = text.get_rect()
            dest.center = surf.get_rect().center
            dest.top += buffer
            buffer += d.size
            surf.blit(text, dest)
        dest = surf.get_rect()
        dest.center = screen.get_rect().center
        screen.blit(surf, dest)
        
def draw_font_selector():
    SELECT_SIZE = 18
    screenblit_buff = 20
    surf = pygame.surface.Surface(SELECTOR_SIZE)
    surf.fill(GREY)
    d.rects = []
    left, top = 10, 10 + d.sel_buff
    for item in d.fontlist:
        match = pygame.font.match_font(item)
        font = pygame.font.Font(match, SELECT_SIZE)
        text = font.render(item, 1, WHITE)
        dest = text.get_rect()
        dest.left = left
        dest.top = top
        surf.blit(text, dest)
        dest.top += screenblit_buff
        dest.left += screenblit_buff
        d.rects.append((dest, item))
        top += SELECT_SIZE + 4
    screen.blit(surf,(screenblit_buff, screenblit_buff))
    
    
            

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
        for pair in d.rects:
            rect = pair[0]
            if rect.collidepoint(pygame.mouse.get_pos()):
                d.overfont = pair[1]
        events()
        
main()
        