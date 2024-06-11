from sevices.firebase import db
from google.cloud import firestore
import pandas as pd
import flet as ft
import config

def headers(df: pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]

def rows(df: pd.DataFrame) -> list:
    return [ft.DataRow(cells=[ft.DataCell(ft.Text(row[header])) for header in df.columns]) for index, row in df.iterrows()]
    
def update_name(e):
    config.name = e.control.value
    
def login_db(user_name):
    user = db.collection('users').document(user_name).get()
    if user.exists:
        config.communities = user.to_dict().get("communities", [])
        set_communities_data()
        return True
    return False

def signup_db(user_name):
    user_ref = db.collection('users').document(user_name)
    if user_ref.get().exists:
        print("User alredy exists") 
    else:
        user_ref.set({"name": user_name, "communities": [], "points": 0})
    
def add_community_db(com_name):
    if len(config.communities) < 5:
        community_ref = db.collection("communities").document(com_name)
        community_ref.set({'name': com_name, 'members': []})
        return join_community_db(com_name)
    return False
    
def join_community_db(com_name):
    user_ref = db.collection("users").document(config.name)
    community_ref = db.collection("communities").document(com_name)
    if not community_ref.get().exists or not user_ref.get().exists:
        return False
    
    user_ref.update({"communities": firestore.ArrayUnion([com_name])})
    community_ref.update({"members": firestore.ArrayUnion([config.name])})
    config.communities.append(com_name)
    return True
    
def get_all_communities():
    docs = db.collection("communities").stream()
    return [doc.id for doc in docs]
    
def get_communities_to_join():
    if len(config.communities) < 5:
        com_all = get_all_communities()
        for x in config.communities:
            com_all.remove(x)
        return com_all
    return []
    
def bet_on_game_db(first, second):
    doc_ref = db.collection("bets").document(f"{config.name}_{config.game_time}")
    doc_ref.set({
        'user': config.name,
        'home_team': first,
        'away_team': second,
        'bet_time': pd.Timestamp.now()
    })
    
def set_games_today(today):
    config.games_today = []
    today_date = today.split(" ")[0]
    games = db.collection("games").stream()
    for game in games:
        game_date = game.id.split(" ")[0]
        if today_date == game_date:
            config.games_today.append(game.id)
    
def set_communities_data():
    docs = db.collection("communities").stream()
    #creating a dict of community and pd.DataFrame of users and points {community, pd.DataFrame}
    for doc in docs:
        members = doc.get("members")
        config.communities_data[doc.id] = {}
        users = db.collection("users").stream()
        data = []
        data = [[user.id, user.to_dict().get("points", 0)] for user in users if user.id in members]
        df = pd.DataFrame(data, columns=["User", "Points"])
        #adding ranking
        df.insert(loc=0, column="Position", value=df["Points"].rank(method='dense', ascending=False).astype('Int64'))
        df = df.sort_values(by=['Position', 'Points'], ascending=[True, True])
        config.communities_data[doc.id].update(df)
    return True

def add_single_community_data(com):
    doc = db.collection("communities").document(com).get()
    members = doc.get("members")
    config.communities_data[com] = {}
    users_ref = db.collection("users")
    users = users_ref.stream()
    data = [[user.id, user.to_dict().get("points", 0)] for user in users if user.id in members]
    df = pd.DataFrame(data, columns=["User", "Points"])
    #Adding ranking
    df.insert(loc=0, column="Position", value=df["Points"].rank(method='dense', ascending=False).astype('Int64'))
    df = df.sort_values(by=['Position', 'Points'], ascending=[True, True])
    config.communities_data[com].update(df)
    
        
def add_new_community_data(com):
    user = db.collection("users").document(config.name).get()
    config.communities_data[com] = {}
    data = [[user.id, user.to_dict().get("points", 0)]]
    df = pd.DataFrame(data, columns=["User", "Points"])
    df.insert(loc=0, column="Position", value=[1])
    config.communities_data[com].update(df)
    
    
#ADMIN FUNCTIONS START
    
def start_game_db(game):
     db.collection("games").document(game).update({"game_started": True})
    
def end_game_db(game):
    doc_ref = db.collection("games").document(game)
    doc_ref.update({"game_ended": True})
    doc = doc_ref.get()
    result_split = doc.to_dict().get("result", "0_0").split("_")
    home_team_result, away_team_result = result_split
    
    #POINTS UPDATE
    bets = db.collection("bets").stream()
    for bet in bets:
        bet_user, bet_game = bet.id.split("_")
        if bet_game == game:
            user_ref = db.collection("users").document(bet_user)
            user = user_ref.get()
            current_points = user.to_dict().get("points", 0)
            home_team, away_team = bet.to_dict().get("home_team", 0), bet.to_dict().get("away_team", 0)
            
            #8 points for the exact result
            if home_team_result == home_team and away_team_result == away_team:
                current_points += 8
            #6 points for the correct goal difference
            elif int(home_team_result) - int(away_team_result) == int(home_team) - int(away_team):
                current_points += 6
            #4 points for the correct tendency 
            elif (int(home_team_result) > int(away_team_result) and int(home_team) > int(away_team)) or \
                 (int(home_team_result) < int(away_team_result) and int(home_team) < int(away_team)):
                current_points += 4
            
            user_ref.update({"points": current_points})
            db.collection("bets").document(bet.id).delete()

        
def update_game_score_db(game, result):
    db.collection("games").document(game).update({"result": result})
    
#ADMIN FUCTIONS END