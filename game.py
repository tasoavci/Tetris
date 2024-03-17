from grid import Grid
from blocks import *
import random
import pygame


class Game:
    def __init__(self, game_update_event):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                       SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.GAME_UPDATE = game_update_event
        self.update_speed()
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        self.lines_cleared += lines_cleared
        if self.lines_cleared >= 1:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.lines_cleared = 0
        self.update_speed()

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                           SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def update_speed(self):
        interval = max(75, 300 - (self.level - 1) * 25)
        pygame.time.set_timer(self.GAME_UPDATE, interval)

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                       SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.update_speed()

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 0, 0)
        if self.next_block.id == 3:
            self.next_block.draw(screen, 245, 300)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 245, 280)
        else:
            self.next_block.draw(screen, 230, 280)
