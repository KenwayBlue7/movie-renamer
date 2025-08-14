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
    # Replace separators with space
    name = re.sub(r'[._]', ' ', name)

    # Find year (between 1900 and 2099)
    year_match = re.search(r'(19|20)\d{2}', name)
    year = year_match.group(0) if year_match else ''

    if year:
        name = name[:name.find(year)].strip() + f' ({year})'

    # Remove unwanted keywords
    for word in UNWANTED_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def rename_folders_and_files(base_dir):
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            # Find first video file in the folder
            movie_file = None
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.mkv', '.mp4', '.avi')):
                    movie_file = file
                    break

            if movie_file:
                cleaned_name = clean_movie_name(movie_file)
                new_folder_path = os.path.join(base_dir, cleaned_name)
                new_movie_file_path = os.path.join(new_folder_path, cleaned_name + Path(movie_file).suffix)

                # Rename folder
                os.rename(folder_path, new_folder_path)

                # Rename movie file
                old_movie_path = os.path.join(new_folder_path, movie_file)
                os.rename(old_movie_path, new_movie_file_path)

                print(f'Renamed: {folder} -> {cleaned_name}')

if __name__ == '__main__':
    rename_folders_and_files(BASE_DIR)
