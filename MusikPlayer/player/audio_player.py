import pygame


class AudioPlayer:
    

    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
        pygame.mixer.music.set_volume(0.7)

    def load(self, file_path):
        
        try:
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.is_playing = False
            self.is_paused = False
            return True
        except pygame.error as e:
            print(f"❌ Ошибка загрузки: {e}")
            return False

    def play(self):
        
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            return True
        except pygame.error as e:
            print(f"❌ Ошибка воспроизведения: {e}")
            return False

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause()
            return "paused"
        else:
            self.play()
            return "playing"

    def set_volume(self, volume):
        
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)

    def get_position(self):
       
        pos_ms = pygame.mixer.music.get_pos()
        return max(0, pos_ms) // 1000

    def is_busy(self):
        
        return pygame.mixer.music.get_busy()

    def close(self):
       
        pygame.mixer.quit()