import numpy as np
import pygame
import math
import random
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
import threading
from helpers import *
from bresenham import bresenham
from skimage.draw import line

from threading import Thread
from scene_elements import Point
from helpers import *
import pygame
class threadBresenham(Thread):
    def __init__(self,sx,sy,ix,iy):
        Thread.__init__(self)
        self.sx=sx
        self.sy=sy
        self.ix=ix
        self.iy=iy
    def run(self):
        rr, cc = line(self.sx,self.sy,self.ix,self.iy)
        thread=threadpinta(rr,cc,Point(self.sx,self.sy))
        thread.start()
class threadpinta(Thread):
    def __init__(self,rr,cc,source):
        """Initialize the thread"""
        Thread.__init__(self)
        self.rr = rr
        self.cc = cc
        self.source = source


    def run(self):
        for i in range(len(self.rr)):

            x=self.rr[i]
            y=self.cc[i]
            values = imagen[y][x][:3]
            length = getLenght(self.source, Point(x, y))
            intensity = ((1 - (length / 500)) ** 2)/2
            values = values * intensity * light
            values = np.add(canvas[x][y], values) / 2
            canvas[x][y] = values


def pathTrace(ray,depth,maxDepth):
    #print(depth)
    if depth<=maxDepth:
        infoIntersec=hitSomething(ray)
        punto=infoIntersec[0]
        pared=infoIntersec[1]
        if punto==-1.0:
            print("No chocó")
            return
        rebote=anguloRebote(ray,punto,pared,depth)
        thread=threadBresenham(ray.origen.x,ray.origen.y,int(punto.x-1),int(punto.y-1))
        thread.start()
        pathTrace(rebote,depth+1,maxDepth)
    return
def randomPathTrace(depth,maxDepth):
    while True:
      for source in sources:
            ray = Ray(source, math.radians(random.uniform(0,360)))
            pathTrace(ray,depth,maxDepth)

def anguloRebote(ray,punto,pared,depth):
    if pared.horizontal:
        if ray.origen.y>punto.y:
            #pared inferior
            angulo = math.radians(random.uniform(5, 175))
            #print("El rebote",depth, "debe ir abajo")
            return Ray(Point(punto.x,punto.y + 2),angulo)
        else:
            #pared superior
            angulo = math.radians(random.uniform(-175, -5))
            #print("El rebote" , depth , "debe ir arriba")
            return Ray(Point(punto.x , punto.y - 2), angulo)
    else:
        if ray.origen.x<punto.x:
            #pared derecha
            angulo = math.radians(random.uniform(-270, -90))
            #print("El rebote" , depth , "debe ir a la izquierda")
            return Ray(Point(punto.x - 2, punto.y), angulo)
        else:
            #pared izquierda
            angulo = math.radians(random.uniform(-85, 85))
            #print("El rebote" ,depth , "debe ir a la derecha")
            return Ray(Point(punto.x + 2, punto.y), angulo)


def hitSomething(ray):
    closest=-1.0
    hittedWall=None
    record=1000000000
    for wall in segments:
        point = ray.cast(wall)
        if point != -1:
            dist = ray.raySegmentIntersect(wall)
            if dist < record:
                record = dist
                closest = point
                hittedWall=wall

    return [closest,hittedWall]




def main():
    """Funcion principal de la aplicacion
    """
    # Segmentos y fuentes
    pygame.display.set_caption("Path Tracer")
    clock = pygame.time.Clock()
    # Desplegar imagen
    surface = pygame.surfarray.make_surface(canvas)
    screen.blit(surface, (border, border))
    # Crear segmentos
    for segment in segments:
        pygame.draw.line(window, Color, (segment.point1.x,
                                         segment.point1.y), (segment.point2.x, segment.point2.y), 4)
    pygame.draw.circle(window, Color, (sources[0].x, sources[0].y), 2, 1)
    #Setup de los threads
    t = threading.Thread(target=randomPathTrace,args=[0,0])  # f being the function that tells how the ball should move
    t.setDaemon(True)  # Alternatively, you can use "t.daemon = True"
    t.start()


    # Main loop
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()
        surface = pygame.surfarray.make_surface(canvas)
        screen.blit(surface, (border, border))


if __name__ == "__main__":
    light = np.array([1, 1, 1])
    Color = [0, 0, 0]
    segments = [
        Segment(Point(0, 0), Point(500, 0), True,False),
        Segment(Point(0, 0), Point(0, 500), False,False),
        Segment(Point(0, 500), Point(500, 500), True,False),
        Segment(Point(500, 500), Point(500, 0), False,False),
        Segment(Point(180, 135), Point(215, 135), True,False),
        Segment(Point(285, 135), Point(320, 135), True,False),
        Segment(Point(320, 135), Point(320, 280), False,False),
        Segment(Point(320, 320), Point(320, 355), False,False),
        Segment(Point(320, 355), Point(215, 355), True,False),
        Segment(Point(180, 390), Point(180, 286), False,False),
        Segment(Point(180, 286), Point(140, 286), True,False),
        Segment(Point(320, 320), Point(360, 320), True,False),
        Segment(Point(180, 250), Point(180, 135), False,False),
    ]
    img_file = Image.new("RGB", (500, 500), (0, 0, 0) )
    canvas = np.array(img_file)
    img_file = Image.open("assets/fondo.png")
    imagen = np.array(img_file)
    sources = [  Point( 294, 200),Point(195, 200)]
    # Crear ventana
    HEIGHT, WIDTH = 500, 500
    border = 0
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    screen = pygame.display.set_mode(
        (WIDTH + (2 * border), HEIGHT + (2 * border)))
    main()
