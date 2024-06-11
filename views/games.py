import flet as ft
from components.flet_components import ButtonWithInfo
from sevices.firebase import db
from components.paginated_dt import PaginatedDataTable
from views.bet import set_up_current_betting_game

dt_games = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Team Home")),
                ft.DataColumn(ft.Text("Team Away")),
                ft.DataColumn(ft.Text("Starts")),
                ft.DataColumn(ft.Text("Betting")),
            ],
            rows=[],
        )
games_view_controls = [
                ft.AppBar(title=ft.Text("Games"), bgcolor=ft.colors.SURFACE_VARIANT),
                PaginatedDataTable(datatable=dt_games, table_title="Games In Euro 2024", rows_per_page=5),
            ]

def games_view(page: ft.Page, navbar):
    if len(games_view_controls) < 3:
        games_view_controls.append(navbar)
    init_games(page)
    page.views.append(
        ft.View(
            "/games",
            games_view_controls,
        )
    )
    
def init_games(page: ft.Page):
    docs_ref = db.collection("games")
    docs = docs_ref.stream()
    dt_games.rows.clear()
    for game in docs:
        team_home_name = game.to_dict().get("team_home_name", "")
        team_away_name = game.to_dict().get("team_away_name", "")
        game_starts_at = game.to_dict().get("game_starts_at", "")
        started = game.to_dict().get("game_started", False)
        dt_games.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(team_home_name)),
                    ft.DataCell(ft.Text(team_away_name)),
                    ft.DataCell(ft.Text(game_starts_at)),
                    ft.DataCell(ButtonWithInfo(
                            text = "Bet", 
                            info = [team_home_name, team_away_name, game_starts_at, started],
                            on_click=lambda e: set_up_current_betting_game(e.control.info[0], e.control.info[1], e.control.info[2], page)
                        )
                    )
                ]
            )
        )
    games_view_controls[1] = PaginatedDataTable(datatable=dt_games, table_title="Games In Euro 2024", rows_per_page=5)
        
    