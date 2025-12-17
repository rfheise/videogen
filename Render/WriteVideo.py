import cv2 
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
import subprocess
from ..Helper import Logger
from tqdm import tqdm 

def write_video(frames, output_path, fps):
    """
    Writes a list of frames (numpy arrays) to a video file.
    
    Parameters:
      frameList (FrameList): FrameList object containing frames
      output_path (str): Path to the output video file.
      fps (int): Frames per second for the output video.
    """
    # Get dimensions from the first frame.
    init_frame = frames.get_item(0).frame
    height, width = init_frame.shape[:2]
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can choose another codec if desired.
    # video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    # for frame in frames:
    #     video_writer.write(frame)
    # video_writer.release()
    if not Logger.debug_mode:
        command = [
            'ffmpeg',
            '-y',                # Overwrite output file if it exists.
            '-f', 'rawvideo',    # Input format: raw video.
            '-pix_fmt', 'rgb24', # Pixel format of the raw data.
            '-s', f'{width}x{height}', # Frame size.
            '-r', str(fps),      # Frame rate.
            '-i', '-',           # Input comes from standard input.
            '-c:v', 'libx264',# Use libx264rgb for lossless RGB encoding.
            '-crf', '18',         # CRF 0 for lossless quality.
            '-preset', 'medium', # Use a slower preset for optimal compression.
            output_path
        ]
    else:
        command = [
            'ffmpeg',
            '-y',                # Overwrite output file if it exists.
            '-f', 'rawvideo',    # Input format: raw video.
            '-pix_fmt', 'rgb24', # Pixel format of the raw data.
            '-s', f'{width}x{height}', # Frame size.
            '-r', str(fps),      # Frame rate.
            '-i', '-',           # Input comes from standard input.
            '-c:v', 'libx264',# Use libx264rgb for lossless RGB encoding.
            '-crf', '30',         # CRF 0 for lossless quality.
            '-preset', 'fast', # Use a slower preset for optimal compression.
            output_path
        ]
    
    # Open a subprocess with FFmpeg.
    process = subprocess.Popen(command, stdin=subprocess.PIPE,   
                               stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
    
    # Write each frame's raw bytes to FFmpeg's stdin.
    for frame in tqdm(frames, total=len(frames)):
        f = cv2.cvtColor(frame.frame, cv2.COLOR_BGR2RGB)
        process.stdin.write(f.tobytes())
    
    # Close stdin and wait for FFmpeg to finish.
    process.stdin.close()
    process.wait()

def combine_audio_video(outfile, video_file, audio_file):

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        outfile
    ], capture_output=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
