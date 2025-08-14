# Movie & TV Show Renamer Scripts

This project is a collection of Python scripts designed to **automate the cleaning and renaming of movie and TV show files and their parent folders**. If your media library is cluttered with messy filenames like `The.Movie.Title.2023.1080p.BluRay.x264-SOMEGROUP`, these scripts will standardize them into a clean, human-readable format like `The Movie Title (2023)`.

This is essential for maintaining a tidy media collection and is especially useful for media servers like **Plex, Jellyfin, or Kodi**, which rely on a clean naming convention to correctly identify and fetch metadata for your library.

-----

## \#\# Key Features

  * **Standardized Naming**: Renames files and folders to the clean `Movie Title (Year)` format.
  * **Junk Removal**: Automatically detects and removes a wide range of unwanted keywords, such as resolution (`1080p`, `720p`), source (`BluRay`, `WEBRip`), release group (`YIFY`, `RARBG`), and other clutter.
  * **Intelligent Parsing**: Uses regular expressions to reliably extract the movie title and year from the original messy filename.
  * **Subtitle Support**: Automatically finds and renames associated subtitle files (`.srt`) to match the new movie filename.
  * **Online Verification (Advanced)**: Optionally uses the **OMDb API** to fetch the official movie title and year, ensuring the highest level of accuracy.
  * **Safe Execution**: Includes a **`--dry-run`** mode that lets you preview all proposed changes without actually renaming any files.
  * **Change Logging**: Generates a log file (`rename_log.txt` or `backup_log.txt`) that records all the renaming operations for easy tracking.
  * **Efficiency**: The scripts are designed to automatically skip any files or folders that are already named correctly, saving time on subsequent runs.

-----

## \#\# How It Works

The scripts employ two main strategies for renaming your media:

1.  **Local Cleaning (Default Method)**: This is the fastest method. The script parses the existing filename, removes all the predefined junk keywords, normalizes separators (like `.` and `_` to spaces), and identifies the year. It then reconstructs the name in the standard `Title (Year)` format.

2.  **Online Verification (Optional Method)**: For maximum accuracy, you can enable this mode. The script first performs a local clean to create a best-guess title. It then sends this title to the OMDb (The Open Movie Database) API. OMDb returns the official title and year, which the script then uses for the final name. This is great for correcting misspelled titles or movies with complex names.

-----

## \#\# Getting Started

While there are several script versions in this project, the most powerful and flexible one is **`rename_movies_advanced.py`**.

### \#\#\# 1. Prerequisites

  * **Python 3**: Make sure you have Python 3 installed.
  * **requests Library**: This is required for the online verification feature. You can install it via pip:
    ```bash
    pip install requests
    ```

### \#\#\# 2. Configuration

Before running the script, you'll need a **free API key from OMDb**.

1.  Visit [**http://www.omdbapi.com/apikey.aspx**](http://www.omdbapi.com/apikey.aspx) and get your free API key.
2.  Open the `rename_movies_advanced.py` file and replace the placeholder key with your own:
    ```python
    OMDB_API_KEY = "your_key_here" # Replace with your actual OMDb API key
    ```

### \#\#\# 3. Usage

The script is run from your terminal or command line.

  * **To preview changes (Dry Run)**:
    This is the **safest** way to start. It will print out what it *would* do without changing anything.

    ```bash
    python rename_movies_advanced.py "/path/to/your/movies" --dry-run
    ```

  * **To rename using Local Cleaning**:
    This will perform the renaming based on the existing filenames.

    ```bash
    python rename_movies_advanced.py "/path/to/your/movies"
    ```

  * **To rename using OMDb Verification**:
    This is the recommended method for the best results. It will contact OMDb to get accurate names.

    ```bash
    python rename_movies_advanced.py "/path/to/your/movies" --verify-online
    ```

-----

## \#\# Script Variants

This project contains multiple scripts that represent the evolution of the tool. While `rename_movies_advanced.py` is the most feature-rich, the others are simpler and can be useful for basic tasks:

  * **`rename_movies_basic.py`**: A minimal script for renaming movie folders and files based on local cleaning.
  * **`rename_movies_subtitles.py`**: A basic version that adds support for renaming `.srt` subtitle files.
  * **`rename_movies.py`**: An interactive version that prompts the user for inputs and uses the OMDb API.

> **Disclaimer**: Always back up your data before running any file modification script. Start with the `--dry-run` flag to ensure the results are what you expect.
