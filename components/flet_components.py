import flet as ft

def options_0_9():
    return [ft.dropdown.Option(str(i)) for i in range(10)]

class ButtonWithInfo(ft.ElevatedButton):
    def __init__(self, text, on_click, info: list):
        super().__init__(text=text, on_click=on_click)
        self.info = info
        self.disabled = len(info) >= 4 and info[3]