import pygame
from chaser.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from chaser.game import Game
from chaser.board import Board


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

        board.draw_cubes(WIN)
        pygame.display.update()
main()
