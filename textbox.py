import pygame


"""
textbox for keyboard input
"""


class TextBox:
    content = ""
    activated = False

    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = pygame.rect.Rect(position, size)
        self.font = pygame.font.SysFont("monospace", size[1])

    def render(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.font.render(self.content, 1, (0, 0, 0)), self.rect)

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.activated = True
                else:
                    self.activated = False
            if e.type == pygame.KEYDOWN:
                if self.activated:
                    if e.type == pygame.K_BACKSPACE:
                        self.content = self.content[:-1]
                    else:
                        self.content = e.unicode
