"""
Лабораторная работа №30. Вариант 2.
Исходное приложение: изображение + две кнопки управления.
Сборка в формат EXE с помощью PyInstaller (режимы onedir и onefile).
"""

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label


def resource_path(relative_path):
    """
    Возвращает корректный путь к ресурсу как при запуске из Python,
    так и после упаковки PyInstaller (sys._MEIPASS).
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=5, padding=10, **kwargs)

        # --- Статус ---
        self.status = Label(
            text="Приложение запущено",
            size_hint=(1, 0.08),
            color=(0.2, 0.7, 0.2, 1),
        )
        self.add_widget(self.status)

        # --- Область изображения ---
        img_path = resource_path("resources/image.png")
        if os.path.exists(img_path):
            self.image = Image(
                source=img_path,
                size_hint=(1, 0.75),
                allow_stretch=True,
                keep_ratio=True,
            )
            self.status.text = "Изображение загружено"
        else:
            # Изображение не найдено — показываем заглушку
            self.image = Image(
                size_hint=(1, 0.75),
            )
            self.status.text = f"Файл не найден: {img_path}"
            self.status.color = (0.9, 0.2, 0.2, 1)

        self.add_widget(self.image)

        # --- Панель кнопок ---
        controls = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.17),
            spacing=10,
        )

        btn_zoom_in = Button(
            text="Увеличить",
            background_color=(0.2, 0.6, 0.9, 1),
        )
        btn_zoom_in.bind(on_press=self.zoom_in)

        btn_zoom_out = Button(
            text="Уменьшить",
            background_color=(0.9, 0.5, 0.2, 1),
        )
        btn_zoom_out.bind(on_press=self.zoom_out)

        controls.add_widget(btn_zoom_in)
        controls.add_widget(btn_zoom_out)
        self.add_widget(controls)

    def zoom_in(self, instance):
        w, h = self.image.size_hint
        new_w = min(round(w + 0.1, 1), 1.0)
        new_h = min(round(h + 0.05, 2), 0.85)
        self.image.size_hint = (new_w, new_h)
        self.status.text = f"Масштаб: {int(new_w * 100)}%"
        self.status.color = (0.2, 0.7, 0.2, 1)

    def zoom_out(self, instance):
        w, h = self.image.size_hint
        new_w = max(round(w - 0.1, 1), 0.3)
        new_h = max(round(h - 0.05, 2), 0.35)
        self.image.size_hint = (new_w, new_h)
        self.status.text = f"Масштаб: {int(new_w * 100)}%"
        self.status.color = (0.9, 0.6, 0.1, 1)


class ImageControlApp(App):
    title = "Управление изображением — Лаб. №30 Вариант 2"

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    ImageControlApp().run()
