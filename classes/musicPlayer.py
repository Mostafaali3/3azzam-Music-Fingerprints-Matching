from classes.audio import Audio


class MusicPlayer():
    def __init__(self, audio):
        self.__current_audio = audio
        self.loaded = False #change this flag when you load the sound

    def play_audio(self):
        if self.loaded:
            self.current_audio.play()
        
    @property
    def current_audio(self):
        return self.__current_audio
    
    @current_audio.setter
    def current_audio(self, audio):
        if isinstance(audio, Audio):
            self.__current_audio = audio