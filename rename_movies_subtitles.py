import os
import re
from pathlib import Path

# Keywords to remove from movie file names
UNWANTED_KEYWORDS = [
    '1080p', '720p', '2160p', '480p',
    '10bit', '8bit', 'BluRay', 'WEBRip', 'HDRip',
    'BRRip', 'WEB-DL', 'x264', 'x265', 'HEVC',
    'H264', 'AAC', 'DD5.1', 'DVDRip', 'AVC',
    'PSA', 'YIFY', 'RARBG', 'EXTENDED', 'PROPER',
    'REMASTERED', 'CH', '-', '_'
]

# Your target directory here
BASE_DIR = r'D:\Movies\trial'

def clean_movie_name(name: str) -> str:
    name = re.sub(r'[._]', ' ', name)

    # Find year (1900–2099)
    year_match = re.search(r'(19|20)\d{2}', name)
    year = year_match.group(0) if year_match else ''

    if year:
        name = name[:name.find(year)].strip() + f' ({year})'

    for word in UNWANTED_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    return re.sub(r'\s+', ' ', name).strip()

def is_already_renamed(folder_name: str) -> bool:
    return bool(re.match(r'^.+ \(\d{4}\)$', folder_name))

def rename_folders_and_files(base_dir):
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            if is_already_renamed(folder):
                print(f"Skipping already renamed folder: {folder}")
                continue

            movie_file = None
            subtitle_file = None

            for file in os.listdir(folder_path):
                if file.lower().endswith(('.mkv', '.mp4', '.avi')):
                    movie_file = file
                elif file.lower().endswith('.srt'):
                    subtitle_file = file

            if movie_file:
                cleaned_name = clean_movie_name(movie_file)
                new_folder_path = os.path.join(base_dir, cleaned_name)

                # Rename folder
                os.rename(folder_path, new_folder_path)

                # Rename movie file
                old_movie_path = os.path.join(new_folder_path, movie_file)
                new_movie_path = os.path.join(new_folder_path, cleaned_name + Path(movie_file).suffix)
                os.rename(old_movie_path, new_movie_path)

                # Rename subtitle file if exists
                if subtitle_file:
                    old_subtitle_path = os.path.join(new_folder_path, subtitle_file)
                    new_subtitle_path = os.path.join(new_folder_path, cleaned_name + '.srt')
                    os.rename(old_subtitle_path, new_subtitle_path)

                print(f"Renamed: {folder} -> {cleaned_name}")
            else:
                print(f"No movie file found in: {folder}")

if __name__ == '__main__':
    rename_folders_and_files(BASE_DIR)
