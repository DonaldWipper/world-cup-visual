from flask import Flask, render_template
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sql
from flask import request, flash
import json
import requests
import csv
#https://127.0.0.1:5000/


#mysql = MySQL()
cursor = None

info = []
profiles = []
cur_profile_index = 0

global_path = ""
local_path = "../csv"
path = global_path



app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'



def initSQL():
    global mysql, cursor
    settings  = read_params("/home/dmitry/settings2.json")
    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = settings['sql_user']
    app.config['MYSQL_DATABASE_PASSWORD'] = settings['sql_passwd']
    app.config['MYSQL_DATABASE_DB'] = settings['sql_db']
    app.config['MYSQL_DATABASE_HOST'] = settings['sql_host']
    mysql.init_app(app)
 
    conn = mysql.connect()
    cursor = conn.cursor() 
    query = 'SHOW TABLES;'
    cursor.execute(query)
    for row in cursor.fetchall() :
        for field in row:
            print (field, end= " | ")
        print("\n")   

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
    settings  = read_params("settings2.json")
    print(settings)
    db = sql.database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])
    teams = db.getDictFromQueryRes("teams_wc")
    #matches = getDataFromCSV(path + 'matches.csv')
    #tournaments = getDataFromCSV(path + 'tournaments.csv')
    #standings = getDataFromCSV(path + 'standings.csv')
    standings = []
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
    app.run()
