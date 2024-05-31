import flet as ft
from google.cloud import firestore
from firebase import db
from paginated_dt import PaginatedDataTable
from collections import defaultdict
import config

def main(page: ft.Page): 
    page.title = "Betting App"
    page.adaptive = True
    
    #creating one dictionary of many dictionaries with default value of list.
    d = defaultdict(lambda: defaultdict(list))
    
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
    
    dt_community= ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Position")),
                ft.DataColumn(ft.Text("User")),
                ft.DataColumn(ft.Text("Points")),
            ],
            rows=[],
        )
            
    def update_name(e):
        config.name = e.control.value
        
    def update_communities(e):
        config.communities = e
        get_communities_data()
    
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
        users_ref = db.collection("users")
        docs = users_ref.stream()
        for doc in docs:
            if user_name == doc.id:
                page.go("/communities")
                print("logged in as " + user_name)
                update_communities(doc.to_dict().get("communities", []))
                init()
                return True
        return False
               
    def signup(user_name):
        if not login(user_name):
            users_ref = db.collection("users")
            doc_ref = users_ref.document(user_name)
            doc_ref.set({"name": user_name, "comunities": [], "friends": [], "points": 0})
            page.go("/communities")
            print("registered as " + user_name)
            init()
            #page.client_storage.set("name", name)
            #page.client_storage.set("communities", [])
            #page.client_storage.set("friends", [])
            
    def get_all_communities():
        doc_ref = db.collection("communities")
        docs = doc_ref.stream()
        return [doc.id for doc in docs] 
    
    def get_communities_to_join():
        #com = page.client_storage.get("communities")
        if len(config.communities) < 5:
            com_all = get_all_communities()
            for x in config.communities:
                com_all.remove(x)
        return com_all
    
    def join_community(com_name):
        doc_ref = db.collection("users").document(config.name)
        doc_ref.update({"communities": firestore.ArrayUnion([com_name])})
        
        doc_ref = db.collection("communities").document(com_name)
        doc_ref.update({"members": firestore.ArrayUnion([config.name])})
        #page.client_storage.get("communities").append(com_name)
        config.communities.append(com_name)
        page.go("/communities")
            
        
    def add_community(com_name):
        if len(config.communities) < 5:
            #print(com_name)
            doc_ref = db.collection("communities").document(com_name)
            doc_ref.set({})
        
            join_community(com_name)
    
    def bet_on_game(first, second):
        doc_ref = db.collection("bets").document(config.name + "_" + config.game_time)
        doc_ref.set({"home_team": first,"away_team": second})
        
    def set_up_current_betting_game(team_home_name, team_away_name, game_starts_at):
        config.team_home = team_home_name
        config.team_away = team_away_name
        config.game_time = game_starts_at
        page.go("/bet")
      
    def init():
        docs_ref = db.collection("games")
        docs = docs_ref.stream()
        for game in docs:
            team_home_name = game.to_dict().get("team_home_name", "")
            team_away_name = game.to_dict().get("team_away_name", "")
            game_starts_at = game.to_dict().get("game_starts_at", "")
            dt_games.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(team_home_name)),
                        ft.DataCell(ft.Text(team_away_name)),
                        ft.DataCell(ft.Text(game_starts_at)),
                        #TODO: Change for already started games
                        #TODO: Fix names
                        ft.DataCell(ft.ElevatedButton("Bet", 
                                                      on_click=lambda team_home_name, team_away_name, game_starts_at:
                                                          set_up_current_betting_game(team_home_name, team_away_name, game_starts_at)
                                )
                            ),
                    ],
                ),)
            
            
    def get_communities_data():
        #config.communities_data = defaultdict(list)
        doc_ref = db.collection("communities")
        docs = doc_ref.stream()
        #creating a dict of keys: communities with value: list of dict with key:member_name and value: points 
        for doc in docs:
            members = doc.get("members")
            config.communities_data[doc.id] = {}
            users_ref = db.collection("users")
            users = users_ref.stream()
            for user in users:
                if user.id in members:
                    #users_dict_list.append({user.id, user.to_dict().get("points", 0)})
                    config.communities_data[doc.id].update({user.id : user.to_dict().get("points", 0)})
                    #print(user.id, user.to_dict().get("points", 0))
                    print(doc.id, config.communities_data[doc.id])
            #communities_data.update({doc.id, defaultdict(users_dict_list)})
    
    #def add_community_data
        #TODO
        
            
    def set_up_dt_community(com):
        print(com)
        print(config.communities_data[com])
        dt_community.rows = []
        for user in config.communities_data[com]:
            print(user)
            dt_community.rows.append(ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text(0)),
                                            ft.DataCell(ft.Text(user)),
                                            ft.DataCell(ft.Text(config.communities_data[com][user])),
                                            ],
                                        )
            )
        
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
                        #ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
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
                        #ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        elif page.route == "/communities":
            #com_list = page.client_storage.get("communities")
            
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
                        ft.AppBar(title=ft.Text("Euro 2024 Communities"), bgcolor=ft.colors.SURFACE_VARIANT),
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
            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.SURFACE_VARIANT),
                        navbar
                    ],
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
                        options=[ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                 ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                 ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                 ft.dropdown.Option(9),],
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
                        options=[ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                 ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                 ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                 ft.dropdown.Option(9),],
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