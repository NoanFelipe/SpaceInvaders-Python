import pygame

class SoundEffect:
    def __init__(self):
        pygame.mixer.init()
        self.shoot = pygame.mixer.Sound("SoundEffects/shoot.wav")
        self.shoot.set_volume(0.15)

        self.fastInvader1 = pygame.mixer.Sound("SoundEffects/fastinvader1.wav")
        self.fastInvader1.set_volume(0.3)

        self.fastInvader2 = pygame.mixer.Sound("SoundEffects/fastinvader2.wav")
        self.fastInvader2.set_volume(0.3)

        self.fastInvader3 = pygame.mixer.Sound("SoundEffects/fastinvader3.wav")
        self.fastInvader3.set_volume(0.3)

        self.fastInvader4 = pygame.mixer.Sound("SoundEffects/fastinvader4.wav")
        self.fastInvader4.set_volume(0.3)

        self.explosion = pygame.mixer.Sound("SoundEffects/explosion.wav") 
        self.explosion.set_volume(0.2)

        self.invaderKilled = pygame.mixer.Sound("SoundEffects/invaderkilled.wav") 
        self.invaderKilled.set_volume(0.15)

        self.timerLength = 60
        self.timer = 59
        self.currentSongIndex = 3;

    def playSong(self):
        self.timer += 1
        if self.timer >= self.timerLength:
            self.timer = 0

            if (self.currentSongIndex == 0):
                self.fastInvader1.play()
            elif (self.currentSongIndex == 1):
                self.fastInvader2.play()
            elif (self.currentSongIndex == 2):
                self.fastInvader3.play()
            elif (self.currentSongIndex == 3):
                self.fastInvader4.play()

            if (self.currentSongIndex < 3):
                self.currentSongIndex += 1
            else:
                self.currentSongIndex = 0
