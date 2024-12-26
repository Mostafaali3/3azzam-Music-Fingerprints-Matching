import csv
from classes.audio import Audio
from copy import deepcopy

class Controller():
    def __init__(self, music_player_1, music_player_2,mixed_music_player, audio_1:Audio, audio_2:Audio, mixed_audio:Audio):
        self.audio_1 = audio_1
        self.audio_2 = audio_2
        self.mixed_audio = mixed_audio
        self.music_player_1 = music_player_1
        self.music_player_2 = music_player_2
        self.mixed_music_player = mixed_music_player
        self.search_list = []
        self.csv_data_similarity_index = []
        self.top_5_audio_instances_list = []
        
    def check_similarity(self):
        self.mixed_audio.hash_sound()
        csv_file_path = "hashed_music_files.csv"
        with open(csv_file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                similarity_index =self.mixed_audio.compare(row[1])
                self.csv_data_similarity_index.append((row[0],similarity_index ))
        
    def search_and_sort_most_similar(self):
        sorted_data = sorted(self.csv_data_similarity_index, key=lambda x: x[1], reverse=True)
        for idx in range(5):
            self.search_list.append(sorted_data[idx])
            
    def init_top_5(self):
        for idx in range(5):
            audio_obj = Audio()
            song_name = self.search_list[idx][0].split('.')[0]
            audio_obj.song_name = song_name
            audio_obj.load_audio(f'./data/{self.search_list[idx][0]}')
            self.top_5_audio_instances_list.append(audio_obj)
            # print(f'{song_name} --- {self.search_list[idx][1]}')
    
    def mix_audio(self, weight):
        new_data = self.audio_1.mix_with_friend(self.audio_2, weight)
        self.mixed_audio.data = deepcopy(new_data)
        self.mixed_audio.sampling_rate = max(self.audio_1.sampling_rate, self.audio_2.sampling_rate)
        self.mixed_music_player.loaded = True
        
    def search(self):
        self.search_list.clear()
        self.csv_data_similarity_index.clear()
        self.top_5_audio_instances_list.clear()
        self.check_similarity()
        self.search_and_sort_most_similar()
        self.init_top_5()
# Test
# cont = Controller(None, None , None ,None , None ,None)
# cont.import_csv_hash_data()