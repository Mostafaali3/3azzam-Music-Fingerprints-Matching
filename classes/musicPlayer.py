from classes.audio import Audio
from PyQt5.QtCore import QTimer
import sounddevice as sd
import numpy as np

class MusicPlayer:
    def __init__(self, audio, progressbarSlider,
                 playPauseButton, replayButton, PlayIcon, PauseIcon):
        
        if audio is None:
            raise ValueError('Audio object must be provided')
        
        self.__current_audio = audio
        self.loaded = False
        
        self.progressbarSlider = progressbarSlider
        self.playPauseButton = playPauseButton
        self.replayButton = replayButton
        
        self.playPauseButton.clicked.connect(self.play_pause)
        self.replayButton.clicked.connect(self.replay)
        
        self.playIcon = PlayIcon
        self.pauseIcon = PauseIcon
        
        # Audio stream properties
        self.stream = None
        self.current_frame = 0
        self.is_playing = False
        
        # Timer for updating progress
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.setInterval(100)  # Update every 100ms
        
        # Set initial audio
        if audio is not None:
            self.current_audio = audio

    @property
    def current_audio(self):
        return self.__current_audio
    
    @current_audio.setter
    def current_audio(self, audio):
        if isinstance(audio, Audio):
            self.__current_audio = audio
            self.reset_player()
            
            # Configure stream (but don't start it)
            self.stream = sd.OutputStream(
                samplerate=audio.sampling_rate,
                channels=1,
                dtype=np.float32,
                callback=self._audio_callback
            )
    
    def _audio_callback(self, outdata, frames, time, status):
        if self.current_frame + frames > len(self.current_audio.data):
            # If we're at the end of the audio
            remaining = len(self.current_audio.data) - self.current_frame
            if remaining > 0:
                outdata[:remaining, 0] = self.current_audio.data[self.current_frame:self.current_frame + remaining]
                outdata[remaining:, 0] = 0
            else:
                outdata[:, 0] = 0
            self.current_frame = len(self.current_audio.data)
            # Stop playback when we reach the end
            self.pause()
            self.playPauseButton.setIcon(self.playIcon)
        else:
            # Normal playback
            outdata[:, 0] = self.current_audio.data[self.current_frame:self.current_frame + frames]
            self.current_frame += frames
    
    def play_pause(self):
        if not self.loaded:
            return
        
        if self.is_playing:
            self.pause()
        else:
            self.play()
        
        button_icon = self.pauseIcon if self.is_playing else self.playIcon
        self.playPauseButton.setIcon(button_icon)
    
    def play(self):
        if not self.loaded:
            return
        
        print('Playing')
        self.is_playing = True
        if not self.stream.active:
            self.stream.start()
        self.timer.start()
    
    def pause(self):
        if not self.loaded:
            return
        
        print('Pausing')
        self.is_playing = False
        if self.stream and self.stream.active:
            self.stream.stop()
        self.timer.stop()
    
    def replay(self):
        if not self.loaded:
            return
        
        self.current_frame = 0
        self.progressbarSlider.setValue(0)
        
        if self.is_playing:
            if self.stream and self.stream.active:
                self.stream.stop()
            self.stream.start()
    
    def update_progress(self):
        if not self.loaded or not self.is_playing:
            return
        
        print('Updating progress')
        
        # Calculate progress as percentage
        total_frames = len(self.current_audio.data)
        progress = (self.current_frame / total_frames) * 100
        
        self.progressbarSlider.setValue(int(progress))
        
        if progress >= 100:
            self.pause()
            self.current_frame = 0
            self.playPauseButton.setIcon(self.playIcon)
    
    def reset_player(self):
        self.is_playing = False
        self.current_frame = 0
        if self.stream and self.stream.active:
            self.stream.stop()
        self.timer.stop()
        self.progressbarSlider.setValue(0)
        self.playPauseButton.setIcon(self.playIcon)
    
    def __del__(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()