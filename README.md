# Photo-to-Video Automator 🎞️

A Python-based tool to automatically generate high-quality slideshow videos from a collection of images with background music and smooth transitions.

## Features
- **Batch Processing**: Handle hundreds of photos in seconds.
- **Smooth Transitions**: Automatic crossfade effects between slides.
- **Audio Integration**: Automatically syncs and trims your background music.
- **Auto-Resizing**: Normalizes all images to 1080p to prevent rendering errors.

## Project Structure
```text
video-photo/
├── data/
│   ├── images/       # Drop your JPG/PNG files here
│   └── audio/        # Drop your MP3 file here
├── output/           # Rendered videos will appear here
├── src/
│   └── main.py       # Core logic
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── .gitignore        # Git ignore rules
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd video-photo
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .photo-audio_env
   source .photo-audio_env/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare your files**:
   - Place your images (`.jpg`, `.png`) in `data/images/`
   - Place your audio files (`.mp3`, `.wav`, `.m4a`, `.ogg`) in `data/audio/`

2. **Run the script**:
   ```bash
   python src/main.py
   ```

3. **Find your output**:
   - The generated video will be saved in `output/slideshow_ripristinato_8.mp4`

## Configuration

Edit these parameters in `src/main.py` to customize your slideshow:
- `target_res`: Video resolution (default: 1920x1080)
- `duration_per_img`: Seconds each image is displayed (default: 2.3)
- `transition`: Crossfade duration in seconds (default: 0.4)
- `chunk_size`: Number of images per processing batch (default: 15)