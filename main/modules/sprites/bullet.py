
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image_paths, screensize, direction, position, border_len, is_stronger=False, speed=8, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_image_paths = bullet_image_paths
        self.width, self.height = screensize
        self.direction = direction
        self.position = position
        self.image = pygame.image.load(self.bullet_image_paths.get(direction))
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.border_len = border_len
        
        self.is_stronger = is_stronger
        
        self.speed = speed
    
    def move(self):
        if self.direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
        elif self.direction == 'down':
            self.rect = self.rect.move(0, self.speed)
        elif self.direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
        elif self.direction == 'right':
            self.rect = self.rect.move(self.speed, 0)
        if (self.rect.top < self.border_len) or (self.rect.bottom > self.height) or (self.rect.left < self.border_len) or (self.rect.right > self.width):
            return True
        return False
