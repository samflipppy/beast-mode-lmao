#!/usr/bin/env python3
"""
MrBeast Puzzle — Video Frame Extractor & Analyzer
Downloads YouTube videos, extracts frames, and saves them for analysis.

Usage:
    python video_analyzer.py <youtube_url> [options]

Examples:
    # Extract every frame from the Super Bowl ad
    python video_analyzer.py "https://youtube.com/watch?v=VIDEO_ID" --every-frame

    # Extract 1 frame per second (default)
    python video_analyzer.py "https://youtube.com/watch?v=VIDEO_ID"

    # Extract every 5th frame with custom output dir
    python video_analyzer.py "https://youtube.com/watch?v=VIDEO_ID" --nth-frame 5 --output ./ad_frames

    # Extract specific time range (in seconds)
    python video_analyzer.py "https://youtube.com/watch?v=VIDEO_ID" --start 10 --end 30
"""

import argparse
import os
import sys
import subprocess
import cv2
import hashlib
from pathlib import Path


def download_video(url, output_dir):
    """Download YouTube video using yt-dlp."""
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, "video.mp4")

    if os.path.exists(video_path):
        print(f"[*] Video already downloaded: {video_path}")
        return video_path

    print(f"[*] Downloading video from: {url}")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", video_path,
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] yt-dlp error: {result.stderr}")
        # Try simpler format
        cmd = ["yt-dlp", "-f", "best", "-o", video_path, url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[!] Download failed: {result.stderr}")
            sys.exit(1)

    print(f"[+] Downloaded: {video_path}")
    return video_path


def extract_frames(video_path, output_dir, nth_frame=None, every_frame=False,
                   start_sec=None, end_sec=None, fps_target=None):
    """Extract frames from video using OpenCV."""
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[!] Cannot open video: {video_path}")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0

    print(f"[*] Video info:")
    print(f"    Total frames: {total_frames}")
    print(f"    FPS: {fps:.2f}")
    print(f"    Duration: {duration:.2f}s")

    # Determine frame extraction interval
    if every_frame:
        interval = 1
    elif nth_frame:
        interval = nth_frame
    elif fps_target:
        interval = max(1, int(fps / fps_target))
    else:
        # Default: 1 frame per second
        interval = max(1, int(fps))

    # Calculate start/end frames
    start_frame = int(start_sec * fps) if start_sec else 0
    end_frame = int(end_sec * fps) if end_sec else total_frames

    start_frame = max(0, min(start_frame, total_frames))
    end_frame = max(start_frame, min(end_frame, total_frames))

    print(f"[*] Extracting frames {start_frame}-{end_frame}, every {interval} frame(s)")

    frame_num = 0
    saved_count = 0
    prev_hash = None

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while frame_num + start_frame < end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        actual_frame = start_frame + frame_num

        if frame_num % interval == 0:
            # Skip duplicate frames (common in ads)
            frame_small = cv2.resize(frame, (160, 90))
            frame_hash = hashlib.md5(frame_small.tobytes()).hexdigest()

            if frame_hash != prev_hash:
                timestamp = actual_frame / fps
                filename = f"frame_{actual_frame:06d}_t{timestamp:.3f}s.jpg"
                filepath = os.path.join(frames_dir, filename)
                cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                saved_count += 1
                prev_hash = frame_hash

                if saved_count % 100 == 0:
                    print(f"    Saved {saved_count} frames (at frame {actual_frame})...")

        frame_num += 1

    cap.release()
    print(f"[+] Saved {saved_count} unique frames to: {frames_dir}")
    return frames_dir, saved_count


def detect_scene_changes(video_path, output_dir, threshold=30.0):
    """Detect scene changes (cuts) in the video — useful for ads with rapid cuts."""
    print(f"[*] Detecting scene changes (threshold={threshold})...")
    scenes_dir = os.path.join(output_dir, "scene_changes")
    os.makedirs(scenes_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_frame = None
    frame_num = 0
    scenes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray)
            mean_diff = diff.mean()

            if mean_diff > threshold:
                timestamp = frame_num / fps
                filename = f"scene_{frame_num:06d}_t{timestamp:.3f}s.jpg"
                filepath = os.path.join(scenes_dir, filename)
                cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                scenes.append((frame_num, timestamp, mean_diff))

        prev_frame = gray
        frame_num += 1

    cap.release()

    print(f"[+] Found {len(scenes)} scene changes:")
    for fnum, ts, diff in scenes:
        print(f"    Frame {fnum} at {ts:.3f}s (diff={diff:.1f})")

    return scenes


def extract_text_regions(frames_dir, output_dir):
    """Find frames with high-contrast text-like regions (no OCR dependency)."""
    print(f"[*] Scanning for frames with text-like regions...")
    text_dir = os.path.join(output_dir, "text_candidates")
    os.makedirs(text_dir, exist_ok=True)

    frame_files = sorted(Path(frames_dir).glob("*.jpg"))
    text_frames = []

    for fpath in frame_files:
        img = cv2.imread(str(fpath))
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection to find text-heavy areas
        edges = cv2.Canny(gray, 50, 150)
        edge_density = edges.mean()

        # High edge density often means text, signs, or detailed graphics
        if edge_density > 25:
            outpath = os.path.join(text_dir, fpath.name)
            cv2.imwrite(outpath, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            text_frames.append((fpath.name, edge_density))

    print(f"[+] Found {len(text_frames)} frames with high text/detail density")
    # Sort by density (most text-heavy first)
    text_frames.sort(key=lambda x: x[1], reverse=True)
    for name, density in text_frames[:20]:
        print(f"    {name} (density={density:.1f})")

    return text_frames


def generate_report(output_dir, total_frames, scenes, text_frames):
    """Generate a summary report."""
    report_path = os.path.join(output_dir, "ANALYSIS_REPORT.md")
    with open(report_path, "w") as f:
        f.write("# Video Frame Analysis Report\n\n")
        f.write(f"- **Total unique frames extracted:** {total_frames}\n")
        f.write(f"- **Scene changes detected:** {len(scenes)}\n")
        f.write(f"- **Text-heavy frames found:** {len(text_frames)}\n\n")

        f.write("## Scene Changes\n\n")
        f.write("| Frame | Timestamp | Diff Score |\n")
        f.write("|-------|-----------|------------|\n")
        for fnum, ts, diff in scenes:
            f.write(f"| {fnum} | {ts:.3f}s | {diff:.1f} |\n")

        f.write("\n## Top 30 Text-Heavy Frames\n\n")
        f.write("| Filename | Edge Density |\n")
        f.write("|----------|-------------|\n")
        for name, density in text_frames[:30]:
            f.write(f"| {name} | {density:.1f} |\n")

    print(f"[+] Report saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="MrBeast Puzzle Video Frame Extractor")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output", "-o", default="./video_analysis",
                        help="Output directory (default: ./video_analysis)")
    parser.add_argument("--every-frame", action="store_true",
                        help="Extract every single frame (large output!)")
    parser.add_argument("--nth-frame", type=int,
                        help="Extract every Nth frame")
    parser.add_argument("--fps", type=float,
                        help="Target frames per second to extract")
    parser.add_argument("--start", type=float,
                        help="Start time in seconds")
    parser.add_argument("--end", type=float,
                        help="End time in seconds")
    parser.add_argument("--scene-threshold", type=float, default=30.0,
                        help="Scene change detection threshold (default: 30)")
    parser.add_argument("--skip-download", action="store_true",
                        help="Skip download, use existing video.mp4")
    parser.add_argument("--skip-text-scan", action="store_true",
                        help="Skip text region detection")

    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Download
    if args.skip_download:
        video_path = os.path.join(output_dir, "video.mp4")
        if not os.path.exists(video_path):
            print(f"[!] No video found at {video_path}")
            sys.exit(1)
    else:
        video_path = download_video(args.url, output_dir)

    # Step 2: Extract frames
    frames_dir, total_frames = extract_frames(
        video_path, output_dir,
        nth_frame=args.nth_frame,
        every_frame=args.every_frame,
        start_sec=args.start,
        end_sec=args.end,
        fps_target=args.fps
    )

    # Step 3: Detect scene changes
    scenes = detect_scene_changes(video_path, output_dir, args.scene_threshold)

    # Step 4: Find text-heavy frames
    text_frames = []
    if not args.skip_text_scan:
        text_frames = extract_text_regions(frames_dir, output_dir)

    # Step 5: Generate report
    generate_report(output_dir, total_frames, scenes, text_frames)

    print(f"\n{'='*60}")
    print(f"DONE! Results in: {output_dir}")
    print(f"  frames/          — All extracted frames")
    print(f"  scene_changes/   — Frames at scene cuts")
    print(f"  text_candidates/ — Frames with text/detail")
    print(f"  ANALYSIS_REPORT.md — Summary report")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
