from flask import Flask, render_template, make_response
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#import FlaskApp.sql
from flask import request, flash
import json
import requests
import csv
import re
from datetime import date
from datetime import datetime
#https://127.0.0.1:5000/


world_cups = ['germany2006', 'mexico1986','france1938'] 


'''
</div><div data-bt-id="43921" class="bt away bt-43921"><span>USA</span></div><div class="m-row-wrap not-fake"><div class="m-row"><div data-id="300186497" data-status="0" class="mu result"><a href="/worldcup/matches/round=255951/match=300186497/index.html#nosticky" class="mu-m-link"><div class="mu-i"><div class="mu-i-datetime">01 Jul 2014 - 17:00 <span class="wrap-localtime">Local time</span></div><div class="mu-i-date">01 Jul 2014</div><div class="mu-i-matchnum">Match 56</div><div class="mu-i-cupname">FIFA World Cup™ Final</div><div class="mu-i-group">Round of 16</div><div class="mu-i-location"><div class="mu-i-stadium">Arena Fonte Nova</div><div class="mu-i-venue">Salvador </div> </div></div><div class="mu-day"><span class="t-day">01</span><span class="t-month">Jul</span></div><div class="mu-m"><div class="t home" data-team-id="43935"><div class="t-i i-4"><span class="t-i-wrap"><img src="//img.fifa.com/images/flags/4/bel.png" alt="Belgium" title="Belgium" class="BEL i-4-flag flag" /></span></div><div class="t-n"><span class="t-nText ">Belgium</span><span class="t-nTri">BEL</span></div></div><div class="t away" data-team-id="43921"><div class="t-i i-4"><span class="t-i-wrap"><img src="//img.fifa.com/images/flags/4/usa.png" alt="USA" title="USA" class="USA i-4-flag flag" /></span></div><div class="t-n"><span class="t-nText ">USA</span><span class="t-nTri">USA</span></div></div><div class="s"><div class="s-fixture"><div class="s-status">Full-time </div><div class="s-status-abbr">FT </div><div class="s-score s-date-HHmm" data-daymonthutc="0107"><span class="s-scoreText">2-1</span>   </div></div></div><div class="mu-liveblogstatus"><span class="text-liveblogstatus"> </span></div><div class="mu-reasonwin"><span class="text-reasonwin">Belgium win after extra time </span><span class="icon-mrep"> </span><span class="icon-hl"> </span> </div><div class="mu-reasonwin-abbr"><span class="text-reasonwin">Belgium win AET </span><span class="icon-mrep"> </span><span class="icon-hl"> </span> </div></div></a></div>
'''



result = {2:"match_fifa_id", 3:"datetime", 4:"matchnum", 5:"group_name",  6:"stadium", 7: "city", 8: "teams_info", 9:"status", 10:"score_text", 11:"reasonwin"}

key_words = [['</script><div id="div', None],
              [' <div class="match-list"><div class="matches">', None],
              ['<div data-id="', '" data'],                 #match_fifa_id" 
              ['<div class="mu-i-datetime">', '<span class="wrap-localtime">'], #datetime
              ['<div class="mu-i-matchnum">', '</div>'],   #match num
              ['<div class="mu-i-group">', '</div>'],      #group name
              ['<div class="mu-i-stadium">','</div>'],     #stadium
              ['<div class="mu-i-venue">','</div>'],       #city
              ['<div class="mu-m">', '<div class="s-fixture">'],            #teams_info
              ['<div class="s-status">', '</div>'],        #status
              ['<span class="s-scoreText">', '</span>'],   #score
              ['<span class="text-reasonwin">', '</span']  #reason win
            ]


'''
<div class="mu-m"><div class="t home" data-team-id="43935"><div class="t-i i-4"><span class="t-i-wrap"><img src="//img.fifa.com/images/flags/4/bel.png" alt="Belgium" title="Belgium" class="BEL i-4-flag flag" /></span></div><div class="t-n"><span class="t-nText ">Belgium</span><span class="t-nTri">BEL</span></div></div><div class="t away" data-team-id="43921"><div class="t-i i-4"><span class="t-i-wrap"><img src="//img.fifa.com/images/flags/4/usa.png" alt="USA" title="USA" class="USA i-4-flag flag" /></span></div><div class="t-n"><span class="t-nText ">USA</span><span class="t-nTri">USA</span></div>
'''



{'urlHome': 'img.fifa.com/images/flags/4/bra.png', 'teamHome': 'ags/4/bra.png" alt="Brazil" title="Brazil" class="BRA i-4-flag flag" /></s', 'urlAway': '="Brazil" class="BRA i-4-flag flag" /><', 'teamHomeId': '43924', 'teamAway': '-4-flag flag" />', 'teamAwayId': 'azil" title="Brazil" class="BRA i-4-flag flag" /></'}





result2 = {0:"teamHomeId", 1:"urlHome", 2:"teamHome", 3:"shortHomeTeam",  4:"teamAwayId", 5:"urlAway", 6:"teamAway", 7:"shortAwayTeam" }
result_scores = ["goalsHomeTeam", "goalsAwayTeam", "extraTimeHomeGoals", "extraTimeAwayGoals", "penaltyShootoutHomeGoals", "penaltyShootoutAwayGoals"]


key_words_teams = [ ['"t home" data-team-id="', '"><div class='], 
                    ['<img src="//', '" alt='],
                    ['<span class="t-nText ">', '</span>'],
                    ['<span class="t-nTri">', '</span>'],
                    ['"t away" data-team-id="', '"><div class='], 
                    ['<img src="//', '" alt='],
                    ['<span class="t-nText ">', '</span>'],
                    ['<span class="t-nTri">', '</span>']
                  ]
                  



def parse_team_str(resp):
    res = {}
    i = 0 
    for key in key_words_teams:
        pos = resp.find(key[0])    
        resp = resp[pos + len(key[0]):len(resp) - 1]
        index = resp.find(key[1])
        res[result2[i]] = resp[0:index].strip()
        i += 1     
    return res

def parse_time(resp):
    res = {}
    i = 0 
    pos = resp.find("-")
    res["date"] = resp[0:pos].strip()
    res["time"] = resp[pos+1:len(resp)].strip() 
    return res

def parse_score_str(resp):
    res = {}
    i = 0 
    pos = resp.find("-")
    res["goalsHomeTeam"] = resp[0:pos].strip()
    res["goalsAwayTeam"] = resp[pos+1:len(resp)].strip() 
    return res

#Belgium win after extra time
#Argentina win on penalties (2 - 4)
def parse_extra_score(resp, x):
    res = {}
    i = 0 
    key1 = 'extra time'
    key2 = 'on penalties ('
    pos1 = resp.find(key1)
    pos2 = resp.find(key2)

    if pos1 > 0:
        res["extraTimeHomeGoals"] = x["goalsHomeTeam"]
        res["extraTimeAwayGoals"] = x["goalsAwayTeam"]
        return res 
   
    if pos2 > 0:
       resp = resp[pos2+len(key2):len(resp)-1].strip() 
       x = parse_score_str(resp)
       res["penaltyShootoutHomeGoals"] = x["goalsHomeTeam"]
       res["penaltyShootoutAwayGoals"] = x["goalsAwayTeam"]
       return res  
    return res

     


games = open("games_wc_all_additional.csv", 'w', encoding="utf-8") 
#fieldnames = ["stadium", "city","homeTeam", "awayTeam", "date", "time", "shortHomeTeam", "shortAwayTeam", "datetime"]
fieldnames = list(result.values()) + list(result2.values()) + result_scores + ["tournament", "date", "time"]
print(fieldnames)
#fieldnames.remove("teams_info") 
writer = csv.DictWriter(games, fieldnames = fieldnames)
writer.writeheader()

for turn in world_cups:
    url = "https://www.fifa.com/worldcup/archive/" + turn + "/matches/index.html"
    resp = requests.get(url).text
    resp = resp[resp.find(key_words[0][0]) + len(key_words[0][0]):len(resp) - 1]

    while len(resp) > 0:
        a = {}
 
        resp = resp[resp.find(key_words[1][0]) + len(key_words[1][0]):len(resp) - 1]
        for k in range(2, 12): 
            pos = resp.find(key_words[k][0])
            resp = resp[pos + len(key_words[k][0]):len(resp) - 1]
            if pos < 0:
                break;
            index = resp.find(key_words[k][1])
            text = resp[0:index].strip()
            #text = datetime.strptime("2018 " + text, '%Y %d %B') 
            
            if (k == 3):
                x = parse_time(text)
                for i in x:
                    a[i] = x[i]
            elif (k == 8):
                x = parse_team_str(text)
                for i in x:
                    a[i] = x[i]
            elif (k == 10):
                x = parse_score_str(text) 
                for i in x:
                    a[i] = x[i]  
            elif (k == 11):
                x = parse_extra_score(text, a) 
                for i in x:
                    a[i] = x[i]
            a[result[k]] = text

        if a != {}:
            print(a)
            if (len(a["match_fifa_id"]) > 50):
                pos = a["match_fifa_id"].find(' class')  
                a["match_fifa_id"] =  a["match_fifa_id"][1:pos].replace('"','')  
            a["tournament"] = turn 
            a["teams_info"] = ''
            a["date"] = datetime.strptime(a["date"].replace('June', 'Jun'), '%d %b %Y')
            a["datetime"] = str(a["date"])[0:10] + "T" +  a["time"] + "Z"
            writer.writerow(a)

    


