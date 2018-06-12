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

stages = []
teams = [] 
places = []
rounds = [] 
groups = []
space = None


outGroups = [{ "name":"NATIONAL TEAMS", "color":"#ABDDA4"}, { "name":"WORLD CUP SCHEDULE", "color":"#2c7bb6"},
             { "name":"CITIES AND STADIUMS", "color":"#d7191c"}, { "name":"GROUPS ANS STAGES", "color":"#d7c119"}]


dic_sliceId = {}
dic_name2sliceId = {}
dic_sliceId2name = {}


settings = {"sql_host":"us-iron-auto-dca-04-a.cleardb.net", 
            "sql_user":"b1df3776b2b56c",
            "sql_passwd":"2153543acdac76f",
            "sql_db":"heroku_0c1d0ea4e380413"
           }

app = Flask(__name__)
app.config.from_object(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True



def getConnectionBySliceId(sliceId):
    groupId = dic_sliceId[sliceId]
    if groupId == 0:
        return getAllCorellByTeamId(dic_sliceId2name[sliceId])     



#календарь, стадионы, стадии
def getAllCorellByTeamId(teamId):
    dates_home = [datetime.strptime(d["date"].strip()[0:10], '%Y-%m-%d') for d in db.getDictFromQueryRes("games", {"homeTeamId": teamId, "competitionId": competitionId}, ["date"])]
    dates_away = [datetime.strptime(d["date"].strip()[0:10], '%Y-%m-%d') for d in db.getDictFromQueryRes("games", {"awayTeamId": teamId, "competitionId": competitionId}, ["date"])]   
    groups = [d["group_"] for d in db.getDictFromQueryRes("standings", {"teamId": teamId, "competitionId": competitionId}, ["group_"])]

    names = dates_home + dates_away + groups
    print(names)  
    sliceIds = []
    for name in names:
        if name in dic_name2sliceId:
            sliceIds.append(dic_name2sliceId[name])
    return sliceIds



def init_data():
    global stages, teams, places, rounds, groups, space, db 
    #initSQL()
    #settings  = read_params("settings2.json")
    #print(settings)
    db = FlaskApp.sql.database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])
    standings = db.getDictFromQueryRes("standings", {"competitionId": competitionId})
    teams = [team for team in db.getDictFromQueryRes("teams_wc") if team["id"] in   [t["teamId"] for t in  standings] ]
    places = db.getDictFromQueryRes("places", {"competitionId": competitionId})  
    rounds = db.getDictFromQueryRes("rounds", {"competitionId": competitionId})
    groups = db.getDictFromQueryRes("groups", {"competitionId": competitionId})
    stages = db.getDictFromQueryRes("stages", {"competitionId": competitionId})    



def render():
    global stages, teams, places, rounds, groups, space 
    sliceId = 0
    shares = {"teams":350, "calendar":600//3, "places":600//3, "stages":600//3}
    space  = (1000 - (shares["teams"] + shares["calendar"] +  shares["places"] + shares["stages"])) // 4

    #список команд
    for t in teams:
        t["value"] =  shares["teams"] / len(teams)
        t["color"] = "#4daa4b"
        t["sliceId"] = sliceId
        t["id_group"] = 0
        dic_sliceId[sliceId] = 0
        dic_name2sliceId[t["id"]] = sliceId
        dic_sliceId2name[sliceId] = t["id"]
        sliceId += 1

    sliceId += 1 #для пространства
    #календарь игр
    for date in rounds:
        strTime =  datetime.strptime(date["start_at"].strip(), '%Y-%m-%d')
        date["value"] =  shares["calendar"] / len(rounds)
        date["name"] =  strTime.strftime("%A")[0:3] + "." + strTime.strftime(" %d. %B")     
        date["color"] = "#ddea4f"
        date["sliceId"] = sliceId
        date["id_group"] = 1
        dic_sliceId[sliceId] = 1
        dic_name2sliceId[strTime] = sliceId
        sliceId += 1
    
    sliceId += 1 #для пространства  
    #стадион + город
    for p in places:
        p["name"] = p["stadium"].split("|")[0] + " " + p["city"]
        p["value"] =  shares["places"] / len(places)
        p["color"] = "#4a69a9"
        p["sliceId"] = sliceId
        p["id_group"] = 2
        dic_sliceId[sliceId] = 2
        dic_name2sliceId[p["stadium"]] = sliceId
        sliceId += 1
    sliceId += 1 #для пространства
    #раунды
    for s in stages:
        s["value"] =  shares["stages"] / len(stages)
        s["color"] = "#a89449"
        s["sliceId"] = sliceId
        s["id_group"] = 3
        dic_sliceId[sliceId] = 3
        dic_name2sliceId[s["title"]] = sliceId
        dic_sliceId2name[sliceId] = s["title"]
        sliceId += 1
    
    
    

    return render_template("world_cup2.html", teams = teams, groups = groups, rounds = rounds, places = places, stages = stages, space = space, outGroups = outGroups)




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


    


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        index = request.form['index']
        #del places
        resp = make_response(json.dumps({index:getConnectionBySliceId(int(index))} ))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
       init_data()
    return render()
    

if __name__ == "__main__":
    app.run(debug = True)
