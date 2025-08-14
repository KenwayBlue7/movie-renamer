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
    'Korean', 'AV1Saon', '-', '-[YTS AM]', 'NF', 'DDP5 1', 'Pahe in',
    'ZEE5', '8CH', 'AA', 'BONE'
]

BASE_DIR = r'G:\Movies\Watchlist\Requiem for a Dream DIRECTORS CUT (2000)'

def clean_movie_name(name: str) -> str:
    name = re.sub(r'[._]', ' ', name)

    years = re.findall(r'\b(?:19|20)\d{2}\b', name)
    year = years[-1] if years else ''

    for word in UNWANTED_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    name = re.sub(r'\s+', ' ', name).strip()

    if year and f'({year})' not in name:
        name = re.sub(rf'\b{year}\b(?!.*\b{year}\b)', f'({year})', name)

    return name.strip()

def is_already_renamed(name: str) -> bool:
    return bool(re.match(r'^.+ \(\d{4}\)$', name))

def final_clean_name(name: str) -> str:
    base = Path(name).stem
    ext = Path(name).suffix

    for word in UNWANTED_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        base = re.sub(pattern, '', base, flags=re.IGNORECASE)

    base = base.replace('-', ' ')
    base = re.sub(r'\s+', ' ', base).strip()

    return f"{base}{ext}" if ext else base

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

    # Handle loose movie files
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.mkv', '.mp4', '.avi')):
            cleaned_name = clean_movie_name(file)
            new_file_path = os.path.join(base_dir, cleaned_name + Path(file).suffix)
            os.rename(file_path, new_file_path)
            print(f"Renamed loose file: {file} -> {Path(new_file_path).name}")

    # Second pass: Clean all leftover junk, even inside renamed folders
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            if name.lower().endswith(('.mkv', '.mp4', '.avi', '.srt')):
                old_path = os.path.join(root, name)
                cleaned = final_clean_name(name)
                new_path = os.path.join(root, cleaned)
                if cleaned != name:
                    os.rename(old_path, new_path)
                    print(f"Cleaned leftover: {name} -> {cleaned}")

if __name__ == '__main__':
    rename_folders_and_files(BASE_DIR)
