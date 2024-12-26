import librosa
import numpy as np
from PIL import Image
import imagehash

# import soundfile as sf
class Audio():
    def __init__(self):
        self.data = None
        self.melspectrogram = None
        self.hashing_result = []
        self.sampling_rate = 22050 # arbitrary value 
        self.cut_duration = 29
        self.unified_sampling_rate = 22050
        self.mfccs = None
        self.features = None
        self.song_name = "untitled"
        
    def preprocess_data(self):
        self.cut_audio()
        # sf.write('./Alkanas(instruments)_22050.wav', self.data, self.sampling_rate)
    
    def hash_sound(self):
        self.hashing_result = imagehash.phash(self.features) 
    
    '''
    def change_sample_rate(self):
        if (self.sampling_rate != self.unified_sampling_rate):
            self.data = librosa.resample(self.data , self.sampling_rate, 22050)
    '''
    
    def cut_audio(self):
        num_of_samples = int(self.cut_duration * self.sampling_rate)
        self.data = self.data[:num_of_samples]
    
    def generate_melspectrogram(self):
        melspectrogram = librosa.feature.melspectrogram(y=self.data, sr=self.sampling_rate, n_mels=128, fmax=self.sampling_rate//2)
        self.melspectrogram = librosa.power_to_db(melspectrogram, ref=np.max)

    def get_mfccs(self):
        mfccs = librosa.feature.mfcc(y=self.data, sr=self.sampling_rate, n_mfcc=13)
        self.mfccs = (255 * (mfccs - np.min(mfccs)) / (np.max(mfccs) - np.min(mfccs))).astype(np.uint8)
    
    def get_features(self):
        self.generate_melspectrogram()
        self.get_mfccs()
        melspectrogram_pil = Image.fromarray(self.melspectrogram)
        mfccs_pil = Image.fromarray(self.mfccs) 
        total_height = melspectrogram_pil.height + mfccs_pil.height
        stacked_width = max(melspectrogram_pil.width, mfccs_pil.width)
        stacked_features = Image.new("L", (stacked_width, total_height))
        stacked_features.paste(melspectrogram_pil, (0, 0))
        stacked_features.paste(mfccs_pil, (0, melspectrogram_pil.height))
        self.features = stacked_features
        
    def compare(self , hash_to_compare_with):
        hamming_distance = self.hashing_result - hash_to_compare_with
        similarity_score = 1 - hamming_distance / len(self.hashing_result.hash.flatten())
        
        return similarity_score
    
    def load_audio(self, file_path):
        data, sample_rate = librosa.load(file_path, mono=True)
        self.data = data
        self.sampling_rate = sample_rate
    
    def mix_with_friend(self):
        pass


# Hashing Implementation Test
# audio1 = Audio()
# data1 , sr1 = librosa.load('./data/Alkanas(vocals).wav' , mono=True)
# audio1.data = data1
# audio1.sampling_rate = sr1

# audio2 = Audio()
# data2 , sr2 = librosa.load('./data/Alkanas(original).wav')
# audio2.data = data2
# audio2.sampling_rate = sr2

# audio1.preprocess_data()
# audio1.get_features()
# audio1.hash_sound()

# audio2.preprocess_data()
# audio2.get_features()
# audio2.hash_sound()

# hash1 = audio1.hashing_result
# hash2 = audio2.hashing_result

# hamming_distance = hash1 - hash2
# similarity_score = 1 - hamming_distance / len(hash1.hash.flatten())

# print(similarity_score)