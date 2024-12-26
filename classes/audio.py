import librosa
import numpy as np
from PIL import Image
import imagehash
from copy import deepcopy

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
        self.preprocess_data()
        self.get_features()
        self.hashing_result = imagehash.phash(self.features) 
    
    '''
    def change_sample_rate(self):
        if (self.sampling_rate != self.unified_sampling_rate):
            self.data = librosa.resample(self.data , self.sampling_rate, 22050)
    '''
    
    def cut_audio(self):
        if self.data is not None:
            num_of_samples = int(self.cut_duration * self.sampling_rate)
            self.data = self.data[:num_of_samples]
    
    def generate_melspectrogram(self):
        if self.data is not None:
            melspectrogram = librosa.feature.melspectrogram(y=self.data, sr=self.sampling_rate, n_mels=128, fmax=self.sampling_rate//2)
            self.melspectrogram = librosa.power_to_db(melspectrogram, ref=np.max)

    def get_mfccs(self):
        if self.data is not None:
            mfccs = librosa.feature.mfcc(y=self.data, sr=self.sampling_rate, n_mfcc=13)
            self.mfccs = (255 * (mfccs - np.min(mfccs)) / (np.max(mfccs) - np.min(mfccs))).astype(np.uint8)
    
    def create_constellation_map(self):
        if self.data is not None:
            # Higher resolution spectrogram
            spectrogram = librosa.stft(self.data, n_fft=4096, hop_length=512)
            spectrogram_db = librosa.amplitude_to_db(abs(spectrogram))
            
            # Improved peak detection parameters
            peaks = librosa.util.peak_pick(spectrogram_db,
                                        pre_max=30,
                                        post_max=30,
                                        pre_avg=30,
                                        post_avg=30,
                                        delta=0.8,  # Higher threshold
                                        wait=25)    # Increased wait time
            
            # Create fingerprint map
            peak_map = np.zeros_like(spectrogram_db)
            peak_map[peaks] = 255
            
            # Apply target zone analysis (Shazam-like approach)
            target_map = self.create_target_zones(peak_map)
            self.features = Image.fromarray(target_map.astype(np.uint8))
            return self.features

    def create_constellation_map(self):
        if self.data is not None:
            spectrogram = librosa.stft(self.data, n_fft=4096, hop_length=512)
            spectrogram_db = librosa.amplitude_to_db(abs(spectrogram))
            
            # Find peaks using 2D local maximum
            peaks = self.find_peaks_2d(spectrogram_db)
            
            peak_map = np.zeros_like(spectrogram_db)
            peak_map[peaks] = 255
            
            target_map = self.create_target_zones(peak_map)
            self.features = Image.fromarray(target_map.astype(np.uint8))
            return self.features

    def find_peaks_2d(self, spec, threshold=0.5, neighborhood_size=20):
        """Find peaks in 2D spectrogram"""
        from scipy.ndimage import maximum_filter
        from scipy.ndimage import generate_binary_structure, binary_erosion
        
        neighborhood = generate_binary_structure(2,2)
        local_max = maximum_filter(spec, size=neighborhood_size) == spec
        background = (spec < threshold)
        peaks = local_max ^ binary_erosion(local_max, structure=neighborhood)
        peaks[background] = False
        return peaks

    def get_features(self):
        if self.data is not None:
            return self.create_constellation_map()
        
    def create_target_zones(self, peak_map, zone_size=10):
        """Create target zones around peaks for better matching"""
        height, width = peak_map.shape
        target_map = np.copy(peak_map)
        
        for i in range(height):
            for j in range(width):
                if peak_map[i,j] > 0:
                    y_start = max(0, i - zone_size)
                    y_end = min(height, i + zone_size)
                    x_start = max(0, j - zone_size)
                    x_end = min(width, j + zone_size)
                    target_map[y_start:y_end, x_start:x_end] = 200
                    target_map[i,j] = 255
        
        return target_map
    
    # def get_features(self):
    #     if self.data is not None:
    #         self.generate_melspectrogram()
    #         self.get_mfccs()
    #         melspectrogram_pil = Image.fromarray(self.melspectrogram)
    #         mfccs_pil = Image.fromarray(self.mfccs) 
    #         total_height = melspectrogram_pil.height + mfccs_pil.height
    #         stacked_width = max(melspectrogram_pil.width, mfccs_pil.width)
    #         stacked_features = Image.new("L", (stacked_width, total_height))
    #         stacked_features.paste(melspectrogram_pil, (0, 0))
    #         stacked_features.paste(mfccs_pil, (0, melspectrogram_pil.height))
    #         self.features = stacked_features
    
    # def get_features(self):
    #     if self.data is not None:
    #         # Generate basic features 
    #         self.generate_melspectrogram()
    #         self.get_mfccs()
    #         chroma = self.get_chroma_features()
    #         cqt = self.get_cqt_features()
    #         spectral_centroid, spectral_bandwidth, spectral_rolloff = self.get_spectral_features()
    #         _, _, tempogram = self.get_rhythm_features()
            
    #         # Get vocal-specific features
    #         f0, voiced_flag, _ = librosa.pyin(self.data, 
    #                                         fmin=librosa.note_to_hz('C2'),
    #                                         fmax=librosa.note_to_hz('C7'),
    #                                         sr=self.sampling_rate)
    #         zcr = librosa.feature.zero_crossing_rate(self.data)
            
    #         # Normalize all features
    #         features_list = [
    #             librosa.util.normalize(self.melspectrogram),
    #             librosa.util.normalize(self.mfccs),
    #             librosa.util.normalize(chroma), 
    #             librosa.util.normalize(cqt),
    #             librosa.util.normalize(spectral_centroid),
    #             librosa.util.normalize(np.nan_to_num(f0).reshape(1, -1)),
    #             librosa.util.normalize(zcr),
    #             librosa.util.normalize(tempogram)
    #         ]
            
    #         # Ensure same width and aggregate
    #         max_width = max(f.shape[1] for f in features_list)
    #         resized_features = []
            
    #         for feature in features_list:
    #             if feature.shape[1] != max_width:
    #                 feature_resized = librosa.util.fix_length(feature, size=max_width, axis=1)
    #                 resized_features.append(feature_resized)
    #             else:
    #                 resized_features.append(feature)
            
    #         # Stack and aggregate features
    #         stacked_features = np.vstack(resized_features)
    #         aggregated_features = self.aggregate_features(stacked_features)
            
    #         # Convert to image
    #         normalized_features = (aggregated_features - aggregated_features.min()) / (aggregated_features.max() - aggregated_features.min())
    #         self.features = Image.fromarray((normalized_features * 255).astype(np.uint8))
            
    #         return self.features

    def get_cqt_features(self):
        if self.data is not None:
            cqt = librosa.cqt(y=self.data, sr=self.sampling_rate)
            return librosa.amplitude_to_db(np.abs(cqt))
        return None

    def aggregate_features(self, features, window_size=100):
        return np.array([np.mean(features[:, i:i+window_size], axis=1) 
                        for i in range(0, features.shape[1], window_size)])
        
    def get_rhythm_features(self):
        # Tempo and beat features
        tempo, beat_frames = librosa.beat.beat_track(y=self.data, sr=self.sampling_rate)
        
        # Onset strength
        onset_env = librosa.onset.onset_strength(y=self.data, sr=self.sampling_rate)
        
        # Tempogram
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=self.sampling_rate)
        return tempo, beat_frames, tempogram
    
    def get_spectral_features(self):
        spectral_centroid = librosa.feature.spectral_centroid(y=self.data, sr=self.sampling_rate)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.data, sr=self.sampling_rate)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.data, sr=self.sampling_rate)
        return spectral_centroid, spectral_bandwidth, spectral_rolloff
    
    def get_chroma_features(self):
        chroma = librosa.feature.chroma_stft(y=self.data, sr=self.sampling_rate)
        return chroma
    
    def compare(self , hash_to_compare_with):
        hash_to_compare_with = imagehash.hex_to_hash(hash_to_compare_with)
        hamming_distance = self.hashing_result - hash_to_compare_with
        similarity_score = 1 - hamming_distance / len(self.hashing_result.hash.flatten())
        
        return similarity_score
    
    def load_audio(self, file_path):
        data, sample_rate = librosa.load(file_path, mono=True)
        self.data = data
        self.sampling_rate = sample_rate
    
    def mix_with_friend(self, friend, weight):
        if isinstance(friend,Audio):
            if friend.data is not None and self.data is not None:
                min_len = min(len(self.data), len(friend.data))
                audio_1 = self.data[:min_len]
                audio_2 = friend.data[:min_len]
                mixed_audio = weight * audio_1 + (1-weight) * audio_2
                data = deepcopy(mixed_audio)
                return data
            elif friend.data is not None:
                return deepcopy(friend.data) 
            elif self.data is not None:
                return deepcopy(self.data) 

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