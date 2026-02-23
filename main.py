import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class CameraWrapper(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Image widget to display the camera feed
        self.img1 = Image()
        self.add_widget(self.img1)

        # Button to take a photo
        self.btn = Button(text="Capture Photo", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.take_photo)
        self.add_widget(self.btn)

        # Connect to the webcam (0 is the default camera)
        self.capture = cv2.VideoCapture(1)

        # Update the screen at 30 frames per second
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = self.capture.read()
        if ret:
            # Flip the frame to make it a mirror image (standard for webcams)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            # Create a texture to show in Kivy
            texture1 = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
            )
            texture1.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")

            # Display the texture in the Image widget
            self.img1.texture = texture1

    def take_photo(self, *args):
        # Capture the current frame and save it
        ret, frame = self.capture.read()
        if ret:
            filename = "captured_photo.png"
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")


class WebcamApp(App):
    def build(self):
        return CameraWrapper()


if __name__ == "__main__":
    WebcamApp().run()
