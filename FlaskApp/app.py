from flask import Flask, render_template
#from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#import sql
from flask import request, flash
import json
import csv
#https://127.0.0.1:5000/
#mysql = MySQL()
cursor = None

info = []
profiles = []
cur_profile_index = 0






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




def getDataFromCSV(name):
    result = []
    with open(name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:    
            result.append(row)
    return result

@app.route("/", methods=['GET', 'POST'])
def main():
    #initSQL()
    teams = getDataFromCSV('../csv/teams_wc.csv')
    matches = getDataFromCSV('../csv/matches.csv')
    tournaments = getDataFromCSV('../csv/tournaments.csv')
    standings = getDataFromCSV('../csv/standings.csv')

    groups = []
    for name in list(set([g["group"] for g in standings])):
        g = {}
        g["name"] = name
        g["value"] =  40
        g["color"] = "#8d4aa9"
        groups.append(g)

    for t in teams:
        t["value"] =  10
        t["color"] = "#4daa4b"

    return render_template("world_cup2.html", teams = teams, groups = groups)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port = 5000)
