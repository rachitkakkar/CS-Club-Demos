import pygame
import numpy as np
from math import sin, cos

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D Renderer")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def project(point, angle, scale):
    global WIDTH
    global HEIGHT
    
    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    rotated = np.dot(rotation_z, point.reshape((3, 1)))
    rotated = np.dot(rotation_y, rotated)
    rotated = np.dot(rotation_x, rotated)

    projected = np.dot(projection_matrix, rotated)

    x = int(projected[0][0] * scale) + WIDTH / 2
    y = int(projected[1][0] * scale) + HEIGHT / 2

    return (x, y)

points = []
points.append(np.array([-1, -1, 1]))
points.append(np.array([1, -1, 1]))
points.append(np.array([1,  1, 1]))
points.append(np.array([-1, 1, 1]))
points.append(np.array([-1, -1, -1]))
points.append(np.array([1, -1, -1]))
points.append(np.array([1, 1, -1]))
points.append(np.array([-1, 1, -1]))

angle = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    screen.fill((255, 255, 255))

    projected_points = []
    for point in points:
        new_point = project(point, angle, 100)
        projected_points.append(new_point)
        pygame.draw.circle(screen, (0, 0, 0), new_point, 5)

    pygame.draw.line(screen, (0, 0, 0), (projected_points[0][0], projected_points[0][1]), (projected_points[1][0], projected_points[1][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[4][0], projected_points[4][1]), (projected_points[5][0], projected_points[5][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[0][0], projected_points[0][1]), (projected_points[4][0], projected_points[4][1]))

    pygame.draw.line(screen, (0, 0, 0), (projected_points[1][0], projected_points[1][1]), (projected_points[2][0], projected_points[2][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[5][0], projected_points[5][1]), (projected_points[6][0], projected_points[6][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[1][0], projected_points[1][1]), (projected_points[5][0], projected_points[5][1]))

    pygame.draw.line(screen, (0, 0, 0), (projected_points[2][0], projected_points[2][1]), (projected_points[3][0], projected_points[3][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[6][0], projected_points[6][1]), (projected_points[7][0], projected_points[7][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[2][0], projected_points[2][1]), (projected_points[6][0], projected_points[6][1]))
        
    pygame.draw.line(screen, (0, 0, 0), (projected_points[3][0], projected_points[3][1]), (projected_points[0][0], projected_points[0][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[7][0], projected_points[7][1]), (projected_points[4][0], projected_points[4][1]))
    pygame.draw.line(screen, (0, 0, 0), (projected_points[3][0], projected_points[3][1]), (projected_points[7][0], projected_points[7][1])) 
    
    pygame.display.update()
    angle += 0.01