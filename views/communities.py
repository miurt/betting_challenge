import flet as ft
import config
import pandas as pd
from components.leaderboard_dt import LeaderboardDataTable
from helpers import add_community_db, add_new_community_data, add_single_community_data, get_communities_to_join, join_community_db
from views.dashboard import init_dashboard

communities_view_ = ft.Column(controls = [])

def communities_view(page: ft.Page, navbar):
    communities_view_.controls.clear()
    communities_view_.controls.append(ft.Text("My Communities:", theme_style=ft.TextThemeStyle.HEADLINE_SMALL))
    if len(config.communities) > 0:
        for com in config.communities:
            communities_view_.controls.append(ft.ElevatedButton(com, on_click=lambda e: page.go("/community_" + e.control.text)))
    else:
        communities_view_.controls.append(ft.Text("you haven't joined any communities"))
                
    if len(config.communities) < 5:
        communities_view_.controls.append(ft.ElevatedButton("Join a Community", on_click=lambda _: page.go("/communities_join")))
            
    communities_view_.alignment=ft.alignment.center
    page.views.append(
            ft.View(
                "/communities",
                [
                    ft.AppBar(title=ft.Text("Euro 2024 Communities"), leading=None, bgcolor=ft.colors.SURFACE_VARIANT),
                    communities_view_,
                    navbar
                ],
            )
        )

def join_community_view(page: ft.Page, navbar):
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
                ft.ElevatedButton("Join", on_click=lambda _: join_community(dd_join_community.value, page)),
                tf,
                ft.ElevatedButton("Add a new Community", on_click=lambda _: add_community(tf.value, page)),
                navbar
            ],
        )
    )

def community_detail_view(page: ft.Page, route: str, navbar):
    community_split = route.split("_")
    df_community = pd.DataFrame(config.communities_data[community_split[1]])
    leaderboard = LeaderboardDataTable(dataframe=df_community, com = community_split[1], user = config.name)
    page.views.append(
        ft.View(
            "/community_" + community_split[1],
            [
                ft.AppBar(title=ft.Text("Community " + community_split[1]), bgcolor=ft.colors.SURFACE_VARIANT),
                leaderboard,
                navbar
            ],
            scroll=ft.ScrollMode.ADAPTIVE
        )
    )
    
def join_community(com_name, page: ft.Page):
        page.pubsub.send_all(f"{config.name}: {com_name}")
        if join_community_db(com_name):
            add_single_community_data(com_name)
        init_dashboard(page)
        page.update()
        page.go("/communities")
        
def add_community(com_name, page: ft.Page):
        if add_community_db(com_name):
            add_new_community_data(com_name)
            init_dashboard(page)
        init_dashboard(page)
        page.update()
        page.go("/communities")
