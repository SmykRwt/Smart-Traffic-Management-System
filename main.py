from pathlib import Path

from app.detection.image_processor import ImageProcessor
from app.detection.video_processor import VideoProcessor


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

        processor = ImageProcessor()
        output_path, summary = processor.process_image(path)

    elif extension in VIDEO_EXTENSIONS:

        processor = VideoProcessor()
        output_path, summary = processor.process_video(path)

    else:

        print("Unsupported file.")

        return

    print(f"\nProcessing complete! Output saved to: {output_path}")
    print("\nSummary Statistics:")
    print(f"Total Detections: {summary['detections']}")
    print(f"Traffic Density: {summary['analytics'].traffic_density}")
    print(f"Congestion Level: {summary['analytics'].congestion_level}")
    if summary['events']:
        print("\nGenerated Events:")
        for event in summary['events']:
            print(f"- {event}")


if __name__ == "__main__":

    main()