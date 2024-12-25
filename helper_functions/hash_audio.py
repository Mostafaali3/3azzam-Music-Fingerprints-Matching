import librosa
import numpy as np
from PIL import Image
import imagehash

def hash_spectrograms(file_path, hash_func=imagehash.phash):
    
    y, sr = librosa.load(file_path, sr=None, mono=True)
    
    # S = librosa.stft(y, n_fft=2048, hop_length=512)
    # S_magnitude, _ = librosa.magphase(S)  
    # S_dB = librosa.amplitude_to_db(S_magnitude, ref=np.max)
    
    S_mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=sr//2)
    S_dB = librosa.power_to_db(S_mel, ref=np.max)

    
    main_spectrogram_image = (255 * (S_dB - np.min(S_dB)) / (np.max(S_dB) - np.min(S_dB))).astype(np.uint8)
    main_spectrogram_pil = Image.fromarray(main_spectrogram_image)
    
    # main_spectrogram_hash = hash_func(main_spectrogram_pil)
    
    
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_normalized = (255 * (mfccs - np.min(mfccs)) / (np.max(mfccs) - np.min(mfccs))).astype(np.uint8)
    mfccs_image = Image.fromarray(mfccs_normalized)
    
    
    total_height = main_spectrogram_pil.height + mfccs_image.height
    stacked_width = max(main_spectrogram_pil.width, mfccs_image.width)
    stacked_image = Image.new("L", (stacked_width, total_height))
    stacked_image.paste(main_spectrogram_pil, (0, 0))
    stacked_image.paste(mfccs_image, (0, main_spectrogram_pil.height))
    stacked_image_hash = hash_func(stacked_image)

    # mfccs_hash = hash_func(mfccs_image)
    
    # return main_spectrogram_hash, mfccs_hash
    return stacked_image_hash

wav_file = "./data/Nina Cried Power [original].wav"  
wav_file2 = "./data/Nina Cried Power [vocals].wav"  
main_hash = hash_spectrograms(wav_file)
new_hash = hash_spectrograms(wav_file2)
hamming_distance = main_hash - new_hash
similarity_score = 1 - hamming_distance / len(main_hash.hash.flatten())

print(f"Hamming Distance: {hamming_distance}")
print(f"Similarity Score: {similarity_score:.2f}")


# main_hash, mfcc_hash = hash_spectrograms(wav_file)
# print("Main Spectrogram Hash:", main_hash)
# print("MFCCs Spectrogram Hash:", mfcc_hash)
