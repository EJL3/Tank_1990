
import sys
import pygame
import random
from .sprites import *

class GameLevel():
    def __init__(self, gamelevel, levelfilepath, sounds, is_dual_mode, cfg, **kwargs):
        
        self.gamelevel = gamelevel
        self.levelfilepath = levelfilepath
        
        self.sounds = sounds
        
        self.is_dual_mode = is_dual_mode
        
        self.border_len = cfg.BORDER_LEN
        self.grid_size = cfg.GRID_SIZE
        self.width, self.height = cfg.WIDTH, cfg.HEIGHT
        self.panel_width = cfg.PANEL_WIDTH
        
        self.scene_image_paths = cfg.SCENE_IMAGE_PATHS
        self.other_image_paths = cfg.OTHER_IMAGE_PATHS
        self.player_tank_image_paths = cfg.PLAYER_TANK_IMAGE_PATHS
        self.bullet_image_paths = cfg.BULLET_IMAGE_PATHS
        self.enemy_tank_image_paths = cfg.ENEMY_TANK_IMAGE_PATHS
        self.food_image_paths = cfg.FOOD_IMAGE_PATHS
        self.home_image_paths = cfg.HOME_IMAGE_PATHS
        
        self.font = pygame.font.Font(cfg.FONTPATH, cfg.HEIGHT//30)
        
        self.scene_elems = {
            'brick_group': pygame.sprite.Group(), 
            'iron_group': pygame.sprite.Group(),
            'ice_group': pygame.sprite.Group(), 
            'river_group': pygame.sprite.Group(),
            'tree_group': pygame.sprite.Group()
        }
        
        self.__parseLevelFile()
    
    def start(self, screen):
        screen = pygame.display.set_mode((self.width+self.panel_width, self.height))
        
        background_img = pygame.image.load(self.other_image_paths.get('background'))
        
        player_tanks_group = pygame.sprite.Group()
        enemy_tanks_group = pygame.sprite.Group()
        player_bullets_group = pygame.sprite.Group()
        enemy_bullets_group = pygame.sprite.Group()
        foods_group = pygame.sprite.Group()
        
        generate_enemies_event = pygame.constants.USEREVENT
        pygame.time.set_timer(generate_enemies_event, 20000)
        
        home = Home(position=self.home_position, imagepaths=self.home_image_paths)
        
        tank_player1 = PlayerTank('player1', position=self.player_tank_positions[0], player_tank_image_paths=self.player_tank_image_paths, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, protected_mask_path=self.other_image_paths.get('protect'), boom_image_path=self.other_image_paths.get('boom_static'))
        player_tanks_group.add(tank_player1)
        if self.is_dual_mode:
            tank_player2 = PlayerTank('player2', position=self.player_tank_positions[1], player_tank_image_paths=self.player_tank_image_paths, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, protected_mask_path=self.other_image_paths.get('protect'), boom_image_path=self.other_image_paths.get('boom_static'))
            player_tanks_group.add(tank_player2)
        
        for position in self.enemy_tank_positions:
            enemy_tanks_group.add(EnemyTank(enemy_tank_image_paths=self.enemy_tank_image_paths, appear_image_path=self.other_image_paths.get('appear'), position=position, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, food_image_paths=self.food_image_paths, boom_image_path=self.other_image_paths.get('boom_static')))
        
        self.sounds['start'].play()
        clock = pygame.time.Clock()
        
        is_win = False
        is_running = True
        
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(background_img, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == generate_enemies_event:
                    if self.max_enemy_num > len(enemy_tanks_group):
                        for position in self.enemy_tank_positions:
                            if len(enemy_tanks_group) == self.total_enemy_num:
                                break
                            enemy_tank = EnemyTank(enemy_tank_image_paths=self.enemy_tank_image_paths, appear_image_path=self.other_image_paths.get('appear'), position=position, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, food_image_paths=self.food_image_paths, boom_image_path=self.other_image_paths.get('boom_static'))
                            if (not pygame.sprite.spritecollide(enemy_tank, enemy_tanks_group, False, None)) and (not pygame.sprite.spritecollide(enemy_tank, player_tanks_group, False, None)):
                                enemy_tanks_group.add(enemy_tank)
            
            key_pressed = pygame.key.get_pressed()
            
            if tank_player1.num_lifes >= 0:
                if key_pressed[pygame.K_w]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_s]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_a]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_d]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_SPACE]:
                    bullet = tank_player1.shoot()
                    if bullet:
                        self.sounds['fire'].play() if tank_player1.tanklevel < 2 else self.sounds['Gunfire'].play()
                        player_bullets_group.add(bullet)
            
            if self.is_dual_mode and (tank_player2.num_lifes >= 0):
                if key_pressed[pygame.K_UP]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_DOWN]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_LEFT]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_RIGHT]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_KP0]:
                    bullet = tank_player2.shoot()
                    if bullet:
                        player_bullets_group.add(bullet)
                        self.sounds['fire'].play() if tank_player2.tanklevel < 2 else self.sounds['Gunfire'].play()
            
            pygame.sprite.groupcollide(player_bullets_group, self.scene_elems.get('brick_group'), True, True)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('brick_group'), True, True)
            
            for bullet in player_bullets_group:
                if pygame.sprite.spritecollide(bullet, self.scene_elems.get('iron_group'), bullet.is_stronger, None):
                    player_bullets_group.remove(bullet)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('iron_group'), True, False)
            
            pygame.sprite.groupcollide(player_bullets_group, enemy_bullets_group, True, True)
            
            for tank in enemy_tanks_group:
                if pygame.sprite.spritecollide(tank, player_bullets_group, True, None):
                    if tank.food:
                        foods_group.add(tank.food)
                        tank.food = None
                    if tank.decreaseTankLevel():
                        self.sounds['bang'].play()
                        self.total_enemy_num -= 1
            
            for tank in player_tanks_group:
                if pygame.sprite.spritecollide(tank, enemy_bullets_group, True, None):
                    if tank.is_protected:
                        self.sounds['blast'].play()
                    else:
                        if tank.decreaseTankLevel():
                            self.sounds['bang'].play()
                        if tank.num_lifes < 0:
                            player_tanks_group.remove(tank)
            
            if pygame.sprite.spritecollide(home, player_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            
            if pygame.sprite.spritecollide(home, enemy_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            
            if pygame.sprite.groupcollide(player_tanks_group, self.scene_elems.get('tree_group'), False, False):
                self.sounds['hit'].play()
            
            for player_tank in player_tanks_group:
                for food in foods_group:
                    if pygame.sprite.collide_rect(player_tank, food):
                        if food.name == 'boom':
                            self.sounds['add'].play()
                            for _ in enemy_tanks_group:
                                self.sounds['bang'].play()
                            self.total_enemy_num -= len(enemy_tanks_group)
                            enemy_tanks_group = pygame.sprite.Group()
                        elif food.name == 'clock':
                            self.sounds['add'].play()
                            for enemy_tank in enemy_tanks_group:
                                enemy_tank.setStill()
                        elif food.name == 'gun':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                        elif food.name == 'iron':
                            self.sounds['add'].play()
                            self.__pretectHome()
                        elif food.name == 'protect':
                            self.sounds['add'].play()
                            player_tank.setProtected()
                        elif food.name == 'star':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                            player_tank.improveTankLevel()
                        elif food.name == 'tank':
                            self.sounds['add'].play()
                            player_tank.addLife()
                        foods_group.remove(food)
            
            for key, value in self.scene_elems.items():
                if key in ['ice_group', 'river_group']:
                    value.draw(screen)
            
            for bullet in player_bullets_group:
                if bullet.move():
                    player_bullets_group.remove(bullet)
            player_bullets_group.draw(screen)
            
            for bullet in enemy_bullets_group:
                if bullet.move():
                    enemy_bullets_group.remove(bullet)
            enemy_bullets_group.draw(screen)
            
            for tank in player_tanks_group:
                tank.update()
                tank.draw(screen)
            
            for tank in enemy_tanks_group:
                enemy_tanks_group.remove(tank)
                data_return = tank.update(self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                enemy_tanks_group.add(tank)
                if data_return.get('bullet'):
                    enemy_bullets_group.add(data_return.get('bullet'))
                if data_return.get('boomed'):
                    enemy_tanks_group.remove(tank)
            enemy_tanks_group.draw(screen)
            
            for key, value in self.scene_elems.items():
                if key not in ['ice_group', 'river_group']:
                    value.draw(screen)
            
            home.draw(screen)
            
            for food in foods_group:
                if food.update():
                    foods_group.remove(food)
            foods_group.draw(screen)
            self.__showGamePanel(screen, tank_player1, tank_player2) if self.is_dual_mode else self.__showGamePanel(screen, tank_player1)
            
            if len(player_tanks_group) == 0:
                is_win = False
                is_running = False
            
            if self.total_enemy_num <= 0:
                is_win = True
                is_running = False
            pygame.display.flip()
            clock.tick(60)
        screen = pygame.display.set_mode((self.width, self.height))
        return is_win
    
    def __showGamePanel(self, screen, tank_player1, tank_player2=None):
        color_white = (255, 255, 255)
        # 玩家一操作提示
        player1_operate_tip = self.font.render('Operate-P1:', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_w: Up', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*2/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_s: Down', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*3/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_a: Left', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*4/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_d: Right', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*5/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_SPACE: Shoot', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*6/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        
        player2_operate_tip = self.font.render('Operate-P2:', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*8/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_UP: Up', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*9/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_DOWN: Down', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*10/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_LEFT: Left', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*11/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_RIGHT: Right', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*12/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_KP0: Shoot', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*13/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        
        player1_state_tip = self.font.render('State-P1:', True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*15/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('Life: %s' % tank_player1.num_lifes, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*16/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('TLevel: %s' % tank_player1.tanklevel, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*17/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        
        player2_state_tip = self.font.render('State-P2:', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*19/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('Life: %s' % tank_player2.num_lifes, True, color_white) if tank_player2 else self.font.render('Life: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*20/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('TLevel: %s' % tank_player2.tanklevel, True, color_white) if tank_player2 else self.font.render('TLevel: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*21/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        
        game_level_tip = self.font.render('Game Level: %s' % self.gamelevel, True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*23/30
        screen.blit(game_level_tip, game_level_tip_rect)
        
        remaining_enemy_tip = self.font.render('Remain Enemy: %s' % self.total_enemy_num, True, color_white)
        remaining_enemy_tip_rect = remaining_enemy_tip.get_rect()
        remaining_enemy_tip_rect.left, remaining_enemy_tip_rect.top = self.width+5, self.height*24/30
        screen.blit(remaining_enemy_tip, remaining_enemy_tip_rect)
    
    def __pretectHome(self):
        for x, y in self.home_around_positions:
            self.scene_elems['iron_group'].add(Iron((x, y), self.scene_image_paths.get('iron')))
    
    def __parseLevelFile(self):
        f = open(self.levelfilepath, errors='ignore')
        num_row = -1
        for line in f.readlines():
            line = line.strip('\n')
            
            if line.startswith('#') or (not line):
                continue
            
            elif line.startswith('%TOTALENEMYNUM'):
                self.total_enemy_num = int(line.split(':')[-1])
            
            elif line.startswith('%MAXENEMYNUM'):
                self.max_enemy_num = int(line.split(':')[-1])
            
            elif line.startswith('%HOMEPOS'):
                self.home_position = line.split(':')[-1]
                self.home_position = [int(self.home_position.split(',')[0]), int(self.home_position.split(',')[1])]
                self.home_position = (self.border_len+self.home_position[0]*self.grid_size, self.border_len+self.home_position[1]*self.grid_size)
            
            elif line.startswith('%HOMEAROUNDPOS'):
                self.home_around_positions = line.split(':')[-1]
                self.home_around_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.home_around_positions.split(' ')]
                self.home_around_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.home_around_positions]
            
            elif line.startswith('%PLAYERTANKPOS'):
                self.player_tank_positions = line.split(':')[-1]
                self.player_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.player_tank_positions.split(' ')]
                self.player_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.player_tank_positions]
            
            elif line.startswith('%ENEMYTANKPOS'):
                self.enemy_tank_positions = line.split(':')[-1]
                self.enemy_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.enemy_tank_positions.split(' ')]
                self.enemy_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.enemy_tank_positions]
            
            else:
                num_row += 1
                for num_col, elem in enumerate(line.split(' ')):
                    position = self.border_len+num_col*self.grid_size, self.border_len+num_row*self.grid_size
                    if elem == 'B':
                        self.scene_elems['brick_group'].add(Brick(position, self.scene_image_paths.get('brick')))
                    elif elem == 'I':
                        self.scene_elems['iron_group'].add(Iron(position, self.scene_image_paths.get('iron')))
                    elif elem == 'R':
                        self.scene_elems['river_group'].add(River(position, self.scene_image_paths.get(random.choice(['river1', 'river2']))))
                    elif elem == 'C':
                        self.scene_elems['ice_group'].add(Ice(position, self.scene_image_paths.get('ice')))
                    elif elem == 'T':
                        self.scene_elems['tree_group'].add(Tree(position, self.scene_image_paths.get('tree')))
