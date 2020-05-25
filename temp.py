import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from  kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import time

class Home(Screen):
    def animation_begins(self):
        textvalue=self.labelvalue.text.split()
        var=" "
        for i in textvalue:
            var+=i
            self.labelvalue.text=var
            time.sleep(3)

class WindowManager(ScreenManager):
    pass

kv=Builder.load_file('designing.kv')

sm = WindowManager()
screens=[Home(name="home")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "home"

class CafeApp(App):
    def build(self):
        return sm

if __name__=='__main__':
    CafeApp().run()