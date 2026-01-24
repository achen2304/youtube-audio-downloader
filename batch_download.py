#!/usr/bin/env python3
"""
YouTube Batch Audio Downloader
Downloads multiple YouTube videos as audio files in parallel.
"""

import sys
import os
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


def download_single_audio(url, output_path, index, total):
    """
    Download a single YouTube video as audio.

    Args:
        url: YouTube video URL
        output_path: Directory to save the audio file
        index: Current download index (for progress tracking)
        total: Total number of downloads

    Returns:
        Tuple of (url, success, error_message)
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,  # Suppress yt-dlp output for cleaner batch processing
        'no_warnings': True,
        # Timeout and retry settings for large files
        'socket_timeout': 30,  # Socket timeout in seconds
        'retries': 10,  # Number of retries for failed fragments
        'fragment_retries': 10,  # Retries for each fragment
        'file_access_retries': 3,  # Retries for file access issues
        'extractor_retries': 3,  # Retries for extractor
        # Connection settings
        'http_chunk_size': 10485760,  # 10MB chunks for better handling of large files
        'concurrent_fragment_downloads': 5,  # Download multiple fragments simultaneously
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            print(f"[{index}/{total}] Downloading: {title}")
            ydl.download([url])
            print(f"[{index}/{total}] ✓ Complete: {title}")
            return (url, True, None)
    except Exception as e:
        print(f"[{index}/{total}] ✗ Error: {url} - {str(e)}")
        return (url, False, str(e))


def download_batch(urls, output_path, max_workers=3):
    """
    Download multiple videos in parallel.

    Args:
        urls: List of YouTube URLs
        output_path: Directory to save audio files
        max_workers: Maximum number of parallel downloads (default: 3)
    """
    total = len(urls)
    print(f"\nStarting batch download of {total} video(s)")
    print(f"Output directory: {output_path}")
    print(f"Parallel downloads: {max_workers}\n")

    results = {'success': [], 'failed': []}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_url = {
            executor.submit(download_single_audio, url, output_path, i+1, total): url
            for i, url in enumerate(urls)
        }

        # Process completed downloads
        for future in as_completed(future_to_url):
            url, success, error = future.result()
            if success:
                results['success'].append(url)
            else:
                results['failed'].append((url, error))

    # Print summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total: {total}")
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")

    if results['failed']:
        print("\nFailed downloads:")
        for url, error in results['failed']:
            print(f"  - {url}")
            print(f"    Error: {error}")


def read_urls_from_file(file_path):
    """Read URLs from a text file (one URL per line)."""
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Batch download YouTube videos as audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download multiple videos (space-separated)
  python batch_download.py "URL1" "URL2" "URL3"

  # Download from a text file (one URL per line)
  python batch_download.py -f urls.txt

  # Download to subdirectory
  python batch_download.py -f urls.txt -d "scifi"

  # Control parallel downloads (default: 3)
  python batch_download.py -f urls.txt -w 5
        """
    )

    parser.add_argument(
        'urls',
        nargs='*',
        help='YouTube video URLs (space-separated)'
    )

    parser.add_argument(
        '-f', '--file',
        help='Read URLs from a text file (one URL per line)',
        default=None
    )

    parser.add_argument(
        '-o', '--output',
        help='Full output directory path',
        default=None
    )

    parser.add_argument(
        '-d', '--dir',
        help='Subdirectory within I:\\audiobooks',
        default=None
    )

    parser.add_argument(
        '-w', '--workers',
        type=int,
        help='Number of parallel downloads (default: 3)',
        default=3
    )

    args = parser.parse_args()

    # Get URLs from either arguments or file
    urls = []
    if args.file:
        urls = read_urls_from_file(args.file)
    elif args.urls:
        urls = args.urls
    else:
        print("Error: Please provide URLs or use -f to specify a file")
        parser.print_help()
        sys.exit(1)

    # Validate URLs
    valid_urls = []
    for url in urls:
        if 'youtube.com' in url or 'youtu.be' in url:
            valid_urls.append(url)
        else:
            print(f"Warning: Skipping invalid URL: {url}")

    if not valid_urls:
        print("Error: No valid YouTube URLs found")
        sys.exit(1)

    # Determine output path
    if args.output and args.dir:
        print("Error: Cannot use both -o and -d flags together")
        sys.exit(1)

    output_path = r"I:\audiobooks"
    if args.output:
        output_path = args.output
    elif args.dir:
        output_path = os.path.join(r"I:\audiobooks", args.dir)

    # Download batch
    download_batch(valid_urls, output_path, args.workers)


if __name__ == '__main__':
    main()
