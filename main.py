import flet as ft
from firebase import db
from paginated_dt import PaginatedDataTable
from leaderboard_dt import LeaderboardDataTable
from collections import defaultdict
from helpers import(
    update_name,
    login_db,
    signup_db,
    join_community_db,
    get_communities_to_join,
    add_community_db,
    bet_on_game_db, 
    headers,
    rows,
    start_game_db,
    end_game_db,
    update_game_score_db,
    set_games_today,
    set_communities_data,
    ButtonWithInfo
    #add_user_to_community_data
    )
import pandas as pd
import config

current_time = "2024-06-15 8:00:00"

def main(page: ft.Page): 
    page.title = "Betting App"
    page.adaptive = True
    
    def on_message(msg):
        print(str(msg))
        msg = msg.split(": ")
        #ADMIN UPDATES
        if msg[0] == "admin":
            msg = msg[0].split("_")
        #Game started
            if msg[0] == "start":
                init_games()
                init_dashboard()
        #Game result updated
            if msg[0] == "result":
                init_dashboard()
        #Game ended
            if msg[0] == "end":
                set_communities_data()
            page.go("/admin")
            page.update()
            page.go("/admin")
        
        #ADMIN UPDATES END
        
        else:
            set_communities_data()
            #new_user = msg[0]
            #com = msg[1]
            #add_user_to_community_data(new_user, com)
        
            page.update()

    page.pubsub.subscribe(on_message)
    
    navbar = ft.NavigationBar(
                            destinations=[
                                ft.NavigationDestination(icon=ft.icons.GROUPS_OUTLINED, selected_icon=ft.icons.GROUPS, label="Communities"),
                                ft.NavigationDestination(icon=ft.icons.DASHBOARD_OUTLINED, selected_icon=ft.icons.DASHBOARD, label="Dashboard"),
                                ft.NavigationDestination(icon=ft.icons.SPORTS_SOCCER_OUTLINED, selected_icon=ft.icons.SPORTS_SOCCER, label="Games",
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
    
    options_0_9 = [ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                    ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                    ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                    ft.dropdown.Option(9),]
    
    games_view = ft.Column(controls = [])
    
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
            set_games_today(current_time)
            page.go("/admin")
        elif login_db(user_name):
                page.go("/communities")
                print("logged in as " + user_name)
                set_games_today(current_time)
                init_games()
                init_dashboard()
                return True
        return False
               
    def signup(user_name):
        if not login(user_name):
            signup_db(user_name)
            page.go("/communities")
            print("registered as " + user_name)
            set_games_today(current_time)
            init_games()
            init_dashboard()
            
    
    def join_community(com_name):
        page.pubsub.send_all(f"{config.name}: {com_name}")
        join_community_db(com_name)
        page.go("/communities")
        
    def add_community(com_name):
        add_community_db(com_name)
        page.go("/communities")
        
    def set_up_current_betting_game(team_home_name, team_away_name, game_starts_at):
        config.team_home = team_home_name
        config.team_away = team_away_name
        config.game_time = game_starts_at
        page.go("/bet")
        
    def bet_on_game(first, second):
        bet_on_game_db(first, second)
        page.go("/games")
        
    def init_dashboard():
        #Preview for today games
        cards.clear()
        for game in config.games_today:
            doc_ref = db.collection("games").document(game)
            doc = doc_ref.get()
            game_started = doc.to_dict().get("game_started", False)
            team_home = doc.to_dict().get("team_home_name", "")
            team_away = doc.to_dict().get("team_away_name", "")
            text = [ft.Text(team_home + " vs " + team_away, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text("Today at: " + game, theme_style=ft.TextThemeStyle.HEADLINE_SMALL)]
            
            if game_started:
                result = doc.to_dict().get("result", "")
                text.append(ft.Text("Score: " + result, theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
            cards.append(
                ft.Card(
                    ft.Column(
                        text
                    )
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
                                    ft.TextButton(com, on_click=lambda e: page.go("/community_" + e.control.text)),
                                ],
                                alignment=ft.alignment.bottom_right
                            ),
                        ]
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
            started = game.to_dict().get("game_started", False)
            x = [team_home_name, team_away_name, game_starts_at]
            dt_games.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(team_home_name)),
                        ft.DataCell(ft.Text(team_away_name)),
                        ft.DataCell(ft.Text(game_starts_at)),
                        ft.DataCell(ButtonWithInfo(
                                text = "Bet", 
                                info = [team_home_name, team_away_name, game_starts_at, started],
                                on_click=lambda e: set_up_current_betting_game(e.control.info[0], e.control.info[1], e.control.info[2])
                            )
                        )
                    ]
                )
            )
        
    #ADMIN FUNCTIONS START
    
    def start_game(game):
        start_game_db(game)
        page.pubsub.send_all("admin: start_"+ f"{game}")
        page.update()
    
    def end_game(game):
        end_game_db(game)
        page.pubsub.send_all("admin: end_" + f"{game}")
        page.update()
    
    def update_game_score(game, result):
        update_game_score_db(game, result)
        page.pubsub.send_all("admin: result_" + f"{game}")
        page.update()
    
    #ADMIN FUCTIONS END
        
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
            #ADMIN MODE
        elif page.route == "/admin":
            games_view.controls.clear()
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
            games_view.controls.append(ft.Text("Today's Games:", theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
            if len(config.games_today) > 0:
                for game in config.games_today:
                    doc_ref = db.collection("games").document(game)
                    doc = doc_ref.get()
                    game_started = doc.to_dict().get("game_started", False)
                    team_home = doc.to_dict().get("team_home_name", "")
                    team_away = doc.to_dict().get("team_away_name", "")
                    games_view.controls.append(ft.Text(team_home + " vs " + team_away, theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
                    if not game_started:
                        games_view.controls.append(ButtonWithInfo(text ="Start", info = [game], on_click=lambda e: start_game(e.control.info[0])))
                    else:
                        games_view.controls.extend(
                            [
                                ft.Row(spacing=3, controls=items),
                                ButtonWithInfo(text = "Update", info = [game], on_click=lambda e: update_game_score(e.control.info[0], str(items[0].value) + "_" + str(items[2].value))),
                                ButtonWithInfo(text = "Stop", info = [game], on_click=lambda e: end_game(e.control.info[0])),
                            ]
                        )
            
            games_view.alignment=ft.alignment.center
            page.views.append(
                ft.View(
                    "/communities",
                    [
                        #GAMES TODAY #START 
                        #IF STARTED UPDATE SCORE / END
                        games_view,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
            
        elif page.route == "/communities":
            communities_view = ft.Column(
                [
                    ft.Text("My Communities:", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                ],
            )
            if len(config.communities) > 0:
                for com in config.communities:
                    communities_view.controls.append(ft.ElevatedButton(com, on_click=lambda e: page.go("/community_" + e.control.text)))
            else:
                communities_view.controls.append(ft.Text("you haven't joined any communities"))
                
            if len(config.communities) < 5:
                    communities_view.controls.append(ft.ElevatedButton("Join a Community", on_click=lambda _: page.go("/communities_join")))
            
            communities_view.alignment=ft.alignment.center
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
            df_community = pd.DataFrame(config.communities_data[community_split[1]])
            page.views.append(
                ft.View(
                    "/community_" + community_split[1],
                    [
                        ft.AppBar(title=ft.Text("Community " + community_split[1]), bgcolor=ft.colors.SURFACE_VARIANT),
                        LeaderboardDataTable(dataframe=df_community, com = community_split[1], user = config.name),
                        navbar,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        
        elif page.route == "/dashboard":
            cards.insert(0, ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.SURFACE_VARIANT))
            cards.append(navbar)
            page.views.append(
                ft.View(
                    "/dashboard",
                    cards,
                    scroll=ft.ScrollMode.ADAPTIVE
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

ft.app(target=main, view = ft.WEB_BROWSER)