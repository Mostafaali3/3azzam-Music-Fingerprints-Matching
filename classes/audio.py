import librosa
import soundfile as sf
class Audio():
    def __init__(self):
        self.data = None
        self.spectrogram = None
        self.hashing_result = []
        self.sampling_rate = 22050 # arbitrary value 
        self.cut_duration = 29
        self.unified_sampling_rate = 22050
        
    def preprocess_data(self):
        self.cut_audio()
        sf.write('./test.wav', self.data, self.sampling_rate)
    
    def hash_sound(self):
        pass 
    
    def change_sample_rate(self):
        if (self.sampling_rate != self.unified_sampling_rate):
            self.data = librosa.resample(self.data , self.sampling_rate, 22050)
    
    def cut_audio(self):
        num_of_samples = int(self.cut_duration * self.sampling_rate)
        self.data = self.data[:num_of_samples]
    
    def generate_spectrogram(self):
        pass
    
    def get_features(self):
        pass 
    
    def compare(self):
        pass


# Test
# audio = Audio()
# data , sr = librosa.load('./data/Alkanas(original).wav')
# audio.data = data
# audio.sampling_rate = sr
# audio.preprocess_data() 
