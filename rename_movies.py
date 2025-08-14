import os
import re
import json
import shutil
import requests

from pathlib import Path
from difflib import SequenceMatcher

def clean_title(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'^backup_+', '', name)  # remove all backup_ prefixes
    name = re.sub(r'[\[\](){}]', '', name)  # remove brackets
    name = re.sub(r'[._\-]', ' ', name)  # normalize separators
    name = re.sub(r'\s+', ' ', name).strip()
    # remove common quality/format tags
    tags = [
        '1080p', '720p', 'WEB-DL', 'WEBRip', 'BluRay', 'BRRip', 'DVDRip', 'HDRip', 'x264', 'x265',
        'HEVC', 'AAC5.1', '10bit', '8CH', 'NF', 'YIFY', 'BONE', 'HIN', 'KAN', 'MAL', 'EXTENDED', 'IMAX',
        'AV1', 'PROPER', 'DDP5.1', 'Saon', 'Korean'
    ]
    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(tag) for tag in tags) + r')\b', re.IGNORECASE)
    name = pattern.sub('', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def get_best_match(title, api_key):
    url = f"http://www.omdbapi.com/?s={title}&apikey={api_key}"
    try:
        r = requests.get(url)
        data = r.json()
        if data.get("Response") == "True":
            best = None
            best_score = 0
            for result in data.get("Search", []):
                result_title = result.get("Title", '')
                score = SequenceMatcher(None, title.lower(), result_title.lower()).ratio()
                if score > best_score:
                    best = result
                    best_score = score
            if best:
                return f"{best['Title']} ({best['Year']})"
    except Exception as e:
        print(f"Error querying OMDb: {e}")
    return None

def rename_files_in_directory(directory, api_key, dry_run=True, include_loose=False):
    backup_log = []

    for root, dirs, files in os.walk(directory):
        if root == directory and not include_loose:
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ['.mkv', '.mp4', '.avi', '.srt']:
                continue
            original_path = os.path.join(root, file)
            cleaned = clean_title(file)
            temp_name = f"temp_{cleaned}{ext}"
            temp_path = os.path.join(root, temp_name)
            if not dry_run:
                try:
                    os.rename(original_path, temp_path)
                except Exception as e:
                    print(f"Failed to temporarily rename {file}: {e}")
                    continue
            else:
                temp_path = original_path

            omdb_title = get_best_match(cleaned, api_key)
            if omdb_title:
                final_name = f"{omdb_title}{ext}"
                final_path = os.path.join(root, final_name)
                if not dry_run:
                    try:
                        os.rename(temp_path, final_path)
                    except Exception as e:
                        print(f"Failed to rename {temp_name} to {final_name}: {e}")
                print(f"Would rename: {file} -> {final_name}" if dry_run else f"Renamed: {file} -> {final_name}")
                backup_log.append(f"{file} -> {final_name}")
            else:
                print(f"Could not find title for {file}")
                if not dry_run and temp_path != original_path:
                    os.rename(temp_path, original_path)  # revert temp name if match fails

    log_path = os.path.join(directory, "backup_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        for line in backup_log:
            f.write(f"{line}\n")

if __name__ == "__main__":
    api_key = "6b03617a"  # hardcoded API key

    print("--- Movie Renamer ---")
    directory = input("Enter the directory path: ").strip()
    include_loose = input("Include loose files in root directory? (y/n): ").strip().lower() == 'y'
    dry_run = input("Dry run (only preview changes)? (y/n): ").strip().lower() == 'y'

    rename_files_in_directory(directory, api_key, dry_run=dry_run, include_loose=include_loose)
