#https://github.com/hpsaturn/p4a_grpc_recipe
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.camera import Camera
from kivy.metrics import dp
import kivy.core.window
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ObjectProperty,
)
import ssl
import weakref
from card import Card
import textDetection
from PIL import Image

from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.CAMERA])


# Para a internet funfar no app
ssl._create_default_https_context = ssl._create_unverified_context


def generateCardListId(carta: Card, acabamento: str, set_name: str):
    # [CardName]-[SET]-[Finish]
    cardName = "".join(filter(str.isalpha, carta.name))
    finish = "".join(filter(str.isalpha, acabamento))
    set = "".join(filter(str.isalpha, set_name))
    return f"{cardName.upper()}-{finish.upper()}-{set.upper()}"


class CartaTab(MDScrollView):
    image_url = StringProperty("./assets/images/overlay.png")
    card_name = StringProperty()

    def search(self, text):
        carta = Card(text)
        print(carta.__dict__)
        self.image_url = carta.image_url
        self.card_name = carta.name

        set_cards = self.ids["set_cards"]
        set_cards.clear_widgets()
        for set_name, precos in carta.precos.items():
            set_widget = SetCard()
            lista_precos_widget = ListaPrecos(set_name=set_name)
            for acabamento, preco in precos.items():
                lista_precos_widget.add_widget(
                    LinhaPreco(
                        carta=carta,
                        acabamento=acabamento,
                        preco=preco,
                        set_name=set_name,
                    )
                )

            set_widget.add_widget(lista_precos_widget)
            set_cards.add_widget(set_widget)


class ScannerTab(MDFloatLayout):
    def lookup_card_from_camera(self):
        image = self.capture()
        text:str = self.scan_text(image)
        app = MyApp.get_running_app()
        print(app.root.ids)
        carta_tab = app.root.ids['carta_tab']
        lines = text.split("\n")
        carta_tab.search(lines[0])
        
    
    def capture(self):
        camera: Camera = self.ids['camera']
        camera.export_to_png("captura.png")
        
        image = Image.open("captura.png")
        return image
    
    def scan_text(self, image):
        coords = (
            image.width/2 - dp(100),
            image.height/2 - dp(138),
            image.width/2 + dp(100),
            image.height/2 + dp(138),
            
        )
        image= image.crop(coords)
        image.save("captura.png", format='PNG')
        with open("captura.png",'rb') as file:
            image_bytes=file.read()
        
        response = textDetection.analyse_image(
            image_bytes=image_bytes
        )
        return textDetection.get_text(response)
        
        
    


class ListaTab(MDScrollView):
    pass


class HomePage(MDFloatLayout):
    pass


class CartaNaLista(MDFloatLayout):
    image = StringProperty()
    name = StringProperty()
    set_name = StringProperty()
    acabamento = StringProperty()
    qnt = NumericProperty()
    preco = NumericProperty()
    
    def get_qnt(self):
        return self.qnt


class LinhaPreco(MDGridLayout):
    carta: Card = ObjectProperty()
    acabamento = StringProperty()
    preco = NumericProperty()
    set_name = StringProperty()

    def add_to_list(self):
        app = MDApp.get_running_app()
        lista_cards = app.root.ids['lista_cards'].ids['lista']
        id = generateCardListId(
            carta=self.carta, acabamento=self.acabamento, set_name=self.set_name
        )
        print(id)
        print(app.root.ids['lista_cards'].ids)
        if not id in lista_cards.ids:
            card_on_list = CartaNaLista(
                image=self.carta.art_crop,
                name=self.carta.name,
                set_name=self.set_name,
                acabamento=self.acabamento,
                qnt=1,
                preco=self.preco,
            )
            lista_cards.add_widget(card_on_list)
            lista_cards.ids[id] = weakref.ref(card_on_list)
        else:
            card_on_list:CartaNaLista = lista_cards.ids[id]
            card_on_list().qnt +=1
        app.root.ids['preco_total'].text = "{:.2f}".format(float(app.root.ids['preco_total'].text) + self.preco)

    def remove_from_list(self):
        app = MDApp.get_running_app()
        lista_cards = app.root.ids['lista_cards'].ids['lista']
        id = generateCardListId(
            carta=self.carta, acabamento=self.acabamento, set_name=self.set_name
        )
        
        if id in lista_cards.ids:
            entry = lista_cards.ids[id]()
            if entry.qnt>1:
                entry.qnt -=1
            else:
                lista_cards.remove_widget(entry)
                del lista_cards.ids[id]
            app.root.ids['preco_total'].text = "{:.2f}".format(float(app.root.ids['preco_total'].text) - self.preco)
        


class ListaPrecos(MDBoxLayout):
    set_name = StringProperty()
    pass


class SetCard(MDBoxLayout):
    set_name = StringProperty()
    lista_precos = ListProperty()


class MyApp(MDApp):
    def build(self):
        if platform in ["linux", "win"]:
            kivy.core.window.Window.size = (350, 800)
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        return HomePage()


if __name__ == "__main__":
    MyApp().run()
