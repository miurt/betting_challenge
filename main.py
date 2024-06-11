import flet as ft
from helpers import set_communities_data
import config
from views import admin, auth, bet, communities, dashboard, games

def main(page: ft.Page): 
    page.title = "Betting App"
    page.adaptive = True
    
    def on_message(msg):
        print(str(msg))
        msg = msg.split(": ")
        if msg[0] == "admin" and page.route != "/admin":
            msg = msg[1].split("_")
            if msg[0] == "start":
                games.init_games(page)
                dashboard.init_dashboard(page)
                print(f"{msg[1]} started")
            elif msg[0] == "result":
                dashboard.init_dashboard(page)
                print(f"{msg[1]} new Score")
            elif msg[0] == "end":
                set_communities_data()
                print(f"{msg[1]} ended")
            page.update()
            page.go("/dashboard")
        elif msg[0] != config.name:
            print("Updating community data")
            set_communities_data()

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
    
    def navigation():
        match navbar.selected_index:
            case 0:
                page.go("/communities")
            case 1:
                page.go("/dashboard")
            case 2: 
                page.go("/games")
            case _:
                print("something wrong")              
        
    def route_change(route):
        page.views.clear()
        if page.route == "/":
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
        elif page.route == "/login":
            auth.login_view(page)
        elif page.route == "/signup":
            auth.signup_view(page)
        elif page.route == "/admin":
            admin.admin_view(page)
        elif page.route == "/communities":
            communities.communities_view(page, navbar)
        elif page.route == "/communities_join":
            communities.join_community_view(page, navbar)
        elif page.route.startswith("/community_"):
            communities.community_detail_view(page, page.route, navbar)
        elif page.route == "/dashboard":
            dashboard.dashboard_view(page, navbar)
        elif page.route == "/games":
            games.games_view(page, navbar)
        elif page.route == "/bet":
            bet.bet_view(page, navbar)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)