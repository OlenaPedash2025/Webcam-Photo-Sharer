from email.mime import image

import requests
import wikipedia
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file("frontend.kv")


class MainScreen(Screen):
    def search_image(self):
        user_query = self.manager.current_screen.ids.user_query.text
        print(f"User query: {user_query}")
        page = wikipedia.page(user_query)
        print(f"Page title: {page.title}")
        image_url = page.images[0] if page.images else None
        return image_url

    def download_image(self):
        headers = {"User-Agent": "MyKivyApp/1.0 (olena.pedash@edu.dualis-institut.de)"}
        image_path = "images/downloaded_image.jpg"
        image_url = self.search_image()
        if image_url:
            print(f"Image URL: {image_url}")
            try:
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    print("Image downloaded successfully.")
                    return image_path
                else:
                    print(
                        f"Failed to download image. Status code: {response.status_code}"
                    )
            except Exception as e:
                print(f"Error downloading image: {e}")

        else:
            print("No images found for this query.")

    def set_image(self):
        self.manager.current_screen.ids.img.source = self.download_image()
        self.manager.current_screen.ids.img.reload()

    pass


class RootWidget(ScreenManager):
    pass


class TestApp(App):
    def build(self):
        return RootWidget()


TestApp().run()
