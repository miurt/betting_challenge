from firebase import db
from google.cloud import firestore
import pandas as pd
import config

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
        
def update_betting_game(team_home_name, team_away_name, game_starts_at):
    config.team_home = team_home_name
    config.team_away = team_away_name
    config.game_time = game_starts_at
    
def bet_on_game(first, second):
    doc_ref = db.collection("bets").document(config.name + "_" + config.game_time)
    doc_ref.set({"home_team": first,"away_team": second})
    
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