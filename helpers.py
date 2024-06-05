from firebase import db
from google.cloud import firestore
import pandas as pd
import flet as ft
import config


def headers(df : pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]

def rows(df : pd.DataFrame) -> list:
    rows = []
    for index, row in df.iterrows():
        rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows
    
def update_name(e):
    config.name = e.control.value
    
def login_db(user_name):
    users_ref = db.collection("users")
    docs = users_ref.stream()
    for doc in docs:
        if user_name == doc.id:
            config.communities = doc.to_dict().get("communities", [])
            set_communities_data()
            return True
    return False

def signup_db(user_name):
    users_ref = db.collection("users")
    docs = users_ref.stream()
    for doc in docs:
        if user_name == doc.id:
            print("User alredy exists")
    doc_ref = users_ref.document(user_name)        
    doc_ref.set({"name": user_name, "comunities": [], "points": 0})
    
def join_community_db(com_name):
    doc_ref = db.collection("users").document(config.name)
    doc_ref.update({"communities": firestore.ArrayUnion([com_name])})
        
    doc_ref = db.collection("communities").document(com_name)
    doc_ref.update({"members": firestore.ArrayUnion([config.name])})
    config.communities.append(com_name)
    
def get_all_communities():
    doc_ref = db.collection("communities")
    docs = doc_ref.stream()
    return [doc.id for doc in docs] 
    
def get_communities_to_join():
    if len(config.communities) < 5:
        com_all = get_all_communities()
        for x in config.communities:
            com_all.remove(x)
    return com_all

def add_community_db(com_name):
    if len(config.communities) < 5:
        doc_ref = db.collection("communities").document(com_name)
        doc_ref.set({})
        
        join_community_db(com_name)
    
def bet_on_game(first, second):
    doc_ref = db.collection("bets").document(config.name + "_" + config.game_time)
    doc_ref.set({"home_team": first,"away_team": second})
    
def set_games_today(today):
    today_time = today.split(" ")
    games_ref = db.collection("games")
    games = games_ref.stream()
    for game in games:
        game_time = game.id.split(" ")
        if today_time[0] == game_time[0]:
            config.games_today.append(game.id)
    
def set_communities_data():
    doc_ref = db.collection("communities")
    docs = doc_ref.stream()
    #creating a dict of community and pd.DataFrame of users and points {community, pd.DataFrame}
    for doc in docs:
        
        members = doc.get("members")
        config.communities_data[doc.id] = {}
        users_ref = db.collection("users")
        users = users_ref.stream()
        data = []
        for user in users:
            if user.id in members:
                data.append([user.id, user.to_dict().get("points", 0)])     
        df = pd.DataFrame(data, columns=["User", "Points"])
        #adding ranking
        df.insert(loc=0, column="Position", value = df["Points"].rank(method = 'dense',ascending = False).astype('Int64'))
        df = df.sort_values(by=['Position', 'Points'], ascending=[True, True])
        #print(df)
        config.communities_data[doc.id].update(df)
        
#ADMIN FUNCTIONS START
    
def start_game_db(game):
    doc_ref = db.collection("games").document(game)
    doc_ref.update({"game_started": True})
    
def end_game_db(game):
    doc_ref = db.collection("games").document(game)
    doc_ref.update({"game_ended": True})
    
    result_split = doc_ref.get("result").split("_")
    home_team_result = result_split[0]
    away_team_result = result_split[1]
    
    #POINTS UPDATE
    bets_ref = db.collection("bets")
    bets = bets_ref.stream()
    for bet in bets:
        bet_split = bet.id.split("_")
        if bet_split[1] == game:
            user_ref = db.collection("users").document(bet_split[0])
            current_points = user_ref.get("points", 0)
            home_team = bet.get("home_team")
            away_team = bet.get("away_team")
            #8 points for the exact result
            if home_team_result == home_team and away_team_result == away_team:
                current_points += 8
                user_ref.update({"points": current_points})
            #6 points for the correct goal difference
            elif home_team_result - away_team_result == home_team - away_team:
                current_points += 6
                user_ref.update({"points": current_points})
            #4 points for the correct tendency 
            elif (home_team_result > away_team_result and home_team > away_team) or (home_team_result < away_team_result and home_team < away_team):
                current_points += 4
                user_ref.update({"points": current_points})
            bets_ref.document(bet.id).delete()
        
def update_game_score_db(game, result):
    doc_ref = db.collection("games").document(game)
    doc_ref.update({"result": result})
    
#ADMIN FUCTIONS END