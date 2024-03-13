import os
import time
import imageio
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIRECTORY = "YourPathToADirectory"
TARGET_DIRECTORY = "YourPathToADirectory"


class WebPHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.lower().endswith(".webp"):
            time.sleep(2)  # Adding a 2-second delay so it doesnt convert a file that is being downloaded resulting in an error
            convert_webp_to_gif_and_move(event.src_path)


def convert_webp_to_gif_and_move(file_path):
    try:
        print(f"Converting file: {file_path}")
    
        gif_path = os.path.join(TARGET_DIRECTORY, os.path.basename(file_path).replace(".webp", ".gif"))
        
        with imageio.get_reader(file_path) as reader:
            images = [Image.fromarray(img) for img in reader]
            
            # Try to get the frame rate from metadata, default to 30 fps if not available
            try:
                frame_rate = reader.get_meta_data()["fps"]
            except KeyError:
                frame_rate = 30
            
            # Calculate the duration based on the frame rate
            duration = int(1000 / frame_rate) if frame_rate > 0 else 100
            
            images[0].save(
                gif_path,
                save_all=True,
                append_images=images[1:],
                loop=0,
                duration=duration,
                quality=100,
            )
        # Remove the original WebP file
        os.remove(file_path)
        
        # Add a small delay before moving the files so it doesnt move a file that doesnt exitst yet
        time.sleep(0.1)
        
    except Exception as e:
        print(f"Error converting file '{file_path}': {e}")


def main():
    # Process existing files in the source directory
    process_existing_files()
    # Set up a watchdog observer
    event_handler = WebPHandler()
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def process_existing_files():
    source_dir = SOURCE_DIRECTORY
    files = os.listdir(source_dir)
    for file_name in files:
        file_path = os.path.join(source_dir, file_name)
        convert_webp_to_gif_and_move(file_path)

if __name__ == "__main__":
    main()
