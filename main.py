from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
import kivy.core.window
from kivy.properties import StringProperty, NumericProperty, ListProperty
import ssl
from card import Card

from kivy.utils import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA])


# Para a internet funfar no app
ssl._create_default_https_context = ssl._create_unverified_context


class CartaTab(MDScrollView):
    image_url = StringProperty('./assets/images/overlay.png')
    card_name = StringProperty()
    
    def search(self, text):
        carta = Card(text)
        print(carta.__dict__)
        self.image_url = carta.image_url
        self.card_name = carta.name
        
        set_cards = self.ids["set_cards"]
        set_cards.clear_widgets()
        for set, precos in carta.precos.items():
            set_widget = SetCard()
            lista_precos_widget = ListaPrecos(set_name=set)
            for acabamento, preco in precos.items():
                lista_precos_widget.add_widget(
                    LinhaPreco(
                        acabamento=acabamento,
                        preco=preco
                    )
                )
            
            set_widget.add_widget(lista_precos_widget)            
            set_cards.add_widget(set_widget)

class ScannerTab(MDFloatLayout):
    pass

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

class LinhaPreco(MDGridLayout):
    acabamento = StringProperty()
    preco = NumericProperty()


class ListaPrecos(MDBoxLayout):
    set_name = StringProperty()
    pass


class SetCard(MDBoxLayout):

    set_name = StringProperty()
    lista_precos = ListProperty()

    # def __init__(self, **kwargs):
    #     super(SetCard, self).__init__(**kwargs)
    #     print(self.ids)
    #     lista = getattr(self.ids, "lista")
    #     lista.add_widget(MDLabel(text="aaaaaaaaaaaaaaaaaaaa"))
    #     self.add_widget(lista)
        

class MyApp(MDApp):
    def build(self):
        if platform in ["linux", "win"]:
            kivy.core.window.Window.size = (350, 800)
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        return HomePage()


if __name__ == "__main__":
    MyApp().run()
