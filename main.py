from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
import kivy.core.window
import ssl
from kivy.utils import platform
if platform=="android":
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.CAMERA])


# Para a internet funfar no app
ssl._create_default_https_context = ssl._create_unverified_context

class CartaTab(MDScrollView):
    pass

class ScannerTab(MDFloatLayout):
    pass

class HomePage(MDFloatLayout):
    pass    

class MyApp(MDApp):
    def build(self):
        if platform in ["linux", "win"]:
            kivy.core.window.Window.size = (350, 800)
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        return HomePage()

if __name__=="__main__":
    MyApp().run()