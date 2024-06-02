from firebase import db

data = """Deutschland;Schottland;2024-06-14 19:00:00
Ungarn;Schweiz;2024-06-15 13:00:00
Spanien;Kroatien;2024-06-15 16:00:00
Italien;Albanien;2024-06-15 19:00:00
tbd;Niederlande;2024-06-16 13:00:00
Slowenien;Dänemark;2024-06-16 16:00:00
Serbien;England;2024-06-16 19:00:00
Rumänien;tbd;2024-06-17 13:00:00
Belgien;Slowakei;2024-06-17 16:00:00
Österreich;Frankreich;2024-06-17 19:00:00
Türkei;tbd;2024-06-18 16:00:00
Portugal;Tschechische Republik;2024-06-18 19:00:00
Kroatien;Albanien;2024-06-19 13:00:00
Deutschland;Ungarn;2024-06-19 16:00:00
Schottland;Schweiz;2024-06-19 19:00:00
Slowenien;Serbien;2024-06-20 13:00:00
Dänemark;England;2024-06-20 16:00:00
Spanien;Italien;2024-06-20 19:00:00
Slowakei;tbd;2024-06-21 13:00:00
tbd;Österreich;2024-06-21 16:00:00
Niederlande;Frankreich;2024-06-21 19:00:00
tbd;Tschechische Republik;2024-06-22 13:00:00
Türkei;Portugal;2024-06-22 16:00:00
Belgien;Rumänien;2024-06-22 19:00:00
Schottland;Ungarn;2024-06-23 19:00:00
Schweiz;Deutschland;2024-06-23 19:00:00
Albanien;Spanien;2024-06-24 19:00:00
Kroatien;Italien;2024-06-24 19:00:00
Niederlande;Österreich;2024-06-25 16:00:00
Frankreich;tbd;2024-06-25 16:00:00
England;Slowenien;2024-06-25 19:00:00
Dänemark;Serbien;2024-06-25 19:00:00
Slowakei;Rumänien;2024-06-26 16:00:00
tbd;Belgien;2024-06-26 16:00:00
tbd;Portugal;2024-06-26 19:00:00
Tschechische Republik;Türkei;2024-06-26 19:00:00
2A;2B;2024-06-29 16:00:00
1A;2C;2024-06-29 19:00:00
1C;3EDF;2024-06-30 16:00:00
1B;ADEF;2024-06-30 19:00:00
2D;2E;2024-07-01 16:00:00
1F;3ABC;2024-07-01 19:00:00
1E;ABCD;2024-07-02 16:00:00
1D;2F;2024-07-02 19:00:00
W39;W37;2024-07-05 16:00:00
W41;W42;2024-07-05 19:00:00
W40;W38;2024-07-06 16:00:00
W43;W44;2024-07-06 19:00:00
W45;W46;2024-07-09 19:00:00
W47;W48;2024-07-10 19:00:00
W49;W50;2024-07-14 19:00:00"""

def upload_data():
    #team_home_name;team_away_name;game_starts_at
    print("start upload")
    games_ref = db.collection("games")
    for game in data.split("\n"):
        game_split = game.split(";")
        doc_ref = games_ref.document(game_split[2])
        doc_ref.update({"game_started": False,
                     "game_ended": False,
                     "result" : ""
                     })
        print("uploaded" + game_split[2])
    print("finish upload")
    #doc_ref = games_ref.document(name)
    #doc_ref.set({"name": name})
    