import pygame, sys, math


def rotate2d(pos, rad):
    x,y = pos;
    s,c = math.sin(rad), math.cos(rad)

    return x*c-y*s, y*c+x*s

# def rotate2dRev(pos, rad):
#     x,y = pos;
#     s,c = math.sin(rad), math.cos(rad)
#
#     return x*c+y*s, y*c-x*s

class MouseActiveObject:
    def __init__(self, curr, red, green):
        self.curr = curr
        self.red = red
        self.green = green
        self.pos = (100,0)
        self.active = -1
        self.key = []

    def update(self, key):
        if(key[pygame.K_z] or key[pygame.K_x]):
            self.key = key
            if self.active == 1:
                # print("setting deactive")
                self.active = -1
                self.curr = red
            else:
                # print("setting active")
                self.active = 1
                self.curr = green
class Car:
    def __init__(self, pos):
        self.pos = list(pos)
        self.bounds = []

    def moveUp(self):
        print("x %s, y %s, bound x %s, bound y %s",self.pos[0], self.pos[1], self.bounds[0][0], self.bounds[0][1])
        while self.pos[0]>self.bounds[0][0]or self.pos[0]==863:
            self.pos[0]-=int(-15/math.sin(1)*self.pos[2])
            self.pos[1]+=int(5/math.sin(1)*self.pos[2]/1)
            # self.moveDown()
        else:
            self.pos[0]-=int(1*self.pos[2])
        # self.pos[0]-=1*self.pos[2]
            self.pos[1]+=int(1*self.pos[2])

    def moveDown(self):
        # 893, 894, 863
        if self.pos[0] == 796 or self.pos[0] == 827 or self.pos[0] == 826:
            self.pos[0]+=int(-15/math.sin(1)*self.pos[2])
            self.pos[1]-=int(5/math.sin(1)*self.pos[2]/1)
        else:
            self.pos[0]+=int(1*self.pos[2])
        # self.pos[0]-=1*self.pos[2]
            self.pos[1]-=int(1*self.pos[2])

    def update(self, key):
        if key[pygame.K_p]:
            self.moveUp()
        if key[pygame.K_l]:
            self.moveDown()
    def appendBound(self,pos):
        self.bounds += [pos]


class Cam:
    def __init__(self, pos, rot):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event, active, key):
        if event.type==pygame.MOUSEMOTION and active == 1:
            x, y = event.rel
            x/=2000;
            y/=2000;
            # print(str(key)+"key")
            if key[pygame.K_z]:
               # print("event")
               self.rot[0] +=y;
            if key[pygame.K_x]:
               self.rot[1] += x;

    def update(self, dt, key, radian):
        s = dt*10

        if(key[pygame.K_RIGHTBRACKET]): self.pos[2]+=s
        if(key[pygame.K_LEFTBRACKET]): self.pos[2]-=s

        if(key[pygame.K_UP]): self.pos[1]+=s
        if(key[pygame.K_DOWN]): self.pos[1]-=s
        if(key[pygame.K_RIGHT]): self.pos[0]+=s
        if(key[pygame.K_LEFT]): self.pos[0]-=s

        if(key[pygame.K_e]):
            self.pos[0],self.pos[2] = rotate2dRev((self.pos[0],self.pos[2]), radian)
            # print("x %s, z %s, r %s",self.pos[0], self.pos[2] )

        if(key[pygame.K_r]):
            self.pos[0],self.pos[2] = rotate2d((self.pos[0],self.pos[2]), radian)
            # print("x %s, z %s, r %s",self.pos[0], self.pos[2] )



pygame.init()
w, h = 1000, 1000;
cx, cy = w/2, h/2
screen = pygame.display.set_mode((w,h))

gtrLogo = pygame.image.load('gtrLogo.png').convert()
red = pygame.image.load('red.png').convert()
green = pygame.image.load('green.png').convert()

mouse = MouseActiveObject(red, red, green)

verts = (-1, -1, -1), (1, 1, -1), (2, 1, -1), (3, 2, -1), (4, 1, -1), (5, 2, -1), (6,1,-1), (7,2,-1), (8, 1, -1), (9,2,-1), (10, -1, -1), (-1, -1, 1), (1, 1, 1), (2, 1, 1), (3, 2, 1), (4, 1, 1), (5, 2, 1), (6,1,1), (7,2,1), (8, 1, 1), (9,2,1), (10, -1, 1)

edges = (0,1),(1,2), (2,3), (3,4), (4,5), (5,6), (6,7),(7,8),(8,9),(9,10), (11,12), (12,13), (13, 14), (14, 15), (15,16), (16,17), (17,18), (18,19), (19, 20), (20,21), (0,11),(1,12),(2, 13),(3, 14),(4, 15), (5, 16), (6, 17), (7, 18), (8, 19), (9, 20), (10, 21), (0, 10), (11, 21)

cam = Cam((0,5,-5), (2,2))

running = 1

radian = 0

car = Car((0,0))

carDrawn = -1

gtrSound = 'gtr.mp3'

pygame.mixer.init()
pygame.mixer.music.load(gtrSound)


while running:

    try:
        while not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        #pygame clock
        dt = pygame.time.get_ticks()/1000

        # radian +=dt/10000

        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               print("QUIT")
               pygame.quit()
               exit()
           cam.events(event, mouse.active, mouse.key)

        screen.fill((255, 255, 255))

        # for x,y,z in verts:
        #     z+=5
        #     f=150/z
        #     x,y = (x*f), (y*f)*-1
        #     pygame.draw.circle(screen, (0,0,0), (int(cx+int(x)), int(cy+int(y))), 6)

        for edge in edges:
            point = []
            F = []
            for x,y,z in (verts[edge[0]], verts[edge[1]]):
                x-=cam.pos[0]
                y-=cam.pos[1]
                z-=cam.pos[2]

                x,z = rotate2d((x,z), cam.rot[1])
                y,z = rotate2d((y, z), cam.rot[0])

                f=200/z
                F+=[int(f)]
                x,y = (x*f), (y*f)*-1
                point+=[(int(cx+int(x)), int(cy+int(y)))]
            pygame.draw.line(screen, (0,0,0), point[0], point[1], 6)
            if 14 in edge and 3 in edge:
                x = int((point[0][0]+point[1][0])/2)
                y = int((point[0][1]+point[1][1])/2)
                f = int(200/int((F[0]+F[1])/2))
                car.appendBound((x,y))
            if 0 in edge and 11 in edge and carDrawn == -1:
                print(edge)
                print(point[1])
                x = int((point[0][0]+point[1][0])/2)
                y = int((point[0][1]+point[1][1])/2)
                f = int(200/int((F[0]+F[1])/2))
                print(x)
                car = Car((x, y, f))
                carDrawn = 1

        # print(car.pos)
        pygame.draw.circle(screen, (0,0,0), (car.pos[0], car.pos[1]), 6)
        screen.blit(gtrLogo, (500, 0))
        screen.blit(mouse.curr, mouse.pos)
        pygame.display.update()
        key = pygame.key.get_pressed()
        pygame.time.delay(120)
        cam.update(dt, key, radian)
        mouse.update(key)
        car.update(key)
        pygame.time.delay(10)

    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
