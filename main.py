import flet as ft
from firebase import db
from paginated_dt import PaginatedDataTable
from helpers import(
    update_name,
    update_betting_game,
    login_db,
    signup_db,
    join_community_db,
    get_communities_to_join,
    add_community_db,
    bet_on_game
    )
    
import pandas as pd
import config

def main(page: ft.Page): 
    page.title = "Betting App"
    page.adaptive = True
    
    def headers(df : pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

    def rows(df : pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
        return rows
    
    navbar = ft.NavigationBar(
                            destinations=[
                                ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Communities"),
                                ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Dashboard"),
                                ft.NavigationDestination(
                                    icon=ft.icons.BOOKMARK_BORDER,
                                    selected_icon=ft.icons.BOOKMARK,
                                    label="Games",
                                ),
                            ],
                            on_change=lambda _: navigation(),
                            border=ft.Border(
                                top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
                            ),
                        )
    dt_games = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Team Home")),
                ft.DataColumn(ft.Text("Team Away")),
                ft.DataColumn(ft.Text("Starts")),
                ft.DataColumn(ft.Text("Betting")),
            ],
            rows=[],
        )
    
    dt_community= ft.DataTable()
    
    options_0_9 = [ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                    ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                    ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                    ft.dropdown.Option(9),]
    
    cards = []
    
    def navigation():
        match navbar.selected_index:
            case 0:
                page.go("/communities")
            case 1:
                page.go("/dashboard")
            case 2: 
                page.go("/games")
            case _:
                print("something wronggg")         
    
    def login(user_name):
        if user_name == "admin":
            #ADMIN MODE
            page.go("/admin")
        if login_db(user_name):
                page.go("/communities")
                print("logged in as " + user_name)
                init_dashboard()
                init_games()
                return True
        return False
               
    def signup(user_name):
        if not login(user_name):
            signup_db(user_name)
            page.go("/communities")
            print("registered as " + user_name)
            init_games()
    
    def join_community(com_name):
        join_community_db(com_name)
        page.go("/communities")
        
    def add_community(com_name):
        add_community_db(com_name)
        page.go("/communities")
        
    def set_up_current_betting_game(team_home_name, team_away_name, game_starts_at):
        update_betting_game(team_home_name, team_away_name, game_starts_at)
        page.go("/bet")
        
    def init_dashboard():
        
        for com in config.communities:
            df = pd.DataFrame(config.communities_data[com])
            print(df)
            if len(df.index) <= 7:
                dt = ft.DataTable(columns=headers(df), rows=rows(df))
            cards.append(ft.Card(
                ft.Container(
                    ft.Column(
                            [
                                ft.Text(com, style=ft.Text.style.HEADLINE_SMALL),
                                dt,
                            ],
                            scroll=ft.ScrollMode.AUTO
                        ),
                        padding=10,
                    ),
                    elevation=5,
                ),
            )
      
    def init_games():
        docs_ref = db.collection("games")
        docs = docs_ref.stream()
        for game in docs:
            team_home_name = game.to_dict().get("team_home_name", "")
            team_away_name = game.to_dict().get("team_away_name", "")
            game_starts_at = game.to_dict().get("game_starts_at", "")
            cells=[
                        ft.DataCell(ft.Text(team_home_name)),
                        ft.DataCell(ft.Text(team_away_name)),
                        ft.DataCell(ft.Text(game_starts_at)),
                ]
            if not game.to_dict().get("game_started"):
                cells.append(ft.DataCell(ft.ElevatedButton(
                    "Bet", 
                    on_click=lambda team_home_name, team_away_name, game_starts_at:
                    set_up_current_betting_game(team_home_name, team_away_name, game_starts_at)
                )
            ),)
            dt_games.rows.append(ft.DataRow(cells))
            
                
    
    #def add_community_data
        #TODO
        
            
    def set_up_dt_community(com):
        dt_community.columns=headers(config.communities_data[com])
        dt_community.rows=rows(config.communities_data[com])
        
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Betting App"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Login", on_click=lambda _: page.go("/login")),
                    ft.ElevatedButton("Sign up", on_click=lambda _: page.go("/signup")),
                ],
            )
        )
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.TextField(hint_text="Please enter your login information", label="Login Information", on_change=update_name),
                        ft.ElevatedButton("Login", on_click=lambda _: login(config.name)),
                    ],
                )
            )
        elif page.route == "/signup":
            page.views.append(
                ft.View(
                    "/signup",
                    [
                        ft.AppBar(title=ft.Text("Sign Up"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.TextField(hint_text="Please enter your name for registration", label="Sign Up", on_change=update_name),
                        ft.ElevatedButton("Sign up", on_click=lambda _: signup(config.name)),
                    ],
                )
            )
        elif page.route == "/communities":
            communities_view = ft.Column(
                [
                    ft.Text("My Communities:"),
                ]
            )
            if len(config.communities) > 0:
                for com in config.communities:
                    communities_view.controls.append(ft.ElevatedButton(com, on_click=lambda e: page.go("/community_" + e.control.text)))
            else:
                communities_view.controls.append(ft.Text("you haven't joined any communities"))
                
            if len(config.communities) < 5:
                    communities_view.controls.append(ft.ElevatedButton("Join a Community", on_click=lambda _: page.go("/communities_join")))
                
            page.views.append(
                ft.View(
                    "/communities",
                    [
                        ft.AppBar(title=ft.Text("Euro 2024 Communities"), leading=None, bgcolor=ft.colors.SURFACE_VARIANT),
                        communities_view,
                        navbar
                    ],
                )
            )
        elif page.route == "/communities_join":
            dd_join_community = ft.Dropdown(
                        label="Community",
                        hint_text="Choose community to join",
                        options=[],
                        width=200,
            )
            tf = ft.TextField(hint_text="New Community Name", label="New Community")
            com_list = get_communities_to_join()
            for com in com_list:
                dd_join_community.options.append(ft.dropdown.Option(com))
            page.views.append(
                ft.View(
                    "/communities_join",
                    [
                        ft.AppBar(title=ft.Text("Join Communities"), bgcolor=ft.colors.SURFACE_VARIANT),
                        dd_join_community,
                        ft.ElevatedButton("Join", on_click=lambda _: join_community(dd_join_community.value)),
                        tf,
                        ft.ElevatedButton("Add a new Community", on_click=lambda _: add_community(tf.value)),
                        navbar
                    ],
                )
            )
        elif page.route.startswith("/community_"):
            community_split = page.route.split("_")
            set_up_dt_community(community_split[1])
            page.views.append(
                ft.View(
                    "/community_" + community_split[1],
                    [
                        ft.AppBar(title=ft.Text("Community " + community_split[1]), bgcolor=ft.colors.SURFACE_VARIANT),
                        PaginatedDataTable(datatable=dt_community, rows_per_page=8),
                        navbar
                    ],
                )
            )
        
        elif page.route == "/dashboard":
            cards.insert(0, ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.SURFACE_VARIANT))
            cards.append(navbar)
            page.views.append(
                ft.View(
                    "/dashboard",
                    cards,
                )
            )
        elif page.route == "/games":
            page.views.append(
                ft.View(
                    "/games",
                    [
                        ft.AppBar(title=ft.Text("Games"), bgcolor=ft.colors.SURFACE_VARIANT),
                        PaginatedDataTable(datatable=dt_games, table_title="Games In Euro 2024", rows_per_page=5),
                        navbar
                    ],
                )
            )
        elif page.route == "/bet":
            items = [ft.Dropdown(
                        options=options_0_9,
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
                        options=options_0_9,
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
                        ft.ElevatedButton("Bet", on_click=lambda _: bet_on_game(items[0].value, items[2].value)),
                        navbar
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)