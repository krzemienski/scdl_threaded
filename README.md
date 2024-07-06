# SoundCloud Playlist Downloader

This script allows you to download tracks from SoundCloud playlists or users in parallel using SCDL and Python. By utilizing multi-threading, the download process is significantly faster compared to downloading each track sequentially. The script also includes robust logging to track the progress and bandwidth of each download.

## Requirements

- Python 3.x
- SCDL (SoundCloud Downloader)

## Installation

1. Install Python 3.x if you haven't already.
2. Install SCDL using pip:

    ```bash
    pip install scdl
    ```

3. Clone this repository or download the script directly.

## Usage

1. **Set up the environment:**

    Make sure SCDL is properly installed and configured on your system. You can check if SCDL is working by running:

    ```bash
    scdl -h
    ```

2. **Run the script:**

    ```bash
    python scdl_threaded.py <url> --threads <num_threads> --output_dir <output_directory> --archive_file <archive_file> --debug
    ```

    - `<url>`: The URL of the SoundCloud playlist or user you want to download.
    - `--threads <num_threads>`: (Optional) Number of parallel threads for downloading tracks. Default is 4.
    - `--output_dir <output_directory>`: (Optional) Base directory to save downloaded tracks. Default is `./downloads`.
    - `--archive_file <archive_file>`: (Optional) File to keep track of downloaded tracks. Default is `archive.txt`.
    - `--debug`: (Optional) Enable debug logging.

## Example

Below are examples of how to use the script:

1. To download a playlist:

    ```bash
    python scdl_threaded.py "https://soundcloud.com/artist/sets/playlist" --threads 6 --output_dir "./my_downloads" --archive_file "archive.txt" --debug
    ```

2. To download all tracks from a user:

    ```bash
    python scdl_threaded.py "https://soundcloud.com/artist" --threads 6 --output_dir "./my_downloads" --archive_file "archive.txt" --debug
    ```

    The script will download the tracks in parallel, save them to the specified output directory, and log the progress and bandwidth.

## Customization

- **Output Directory:** Use the `--output_dir` argument to set a different base directory for downloaded tracks. The script will create subdirectories for each user or playlist.
- **Max Workers:** Use the `--threads` argument to control the number of parallel downloads. The default is 4.
- **Archive File:** Use the `--archive_file` argument to specify a file for keeping track of downloaded tracks to avoid re-downloading.
- **Debug Logging:** Use the `--debug` argument to enable debug logging for more detailed output.

## Troubleshooting

- Ensure SCDL is installed and working correctly.
- Check the URLs for correctness.
- Make sure you have the necessary permissions to create and write to the output directory.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome
.
