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
            '<div class="fi-t__n">'
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

result = {2: "stadium", 3: "city", 4: "homeTeam",  5:"awayTeam", 6:"shortHomeTeam", 7: "homeTeam",  8: "shortawayTeam"}


filmes = open("games_wc.csv", 'w', encoding="utf-8") 
fieldnames = ["stadium", "city","homeTeam", "awayTeam", "shortHomeTeam", "shortAwayTeam"]
writer = csv.DictWriter(filmes, fieldnames = fieldnames)
writer.writeheader()
    

while len(resp) > 0:
    a = {}
  


    resp = resp[resp.find(key_words[1]) + len(key_words[1]):len(resp) - 1]
    for k in range(2, 6): 
        pos = resp.find(key_words[k])
        resp = resp[pos + len(key_words[k]):len(resp) - 1]
        if pos < 0:
            break;
        index = resp.find('</div>')
        '''
        if k in [4, 6]:
            index = resp.find('<div')
        else:
            index = resp.find('</div>')
        '''
        text = resp[0:index].strip()
        #if len(text) > 100:
         #   break;
        if k in [4, 5]:
            if(k == 4):
                x = parse_team_str(text)
                a["homeTeam"] = x[0]
                a["shortHomeTeam"] = x[1]
            if(k == 5):
                x = parse_team_str(text)
                a["awayTeam"] = x[0]
                a["shortAwayTeam"] = x[1]

        else:
            a[result[k]] = text 
    if a != {}:
        print(a) 
        writer.writerow(a)

    


