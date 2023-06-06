import tkinter as tk
from PIL import Image, ImageTk, ImageGrab 
import tempfile
import hashlib
from os import path
import subprocess
from rembg import remove, new_session

class ImageProcessorApp(tk.Tk):
    def __init__(self, model_name: str):
        super().__init__()

        self.temp_dir = tempfile.gettempdir()
        self.session = new_session(model_name)

        self.title("Image Processor")
        self.geometry("400x400")

        self.process_button = tk.Button(self, text="Process Image", command=self.process_image)
        self.process_button.pack(padx=10, pady=10)

    def process_image(self):
        # Get the image from the clipboard
        image = self.get_image_from_clipboard()

        # Perform processing on the image (resizing in this example)
        processed_image = self.modify_image(image)

        # Display the image using the system default application
        self.display_image_using_system_application(processed_image)

    def get_image_from_clipboard(self):
        # image_data = None

        # try:
        #     # Get image data from clipboard
        #     image_data = self.clipboard_get(type='image/png')
        # except tk.TclError as e:
        #     print('TclError:{}'.format(e))
        #     exit(1)

        # # Create a PIL Image object from the image data
        # image = Image.open(io.BytesIO(image_data))
        image = ImageGrab.grabclipboard()

        return image

    def modify_image(self, image):
        # Resize the image
        # resized_image = image.resize((width, height))
        returned_image = remove(image, session=self.session, alpha_matting=True)

        return returned_image

    def display_image_using_system_application(self, image: Image):
        # Get temp path so save image to
        saved_path = path.join(self.temp_dir, hashlib.sha256(image.tobytes()).hexdigest() + ".png")

        # Save the image
        image.save(saved_path, format='png')

        # Open the image. See https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
        subprocess.run(["open", saved_path], check=True)

    

if __name__ == "__main__":
    app = ImageProcessorApp("isnet-general-use")
    app.mainloop()