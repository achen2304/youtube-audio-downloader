#!/usr/bin/env python3
"""
YouTube Audio Downloader CLI
Downloads YouTube videos as audio files in native format (Opus/WebM) using yt-dlp.
No conversion needed - smaller files and faster downloads!
"""

import sys
import os
import argparse
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


def download_audio(url, output_path=None):
    """
    Download a YouTube video as audio in native format.

    Args:
        url: YouTube video URL
        output_path: Directory to save the audio file (default: I:\audiobooks)
    """
    if output_path is None:
        output_path = r"I:\audiobooks"

    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Downloads best available audio (usually Opus/WebM)
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nDownloading audio: {url}")
            ydl.download([url])
            print("\nDownload complete!")

    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos as audio files (native format - Opus/WebM)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_to_mp3.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python youtube_to_mp3.py "https://youtu.be/dQw4w9WgXcQ" -d "scifi"
  python youtube_to_mp3.py "https://youtu.be/dQw4w9WgXcQ" -o "C:\\Music"
        """
    )

    parser.add_argument(
        'url',
        help='YouTube video URL'
    )

    parser.add_argument(
        '-o', '--output',
        help='Full output directory path',
        default=None
    )

    parser.add_argument(
        '-d', '--dir',
        help='Subdirectory within I:\\audiobooks (e.g., "scifi" -> "I:\\audiobooks\\scifi")',
        default=None
    )

    args = parser.parse_args()

    # Validate URL
    if not ('youtube.com' in args.url or 'youtu.be' in args.url):
        print("Error: Please provide a valid YouTube URL")
        sys.exit(1)

    # Determine output path
    if args.output and args.dir:
        print("Error: Cannot use both -o and -d flags together")
        sys.exit(1)

    output_path = None
    if args.output:
        output_path = args.output
    elif args.dir:
        output_path = os.path.join(r"I:\audiobooks", args.dir)

    download_audio(args.url, output_path)


if __name__ == '__main__':
    main()
