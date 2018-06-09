from flask import Flask, render_template
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


teams = [], 
places = [],
rounds = [] 
groups = []

dic_sliceId = {}

settings = {"sql_host":"us-iron-auto-dca-04-a.cleardb.net", 
            "sql_user":"b1df3776b2b56c",
            "sql_passwd":"2153543acdac76f",
            "sql_db":"heroku_0c1d0ea4e380413"
           }

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




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
    print(groups)
    print(teams)
    print(places)
    
    sliceId = 0
    space = {}
    shares = {"teams":350, "calendar":600//3, "places":600//3, "stages":600//3}
    space  = (1000 - (shares["teams"] + shares["calendar"] +  shares["places"] + shares["stages"])) // 4

    #список команд
    for t in teams:
        t["value"] =  shares["teams"] / len(teams)
        t["color"] = "#4daa4b"
        t["sliceId"] = sliceId
        dic_sliceId[sliceId] = 0
        sliceId += 1

    #календарь игр
    for date in rounds:
        date["value"] =  shares["calendar"] / len(rounds)
        date["name"] = datetime.strptime(date["start_at"].strip(), '%Y-%m-%d').strftime("%A %d. %B")     
        date["color"] = "#ddea4f"
        date["sliceId"] = sliceId
        dic_sliceId[sliceId] = 1
        sliceId += 1
     
    #стадион + город
    for p in places:
        p["name"] = p["stadium"].split("|")[0] + " " + p["city"]
        p["value"] =  shares["places"] / len(places)
        p["color"] = "#4a69a9"
        p["sliceId"] = sliceId
        dic_sliceId[sliceId] = 2
        sliceId += 1
 
    #раунды
    for s in stages:
        s["value"] =  shares["stages"] / len(stages)
        s["color"] = "#a89449"
        s["sliceId"] = sliceId
        dic_sliceId[sliceId] = 3
        sliceId += 1

    return render_template("world_cup2.html", teams = teams, groups = groups, rounds = rounds, places = places, stages = stages, space = space)
    

if __name__ == "__main__":
    app.run()
