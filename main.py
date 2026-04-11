import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, concatenate_audioclips
from moviepy.audio.fx.all import audio_loop

def create_background(pil_img, target_res, blur_radius=30):
    """Create a blurred background image."""
    bg = ImageOps.fit(pil_img, target_res, method=Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return np.array(bg.point(lambda p: p * 0.7))

def create_slideshow(img_folder, audio_folder, output_path, duration_per_img=2.3, transition=0.4):
    """Generate a slideshow video from images and audio."""
    target_res = (1920, 1080)
    
    # 1. Load images
    valid_img_ext = ('.png', '.jpg', '.jpeg')
    all_images = [os.path.join(img_folder, f) for f in sorted(os.listdir(img_folder)) 
                  if f.lower().endswith(valid_img_ext)]

    if not all_images:
        print("Error: No images found in the folder!")
        return False

    print(f"Found {len(all_images)} images. Processing...")

    # 2. Create video clips from images
    clips = []
    for idx, path in enumerate(all_images, 1):
        try:
            with Image.open(path) as pil_img:
                pil_img = ImageOps.exif_transpose(pil_img)
                
                # Foreground (centered image)
                fg_pil = pil_img.copy()
                fg_pil.thumbnail(target_res, Image.LANCZOS)
                fg_clip = ImageClip(np.array(fg_pil)).set_duration(duration_per_img).set_position("center")
                
                # Background (blurred)
                bg_array = create_background(pil_img, target_res)
                bg_clip = ImageClip(bg_array).set_duration(duration_per_img)
                
                # Composite and add transitions
                final_clip = CompositeVideoClip([bg_clip, fg_clip], size=target_res)
                clips.append(final_clip.crossfadein(transition).crossfadeout(transition))
                print(f"  ✓ [{idx}/{len(all_images)}] {os.path.basename(path)}")
        except Exception as e:
            print(f"  ✗ [{idx}/{len(all_images)}] Error processing {os.path.basename(path)}: {e}")

    if not clips:
        print("Error: No images were processed!")
        return False

    # 3. Concatenate all clips
    print("\n--- Concatenating video clips ---")
    try:
        video = concatenate_videoclips(clips, method="compose", padding=-transition)
    except Exception as e:
        print(f"Error concatenating clips: {e}")
        return False

    # 4. Add audio
    valid_audio_ext = ('.mp3', '.wav', '.m4a', '.ogg')
    audio_files = [os.path.join(audio_folder, f) for f in sorted(os.listdir(audio_folder)) 
                   if f.lower().endswith(valid_audio_ext)]

    if audio_files:
        try:
            print(f"\nFound {len(audio_files)} audio file(s). Adding audio...")
            audio_clips = [AudioFileClip(f) for f in audio_files]
            full_audio = concatenate_audioclips(audio_clips)

            # Loop or trim audio to match video duration
            if full_audio.duration < video.duration:
                full_audio = audio_loop(full_audio, duration=video.duration)
                print(f"  Audio looped to {video.duration:.1f}s")
            else:
                full_audio = full_audio.subclip(0, video.duration)
                print(f"  Audio trimmed to {video.duration:.1f}s")
            
            video = video.set_audio(full_audio.audio_fadeout(3))
        except Exception as e:
            print(f"Warning: Could not add audio: {e}")
    else:
        print("\nNo audio files found. Continuing without audio.")

    # 5. Export video
    print(f"\n--- Rendering final video ---")
    print(f"Output: {output_path}")
    try:
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", threads=4)
        print("\n✓ Video successfully generated!")
        video.close()
        for clip in clips:
            clip.close()
        return True
    except Exception as e:
        print(f"Error exporting video: {e}")
        return False

if __name__ == "__main__":
    IMG_DIR = "./data/images"
    AUDIO_DIR = "./data/audio"
    OUT_DIR = "./output"
    os.makedirs(OUT_DIR, exist_ok=True)
    
    success = create_slideshow(
        img_folder=IMG_DIR, 
        audio_folder=AUDIO_DIR, 
        output_path=os.path.join(OUT_DIR, "slideshow.mp4")
    )
    
    exit(0 if success else 1)

