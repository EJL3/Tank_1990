
import pygame


class Home(pygame.sprite.Sprite):
    def __init__(self, position, imagepaths, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.imagepaths = imagepaths
        self.image = pygame.image.load(self.imagepaths[0])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.alive = True
    
    def setDead(self):
        self.image = pygame.image.load(self.imagepaths[1])
        self.alive = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
