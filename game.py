import pygame, random, sys, time
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
BLACK=(0,0,0)
RED=(255,0,0)
ALIENMINSPEED = 1
ALIENMAXSPEED = 2
ALIENSIZE=30
NEWALIEN = 35
NEWBOMB=140
PLAYERMOVERATE = 7

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def spaceshipHit(playerRect, aliens):
    for b in aliens:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Alien Attack')

gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('Aliensound.wav')

playerImage = pygame.image.load('player.jpg')
playerRect = playerImage.get_rect()
alienImage = pygame.image.load('alienship.jpg')
beam=pygame.image.load('beam.png')
bomb=pygame.image.load('bomb.png')

pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
drawText('Alien Attack', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)

pygame.display.update()
waitForPlayerToPressKey()
topScore = 0
while True:

    aliens = []
    beams=[]
    bombs=[]
    score = 0
    life_score=0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    alienCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    beam_strike=True
    over=False
    musicPlaying=True
    life=5
    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if (event.key == K_UP or event.key == K_SPACE) and (beam_strike):
                    newBeam={'rect' : pygame.Rect(playerRect.centerx,playerRect.top-20,3,20), 'speed' : 3 }

                    beams.append(newBeam)
                    beam_strike=False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == K_SPACE:
                    beam_strike = True
                if event.key == ord('m'):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
            if event.type == MOUSEMOTION:
                playerRect.move_ip(event.pos[0] - playerRect.centerx,0)
            if event.type == MOUSEBUTTONDOWN and beam_strike:
                newBeam={'rect' : pygame.Rect(playerRect.centerx,playerRect.top-20,5,20), 'speed' : 4 }
                beams.append(newBeam)
                beam_strike=False
            if event.type == MOUSEBUTTONUP:
                beam_strike=True

        alienCounter += 1
        if alienCounter >= NEWALIEN:
            alienCounter = 0
            newAlien = {'rect': pygame.Rect((random.randint(0, (WINDOWWIDTH - ALIENSIZE)//4 ))*4, 0 - ALIENSIZE, ALIENSIZE, ALIENSIZE),
                        'speed': random.randint(ALIENMINSPEED, ALIENMAXSPEED), 'bomb' : 0}
            aliens.append(newAlien)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        for b in aliens:
            b['rect'].move_ip(0, b['speed'])
            b['bomb']+=1
            if b['rect'].top > WINDOWHEIGHT-ALIENSIZE :
                if score > topScore:
                    topScore = score # set new top score
                over=True
                break
            if b['bomb']==NEWBOMB:
                b['bomb']=0
                newBomb={'rect' : pygame.Rect(b['rect'].centerx,b['rect'].top+20,7,7), 'speed' : b['speed'] + 1}
                bombs.append(newBomb)

        windowSurface.fill(BACKGROUNDCOLOR)
        life_score+=1
        if life_score>=1000:
            life+=1
            life_score=0

        for b in beams:
            b['rect'].move_ip(0,-1 * b['speed'])
            if b['rect'].bottom < 0 :
                beams.remove(b)

        for b in beams:
            for a in aliens:
                if b['rect'].colliderect(a['rect']):
                    score += a['speed']*20
                    life_score += a['speed']*20
                    beams.remove(b)
                    aliens.remove(a)

        windowSurface.blit(playerImage, playerRect)

        for b in bombs:
            b['rect'].move_ip(0,1*b['speed'])
            if b['rect'].top > WINDOWHEIGHT:
                bombs.remove(b)

        for b in bombs:
            if playerRect.colliderect(b['rect']):
                life-=1
                bombs.remove(b)


        if life==0:
            if score>topScore:
                topScore=score
            over=True

        for b in bombs:
            windowSurface.blit(bomb,b['rect'])

        for b in aliens:
            windowSurface.blit(alienImage, b['rect'])

        for b in beams:
            windowSurface.blit(beam, b['rect'])

        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Life: %s' %(life),font,windowSurface,WINDOWWIDTH-200,0)

        if spaceshipHit(playerRect, aliens):
            if score > topScore:
                topScore = score # set new top score
            over=True

        if over:
            break

        pygame.display.update()

        mainClock.tick(40)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
