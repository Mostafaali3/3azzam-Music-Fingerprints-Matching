import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QVBoxLayout, QHBoxLayout, QFileDialog, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_function.compile_qrc import compile_qrc
from classes.controller import Controller
from classes.musicPlayer import MusicPlayer
from classes.audio import Audio
import sounddevice as sd
import librosa

compile_qrc()
from icons_setup.compiledIcons import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Music Similarity Analysis')
        self.setWindowIcon(QIcon('icons_setup/icons/logo.png'))

        self.play_icon = QIcon(':/icons_setup/icons/play.png')
        self.pause_icon = QIcon(':/icons_setup/icons/pause.png')

        self.table_play_icon = QIcon(':/icons_setup/icons/tablePlay.png')
        self.table_pause_icon = QIcon(':/icons_setup/icons/tablePause.png')

        # Find the tableFrame
        self.tableFrame = self.findChild(QFrame, 'tableFrame')
        if not self.tableFrame:
            print("Error: tableFrame not found in the UI file.")
            return
        
        self.no_matched_frame = self.findChild(QFrame , "noMatchedFrame")  
        self.tableFrame.hide() 
        self.table_songs_play_status = [False,False,False,False,False]
        self.table_play_buttons_list = []
        self.setup_table()
        self.init_table_play_buttons()

    def setup_table(self):

        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rank", "Song Name", "Matching %", "Controls"])

        self.table.verticalHeader().setVisible(False)


        # Style table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #142A4A;
                color: #ffffff;
                border: none;
                gridline-color: #39bef7;
                font-size: 16px;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 12px; /* Increased padding */
                border: none;
                margin: 4px; /* Adds spacing around each cell */
                border-radius: 6px;
            }
            QTableWidget::item:selected {
                background-color: #1e3a5f;
            }
            QHeaderView::section {
                background-color: #0f1729;
                color: #39bef7;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #39bef7;
                font-weight: bold;
                font-size: 15px;
                text-transform: uppercase;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QPushButton {
                background-color: #39bef7;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 8px 15px;
                min-width: 80px;
                font-weight: bold;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
            QScrollBar:vertical {
            background: #0f1729;
            width: 12px;
            border: none;
            margin: 2px 0 2px 0;
            border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #39bef7;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: #142A4A;
                height: 12px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #142A4A;
                height: 12px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #0f1729;
                border-radius: 6px;
            }
        """)

        # Configure columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 180)

        # Populate with dummy data
        dummy_data = [
            (1, "Bohemian Rhapsody - Queen", "98.5%"),
            (2, "Hotel California - Eagles", "95.2%"),
            (3, "Stairway to Heaven - Led Zeppelin", "92.8%"),
            (4, "Sweet Child O' Mine - Guns N' Roses", "90.1%"),
            (5, "Imagine - John Lennon", "88.7%"),
        ]

        for row, (rank, song, match) in enumerate(dummy_data):
            # Set row height
            self.table.setRowHeight(row, 100) 

            # Rank
            rank_item = QTableWidgetItem(str(rank))
            rank_item.setTextAlignment(Qt.AlignCenter)
            rank_item.setFlags(rank_item.flags() & ~Qt.ItemIsEditable)  
            self.table.setItem(row, 0, rank_item)

            # Song name
            song_item = QTableWidgetItem(song)
            song_item.setFlags(song_item.flags() & ~Qt.ItemIsEditable)  
            self.table.setItem(row, 1, song_item)

            # Match percentage
            match_item = QTableWidgetItem(match)
            match_item.setTextAlignment(Qt.AlignCenter)
            match_item.setFlags(match_item.flags() & ~Qt.ItemIsEditable)  
            self.table.setItem(row, 2, match_item)

            play_btn = QPushButton()
            play_btn.setIcon(QIcon(":/icons_setup/icons/tablePlay.png"))
            play_btn.setIconSize(QtCore.QSize(15, 15))

            # Create container frame
            container = QFrame()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(play_btn, alignment=Qt.AlignCenter)

            self.table.setCellWidget(row, 3, container)

        self.tableFrame.layout().addWidget(self.table)
        

        self.browse_audio_1 = self.findChild(QPushButton, "browseSong1")
        self.browse_audio_2 = self.findChild(QPushButton, "pushButton")
        self.browse_audio_1.clicked.connect(lambda : self.browse_audio(1))
        self.browse_audio_2.clicked.connect(lambda : self.browse_audio(2))
        
        self.audio_1 = Audio()
        self.audio_2 = Audio()
        self.mixed_audio = Audio()
        
        self.progressbarSong1 = self.findChild(QSlider, 'progressbarSong1')
        self.progressbarSong2 = self.findChild(QSlider, 'progressbarSong2')
        self.progressbarSong3 = self.findChild(QSlider, 'progressbarSong3')

        self.playPauseSong1 = self.findChild(QPushButton, 'playPauseSong1')
        self.playPauseSong2 = self.findChild(QPushButton, 'playPauseSong2')
        self.playPauseSong3 = self.findChild(QPushButton, 'playPauseSong3')

        self.replaySong1 = self.findChild(QPushButton, 'replaySong1')
        self.replaySong2 = self.findChild(QPushButton, 'replaySong2')
        self.replaySong3 = self.findChild(QPushButton, 'replaySong3')
        
        self.music_player_1 = MusicPlayer(self.audio_1, self.progressbarSong1, self.playPauseSong1, self.replaySong1, self.play_icon, self.pause_icon)
        self.music_player_2 = MusicPlayer(self.audio_2, self.progressbarSong2, self.playPauseSong2, self.replaySong2, self.play_icon, self.pause_icon)
        self.mixed_music_player = MusicPlayer(self.mixed_audio, self.progressbarSong3, self.playPauseSong3, self.replaySong3, self.play_icon, self.pause_icon)

        
        self.controller = Controller(self.music_player_1, self.music_player_2, self.mixed_music_player, self.audio_1, self.audio_2, self.mixed_audio)
        
        
        self.mixer_frame = self.findChild(QFrame, "mixerFrame")
        self.mixer_frame.hide()
        self.mixer_error_frame = self.findChild(QFrame, "errorFrame")
        
        self.weight_slider = self.findChild(QSlider, "mixerSlider")
        self.weight_slider.valueChanged.connect(lambda : self.handle_slider_values())
        
        self.search_button = self.findChild(QPushButton, "searchButton")
        self.search_button.clicked.connect(self.update_table)
        self.music_name_label_1 = self.findChild(QLabel, "label")
        self.music_name_label_2 = self.findChild(QLabel, "label_2")
        self.audio_1_weight_label = self.findChild(QLabel, "song1Percentage")
        self.audio_2_weight_label = self.findChild(QLabel, "song2Percentage")
        

    def browse_audio(self, player_number):
        file_path, _ = QFileDialog.getOpenFileName(self,'Open File','', 'WAV Files (*.wav)')
        if file_path.endswith('.wav'):
            if player_number == 1:
                self.audio_1.load_audio(file_path)
                self.music_player_1.loaded = True
                if file_path:
                    self.music_name_label_1.setText((file_path.split('/')[-1]).split('.')[0])
            else:
                self.audio_2.load_audio(file_path)
                self.music_player_2.loaded = True
                if file_path:   
                    self.music_name_label_2.setText((file_path.split('/')[-1]).split('.')[0])
            self.handle_mixer_frame()

    def handle_slider_values(self):
        self.controller.mix_audio(self.weight_slider.value()/100)
        self.audio_1_weight_label.setText(f"{self.weight_slider.value()}%")
        self.audio_2_weight_label.setText(f"{100 - self.weight_slider.value()}%")
    
    def handle_mixer_frame(self):
        if self.music_player_1.loaded and self.music_player_2.loaded:
            self.mixer_frame.show()
            self.mixer_error_frame.hide()
            
    def update_table(self):
        self.controller.mix_audio(self.weight_slider.value()/100)
        self.no_matched_frame.hide()
        self.tableFrame.show()
        self.controller.search()
        for row_idx in range(5):
            song_name = QTableWidgetItem(self.controller.top_5_audio_instances_list[row_idx].song_name)
            song_name.setFlags(song_name.flags() & ~Qt.ItemIsEditable)  
            song_similarity_index = QTableWidgetItem(f'{self.controller.search_list[row_idx][1] * 100:.1f}%')
            song_similarity_index.setFlags(song_similarity_index.flags() & ~Qt.ItemIsEditable)  
            self.table.setItem(row_idx , 1 , song_name)
            self.table.setItem(row_idx , 2 ,song_similarity_index )
            
    def init_table_play_buttons(self):
        for row_idx in range(5):
            container = self.table.cellWidget(row_idx, 3)  
            if container:  
                play_btn = container.findChild(QPushButton)  
                if play_btn:  
                    self.table_play_buttons_list.append(play_btn)
                    play_btn.clicked.connect(lambda _,row_index = row_idx:self.table_play_button_clicked(row_index))
        
    
    def table_play_button_clicked(self , row_idx):
        play_btn = self.table_play_buttons_list[row_idx]
        if (self.table_songs_play_status[row_idx] == False):
            self.table_songs_play_status[row_idx] = True
            song_name = self.controller.top_5_audio_instances_list[row_idx].song_name
            song_data , sr = librosa.load(f'./data/{song_name}.wav')
            sd.play(song_data , sr)
            play_btn.setIcon(QIcon(":/icons_setup/icons/tablePause.png"))
        else:
            self.table_songs_play_status[row_idx] = False
            sd.stop()
            play_btn.setIcon(QIcon(":/icons_setup/icons/tablePlay.png"))
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())