import pygame
import sys
from game import Game
from colors import Colors

pygame.init()
GAME_UPDATE = pygame.USEREVENT
game = Game(GAME_UPDATE)
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
level_surface = title_font.render("Level", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
level_rect = pygame.Rect(320, 155, 170, 60)
next_rect = pygame.Rect(320, 235, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")


clock = pygame.time.Clock()


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_SPACE and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

    score_value_surface = title_font.render(
        str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 300, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (320, 490, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(
        centerx=score_rect.centerx, centery=score_rect.centery))

    level_value_surface = title_font.render(
        str(game.level), True, Colors.white)
    screen.blit(level_surface, (365, 120, 50, 50))
    pygame.draw.rect(screen, Colors.light_blue, level_rect, 0, 10)
    screen.blit(level_value_surface, level_value_surface.get_rect(
        centerx=level_rect.centerx, centery=level_rect.centery))

    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
