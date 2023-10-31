import pygame
pygame.init()

#Screen
size = width, height = 720, 500 #Make sure background image is same size
screen = pygame.display.set_mode(size)

done = False
#Colour
Black = (0,0,0)
White = (255, 255, 255)
#Fonts
screen.fill(Black)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        Font = pygame.font.SysFont("Trebuchet MS", 25)
        DayFont = Font.render("Time elapsed: ",1, White)
        DayFontR=DayFont.get_rect()
        DayFontR.center=(185,20)
        screen.blit(DayFont, DayFontR)



pygame.quit()