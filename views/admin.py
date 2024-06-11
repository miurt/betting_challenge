from components.flet_components import (ButtonWithInfo,  options_0_9)
from helpers import end_game_db, start_game_db, update_game_score_db
from sevices.firebase import db
import flet as ft
import config

games_view = [ft.AppBar(title=ft.Text("Admin Mode"), bgcolor=ft.colors.SURFACE_VARIANT),]

def admin_view(page: ft.Page):
    page.views.append(
        ft.View(
            "/admin",
            #GAMES TODAY #START 
            #IF STARTED UPDATE SCORE / END
            games_view,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    )
    
def init_admin_mode(page: ft.Page):
        games_view.clear()
        games_view.append(ft.AppBar(title=ft.Text("Admin Mode"), bgcolor=ft.colors.SURFACE_VARIANT))
        items = [
            ft.Dropdown(options=options_0_9(), alignment=ft.alignment.center, width=80, height=80, border_radius=ft.border_radius.all(5)),
            ft.Container(content=ft.Text("vs"), alignment=ft.alignment.center, width=80, height=80, bgcolor=ft.colors.LIGHT_BLUE_50, border_radius=ft.border_radius.all(5)),
            ft.Dropdown(options=options_0_9(), alignment=ft.alignment.center, width=80, height=80, border_radius=ft.border_radius.all(5)),
        ]
        games_view.append(ft.Text("Today's Games:", theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
        if len(config.games_today) > 0:
            for game in config.games_today:
                    doc_ref = db.collection("games").document(game)
                    doc = doc_ref.get()
                    game_started = doc.to_dict().get("game_started", False)
                    game_ended = doc.to_dict().get("game_ended", False)
                    team_home = doc.to_dict().get("team_home_name", "")
                    team_away = doc.to_dict().get("team_away_name", "")
                    games_view.append(ft.Text(team_home + " vs " + team_away, theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
                    if not game_started:
                        games_view.append(ButtonWithInfo(text ="Start", info = [game], on_click=lambda e: start_game(e.control.info[0], page)))
                    elif not game_ended:
                        games_view.extend(
                            [
                                ft.Row(spacing=3, controls=items),
                                ButtonWithInfo(text = "Update", info = [game], on_click=lambda e: update_game_score(e.control.info[0], str(items[0].value) + "_" + str(items[2].value), page)),
                                ButtonWithInfo(text = "Stop", info = [game], on_click=lambda e: end_game(e.control.info[0], page)),
                            ]
                        )

#ADMIN FUNCTIONS START
    
def start_game(game: str, page: ft.Page):
    start_game_db(game)
    page.pubsub.send_all("admin: start_"+ f"{game}")
    init_admin_mode(page)
    page.update()
    page.go("/admin")
    
def end_game(game: str, page: ft.Page):
    end_game_db(game)
    page.pubsub.send_all("admin: end_" + f"{game}")
    init_admin_mode(page)
    page.update()
    page.go("/admin")
    
def update_game_score(game: str, result: str, page: ft.Page):
    update_game_score_db(game, result)
    page.pubsub.send_all("admin: result_" + f"{game}")
    init_admin_mode(page)
    page.update()
    page.go("/admin")
    
    #ADMIN FUCTIONS END