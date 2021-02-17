from auto_init import wallpaper, kde_theme, dot_files
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton as MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
import os
from functools import partial


class Main(MDApp):
    def build(self):
        screen = MDFloatLayout()
        auto_btn = MDRectangleFlatButton(
            text="Auto init everything!", pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        wallpaper_btn = MDRectangleFlatButton(
            text="just the wallpaper", pos_hint={"x": 0.4, "y": 0.6}
        )
        dot_files_btn = MDRectangleFlatButton(
            text="hit me with dem dot files", pos_hint={"x": 0.15, "y": 0.6}
        )
        theme_btn = MDRectangleFlatButton(
            text="kde rice, hold everything except the theme",
            pos_hint={"x": 0.6, "y": 0.6},
        )
        theme_btn.bind(on_press=partial(kde_theme, os.getcwd))
        wallpaper_btn.bind(on_press=wallpaper)
        dot_files_btn.bind(on_press=dot_files)
        auto_btn.bind(on_press=self.auto_init)
        screen.add_widget(theme_btn)
        screen.add_widget(wallpaper_btn)
        screen.add_widget(dot_files_btn)
        screen.add_widget(auto_btn)
        return screen

    def auto_init():
        staging_dir = os.getcwd()
        dot_files()
        kde_theme(staging_dir)
        wallpaper()


Main().run()