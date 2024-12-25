import librosa
import numpy as np
from PIL import Image
import imagehash

def hash_spectrograms(file_path, hash_func=imagehash.phash):
    
    y, sr = librosa.load(file_path, sr=None, mono=True)
    
    S = librosa.stft(y, n_fft=2048, hop_length=512)
    S_magnitude, _ = librosa.magphase(S)  
    S_dB = librosa.amplitude_to_db(S_magnitude, ref=np.max)
    
    main_spectrogram_image = (255 * (S_dB - np.min(S_dB)) / (np.max(S_dB) - np.min(S_dB))).astype(np.uint8)
    main_spectrogram_pil = Image.fromarray(main_spectrogram_image)
    
    main_spectrogram_hash = hash_func(main_spectrogram_pil)
    
    
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_normalized = (255 * (mfccs - np.min(mfccs)) / (np.max(mfccs) - np.min(mfccs))).astype(np.uint8)
    mfccs_image = Image.fromarray(mfccs_normalized)
    

    mfccs_hash = hash_func(mfccs_image)
    
    return main_spectrogram_hash, mfccs_hash

wav_file = "./data/Alkanas(vocals).wav"  
main_hash, mfcc_hash = hash_spectrograms(wav_file)
print("Main Spectrogram Hash:", main_hash)
print("MFCCs Spectrogram Hash:", mfcc_hash)
