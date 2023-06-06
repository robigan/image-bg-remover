from io import BytesIO
import tkinter as tk
import threading
from PIL import ImageGrab
from rembg import remove, new_session
from AppKit import NSPasteboard, NSPasteboardTypePNG

class ImageProcessorApp(tk.Tk):
    def __init__(self, model_name: str):
        super().__init__()

        self.session = new_session(model_name)

        self.title("Image Processor")
        self.geometry("400x400")

        self.process_button = tk.Button(self, text="Process Image", command=self.process_image)
        self.process_button.pack(padx=10, pady=10)

        self.process_label = tk.Label(self, text="")
        self.process_label.pack(pady=10)

    def process_image(self):
        # Get the image from the clipboard
        image = self.get_image_from_clipboard()

        # Update the process label text
        self.process_label.config(text="Processing image...")

        # Modify the image in a separate thread
        # Use threading to prevent the GUI from freezing instead of asyncio because using asyncio with Tkinter is not recommended
        threading.Thread(target=self.modify_image, args=(image,)).start()

    def get_image_from_clipboard(self):
        image = ImageGrab.grabclipboard()
        return image

    def modify_image(self, image):
        processed_image = self.run_remove(image)

        # Copy image to clipboard
        self.copy_image_to_clipboard(processed_image)

        # Update the process label text
        self.process_label.config(text="Image processing complete.")

    def run_remove(self, image):
        # Remove the background
        return remove(image, session=self.session)

    def copy_image_to_clipboard(self, image):
        # Convert the PIL image to a PNG byte stream
        byte_stream = BytesIO()
        image.save(byte_stream, format="PNG")
        byte_stream.seek(0)

        # Initialize NSPasteboard
        pasteboard = NSPasteboard.generalPasteboard()

        # Clear pasteboard contents
        pasteboard.clearContents()

        # Set PNG data on the pasteboard
        pasteboard.setData_forType_(byte_stream.read(), NSPasteboardTypePNG)

if __name__ == "__main__":
    app = ImageProcessorApp("isnet-general-use")
    app.mainloop()
