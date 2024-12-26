from classes.audio import Audio
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QTimer

class MusicPlayer:
    def __init__(self, audio, progressbarSlider,
                 playPauseButton, replayButton, PlayIcon, PauseIcon):
        
        self.__current_audio = audio
        self.loaded = False

        self.progressbarSlider = progressbarSlider
        self.playPauseButton = playPauseButton
        self.replayButton = replayButton

        self.playIcon = PlayIcon
        self.pauseIcon = PauseIcon

        self.player = QMediaPlayer()
        self.is_playing = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.setInterval(100)  
        
    @property
    def current_audio(self):
        return self.__current_audio
    
    @current_audio.setter
    def current_audio(self, audio):
        if isinstance(audio, Audio):
            self.__current_audio = audio
            self.loaded = True
            self.reset_player()
    
    def play_pause(self):
        if not self.loaded:
            return
        
        if self.is_playing:
            self.pause()
        else:
            self.play()
            
        if self.is_playing:
            button_icon = self.pauseIcon
        else:
            button_icon = self.playIcon

        self.playPauseButton.setIcon(button_icon)
    
    def play(self):
        if not self.loaded:
            return
            
        self.is_playing = True
        self.player.play()
        self.timer.start()
    
    def pause(self):
        if not self.loaded:
            return
            
        self.is_playing = False
        self.player.pause()
        self.timer.stop()
    
    def replay(self):
        if not self.loaded:
            return
            
        self.current_position = 0
        self.player.setPosition(0)
        
        # Reset progress bar
        self.progressbarSlider.setValue(0)
        
        if self.is_playing:
            self.play()
    
    def update_progress(self):
        if not self.loaded or not self.is_playing:
            return
            
        duration = len(self.current_audio.data) / self.current_audio.sampling_rate
        current_time = self.player.position() / 1000  # Convert ms to seconds
        progress = (current_time / duration) * 100
        
        self.progressbarSlider.setValue(int(progress))
        
        if progress >= 100:
            self.pause()
            self.current_position = 0
            self.playPauseButton.setIcon(self.playIcon)
    
    def reset_player(self):
        
        self.is_playing = False
        self.timer.stop()
        
        self.progressbarSlider.setValue(0)
        self.playPauseButton.setIcon(self.playIcon)

        
            