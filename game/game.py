import os
import pygame

class GameObject:
     def __init__(self, image, height, speed):
         self.speed = speed
         self.image = image
         self.pos = image.get_rect().move(0, height)
     def move(self):
         print(str(self.speed)+" Speed ")
         self.pos = self.pos.move(self.speed, self.speed)
         if self.pos.top > 480:
             self.pos.top = 0
         if self.pos.right > 600:
             self.pos.left = 0

screen = pygame.display.set_mode((640, 480))
player = pygame.image.load('red.png').convert()
background = pygame.image.load('earth.bmp').convert()
screen.blit(background, (0, 0))
objects = []
for x in range(1):                    #create 10 objects</i>
   o = GameObject(player, x*40, 20)
   objects.append(o)
while 1:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_DOWN:
               screen.blit(background, o.pos, o.pos)
               o.move()
               screen.blit(o.image, o.pos)
   pygame.display.update()
   pygame.time.delay(100)

# pygame.display.flip()
