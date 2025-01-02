import os
import csv
from classes.audio import Audio
import librosa

data_folder = "./data"
output_csv = "hashed_music_files.csv"

results = []
i = 0
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    if os.path.isfile(file_path):
        print(i)
        audio_data , audio_sr = librosa.load(file_path , mono=True)
        audio_obj = Audio()
        audio_obj.data = audio_data
        # audio_obj.preprocess_data()
        # audio_obj.get_features()
        audio_obj.hash_sound()
        hash_result = audio_obj.hashing_result
        results.append([file_name, hash_result])
        i += 1

with open(output_csv, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File Name", "Hash"])
    writer.writerows(results)

print(f"Hash results saved to {output_csv}")
import os
import csv
from classes.audio import Audio
import librosa

data_folder = "./data"
output_csv = "hashed_music_files.csv"

results = []
i = 0
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    if os.path.isfile(file_path):
        print(i)
        audio_data , audio_sr = librosa.load(file_path , mono=True)
        audio_obj = Audio()
        audio_obj.data = audio_data
        audio_obj.preprocess_data()
        audio_obj.get_features()
        audio_obj.hash_sound()
        hash_result = audio_obj.hashing_result
        results.append([file_name, hash_result])
        i += 1

with open(output_csv, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File Name", "Hash"])
    writer.writerows(results)

print(f"Hash results saved to {output_csv}")
