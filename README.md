# YouTube Audio Downloader

A simple command-line tool to download YouTube videos as audio files using [yt-dlp](https://github.com/yt-dlp/yt-dlp) that I use to download audiobooks.

## Features

- Downloads audio in native format (Opus/WebM) - no conversion needed
- Smaller file sizes and faster downloads
- Simple CLI interface
- Customizable output directory
- **Batch downloading** with parallel downloads support
- Read URLs from a text file

## Requirements

- Python 3.7+
- yt-dlp

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/achen2304/youtube-audio-downloader.git
   cd youtube-converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:

```bash
python youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Specify output directory:

```bash
python youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID" -o "/path/to/output"
```

Use a subdirectory:

```bash
python youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID" -d "subfolder"
```

### Options

| Option         | Description                                   |
| -------------- | --------------------------------------------- |
| `-o, --output` | Full output directory path                    |
| `-d, --dir`    | Subdirectory within the default output folder |

## Batch Downloading

Use `batch_download.py` to download multiple videos in parallel.

Download multiple URLs:

```bash
python batch_download.py "URL1" "URL2" "URL3"
```

Download from a text file (one URL per line):

```bash
python batch_download.py -f urls.txt
```

Control the number of parallel downloads:

```bash
python batch_download.py -f urls.txt -w 5
```

### Batch Options

| Option          | Description                                   |
| --------------- | --------------------------------------------- |
| `-f, --file`    | Read URLs from a text file                    |
| `-o, --output`  | Full output directory path                    |
| `-d, --dir`     | Subdirectory within the default output folder |
| `-w, --workers` | Number of parallel downloads (default: 3)     |

## License

MIT License
