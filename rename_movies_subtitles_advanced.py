import os
import re
from pathlib import Path

# Keywords to remove from movie file names
UNWANTED_KEYWORDS = [
    '1080p', '720p', '2160p', '480p', '10bit', '8bit',
    'BluRay', 'WEBRip', 'HDRip', 'BRRip', 'WEB-DL',
    'x264', 'x265', 'HEVC', 'H264', 'AAC', 'DD5.1',
    'DVDRip', 'AVC', 'PSA', 'YIFY', 'RARBG', 'EXTENDED',
    'PROPER', 'REMASTERED', 'CH', 'mp4', 'mkv', 'avi',
    'Korean', 'AV1Saon', '-', '-[YTS AM]', 'NF', 'DDP5 1', 'Pahe in', '_'
]

BASE_DIR = r'D:\Movies\trial'

def clean_movie_name(name: str) -> str:
    name = re.sub(r'[._]', ' ', name)

    # Find all 4-digit years
    years = re.findall(r'\b(19|20)\d{2}\b', name)
    all_years = re.findall(r'\b(?:19|20)\d{2}\b', name)
    year = ''

    if all_years:
        year = all_years[-1] if len(all_years) > 1 else all_years[0]

    # Remove unwanted keywords
    for word in UNWANTED_KEYWORDS:
        pattern = re.escape(word)
        name = re.sub(r'\b' + pattern + r'\b', '', name, flags=re.IGNORECASE)

    name = re.sub(r'\s+', ' ', name).strip()

    # Add year in parentheses if found
    if year:
        # Remove the last occurrence of the year from the name
        name = re.sub(r'\b' + year + r'\b', '', name).strip()
        name += f' ({year})'

    return name.strip()

def is_already_renamed(name: str) -> bool:
    return bool(re.match(r'^.+ \(\d{4}\)$', name))

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

                os.rename(folder_path, new_folder_path)

                old_movie_path = os.path.join(new_folder_path, movie_file)
                new_movie_path = os.path.join(new_folder_path, cleaned_name + Path(movie_file).suffix)
                os.rename(old_movie_path, new_movie_path)

                if subtitle_file:
                    old_sub_path = os.path.join(new_folder_path, subtitle_file)
                    new_sub_path = os.path.join(new_folder_path, cleaned_name + '.srt')
                    os.rename(old_sub_path, new_sub_path)

                print(f"Renamed: {folder} -> {cleaned_name}")
            else:
                print(f"No movie file found in: {folder_path}")

    # Handle loose files in base_dir
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.mkv', '.mp4', '.avi')):
            cleaned_name = clean_movie_name(file)
            new_file_path = os.path.join(base_dir, cleaned_name + Path(file).suffix)
            os.rename(file_path, new_file_path)
            print(f"Renamed loose file: {file} -> {Path(new_file_path).name}")

if __name__ == '__main__':
    rename_folders_and_files(BASE_DIR)
