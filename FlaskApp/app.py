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

stages = []
teams = [] 
places = []
rounds = [] 
groups = []
space = None

dic_sliceId = {}
dic_name2sliceId = {}

settings = {"sql_host":"us-iron-auto-dca-04-a.cleardb.net", 
            "sql_user":"b1df3776b2b56c",
            "sql_passwd":"2153543acdac76f",
            "sql_db":"heroku_0c1d0ea4e380413"
           }

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'



'''
//календарь, стадионы, стадии
def getAllCorellByTeamId(teamId):
    standings = db.getDictFromQueryRes("places", {"competitionId": competitionId})
'''





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

@app.route('/', methods=['POST'])
def index():
     data = request.form['index']
     resp = make_response(json.dumps(data))
     resp.status_code = 200
     print(" GET REQUEST " + str(data))
     resp.headers['Access-Control-Allow-Origin'] = '*'
     places[0]["color"] = "#070707"
     return render_template("world_cup2.html", teams = teams, groups = groups, rounds = rounds, places = places, stages = stages, space = space)
    


@app.route("/", methods=['GET'])
def main():
    global stages, teams, places, rounds, groups, space 
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

    #matches = getDataFromCSV(path + 'matches.csv')
    #tournaments = getDataFromCSV(path + 'tournaments.csv')
    #standings = getDataFromCSV(path + 'standings.csv')
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
        dic_name2sliceId[t["name"]] = sliceId
        sliceId += 1

    #календарь игр
    for date in rounds:
        strTime =  datetime.strptime(date["start_at"].strip(), '%Y-%m-%d')
        date["value"] =  shares["calendar"] / len(rounds)
        date["name"] =  strTime.strftime("%A")[0:3] + "." + strTime.strftime(" %d. %B")     
        date["color"] = "#ddea4f"
        date["sliceId"] = sliceId
        date["id_group"] = 1
        dic_sliceId[sliceId] = 1
        dic_name2sliceId[date["start_at"]] = sliceId
        sliceId += 1
     
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
 
    #раунды
    for s in stages:
        s["value"] =  shares["stages"] / len(stages)
        s["color"] = "#a89449"
        s["sliceId"] = sliceId
        s["id_group"] = 3
        dic_sliceId[sliceId] = 3
        dic_name2sliceId[s["title"]] = sliceId
        sliceId += 1

    return render_template("world_cup2.html", teams = teams, groups = groups, rounds = rounds, places = places, stages = stages, space = space)
    

if __name__ == "__main__":
    app.run()
