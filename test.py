import requests
import wikipedia
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file("frontend.kv")


class MainScreen(Screen):
    def search_image(self):
        user_query = self.manager.current_screen.ids.user_query.text
        try:
            page = wikipedia.page(user_query)
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Ambiguous query '{user_query}', picking: {e.options[0]}")
            page = wikipedia.page(e.options[0])
        except wikipedia.exceptions.PageError:
            print(f"Page '{user_query}' not found.")
            return None

        return page.images[0] if page.images else None

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
