import flet as ft
from components.flet_components import options_0_9
import config
from helpers import bet_on_game_db

def bet_view(page: ft.Page, navbar):
    items = [
        ft.Dropdown(
            options=options_0_9(),
            alignment=ft.alignment.center,
            width=80,
            height=80,
            border_radius=ft.border_radius.all(5),
        ),
        ft.Container(
            content=ft.Text("vs"),
            alignment=ft.alignment.center,
            width=80,
            height=80,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            border_radius=ft.border_radius.all(5),
        ),
        ft.Dropdown(
            options=options_0_9(),
            alignment=ft.alignment.center,
            width=80,
            height=80,
            border_radius=ft.border_radius.all(5),
        ),
    ]
    
    page.views.append(
        ft.View(
            "/bet",
            [
                ft.AppBar(title=ft.Text("Betting on " + config.team_home + " vs " + config.team_away + " game" ), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.Row(spacing=3, controls=items),
                ft.ElevatedButton("Bet", on_click=lambda _: bet_on_game(items[0].value, items[2].value, page)),
                navbar
            ],
        )
    )

def set_up_current_betting_game(team_home_name, team_away_name, game_starts_at, page: ft.Page):
        config.team_home = team_home_name
        config.team_away = team_away_name
        config.game_time = game_starts_at
        page.go("/bet")
        
def bet_on_game(first, second, page: ft.Page):
        bet_on_game_db(first, second)
        page.go("/games")
