from flask import Flask, render_template, make_response
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import FlaskApp.sql
from flask import request, flash
import json
import requests
import csv
from datetime import date
from datetime import datetime
#https://127.0.0.1:5000/


#mysql = MySQL()
cursor = None
competitionId = 467

db = None
tournamentPos = 0
stages = []
teams = [] 
places = []
rounds = [] 
games = []
dates = []
games_clear = []
games_update = []
games_update2 = []
games_playoff = []
tournaments = []
space = None

teams_name_dic = {}

outGroups = [{ "name":"NATIONAL TEAMS", "color":"#ABDDA4"}, { "name":"WORLD CUP SCHEDULE", "color":"#2c7bb6"},
             { "name":"CITIES AND STADIUMS", "color":"#d7191c"}, { "name":"GROUPS ANS STAGES", "color":"#d7c119"}]


dic_sliceId = {}
dic_name2sliceId = {}
dic_sliceId2name = {}

dic_slice_2_games = {} #связь кусочка с играми

dic_games = {} #все игры для вывода

settings = {"sql_host":"us-iron-auto-dca-04-a.cleardb.net", 
            "sql_user":"b1df3776b2b56c",
            "sql_passwd":"2153543acdac76f",
            "sql_db":"heroku_0c1d0ea4e380413"
           }

token = 'efda008899e346f693efa9c75f9577ee'
myheaders = { 'X-Auth-Token': token, 'X-Response-Control': 'minified' }
main_url = 'http://api.football-data.org'


#extraTimeHomeGoals, extraTimeAwayGoals, penaltyShootoutHomeGoals, penaltyShootoutAwayGoals

def get_update_data_by_league_id(Idleague):
    global games, games_update, games_update2
    url = main_url +  '/v1/competitions/' + str(Idleague) + '/fixtures'
    resp = requests.get(url, headers = myheaders)
    resp = resp.json()["fixtures"] 
    res_update = [{"id":str(r["homeTeamId"]) + str(r["awayTeamId"]) + getNormalDate(r["date"]),"id2":str(r["date"]),"awayTeamId":r["awayTeamId"], "homeTeamId":r["homeTeamId"],"status":r["status"], "date":r["date"], "goalsHomeTeam": r["result"]["goalsHomeTeam"], "goalsAwayTeam": r["result"]["goalsAwayTeam"], "penaltyShootoutHomeGoals":r["result"].get("penaltyShootout", {}).get("goalsHomeTeam", None), "penaltyShootoutAwayGoals":r["result"].get("penaltyShootout", {}).get("goalsAwayTeam", None),
"extraTimeHomeGoals":r["result"].get("extraTime", {}).get("goalsHomeTeam", None), "extraTimeAwayGoals":r["result"].get("extraTime", {}).get("goalsAwayTeam", None)} for r in resp if (r["status"] != "TIMED" and  r["status"] != "SCHEDULED") or int(r["homeTeamId"]) != 757] 

    for r in res_update:
        if r["id"] in games_update:
            db.updateTableFromConditions("games", {"competitionId": competitionId,  "homeTeamId": r["homeTeamId"],  "awayTeamId": r["awayTeamId"], "date": r["date"]}, {"status":r["status"], "goalsHomeTeam":r["goalsHomeTeam"],  "goalsAwayTeam":r["goalsAwayTeam"]})
            games = db.getDictFromQueryRes("games", {"competitionId": competitionId})    
        if r["id2"] in games_update2:
            if r["goalsHomeTeam"] != None:
                db.updateTableFromConditions("games", {"competitionId": competitionId,  "date": r["date"]}, {"status":r["status"], "goalsHomeTeam":r["goalsHomeTeam"],  "goalsAwayTeam":r["goalsAwayTeam"],  "homeTeamId": r["homeTeamId"],  "awayTeamId": r["awayTeamId"], "penaltyShootoutHomeGoals":r["penaltyShootoutHomeGoals"],"penaltyShootoutAwayGoals":r["penaltyShootoutAwayGoals"], "extraTimeHomeGoals":r["extraTimeHomeGoals"], "extraTimeAwayGoals":r["extraTimeAwayGoals"]})
            else:
                db.updateTableFromConditions("games", {"competitionId": competitionId,  "date": r["date"]}, {"status":r["status"], "homeTeamId": r["homeTeamId"],  "awayTeamId": r["awayTeamId"],  "penaltyShootoutHomeGoals":r["penaltyShootoutHomeGoals"], "penaltyShootoutAwayGoals":r["penaltyShootoutAwayGoals"], "extraTimeHomeGoals":r["extraTimeHomeGoals"], "extraTimeAwayGoals":r["extraTimeAwayGoals"]})
            games = db.getDictFromQueryRes("games", {"competitionId": competitionId})    

    return res_update




app = Flask(__name__)
app.config.from_object(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

def xstr(s):
    if s is None:
        return ''
    return str(s)

def getNormalDate(DateStr):
    return str(datetime.strptime(DateStr.strip()[0:10], '%Y-%m-%d'))[0:10]


def getConnectionBySliceId(sliceId):
    if sliceId not in dic_sliceId or sliceId not in dic_sliceId2name:
        return [-1]
    groupId = dic_sliceId[sliceId]
    if groupId == 0:
        return getAllCorellByTeamId(dic_sliceId2name[sliceId])     
    elif groupId == 1:  
        return getAllCorellByDate(dic_sliceId2name[sliceId])  
    elif groupId == 2:  
        return getAllCorellByPlace(dic_sliceId2name[sliceId]) 
    elif groupId == 3:  
        return getAllCorellByStage(dic_sliceId2name[sliceId]) 

#по команде возвращаем
#календарь, стадионы, стадии
def getAllCorellByTeamId(teamId):
    teamId = str(teamId)
    places = [g["placeId"] for g in games if g["homeTeamId"] == teamId or g["awayTeamId"] == teamId]
    dates =  [getNormalDate(g["date"]) for g in games if g["awayTeamId"] == teamId or g["homeTeamId"] == teamId ] 
    _stages = ["s" + str(d["id_stage"]) for d in games if d["awayTeamId"] == teamId or d["homeTeamId"] == teamId]
    dic_slice_2_games[dic_name2sliceId[teamId]] += [g["id"] for g in games if g["awayTeamId"] == teamId or g["homeTeamId"] == teamId]
    names = dates + _stages + places
    sliceIds = []
    for name in names:
        if name in dic_name2sliceId:
            sliceIds.append(dic_name2sliceId[name])
    return sliceIds


#по дате игры возвращаем
#группы, команды, места
def getAllCorellByDate(date):
    places = [g["placeId"] for g in games if getNormalDate(g["date"]) == date]
    teams = [g["homeTeamId"] for g in games if getNormalDate(g["date"]) == date] + [g["awayTeamId"] for g in games if getNormalDate(g["date"]) == date]  
    _stages = ["s" + str(d["id_stage"]) for d in games if getNormalDate(d["date"]) == date]
    dic_slice_2_games[dic_name2sliceId[date]] += [g["id"] for g in games if getNormalDate(g["date"]) == date]
    names = teams + _stages + places
    sliceIds = []
    for name in names:
        if name in dic_name2sliceId:
            sliceIds.append(dic_name2sliceId[name])
    return sliceIds

#по месту возвращаем
#группы, команды, даты
def getAllCorellByPlace(placeId):
    dates = [getNormalDate(g["date"]) for g in games if g["placeId"] == placeId]
    teams = [g["homeTeamId"] for g in games if g["placeId"] == placeId] + [g["awayTeamId"] for g in games if g["placeId"] == placeId] 
    _stages = ["s" + str(d["id_stage"]) for d in games if d["placeId"] == placeId]
    dic_slice_2_games[dic_name2sliceId[placeId]] += [g["id"] for g in games if g["placeId"] == placeId]
    names = dates + _stages + teams
    sliceIds = []
    for name in names:
        if name in dic_name2sliceId:
            sliceIds.append(dic_name2sliceId[name])
    return sliceIds

#по группе возвращаем
#места, команды, даты
def getAllCorellByStage(id_stage):
    teams =  [g["homeTeamId"] for g in games if "s" + str(g["id_stage"]) == id_stage] + [g["awayTeamId"] for g in games if "s" + str(g["id_stage"]) == id_stage]  
    dates = [getNormalDate(g["date"]) for g in games if "s" + str(g["id_stage"]) == id_stage]
    places = [g["placeId"] for g in games if "s" + str(g["id_stage"]) == id_stage]
    dic_slice_2_games[dic_name2sliceId[id_stage]] += [g["id"] for g in games if "s" + str(g["id_stage"]) == id_stage]
    names = dates + places + teams
    sliceIds = []
    for name in names:
        if name in dic_name2sliceId:
            sliceIds.append(dic_name2sliceId[name])
    return sliceIds

'''
def get_playoff_data():
    global games_clear
    games_playoff = []
    for stage in range(20, 15, -1):
        g_p = [g for g in games if g["id_stage"] = stage]
        games_playoff.append[g_p]
    for gps in games_playoff:
        for gp in gps:
        

        

        for g in games:
            if g["id_stage"] == stage:
                gs["key"] = 

 levelGroups[i], parent: p, team1: p1, team2: p2, parentNumber: parentNumber 
'''       
         


def get_playoff_data():
    global games_clear,  games_playoff
    result_playoff = []
    playoff_games = {}
    for stage in range(13, 8, -1):
        pg = [g for g in games_clear if int(g["id_stage"]) == stage]
        for g in pg:
            g["pair"] = [g["teamHome"], g["teamAway"]]
            g["key"] = None
            g["parent"] = None
            g["goalsHomeTeam"] = g["goalsHomeTeamExtra"] 	
            g["goalsAwayTeam"] = g["goalsAwayTeamExtra"] 
           	
        playoff_games[stage] = pg  
    for stage in range(13, 8, -1):
        i = 0
        for g in  playoff_games[stage]:
            g["key"] = str(stage) + "-" + str(i)
            i += 1
            if stage == 9:
                continue;
            if stage == 11:
                g["parent"] = "13-0"

            for child in  playoff_games[stage-1]:
                if (g["teamHome"] in child["pair"] or g["teamAway"] in child["pair"]) and child["parent"] == None :
                    child["parent"] = g["key"]
    
    for p in playoff_games:
        result_playoff = result_playoff + playoff_games[p]
    del  playoff_games
    del  games_playoff
    games_playoff = result_playoff 
    	
    del result_playoff 

def init_data(_competitionId = competitionId):
    global stages, games, teams, places, games_update, rounds,  space, stages, db, dates, games_update2, games_playoff, games_clear, tournaments, tournamentPos 
    #initSQL()
    #settings  = read_params("settings2.json")
    #print(settings)
    db = FlaskApp.sql.database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])
    places = db.getDictFromQueryRes("places", {"competitionId": _competitionId})  
    rounds = db.getDictFromQueryRes("rounds", {"competitionId": _competitionId})
    stages = db.getDictFromQueryRes("stages", {"competitionId": _competitionId})    
    games = db.getDictFromQueryRes("games", {"competitionId": _competitionId})
    tournaments = db.getDictFromQueryRes("tournaments")
    i = 0
    for t in tournaments:
        t["position"] = i
        if int(t["id"]) == int(_competitionId):
            tournamentPos = i 
        i += 1  
    teams_ids = [g["homeTeamId"] for g in games] + [g["awayTeamId"] for g in games]  
    teams = [team for team in db.getDictFromQueryRes("teams_wc") if str(team["id"]) in teams_ids] 
    dates = [str(r["date"]).strip()[0:10] for r in games] 
    dates = sorted(list(set(dates)))
    #games_update = [str(g["homeTeamId"]) + str(g["awayTeamId"]) + getNormalDate(g["date"]) for g in games if g["status"] != "FINISHED" ]
    #games_update2 = [str(g["date"])  for g in games if g["status"] != "FINISHED" and int(g["homeTeamId"]) == 757]
    res_update = None
    '''
    try:
        get_update_data_by_league_id(competitionId)
    except:
        print("error of api request")
        res_update = None
    '''
    #установим id, чтоб потом ссылаться
    i = 0
    del games_clear
    games_clear = []
    for g in games:
        g_new = get_game_dic(g)
        g["id"] = i 
        g_new["id"] = g["id"]
        i += 1   
        games_clear.append (g_new)
    get_playoff_data()

def get_result_string(g):
    if g["goalsHomeTeam"] is None:
        return None
    if g["extraTimeHomeGoals"] != None:
        if g["penaltyShootoutHomeGoals"] != None:
            return str(g["extraTimeHomeGoals"]) + "(" + str(g["penaltyShootoutHomeGoals"]) +  ")"  + ":" + str(g["extraTimeAwayGoals"]) + "(" + str(g["penaltyShootoutAwayGoals"])  + ")" 
        else:
            return str(g["extraTimeHomeGoals"]) +  ":" + str(g["extraTimeAwayGoals"]) 
    else:  
            return str(g["goalsHomeTeam"]) + ":" + str(g["goalsAwayTeam"])
    
def get_result_home(g):
    if g["goalsHomeTeam"] is None:
        return None
    if g["extraTimeHomeGoals"] != None:
        if g["penaltyShootoutHomeGoals"] != None:
            return str(g["extraTimeHomeGoals"]) + "(" + str(g["penaltyShootoutHomeGoals"]) +  ")" 
        else:
            return str(g["extraTimeHomeGoals"]) 
    else:  
            return str(g["goalsHomeTeam"]) 

def get_result_away(g):
    if g["goalsHomeTeam"] is None:
        return None
    if g["extraTimeHomeGoals"] != None:
        if g["penaltyShootoutHomeGoals"] != None:
            return str(g["extraTimeAwayGoals"]) + "(" + str(g["penaltyShootoutAwayGoals"])  + ")" 
        else:
            return str(g["extraTimeAwayGoals"]) 
    else:  
            return str(g["goalsAwayTeam"])
    


def get_result_string(g):
    if g["goalsHomeTeam"] is None:
        return None
    if g["extraTimeHomeGoals"] != None:
        if g["penaltyShootoutHomeGoals"] != None:
            return str(g["extraTimeHomeGoals"]) + "(" + str(g["penaltyShootoutHomeGoals"]) +  ")"  + ":" + str(g["extraTimeAwayGoals"]) + "(" + str(g["penaltyShootoutAwayGoals"])  + ")" 
        else:
            return str(g["extraTimeHomeGoals"]) +  ":" + str(g["extraTimeAwayGoals"]) 
    else:  
            return str(g["goalsHomeTeam"]) + ":" + str(g["goalsAwayTeam"])


def get_game_dic(g):
    game = {}
    try:
        p = [p for p in places if p["id"] == g["placeId"]][0]
        game["stadium"] = p["stadium"].split("|")[0] 
        game["city"] = p["city"]
    except:
        game["stadium"] = None 
        game["city"] = None    
    
    
    game["teamAway"] = None
    try:
        game["teamHome"] = [t for t in teams if str(t["id"]) == g["homeTeamId"]][0]["name"]
    except:
        game["teamHome"] = None
    try:
        game["teamAway"] = [t for t in teams if str(t["id"]) == g["awayTeamId"]][0]["name"]
    except:
        game["teamAway"] = None
    if(g["goalsAwayTeam"] == None):     
        game["result"] = g["status"][0:5]
    else:
        game["result"] = get_result_string(g)
    game["date"] = g["date"][5:7] + "." + g["date"][8:10]
    game["time"] = g["date"][11:16]
    game["goalsAwayTeam"] = g["goalsAwayTeam"]
    game["goalsHomeTeam"] = g["goalsHomeTeam"]
    game["goalsHomeTeamExtra"] = get_result_home(g)	
    game["goalsAwayTeamExtra"] = get_result_away(g)
    game["id_stage"] = g["id_stage"]
    return game


        

def render():
    global stages, teams, places, rounds,  space, games, places, dic_slice_2_games, dates, tournaments, tournamentPos 
    sliceId = 0
    shares = {"teams":350, "calendar":600//3, "places":650//3, "stages":400 - 650//3}
    space  = (1000 - (shares["teams"] + shares["calendar"] +  shares["places"] + shares["stages"])) // 4
    calendar = []
    #список команд
    for t in teams:
        t["value"] =  shares["teams"] / len(teams)
        t["color"] = "#4daa4b"
        t["sliceId"] = sliceId
        t["id_group"] = 0
        teams_name_dic[str(t["id"])] = t["name"] 
        dic_sliceId[sliceId] = 0
        dic_name2sliceId[str(t["id"])] = sliceId
        dic_sliceId2name[sliceId] = t["id"]
        sliceId += 1

    sliceId += 1 #для пространства
    #календарь игр
    for date in dates:
        c = {}
        strTime =  getNormalDate(date.strip())
        Time =  datetime.strptime(strTime.strip(), '%Y-%m-%d')
        c["value"] =  shares["calendar"] / len(dates)
        c["name"] =  Time.strftime(" %d %B") + " " + Time.strftime("%A")[0:3] + "."    
        c["color"] = "#ddea4f"
        c["sliceId"] = sliceId
        c["id_group"] = 1
        dic_sliceId[sliceId] = 1
        dic_name2sliceId[strTime] = sliceId
        dic_sliceId2name[sliceId] = strTime
        sliceId += 1
        calendar.append(c)    

    sliceId += 1 #для пространства  
    #стадион + город
    for p in places:
        p["name"] = p["stadium"].split("|")[0] + ";" + p["city"]
        p["value"] =  shares["places"] / len(places)
        p["color"] = "#4a69a9"
        p["sliceId"] = sliceId
        p["id_group"] = 2
        dic_sliceId[sliceId] = 2
        dic_name2sliceId[p["id"]] = sliceId
        dic_sliceId2name[sliceId] = p["id"]
        sliceId += 1
    sliceId += 1 #для пространства
    #раунды
    for s in stages:
        s["value"] =  shares["stages"] / len(stages)
        s["color"] = "#a89449"
        s["sliceId"] = sliceId
        s["id_group"] = 3
        dic_sliceId[sliceId] = 3
        dic_name2sliceId["s" + str(s["id"])] = sliceId
        dic_sliceId2name[sliceId] = "s" + str(s["id"])
        sliceId += 1
    
    #какие игры показываем при клике
    for i in range(sliceId):
        dic_slice_2_games[i] = []
    
    click_events = []
    for curSlice in range(sliceId):
        click_events.append({"key":curSlice, "value":getConnectionBySliceId(curSlice)}) 
    
    slice_name = []
    for d in dic_slice_2_games:
        slice_name.append ( {"key":d, "value":dic_slice_2_games[d]})
       
    dic_slice_2_games = {}
    return render_template("world_cup2.html", teams = teams, rounds = calendar, places = places, stages = stages, space = space, outGroups = outGroups, 
click_events = click_events, games_clear = games_clear, slice_name = slice_name, games_playoff  = games_playoff, tournaments = tournaments, tournamentPos = tournamentPos)




#get settings

def read_params(fn): 
    d ={} 
    try:
        with open(fn, 'r',encoding="utf-8") as file: 
            d = json.load(file) 
    except FileNotFoundError:
         print ("Error. Can't find file " + fn)
         d = {}
    return d 


@app.route("/worldcup", methods=['GET'])
def update():
    tournamentId = request.args.get('tournamentId')
    init_data(tournamentId)
    return render()
    


@app.route("/", methods=['GET'])
def main():
    if request.method == 'POST':
        index = request.form['index']
        #del places
        competitionId = index
        init_data()
        render()
        resp = make_response(json.dumps({index:"succesfull"} ))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
       init_data()
    return render()
    

if __name__ == "__main__":
    app.run(debug = True)
