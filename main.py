from pathlib import Path

from app.processors.image_processor import ImageProcessor
from app.processors.video_processor import VideoProcessor


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
}


VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
}


def main():

    path = input("Enter image/video path: ").strip()

    extension = Path(path).suffix.lower()

    if extension in IMAGE_EXTENSIONS:

        processor = ImageProcessor(path)

    elif extension in VIDEO_EXTENSIONS:

        processor = VideoProcessor(path)

    else:

        print("Unsupported file.")

        return

    processor.process()


if __name__ == "__main__":

    main()