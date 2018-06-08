from flask import Flask, render_template
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import FlaskApp.sql
from flask import request, flash
import json
import requests
import csv
#https://127.0.0.1:5000/


#mysql = MySQL()
cursor = None
competitionId = 467


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
    
    #matches = getDataFromCSV(path + 'matches.csv')
    #tournaments = getDataFromCSV(path + 'tournaments.csv')
    #standings = getDataFromCSV(path + 'standings.csv')
  
    for g in groups:
        g["value"] =  10
        g["color"] = "#d82424"

    for t in teams:
        t["value"] =  15
        t["color"] = "#4daa4b"
        
    for p in places:
        p["value"] =  15
        p["color"] = "#4a69a9"


    return render_template("world_cup2.html", teams = teams, groups = groups, places = places)
    

if __name__ == "__main__":
    app.run()
