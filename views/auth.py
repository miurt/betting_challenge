import flet as ft
import config
from helpers import login_db, set_games_today, signup_db, update_name
from views.admin import init_admin_mode
from views.dashboard import init_dashboard
from views.games import init_games

current_time = "2024-06-15 8:00:00"

def login_view(page: ft.Page):
    page.views.append(
        ft.View(
            "/login",
            [
                ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.TextField(hint_text="Please enter your login information", label="Login Information", on_change=update_name),
                ft.ElevatedButton("Login", on_click=lambda _: login(config.name, page)),
            ],
        )
    )

def signup_view(page: ft.Page):
    page.views.append(
        ft.View(
            "/signup",
            [
                ft.AppBar(title=ft.Text("Sign Up"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.TextField(hint_text="Please enter your name for registration", label="Sign Up", on_change=update_name),
                ft.ElevatedButton("Sign up", on_click=lambda _: signup(config.name, page)),
            ],
        )
    )
    
def login(user_name: str, page: ft.Page):
        if user_name == "admin":
            set_games_today(current_time)
            init_admin_mode(page)
            page.go("/admin")
        elif login_db(user_name):
            page.go("/communities")
            print(f"logged in as {user_name}")
            set_games_today(current_time)
            init_games(page)
            init_dashboard(page)
            page.update()
            return True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"User {config.name} not found"))
            page.snack_bar.open = True
            page.update()
            return False
               
def signup(user_name: str, page: ft.Page):
        if (login(user_name, page)):
            page.snack_bar = ft.SnackBar(ft.Text(f"User {config.name} already exists"))
            page.snack_bar.open = True
        else:
            signup_db(user_name)
            page.go("/communities")
            print(f"registered as {user_name}")
            set_games_today(current_time)
            init_games(page)
            init_dashboard(page)
