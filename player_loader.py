from flask import Flask, render_template, make_response
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#import FlaskApp.sql
from flask import request, flash
import json
import requests
import csv
from datetime import date
from datetime import datetime
#https://127.0.0.1:5000/



key_words = ['<div class="fi-matchlist">',
            '<a href="/worldcup/matches/match/',
            '<div class="fi__info__stadium">',
            '<div class="fi__info__venue">',
            '<div class="fi-t__n">',
            '<span class="fi-s__matchDate">',
            'data-timeutc="',
            '<div class="fi-t__n">',
            ]



def parse_team_str(resp):
    key_word = '<span class="fi-t__nText ">'
    pos = resp.find(key_word)    
    resp = resp[pos + len(key_word):len(resp) - 1]
    index = resp.find('</span>')
    team = resp[0:index].strip()
    key_word = '<span class="fi-t__nTri">'
    pos = resp.find(key_word)    
    resp = resp[pos + len(key_word):len(resp) - 1]
    index = resp.find('</span>')
    shortName = resp[0:index-4].strip()
    return [team, shortName]

url = "https://www.fifa.com/worldcup/matches/#groupphase/"
resp = requests.get(url).text
resp = resp[resp.find(key_words[0]) + len(key_words[0]):len(resp) - 1]

result = {2: "stadium", 3: "city", 5:"date", 6:"time"}


filmes = open("games_wc.csv", 'w', encoding="utf-8") 
fieldnames = ["stadium", "city","homeTeam", "awayTeam", "date", "time", "shortHomeTeam", "shortAwayTeam", "datetime"]
writer = csv.DictWriter(filmes, fieldnames = fieldnames)
writer.writeheader()
    

while len(resp) > 0:
    a = {}
  


    resp = resp[resp.find(key_words[1]) + len(key_words[1]):len(resp) - 1]
    for k in range(2, 8): 
        pos = resp.find(key_words[k])
        resp = resp[pos + len(key_words[k]):len(resp) - 1]
        if pos < 0:
            break;
        #index = resp.find('</div>')
        
        if k in [5]:
            index = resp.find('</span>')
        elif k in [6]:
            index = resp.find('" data') 
        else:
            index = resp.find('</div>')
        
        text = resp[0:index].strip()
        if (k == 5):
            text = datetime.strptime("2018 " + text, '%Y %d %B') 
            print(text)
        
        #if len(text) > 100:
         #   break;
        if k in [4, 7]:
            if(k == 4):
                x = parse_team_str(text)
                a["homeTeam"] = x[0]
                a["shortHomeTeam"] = x[1]
            if(k == 7):
                x = parse_team_str(text)
                a["awayTeam"] = x[0]
                a["shortAwayTeam"] = x[1]

        else:
            a[result[k]] = text 
    if a != {}:
        print(a) 
        a["datetime"] = str(a["date"])[0:10] + "T" +  a["time"] + "Z"
        writer.writerow(a)

    


