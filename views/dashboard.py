import flet as ft
import pandas as pd
from helpers import headers, rows
from sevices.firebase import db
import config

cards = []

def dashboard_view(page: ft.Page, navbar):
    cards.append(navbar)
    page.views.append(
        ft.View(
            "/dashboard",
            cards,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    )
    page.update()
    
def init_dashboard(page: ft.Page):
        #Preview for today games
        navbar = cards[len(cards)-1]
        cards.clear()
        cards.append(ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.SURFACE_VARIANT))
        for game in config.games_today:
            doc_ref = db.collection("games").document(game)
            doc = doc_ref.get()
            game_started = doc.to_dict().get("game_started", False)
            team_home = doc.to_dict().get("team_home_name", "")
            team_away = doc.to_dict().get("team_away_name", "")
            text = [
                ft.Text(f"{team_home} vs {team_away}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Text(f"Today at: {game}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
            ]
            if game_started:
                result = doc.to_dict().get("result", "")
                text.append(ft.Text(f"Score: {result}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
            cards.append(
                ft.Card(
                    ft.Column(text)
                )
            )
        
        #Preview for Leaderboards
        for com in config.communities:
            df = pd.DataFrame(config.communities_data[com])
            #When more than 7 users, choose some of them
            if len(df.index) > 7:
                #TOP 3
                indicies = [0, 1, 2]
                #logged user and users around him
                user_row_num = 0
                user_row_num = df.index.get_loc(df[df['User'] == config.name].index[0])
                if user_row_num == 2:
                    indicies.append(3)
                elif user_row_num == 3:
                    indicies.extend([3,4])
                elif user_row_num > 3 and user_row_num + 1 < len(df.index):
                    indicies.extend([user_row_num-1, user_row_num, user_row_num+1])
                    
                #last user
                if user_row_num + 1 < len(df.index):
                    indicies.append(len(df.index) - 1)
                elif user_row_num + 1 == len(df.index):
                    indicies.append(len(df.index) - 2)
                    indicies.append(len(df.index) - 1)
                indicies.sort() 
                df = df.iloc[indicies]
 
            dt = ft.DataTable(columns=headers(df), rows=rows(df))
            cards.append(
                ft.Card(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text(com, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                        dt,
                                    ],
                                ),
                                padding=10,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(name=ft.icons.NAVIGATE_NEXT),
                                    ft.TextButton(com, on_click=lambda e: page.go(f"/community_{e.control.text}")),
                                ],
                                alignment=ft.alignment.bottom_right
                            ),
                        ]
                    ),
                    elevation=5,
                ),
            )
            cards.append(navbar)
