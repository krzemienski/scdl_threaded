import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to download a single track using SCDL
def download_track(track_url, output_dir, archive_file):
    start_time = time.time()
    try:
        command = ["scdl", "-l", track_url, "-o", output_dir, "--download-archive", archive_file, "--extract-artist", "--flac", "--no-original"]

        logging.info(f"Executing command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stderr.read(1)
            if output == '' and process.poll() is not None:
                break
            if output:
                logging.info(output.strip())

        end_time = time.time()
        elapsed_time = end_time - start_time
        return f"Successfully downloaded: {track_url} in {elapsed_time:.2f} seconds"
    except subprocess.CalledProcessError as e:
        return f"Error downloading {track_url}: {e}"

# Function to download a list of tracks in parallel
def download_playlist(track_urls, output_dir, archive_file, max_workers=4):
    os.makedirs(output_dir, exist_ok=True)

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_track, url, output_dir, archive_file): url for url in track_urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(f"Error downloading {url}: {e}")

    return results

def get_playlist_tracks(playlist_url):
    try:
        command = ["scdl", "--url", playlist_url, "--only", "url", "--download-archive", "archive.txt", "--extract-artist", "--flac", "--no-original"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving playlist tracks: {e}")
        return []

def get_user_tracks(user_url):
    try:
        command = ["scdl", "-c", "-l", user_url, "--only", "url", "--download-archive", "archive.txt", "--extract-artist", "--flac", "--no-original"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving user tracks: {e}")
        return []

# Argument parser setup
parser = argparse.ArgumentParser(description="Download SoundCloud playlist or user tracks in parallel.")
parser.add_argument("url", type=str, help="The URL of the SoundCloud playlist or user.")
parser.add_argument("--threads", type=int, default=4, help="Number of parallel threads for downloading tracks.")
parser.add_argument("--output_dir", type=str, default="./downloads", help="Base directory to save downloaded tracks.")
parser.add_argument("--archive_file", type=str, default="archive.txt", help="File to keep track of downloaded tracks.")
parser.add_argument("--debug", action='store_true', help="Enable debug logging.")

args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    url = args.url
    output_base_dir = args.output_dir
    max_workers = args.threads
    archive_file = args.archive_file

    if "soundcloud.com" in url:
        if "/sets/" in url:
            # It's a playlist
            playlist_name = re.findall(r"sets/([^/]+)", url)[0]
            output_dir = os.path.join(output_base_dir, playlist_name)
            track_urls = get_playlist_tracks(url)
        else:
            # It's a user
            user_name = re.findall(r"soundcloud.com/([^/]+)", url)[0]
            output_dir = os.path.join(output_base_dir, user_name)
            track_urls = get_user_tracks(url)

        if track_urls:
            download_results = download_playlist(track_urls, output_dir, archive_file, max_workers=max_workers)

            for result in download_results:
                logging.info(result)
        else:
            logging.info("No tracks found for the given URL.")
    else:
        logging.error("Invalid SoundCloud URL.")
