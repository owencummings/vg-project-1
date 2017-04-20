#A game by Owen Cummings
#Lets go homies
import pygame, sys
import random
import math
from pygame.locals import *
import util
import operator

###screensize for windows###
import ctypes
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

S = min(int(height/216), int(width/384))
resolution = (384*S, 216*S)
FPS = 30
##########
############################
#########Globals############
############################
walkSpeed = 4
mainHealth = 10
floorDisplay = [200,200]
mainDisplay = [(384/2 - 12)*S, (216/2 - 12)*S]
floorEdge = [0,0,0,0]

#room1box = ([31,255,158,307],[128,158,58,170])
#room1edge = [20, 275 ,0, 320]
spriteTimer = 0
floorMark = -1
start = True
start2 = False
playing = False
moving = False
playNote1 = False
noteCounter = 0.0
pressed_up = False
pressed_down = False
pressed_right = False
pressed_left = False
mainCoord = [0,0]
mainDisplay = [0,0]
menu = 0  #are we on the menu
menuPlace = 0 #what is our place in the menu
elapsed = 0.
OLT = 0.0
room1box = 0
enemyList = []
attackList = []
#global dmgTaken
dmgTaken = 0
DMGCOLOR = (0,0,0) #(255,0,82)
dmgAnim = False
dmgCD = 1



class attack:
    def __init__(self, typification, time, timer, source, destination):
        self.type = typification
        self.time = time
        self.timer = timer
        self.source = source
        self.destination = destination
    def changeType(self, typification):
        self.type = typification
    def changeTime(self, time):
        self.time = time
    def changeTimer(self, timer):
        self.timer = timer
    def addTimer(self, add):
        self.timer = self.timer + add
    def changeSource(self, source):
        self.source = source
    def changeDestination(self, destination):
        self.destination = destination

    def processAttack(self):
        if self.type == 1.1: #self.timer should be 1
            if self.time <= self.timer:
                if  self.destination[0] < mainCoord[0] < self.destination[0] + 20 and self.destination[1] < mainCoord[1] < self.destination[1] + 20:
                    global dmgTaken
                    global attackList
                    dmgTaken = dmgTaken +  1
                attackList.remove(self)

            else:
                global elapsed
                self.addTimer(elapsed/1000)


class enemy:
    def __init__(self, typification, coordinates, health, cooldown):
        self.type = typification
        self.coord = coordinates
        self.hp = health
        self.cd = cooldown
        self.timer = 2 #so it starts as moving
    def processEnemy(self):
        if self.type == 1: #drone thing
            if self.timer > 1: #cooldown between shots baby
                if 0 < mainCoord[0] - self.coord[0] < 75: ##moveleft
                    move = 1
                    i = 2
                    for box in floorBox:
                        if box[2] < self.coord[1] + 35 and box[3] > self.coord[1] + 25:
                            i = self.coord[0] - box[1]
                            if i < move and i >= 0:
                                move = i
                    self.coord = (self.coord[0] - move, self.coord[1])

                elif 0 > mainCoord[0] - self.coord[0] > -75: ##moveright
                    move = 1
                    i = 2
                    for box in floorBox:
                        if box[2] < self.coord[1] + 35 and box[3] > self.coord[1] + 25:
                            i = box[0] - (self.coord[0] + (18))
                            if i < move and i >= 0:
                                move = i
                    self.coord = (self.coord[0] + move, self.coord[1])


                if 0 < mainCoord[1] - self.coord[1] < 75: ##move up
                    move = 1
                    i = 2
                    for box in floorBox:
                        if box[0] < self.coord[0] + 18 and box[1] > self.coord[0]:
                            i = (self.coord[1] + 25) - box[3]
                            if i < move and i >= 0:
                                move = i
                    self.coord = (self.coord[0], self.coord[1] - move)


                elif 0 > mainCoord[1] - self.coord[1] > -75: ##movedown
                    move = 1
                    i = 2
                    for box in floorBox:
                        if box[0] < self.coord[0] + 18 and box[1] > self.coord[0]:
                            i = box[2] - (self.coord[1] + 35)
                            if i < move and i >= 0:
                                move = i
                    self.coord = (self.coord[0], self.coord[1] + move)

            if self.timer >= self.cd and math.fabs(mainCoord[0] - self.coord[0]) + math.fabs(mainCoord[1] - self.coord[1]) < 100:
                sampleAttack.changeType(1.1)
                sampleAttack.changeTime(1)
                sampleAttack.changeTimer(0)
                sampleAttack.changeSource((0,0))
                sampleAttack.changeDestination((mainCoord[0], mainCoord[1]))
                a1 = sampleAttack
                attackList.append(a1)
                self.timer = 0


            self.timer = self.timer + elapsed/1000


########Class Specific Globals#######
sampleAttack = attack(0,0,0,(0,0),(0,0))
####################################





#moved function to util.py, should work still?
def fade():
    global elapsed
    '''
    time1 = .2
    timer = 0
    while timer <= time1:
            timer = timer + elapsed/1000
            elapsed = fpsClock.tick(FPS)
    '''
    #cant figure out why the timing for this fade is so bizzare...
    timer = 0
    time1 = 1
    while timer <= time1: #fadeout
        i = 0
        while i < 12:
            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i+1)*S), (384*S, -int((timer/time1)*18*S))))
            i = i + 1
        timer = timer + elapsed/1000
        pygame.display.update()
        elapsed = fpsClock.tick(FPS)
    display.fill((0,0,0))
    pygame.display.update()
    elapsed = fpsClock.tick(FPS)
    timer = 0
    time1 = 1
    while timer <= time1:
        timer = timer + elapsed/1000
        elapsed = fpsClock.tick(FPS)
    timer = 0
    time1 = 1
    mainDisplay[0] = S*(192 - 15)
    mainDisplay[1] = S*(108 - 18)
    floorDisplay[0]= S*(-mainCoord[0] + (192 -15)) #-12 for centering
    floorDisplay[1]= S*(-mainCoord[1] + (108 - 18)) #-12

    if mainCoord[0] < floorEdge[0] + (192 - 15):      #S*(192-12):
        mainDisplay[0] = S*-(floorEdge[0] - mainCoord[0])
        floorDisplay[0] = S* -floorEdge[0]
    elif mainCoord[0] > floorEdge[1] - (192 + 15):        #times S
        mainDisplay[0] = S*(384 + (mainCoord[0] - floorEdge[1]))
        floorDisplay[0] = S*(-floorEdge[1] + 384)
    if mainCoord[1] < floorEdge[2] + (108 - 18):
        mainDisplay[1] = S* -(floorEdge[2] - mainCoord[1])
        floorDisplay[1] = S*(-floorEdge[2])
    elif mainCoord[1] > floorEdge[3] - (108 + 18):
        mainDisplay[1] = S*(216 + (mainCoord[1] - floorEdge[3]))
        floorDisplay[1] = S*(-floorEdge[3]  + 216)

    while timer <= time1: #1-way fade

        display.blit(floor, (floorDisplay[0],floorDisplay[1]))
        display.blit(mainImage, (mainDisplay[0], mainDisplay[1]))
        i = 0
        while i<12:
            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i)*S) , (384*S, 18*S - int((timer/time1)*18*S))))
            i = i + 1
        timer = timer + elapsed/1000
        pygame.display.update()
        elapsed = fpsClock.tick(FPS)



def base(thing): #thing to help the quicksorting of the objects on the surface
    if thing == 'self' :
        return mainCoord[1] + 35
    global floorMark
    if floorMark == 2:
        if thing == 1: #top wall
            return 420
        if thing == 2: #bottom wall
            return 612
    if floorMark == 3:
        if thing == 1:
            return 233
            '''
    elif type(thing) == <class '__main__.attack'>:
        print('attack!!!')
        '''
    if thing.type == 1.1:
        return 0 #this attack is on the floor and thus beneath everything
        '''
    elif type(thing) == <class '__main__.enemy'>:
        print('enemy???')
        '''
    if thing.type == 1:
        return thing.coord[1] + 35



##########
#pygame setup


pygame.init()
 #trying to keep movement to be FPS-adjustable
fpsClock = pygame.time.Clock()
display = pygame.display.set_mode(resolution,pygame.FULLSCREEN) #Create fullscreen display with integer multiple of worked resolution
pygame.mixer.init()
pygame.mouse.set_visible(False)
############################

display.fill((0,0,0))

while True:
    for event in pygame.event.get():    #reading user inputs
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == K_DOWN:
                pressed_down = False
            if event.key == K_UP:
                pressed_up = False
            if event.key == K_RIGHT:
                pressed_right = False
            if event.key == K_LEFT:
                pressed_left = False



        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.key == K_DOWN:
                if menu == True: #might want a system that tracks menuPlace of bar and destination, so that destination can change while in path
                    if menuPlace == 1:
                        timer = 0
                        menusound.play()
                        while timer <= .2:
                            display.fill((0,0,0))
                            pygame.draw.rect(display,(90,65,246), Rect((0, int(S*(46 + timer/(.2)*19))),( 384*S, 17*S)))
                            display.blit(menuStart, (24*S, S*48))
                            display.blit(menuControls, (24*S, 67*S))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        menuPlace = 2


                pressed_down = True

            elif event.key == K_UP:
                if menu == True:
                    if menuPlace == 2:
                        menusound.play()
                        timer = 0
                        while timer <= .2:
                            display.fill((0,0,0))
                            pygame.draw.rect(display,(90,65,246), Rect((0, int(S*(65 - timer/(.2)*19))),( 384*S, 17*S)))
                            display.blit(menuStart, (24*S, S*48))
                            display.blit(menuControls, (24*S, 67*S))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        menuPlace = 1

                pressed_up = True


            elif event.key == K_RIGHT:
                if menu == True: #probably add this on space as well
                    if menuPlace == 2:
                        timer = 0
                        menuCtrlTxt = pygame.image.load('Assets/Images/scene/menuCtrlTxt.png')
                        menuCtrlTxt = pygame.transform.scale(menuCtrlTxt, (324*S, 55*S))
                        menusound.play()
                        while timer <= 0.333:
                            display.fill((0,0,0))
                            pygame.draw.rect(display, (90, 65, 246), Rect((0, 65*S), (384*S, 17*S)))
                            display.blit(menuStart, (int(S*((24) - 384*timer/(.333))),S*48))
                            display.blit(menuControls, (int(S*((24) - 384*timer/(.333))) , 67*S))
                            display.blit(menuCtrlTxt, (int(S*((384 + 24) - 384*timer/(.333))) , 67*S))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        menuPlace = 3


                pressed_right = True

            elif event.key == K_LEFT:
                if menu == True: #prabably add this on space as well
                    if menuPlace == 3:
                        menusound.play()
                        timer = 0
                        while timer <= .333:
                            display.fill((0,0,0))
                            pygame.draw.rect(display, (90, 65, 246), Rect((0, 65*S), (384*S, 17*S)))
                            display.blit(menuStart, (int(S*((24 - 384) + 384*timer/(.333))),S*48))
                            display.blit(menuControls, (int(S*((24-384) + 384*timer/(.333))) , 67*S))
                            display.blit(menuCtrlTxt, (int(S*((24) + 384*timer/(.333))) , 67*S))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        display.fill((0,0,0))
                        pygame.draw.rect(display, (90, 65, 246), Rect((0, 65*S), (384*S, 17*S)))
                        display.blit(menuStart, (S*(24),S*48))
                        display.blit(menuControls, ((S*24) , 67*S))
                        menuPlace = 2

                pressed_left = True


            elif event.key == K_SPACE:
                if start == True:
                    start = False
                    whitenoise = pygame.mixer.Sound('Assets/Sounds/songs/whitenoise.wav')
                    whitenoise.play(loops = -1)
                    title = pygame.image.load("Assets/Images/scene/title.jpg")   #note title2 and 3 are swappe in Assets
                    title = pygame.transform.scale(title, (285*S, 216*S))

                    timer = 0
                    #time1 = FPS
                    while timer <= 1: #1-way fade

                        display.blit(title, (0,0)) #kind of want to do the hair animation but that can be done later...
                        i = 0
                        while i<12:
                            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i)*S) , (384*S, 18*S - int((timer/1)*18*S))))
                            i = i + 1
                        timer = timer + elapsed/1000
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                    display.blit(title, (0,0))
                    pygame.display.update()
                    elapsed = fpsClock.tick(FPS)
                    timer = 0
                    while timer <= .25:
                        timer = timer + elapsed
                        elapsed = fpsClock.tick(FPS)

                    name = pygame.image.load("Assets/Images/scene/byowen.png")
                    name = pygame.transform.scale(name, (100*S,13*S))
                    timer = 0


                    while timer <= 2.5:    #namedrop, timing could be adjusted but i dig it
                        pygame.draw.rect(display, (0,0,0), Rect((285*S,0),(99*S, 216*S)))
                        if timer <= .25:
                            display.blit(name, (289*S, int(S*((75 + 13)*(timer/(.25))-13))))
                        elif timer <= 1.125:
                            display.blit(name, (289*S, int(S*((66)*((timer-(.25))/(2))+ 75))))
                        elif timer <= 2.5:
                            display.blit(name, (289*S, int(S*((75)*((timer-(1.125))/(.25))+ 141))))
                        timer = timer + elapsed/1000
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                    name = 0
                    start2 = True

                elif start2 == True:
                    start2 = False
                    timer = 0
                    #time1 = FPS
                    while timer <= 1: #fadeout
                        i = 0
                        while i < 12:
                            pygame.draw.rect(display, (0,0,0), Rect((0, 18*(i)*S), (384*S, int((timer/1)*18*S))))
                            i = i + 1
                        timer = timer + elapsed/1000
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)

                    timer = 0
                    while timer <= .25:
                        timer = timer + elapsed
                        elapsed = fpsClock.tick(FPS)
                    timer = 0
                    elapsed = 0
                    menuStart = pygame.image.load("Assets/Images/scene/menuStart.png")
                    menuStart = pygame.transform.scale(menuStart, (61*S, 13*S))
                    menuControls = pygame.image.load("Assets/Images/scene/menuControls.png")
                    menuControls = pygame.transform.scale(menuControls, (101*S, 13*S))
                    #menuCtrlTxt = pygame.image.load("Assets/Images/scene/menuCtrlTxt.png")
                    #menuCtrlTxt = pygame.transform.scale(menuCtrlTxt, (384*S, 216*S)) #change dimenions
                    while timer <= .5:
                        display.fill((0,0,0))
                        display.blit(menuControls, (24*S, S*int(80*(timer/(.5))  - 13)))#pathhere
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                        timer = timer + elapsed/1000
                    timer = 0
                    while timer <= .5:
                        display.fill((0,0,0))
                        display.blit(menuControls, (24*S, 67*S))
                        display.blit(menuStart, (24*S, S*int(61*(timer/(.5)) - 13))) #pathhere
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                        timer = timer + elapsed/1000
                    timer = 0
                    elapsed = 0
                    while timer <= .166:
                        pygame.draw.rect(display, (90,65,246), Rect((0, 52*S), (timer/(.166)*384*S,3*S)))
                        display.blit(menuStart, (24*S, S*48))
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                        timer = timer + elapsed/1000
                    timer = 0
                    while timer <= .333:
                        pygame.draw.rect(display, (90,65,246), Rect((0, -8 * S * timer/(.333) + 54*S), (384*S, int(3*S + 14*S*(timer/(.333))))))
                        display.blit(menuStart, (24*S, 48*S))
                        pygame.display.update()
                        elapsed = fpsClock.tick(FPS)
                        timer = timer + elapsed/1000
                    menu = True
                    menuPlace = 1
                    menusound = pygame.mixer.Sound('Assets/Sounds/effects/menumove.wav')
                    letsplay = pygame.mixer.Sound('Assets/Sounds/effects/playsound.wav')
                    #clear the queue?

                elif menu == True:
                    if menuPlace == 1:
                        menu = False
                        menuPlace = 0
                        timer = 0
                        whitenoise.stop()
                        menusound.stop()
                        letsplay.play()
                        while timer <= .666:
                            display.fill((0,0,0))
                            if timer <= .5:
                                pygame.draw.rect(display, (90, 65, 246), Rect((0, int(((timer/(.5)*-10) + 46)*S)), (384*S, int((20 * timer/(.5) +17)*S))))
                                display.blit(menuStart,(24*S, 48*S))
                                display.blit(menuControls, (24*S, 67*S))
                            elif timer <= 2*FPS/3:
                                pygame.draw.rect(display, (90, 65, 246), Rect((0, int((((timer-(.5))/(.166)*17) + 36)*S)), (384*S, int((-34 * (timer-(.5))/(.166) +37)*S))))
                                display.blit(menuStart,(24*S, (48 - 100*(timer - .5)/(.166))*S))
                                display.blit(menuControls, (24*S, (67 - 100*(timer - .5)/(.166))*S))
                            #if timer <= 5*FPS/6:
                                #pygame.draw.rect(display, (90, 65, 246), Rect((0, 65*S), (384*S, 17*S)))
                            timer = timer + elapsed/1000
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        while timer <= 3:
                            display.fill((0,0,0))
                            pygame.draw.rect(display, (90,65,246), Rect((0,int((53 + 77*(timer/(3)))*S)), (384*S, 3*S)))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        menuStart = 0
                        menuControls = 0
                        pygame.event.pump()
                        timer = 0
                        while timer <= 3:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        pygame.event.pump()
                        eye1 = pygame.image.load('Assets/Images/scene/eye1.jpg')
                        eye1 = pygame.transform.scale(eye1 , (384*S, 216*S))
                        heartbeat1 = pygame.image.load('Assets/Images/scene/heartbeat1.jpg')
                        heartbeat1 = pygame.transform.scale(heartbeat1, (151*S, 216*S))
                        heartbeat2 = pygame.image.load('Assets/Images/scene/heartbeat1a.jpg')
                        heartbeat2 = pygame.transform.scale(heartbeat2, (128*S, 216*S))
                        heartbeat3 = pygame.image.load('Assets/Images/scene/heartbeat2.jpg')
                        heartbeat3 = pygame.transform.scale(heartbeat3, (154*S, 216*S))
                        heartbeat4 = pygame.image.load('ASsets/Images/scene/heartbeat3.jpg')
                        heartbeat4 = pygame.transform.scale(heartbeat4, (229*S, 216*S))

                        timer = 0
                        #time1 = 3*FPS
                        while timer <= 1.5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= 1.5:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        while timer <= 1.5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= 1.5:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        while timer <= 1.5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= 1.5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= .5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        display.blit(eye1, (0,0))
                        pygame.display.update()
                        timer = 0
                        while timer <= 2.5:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        display.fill((0,0,0))
                        pygame.draw.rect(display, (90,65,246), Rect((0,130*S), (384*S, 3*S)))
                        while timer <= 1.5:
                            display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= 1.5:
                            display.blit(heartbeat2, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        timer = 0
                        while timer <= 2.5:
                            if timer <= .5:
                                display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                            elif timer <= 2:
                                display.blit(heartbeat1, (int(S*(384 - (2*384*(timer/1.5)))), 0))
                                display.blit(heartbeat1, (int(S*(384 - (2*384*(timer-.5)/1.5))), 0))
                            else:
                                display.blit(heartbeat3, (int(S*(384 - (2*384*(timer-2)/1.5))), 0))

                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        display.blit(eye1, (0,0))
                        pygame.display.update()
                        timer = 0
                        while timer <= 1.75:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        display.fill((0,0,0))
                        pygame.draw.rect(display, (90,65,246), Rect((0,130*S), (384*S, 3*S)))
                        while timer <= 2:
                            display.blit(heartbeat2, (int(S*(384 - (2*384*(timer+.5)/1.5))), 0))
                            display.blit(heartbeat3, (int(S*(384 - (2*384*(timer-.5)/1.5))), 0))
                            display.blit(heartbeat3, (int(S*(384 - (2*384*(timer-1)/1.5))), 0))
                            display.blit(heartbeat3, (int(S*(384 - (2*384*(timer-1.5)/1.5))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        display.blit(eye1, (0,0))
                        pygame.display.update()
                        timer = 0
                        while timer <= .75:
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        timer = 0
                        display.fill((0,0,0))
                        pygame.draw.rect(display, (90,65,246), Rect((0,130*S), (384*S, 3*S)))
                        while timer <= 1:
                            display.blit(heartbeat4, (int(S*(384 - (2*384*(timer+.75)/1.5))), 0))
                            display.blit(heartbeat4, (int(S*(384 - (2*384*(timer+.25)/1.5))), 0))
                            display.blit(heartbeat4, (int(S*(384 - (2*384*(timer-.25)/1.5))), 0))
                            display.blit(heartbeat4, (int(S*(384 - (2*384*(timer-.75)/1.5))), 0))
                            pygame.display.update()
                            elapsed = fpsClock.tick(FPS)
                            timer = timer + elapsed/1000
                        display.blit(eye1, (0,0))
                        pygame.display.update()
                        timer = 0
                        while timer <= .25:     ####this should be quick cut to eye already open!!!!
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        display.fill((0,0,0))
                        pygame.display.update()
                        timer = 0
                        while timer <= .75:     ####this should be quick cut to eye already open!!!!
                            timer = timer + elapsed/1000
                            elapsed = fpsClock.tick(FPS)
                        playing = True
                        moving = True
                        heartbeat1 = 0
                        heartbeat1a = 0
                        heartbeat2 = 0
                        heartbeat3 = 0
                        heartbeat4 = 0
                        mainR1 = pygame.image.load('Assets/Images/sprites/mainright1.png')
                        mainR1 = pygame.transform.scale(mainR1, (29*S,35*S))
                        mainR2 = pygame.image.load('Assets/Images/sprites/mainright2.png')
                        mainR2 = pygame.transform.scale(mainR2, (29*S, 35*S))
                        mainR3 = pygame.image.load('Assets/Images/sprites/mainright3.png')
                        mainR3 = pygame.transform.scale(mainR3, (29*S, 35*S))
                        mainR4 = pygame.image.load('Assets/Images/sprites/mainright4.png')
                        mainR4 = pygame.transform.scale(mainR4, (29*S, 35*S))
                        mainL1 = pygame.image.load('Assets/Images/sprites/mainleft1.png')
                        mainL1 = pygame.transform.scale(mainL1, (29*S,35*S))
                        mainL2 = pygame.image.load('Assets/Images/sprites/mainleft2.png')
                        mainL2 = pygame.transform.scale(mainL2, (29*S, 35*S))
                        mainL3 = pygame.image.load('Assets/Images/sprites/mainleft3.png')
                        mainL3 = pygame.transform.scale(mainL3, (29*S, 35*S))
                        mainL4 = pygame.image.load('Assets/Images/sprites/mainleft4.png')
                        mainL4 = pygame.transform.scale(mainL4, (29*S, 35*S))
                        '''
                        mainU1 = pygame.image.load('Assets/Images/sprites/mainup1.png')
                        mainU1 = pygame.transform.scale(mainU1, (29*S, 35*S))
                        mainD1 = pygame.image.load('Assets/Images/sprites/maindown1.png')
                        mainD1 = pygame.transform.scale(mainD1, (29*S, 35*S))
                        '''
                        mainImage = mainR1
                        room1 = pygame.image.load('Assets/Images/scene/room1.png')
                        room1 = pygame.transform.scale(room1, (400*S,400*S))

                        display.fill((57,29,225))
                        floor = room1
                        mainSong1 = pygame.mixer.Sound('Assets/Sounds/songs/main1.wav')
                        mainSong1.play(-1)
                        #room1box = ([100,324,192,341],[196,228,85,200]) #change this box or make boxes use interior boxes
                        room1box = ([50,75, 75,375], [50, 350, 342,352], [300,325,75,375], [50,163, 25,191], [211,330,25,191], [150,230,60,85])
                        room1edge = [-100, 600, -100, 500]#[0, 425 ,30, 360]
                        floorBox = room1box
                        floorEdge = room1edge
                        mainCoord = [200, 200]
                        spriteTimer = 0
                        floorMark = 1

                if playing and moving:
                    if floorMark == 2:
                        if 410 < mainCoord[0] <440 and 570 < mainCoord[1] < 610:
                            note1 = pygame.image.load('Assets/Images/scene/note1.png')
                            note1 = pygame.transform.scale(note1, (384*S, 622*S))
                            moving = False
                            playNote1 = True

    if playing == True:

        if floorMark == 1:
            if mainCoord[1] < 95:
                floor = pygame.image.load("Assets/Images/scene/room2.png")
                floor = pygame.transform.scale(floor, (850*S, 850*S))
                floorBox = ([235,255, 220,720], [240,399,710, 825], [380, 455, 822, 840], [447,591,710,822], [590, 610, 220,720], [447, 600, 25,230], [380,460,40,60],
                            [235,399,30,230],[328,520,390,420],[328,520,583,613])
                floorEdge = [100, 800, 0,830] #230, 611
                mainCoord = [400,650]
                floorMark = 2
                sprite1 = pygame.image.load('Assets/Images/sprites/minion1.png')
                sprite1 = pygame.transform.scale(sprite1, (18*S, 22*S))
                r2o1 = pygame.image.load('Assets/Images/scene/r2o1.png')
                r2o1 = pygame.transform.scale(r2o1, (S*192, S*71))
                r2o2 = pygame.image.load('Assets/Images/scene/r2o2.png')
                r2o2 = pygame.transform.scale(r2o2, (S*192, S*71))
                e1 = enemy(1, (400,300), 50, 4)
                enemyList.append(e1)
                fade()
        if floorMark == 2:
            if mainCoord[1]  < 60 :
                floor = pygame.image.load("Assets/Images/scene/room3.png")
                floor = pygame.transform.scale(floor, ( 378*S, 1113*S))
                floorBox = ([50,172,950,1100], [160, 230, 1083, 1110], [220,350,950,1100], [260, 280, 40,970], [100, 133, 40,970], [100, 280, 80,100])
                floorEdge = [-100,500,100, 11110]
                mainCoord = [182, 1040]
                r3o1 = pygame.image.load('Assets/Images/scene/r3o1.png')
                r3o1 = pygame.transform.scale(r3o1, (S*127, S*190))
                floorMark = 3
                enemyList.clear()
                fade()




        if moving:
            if pressed_up and pressed_down:
                pass
            elif pressed_up:
                move = walkSpeed
                i = walkSpeed + 1
                for box in floorBox:
                    if box[0] < mainCoord[0] + 29 and box[1] > mainCoord[0]:
                        i = (mainCoord[1] + 20) - box[3]
                        if i < move and i >= 0:
                            move = i
                mainCoord[1] = mainCoord[1] - move

            elif pressed_down:
                move = walkSpeed
                i = walkSpeed + 1
                for box in floorBox:
                    if box[0] < mainCoord[0] + 29 and box[1] > mainCoord[0]:
                        i = box[2] - (mainCoord[1] + 35)
                        if i < move and i >= 0:
                            move = i
                mainCoord[1] = mainCoord[1] + move

            if pressed_right and pressed_left:
                pass
            elif pressed_right:
                move = walkSpeed
                i = walkSpeed + 1
                for box in floorBox:
                    if box[2] < mainCoord[1] + 35 and box[3] > mainCoord[1] + 20:
                        i = box[0] - (mainCoord[0] + (29))
                        if i < move and i >= 0:
                            move = i
                mainCoord[0] = mainCoord[0] + move

            elif pressed_left:
                move = walkSpeed
                i = walkSpeed + 1
                for box in floorBox:
                    if box[2] < mainCoord[1] + 35 and box[3] > mainCoord[1] + 20:
                        i = mainCoord[0] - box[1]
                        if i < move and i >= 0:
                            move = i
                mainCoord[0] = mainCoord[0] - move

            if pressed_right:
                if spriteTimer % .5 < .125:
                    mainImage = mainR1
                elif spriteTimer % .5 < .25:
                    mainImage = mainR2
                elif spriteTimer % .5 < .375:
                    mainImage = mainR3
                else:
                    mainImage = mainR4
            elif pressed_left:
                if spriteTimer % .5 < .125:
                    mainImage = mainL1
                elif spriteTimer % .5 < .25:
                    mainImage = mainL2
                elif spriteTimer % .5 < .375:
                    mainImage = mainL3
                else:
                    mainImage = mainL4
            '''
            elif pressed_up:
                mainImage = mainU1
            elif pressed_down:
                mainImage = mainD1
            '''


        mainDisplay[0] = S*(192 - 15)
        mainDisplay[1] = S*(108 - 18)
        floorDisplay[0]= S*(-mainCoord[0] + (192 -15)) #-12 for centering
        floorDisplay[1]= S*(-mainCoord[1] + (108 - 18)) #-12

        if mainCoord[0] < floorEdge[0] + (192 - 15):      #S*(192-12):
            mainDisplay[0] = S*-(floorEdge[0] - mainCoord[0])
            floorDisplay[0] = S* -floorEdge[0]
        elif mainCoord[0] > floorEdge[1] - (192 + 15):        #times S
            mainDisplay[0] = S*(384 + (mainCoord[0] - floorEdge[1]))
            floorDisplay[0] = S*(-floorEdge[1] + 384)
        if mainCoord[1] < floorEdge[2] + (108 - 18):
            mainDisplay[1] = S* -(floorEdge[2] - mainCoord[1])
            floorDisplay[1] = S*(-floorEdge[2])
        elif mainCoord[1] > floorEdge[3] - (108 + 18):
            mainDisplay[1] = S*(216 + (mainCoord[1] - floorEdge[3]))
            floorDisplay[1] = S*(-floorEdge[3]  + 216)
        if moving:
            for enemy in enemyList:
                enemy.processEnemy()
            for attack in attackList:
                attack.processAttack()

        display.blit(floor, (floorDisplay[0], floorDisplay[1]))

        if dmgTaken > 0 and dmgCD < 0:
            mainHealth = mainHealth - dmgTaken
            dmgAnim = True
            dmgTimer = 0
            dmgTaken = 0
        if dmgAnim == True:

            if mainHealth <= 0:
                playing = False
                moving = False
                mainDead = pygame.image.load("Assets/Images/sprites/mainDead.png")
                mainDead = pygame.transform.scale(mainDead, (29*S,35*S))
                timer = 0
                while timer <= .5:
                    pygame.draw.rect(display, DMGCOLOR, Rect(0,0,384*S, S*2*timer*200))
                    pygame.draw.rect(display, DMGCOLOR, Rect(0, S*216,384*S, -S*2*timer*200  ))
                    timer = timer + elapsed/1000
                    pygame.display.update()
                    elapsed = fpsClock.tick(FPS)
                display.fill((252,0,82))
                display.blit(mainDead,(mainDisplay[0], mainDisplay[1]))
                pygame.display.update()
                elapsed = fpsClock.tick(FPS)
                timer = 0
                while timer <= 1:
                    timer = timer + elapsed/1000
                    elapsed = fpsClock.tick(FPS)
                retriever = pygame.image.load("Assets/Images/sprites/deathRetriever.png")
                retriever = pygame.transform.scale(retriever, (124*S, 52*S))
                youcantdoitalone = pygame.image.load("Assets/Images/scene/youcantdoitalone.png")
                youcantdoitalone = pygame.transform.scale(youcantdoitalone, (191*S, 32*S))
                timer = 0
                while timer <= 12:
                    display.blit(retriever, ((int(S*(384 - 600*timer/12)),mainDisplay[1] - 5*S)))
                    pygame.draw.rect(display, (0,0,0), Rect(int(S*(384- 600*timer/12 + 124)),0,20*S,216*S))
                    display.blit(youcantdoitalone, (int(S*(600 - 600*timer/12 + 192 - 69)), S*(108-16)))
                    timer = timer + elapsed/1000
                    pygame.display.update()
                    elapsed = fpsClock.tick(FPS)


            else:
                pygame.draw.rect(display, DMGCOLOR, Rect(0,     0, 384*S,  (10-mainHealth)/10 * 108*S*math.sin(3.14*dmgTimer)))
                pygame.draw.rect(display, DMGCOLOR, Rect(0, 216*S, 384*S, -(10-mainHealth)/10 * 108*S*math.sin(3.14*dmgTimer))) #150*S is just to make sure it reaches the bottom, this still needs tinkering
                dmgTimer = dmgTimer + elapsed/1000
                if dmgTimer >= 1:
                    dmgAnim = False

        if playing == True:


            objectList1 = []
            for attack in attackList:
                objectList1.append(attack)
            for enemy in enemyList:
                objectList1.append(enemy)
            if floorMark == 2:
                objectList1.append(1)
                objectList1.append(2)
            if floorMark == 3:
                objectList1.append(1)
            objectList1.append('self')
            objectDictionary = {}
            for item in objectList1:
                objectDictionary[item] = base(item)
                #print(item)
                #print(base(item))
            objectList2 = sorted(objectDictionary.items(), key=operator.itemgetter(1))


            for thing in objectList2:


                if thing[0] == 'self':
                    display.blit(mainImage, (mainDisplay[0], mainDisplay[1]))

                elif thing[0] == 1:
                    if floorMark == 2:
                        display.blit(r2o1, (mainDisplay[0] + S*(328 - mainCoord[0]), mainDisplay[1] + S*(350 - mainCoord[1])))
                    if floorMark == 3:
                        display.blit(r3o1, (mainDisplay[0] + S*(133 - mainCoord[0]), mainDisplay[1] + S*(44 - mainCoord[1])))

                elif thing[0] == 2:
                    if floorMark == 2:
                        display.blit(r2o2, (mainDisplay[0] + S*(328 - mainCoord[0]), mainDisplay[1] + S*(542 - mainCoord[1])))

                #if type(thing[0]) == enemy:
                elif thing[0].type == 1:
                    display.blit(sprite1, (mainDisplay[0] + S*(thing[0].coord[0] - mainCoord[0]), mainDisplay[1] + S*(thing[0].coord[1] - mainCoord[1])))


                #if type(thing[0]) == attack:
                elif thing[0].type == 1.1:


                    if thing[0].timer > .6:
                        '''

                        pygame.draw.rect(display,  (255, 207, 150),
                        Rect(mainDisplay[0] + S*(thing[0].destination[0] - mainCoord[0]), mainDisplay[1] + S*(thing[0].destination[1] - mainCoord[1]), 20*S, 20*S))
                        '''
                        pass
                    else:
                        if thing[0].timer > .4:
                            pygame.draw.rect(display,  (255, 207, 150),
                            Rect(mainDisplay[0] + S*(thing[0].destination[0] - mainCoord[0]), mainDisplay[1] + S*(thing[0].destination[1] - mainCoord[1]), 20*S, 20*S))
                        if thing[0].timer > .2:
                            pygame.draw.rect(display,  (255, 139, 116),
                            Rect(mainDisplay[0] + S*(thing[0].destination[0] - mainCoord[0] + 3), mainDisplay[1] + S*(thing[0].destination[1] - mainCoord[1] + 3), (20-6)*S, (20-6)*S))

                        pygame.draw.rect(display,  (255, 77, 116),
                        Rect(mainDisplay[0] + S*(thing[0].destination[0] - mainCoord[0] + 7), mainDisplay[1] + S*(thing[0].destination[1] - mainCoord[1] + 7), (20 - 14)*S, (20 - 14)*S))


                    '''
                    pygame.draw.rect(display, (252-240*(thing[0].timer/thing[0].time), 0, 252-240*(thing[0].timer/thing[0].time) ),
                    Rect(mainDisplay[0] + S*(thing[0].destination[0] - mainCoord[0]), mainDisplay[1] + S*(thing[0].destination[1] - mainCoord[1]), 20*S, 20*S))
                    '''

            if playNote1 == True:
                display.blit(note1, (0, int(S*(216 - 1*30*(noteCounter)))))
                noteCounter = noteCounter + elapsed/1000
                if noteCounter > 30:
                    playNote1 = False
                    noteCounter = 0
                    moving = True



        #dmgTaken = 0
        dmgCD = dmgCD - elapsed/1000
        spriteTimer = spriteTimer + elapsed/1000









    pygame.display.update()
    elapsed = fpsClock.tick(FPS)
