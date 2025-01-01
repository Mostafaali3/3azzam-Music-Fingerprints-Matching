
# Shazam-Like Music Fingerprint Desktop App

A Desktop program for identifying music by analyzing fingerprints generated from song spectrograms. This tool mimics the functionality of Shazam, enabling efficient and accurate song recognition.

![Image Placeholder](assests/program%20laptop%20mockup.png)

## Table of Contents

- [Shazam-Like Music Fingerprint Desktop App](#shazam-like-music-fingerprint-desktop-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Program Preview](#program-preview)
  - [Program Demo](#program-demo)
  - [Installation](#installation)
  - [Usage](#usage)
  - [GUI Features](#gui-features)
  - [Workflow](#workflow)
    - [Hashing and Preparing Data](#hashing-and-preparing-data)
    - [Actual Program Usage](#actual-program-usage)
  - [Contributors ](#contributors-)

## Introduction

This project implements a music identification system using Digital Signal Processing (DSP) techniques. It fingerprints songs by extracting and hashing key features from their spectrograms. The program allows users to query music / vocal files and find the closest matches based on similarity scores.

## Features

- Generate spectrograms for music, vocals, and combined files.
- Extract and hash key spectrogram features into fingerprints.
- Efficiently search for and rank the closest matching songs in a repository.
- Generate similarity scores and display results in a sortable table.
- Mix two sound files with adjustable weights and treat the combination as a new file.

## Program Preview

![Image Placeholder](assests/program%20screenshot.png)

## Program Demo

[Watch Video](https://github.com/Mostafaali3/DSP-Music-Similarity-Matching/blob/main/assests/program_preview.mkv)

## Installation

1. Clone the repository:
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Download Repository Song Data:**

2. **Run the Application:**
    ```bash
    python main.py
    ```

3. **Steps in the GUI:**
   - Upload a single music file or two files from the data folder to start mixing them.
   - Adjust weights for combining two files.
   - Click the search button to find the closest top 5 matching songs.

## GUI Features

- **Similarity Results:** Tabular view with sortable similarity scores.
- **Weighted Mixing:** Mixing with adjustable slider.
- **File Explorer Integration:** Browse and upload songs conveniently.

## Workflow

### Hashing and Preparing Data

1. **Spectrogram Generation:**
   - Extract spectrograms for the first 30 seconds of each song.

2. **Feature Extraction and Hashing:**
   - Identify key features from each spectrogram.
   - Use perceptual hashing to create compact fingerprints.

### Actual Program Usage

1. **Music Matching:**
   - Compute similarity scores using fingerprints.
   - Rank and display matches in a GUI table.

2. **File Combination:**
   - Use a slider to set weight percentages for mixing two files.
   - Treat the combination as a new query for matching.

## Contributors <a name = "Contributors"></a>
<table>
  <tr>
    <td align="center">
    <a href="https://github.com/Mostafaali3" target="_black">
    <img src="https://avatars.githubusercontent.com/u/120139366?v=4" width="150px;" alt="Mostafa Ali"/>
    <br />
    <sub><b>Mostafa Ali</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/Youssef-Abo-El-Ela" target="_black">
    <img src="https://avatars.githubusercontent.com/u/125592387?v=4" width="150px;" alt="Youssef Aboelela"/>
    <br />
    <sub><b>Youssef Aboelela</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/karreemm" target="_black">
    <img src="https://avatars.githubusercontent.com/u/116344832?v=4" width="150px;" alt="Kareem Abdel Nabi"/>
    <br />
    <sub><b>Kareem Abdel Nabi</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/AhmedXAlDeeb" target="_black">
    <img src="https://avatars.githubusercontent.com/u/124098788?v=4" width="150px;" alt="Ahmed Al-Deeb"/>
    <br />
    <sub><b>Ahmed Al-Deeb</b></sub></a>
    </td>
      </tr>