############################################
######Part of a project by Owen Cummings####
############################################
#####Utility functions to project.py########
############################################

import pygame

def fade(): #Fades between 2 scenes while playing == true. Can adjust times if i put them as function inputs but eh
    tfade = 1
    fadetimer = 0
    while fadetimer <= tfade: #fadeout
        i = 0
        while i < 12:
            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i)*S), (384*S, int((fadetimer/tfade)*18*S))))
            #print(i)
            i = i + 1
        fadetimer = fadetimer + elapsed/1000
        pygame.display.update()
        elapsed = fpsClock.tick(FPS)
    fadetimer = 0
    tfade = 1
    while fadetimer <= tfade:
        fadetimer = fadetimer + elapsed/1000
        elapsed = fpsClock.tick(FPS)
    fadetimer = 0
    tfade = 1


    mainDisplay[0] = S*(192)
    mainDisplay[1] = S*(108)
    floorDisplay[0]= S*(-mainCoord[0] + (192)) #-12 for centering    for placement, copied from original code
    floorDisplay[1]= S*(-mainCoord[1] + (108)) #-12                  !!!!!!!Must set new coordinates and flooredge before hand!!!!!!!!!

    if mainCoord[0] < floorEdge[0] + (192):      #S*(192-12):
        mainDisplay[0] = S*-(floorEdge[0] - mainCoord[0])
        floorDisplay[0] = S* -floorEdge[0]
    elif mainCoord[0] > floorEdge[1] - (192):        #times S
        mainDisplay[0] = S*(384 + (mainCoord[0] - floorEdge[1]))
        floorDisplay[0] = S*(-floorEdge[1] + 384)
    if mainCoord[1] < floorEdge[2] + (108):
        mainDisplay[1] = S* -(floorEdge[2] - mainCoord[1])
        floorDisplay[1] = S*(-floorEdge[2])
    elif mainCoord[1] > floorEdge[3] - (108):
        mainDisplay[1] = S*(216 + (mainCoord[1] - floorEdge[3]))
        floorDisplay[1] = S*(-floorEdge[3]  + 216)
    while fadetimer <= tfade: #1-way fade

        display.blit(floor, (floorDisplay[0],floorDisplay[1])) #kind of want to do the hair animation but that can be done later...
        display.blit(mainr1, (mainDisplay[0], mainDisplay[1]))
        i = 0
        while i<12:
            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i)*S) , (384*S, 27*S - int((fadetimer/tfade)*27*S))))
            i = i + 1
        fadetimer = fadetimer + elapsed/1000
        pygame.display.update()
        elapsed = fpsClock.tick(FPS)
