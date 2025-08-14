import os
import re
import argparse
import requests
from pathlib import Path

OMDB_API_KEY = "6b03617a"
OMDB_URL = "http://www.omdbapi.com/"

UNWANTED_KEYWORDS = [
    '1080p', '720p', '2160p', '480p',
    '10bit', '8bit', 'BluRay', 'WEBRip', 'HDRip',
    'BRRip', 'WEB-DL', 'x264', 'x265', 'HEVC',
    'H264', 'AAC', 'DD5.1', 'DVDRip', 'AVC',
    'PSA', 'YIFY', 'RARBG', 'EXTENDED', 'PROPER',
    'REMASTERED', 'CH', '-', '_'
]

def clean_title(raw):
    name = re.sub(r'[._]', ' ', raw)
    name = re.sub(r'\s+', ' ', name)
    for word in UNWANTED_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    return name.strip()

def fetch_omdb_title(raw_title):
    title_guess = clean_title(raw_title)
    params = {'t': title_guess, 'apikey': OMDB_API_KEY}
    try:
        response = requests.get(OMDB_URL, params=params, timeout=5)
        data = response.json()
        if data.get("Response") == "True":
            title = data.get("Title")
            year = data.get("Year")
            return f"{title} ({year})"
    except Exception as e:
        print(f"OMDb request failed for '{title_guess}': {e}")
    return None

def is_renamed(name):
    return bool(re.match(r'^.+ \(\d{4}\)$', name))

def rename_stuff(base_path, dry_run=False, verify_online=False):
    log = []

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path) or is_renamed(folder):
            print(f"Skipping: {folder}")
            continue

        movie_file = None
        subs = []

        for file in os.listdir(folder_path):
            file_lower = file.lower()
            if file_lower.endswith(('.mkv', '.mp4', '.avi')):
                movie_file = file
            elif file_lower.endswith('.srt'):
                subs.append(file)

        if not movie_file:
            print(f"No movie file found in: {folder}")
            continue

        raw_name = os.path.splitext(movie_file)[0]
        new_name = fetch_omdb_title(raw_name) if verify_online else clean_title(raw_name)
        if not new_name:
            print(f"Could not determine new name for {folder}. Skipping.")
            continue

        new_folder_path = os.path.join(base_path, new_name)
        if os.path.exists(new_folder_path):
            print(f"Target folder '{new_name}' already exists. Skipping.")
            continue

        print(f"\n==> Rename folder: '{folder}' → '{new_name}'")
        log.append(f"{folder} -> {new_name}")

        if not dry_run:
            os.rename(folder_path, new_folder_path)

            # Rename movie
            old_movie_path = os.path.join(new_folder_path, movie_file)
            new_movie_path = os.path.join(new_folder_path, new_name + Path(movie_file).suffix)
            os.rename(old_movie_path, new_movie_path)

            # Handle subtitles
            for sub in subs:
                if len(subs) > 1:
                    ans = input(f"Multiple subtitles found. Rename '{sub}' to match '{new_name}'? [y/N] ").lower()
                    if ans != 'y':
                        continue
                old_sub_path = os.path.join(new_folder_path, sub)
                new_sub_path = os.path.join(new_folder_path, new_name + '.srt')
                os.rename(old_sub_path, new_sub_path)

    if not dry_run and log:
        with open(os.path.join(base_path, 'rename_log.txt'), 'w', encoding='utf-8') as log_file:
            log_file.write("\n".join(log))
        print("\n📄 Log saved to rename_log.txt")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rename movie folders & files with optional online verification.")
    parser.add_argument('directory', help="Target base directory containing movie folders")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without renaming")
    parser.add_argument('--verify-online', action='store_true', help="Use OMDb API to fetch correct title/year")

    args = parser.parse_args()
    rename_stuff(args.directory, dry_run=args.dry_run, verify_online=args.verify_online)
