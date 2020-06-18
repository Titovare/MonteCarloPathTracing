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

def rayTrace():
    for i in range(0, 3, 1):
        ray = Ray(sources[0], math.radians(0))
        closest = None
        record = 100000000000000000
        for wall in segments:
            point = ray.cast(wall)
            if point != -1.0:
                dist = ray.raySegmentIntersect(wall)
                if dist < record:
                    record = dist
                    closest = point
        if isinstance(closest, Point):
            pygame.draw.line(window,Color,(sources[0].x,sources[0].y),(closest.x,closest.y),2)
            print(imagen[int(closest.x)][int(closest.y)])
def pintarPixel(rr,cc):
    values = imagen[rr][cc][:3]
    length = getLenght(sources[0], Point(rr, cc))
    intensity = (1 - (length / 500)) ** 2
    values = values * intensity * light
    canvas[rr][cc] = values
    surface = pygame.surfarray.make_surface(canvas)
    screen.blit(surface, (border, border))
def pathTrace(ray,depth,maxDepth):
    Color2=[random.uniform(0,255),random.uniform(0,255),random.uniform(0,255)]
    #print(depth)
    if depth<=maxDepth:
        infoIntersec=hitSomething(ray)
        punto=infoIntersec[0]
        pared=infoIntersec[1]
        if punto==-1.0:
            print("No chocó")
            return
        rebote=anguloRebote(ray,punto,pared,depth)
        rr, cc = line(sources[0].x,sources[0].y,int(punto.x-1),int(punto.y-1))
        #pixeles=list(bresenham(sources[0].x,sources[0].y,int(punto.x-1),int(punto.y-1)))
        for i in range(len(rr)):
            t = threading.Thread(target=pintarPixel,
                                 args=[rr[i], cc[i]])  # f being the function that tells how the ball should move
            t.setDaemon(False)  # Alternatively, you can use "t.daemon = True"
            t.start()
        # for pixel in pixeles:
        #     values=imagen[pixel[0]][pixel[1]][:3]
        #     length= getLenght(sources[0],Point(pixel[0],pixel[1]))
        #     intensity = (1 - (length / 500)) ** 2
        #     values = values * intensity * light
        #     canvas[pixel[0]][pixel[1]]=values
        #     surface = pygame.surfarray.make_surface(canvas)
        #     screen.blit(surface, (border, border))
        #pygame.draw.line(screen,Color,(ray.origen.x,ray.origen.y),(punto.x,punto.y),2)
        pathTrace(rebote,depth+1,maxDepth)
    return
def randomPathTrace(depth,maxDepth):
    for i in range(5000):
        ray = Ray(sources[0], math.radians(random.uniform(-360, 0)))
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
    t = threading.Thread(target=randomPathTrace,args=[0,1])  # f being the function that tells how the ball should move
    t.setDaemon(True)  # Alternatively, you can use "t.daemon = True"
    t.start()
    #a=bresenhamline(np.array([250,250]),np.array([275,275]),max_iter=-1)


    # Main loop
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()


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
    img_file = Image.new("RGB", (500, 500), (255, 255, 255) )
    canvas = np.array(img_file)
    img_file = Image.open("assets/fondo.png")
    imagen = np.array(img_file)
    sources = [Point(195, 200)]
    # Crear ventana
    HEIGHT, WIDTH = 500, 500
    border = 0
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    screen = pygame.display.set_mode(
        (WIDTH + (2 * border), HEIGHT + (2 * border)))
    main()