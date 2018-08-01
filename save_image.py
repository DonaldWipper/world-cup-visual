import json
import requests
import csv
import urllib.request, urllib.error


token = 'efda008899e346f693efa9c75f9577ee'

myheaders = { 'X-Auth-Token': token, 'X-Response-Control': 'minified' }

main_url = 'http://api.football-data.org'
YEAR = 1930
ids_tournaments = []

def get_games_by_league_id(Idleague):
    url = main_url + '/v1/competitions/' + str(Idleague) + '/fixtures'
    resp = requests.get(url, headers = myheaders)
    return resp.json()

def get_standings_by_league_id(Idleague):
    url = main_url +  '/v1/competitions/' + str(Idleague) + '/leagueTable'
    resp = requests.get(url, headers = myheaders)
    return resp.json()

def get_teams_by_league_id(Idleague):
    url = main_url +  '/v1/competitions/' + str(Idleague) + '/teams'
    resp = requests.get(url, headers = myheaders)
    return resp.json()


def get_fixtures_by_league_id(Idleague):
    url = main_url +  '/v1/competitions/' + str(Idleague) + '/fixtures'
    resp = requests.get(url, headers = myheaders)
    return resp.json()

def get_table_by_league_id(Idleague):
    url = main_url +  '/v1/competitions/' + str(Idleague) + '/leagueTable'
    resp = requests.get(url, headers = myheaders)
    return resp.json()

def get_players_by_team_id(Idteam):
    url =  main_url +  '/v1/teams/' + str(Idteam) + '/players'
    resp = requests.get(url, headers = myheaders)
    return resp.json()


def get_id_competion_by_year_and_code(year, code):
    url = main_url + '/v1/competitions/?season=' + str(year)
    resp = requests.get(url, headers = myheaders)
    wdate = resp.json()
    for c in wdate:
        if c['league'] == code:
            return c['id'] 
   

def main():
    #print(get_standings_by_league_id(get_id_competion_by_year_and_code(2017, 'PL')))
    #print(get_players_by_team_id(754))
  
    YEAR = 2018
    resp = requests.get(main_url + '/v1/competitions/?season=' + str(YEAR),  headers = myheaders)
    wdata = resp.json()

   
    csvfile = open('../csv/tournaments.csv', 'w', newline='', encoding='utf-8')
    headers = wdata[0].keys()
    writer = csv.DictWriter(csvfile, headers,  delimiter=',')
    writer.writeheader()    
    while YEAR <= 2018: 
        for data in wdata:
            if data["caption"].lower().find('world') > -1:
                ids_tournaments.append(data["id"])
                writer.writerow(data)
        YEAR += 4
        resp = requests.get(main_url + '/v1/competitions/?season=' + str(YEAR),  headers = myheaders)
        wdata = resp.json()
        
 

    a = []
    teams_WC = {}

    for id in ids_tournaments:
                
        table = get_table_by_league_id(id)
        print(table)
        csvfile = open('../csv/standings.csv', 'w', newline='', encoding='utf-8')
        headers = list(table["standings"]["A"][0].keys())
        headers.append("path")  
        headers.append("gdX") 
        headers.append("gdY") 
        posGroups = {"A":[0, 0], "B":[1, 0], "C":[2, 0],"D":[3, 0], "E":[0, 1], "F":[1, 1], "H":[2, 1],  "G":[3, 1]}
        teamCoords = {}  
 
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()    
        for l in table["standings"]:
            for pos_t in table["standings"][l]:
                flag_img = pos_t["crestURI"]
                reverse = flag_img[::-1]
                name = reverse[0:reverse.find("/")][::-1] 
                path = "flags/" +  pos_t["team"] + ".svg" 
                #urllib.request.urlretrieve(flag_img, path) 
                pos_t["path"] = path     
                pos_t["gdX"] = posGroups[pos_t["group"]][0]
                pos_t["gdY"] = posGroups[pos_t["group"]][1]
                teamCoords [pos_t["teamId"]] = {}
                teamCoords [pos_t["teamId"]]["gdX"] = pos_t["gdX"] 
                teamCoords [pos_t["teamId"]]["gdY"] = pos_t["gdY"]
                teamCoords [pos_t["teamId"]]["rank"] = pos_t["rank"]
                writer.writerow(pos_t)   
 
        
                
        teams = get_teams_by_league_id(id)
        csvfile = open('../csv/teams_wc.csv', 'w', newline='', encoding='utf-8')
        headers = list(teams["teams"][0].keys()) 
        headers.append("path")
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()
        for t in teams["teams"]:
            flag_img = t["crestUrl"]
            reverse = flag_img[::-1]
            name = reverse[0:reverse.find("/")][::-1] 
            path = "flags/" +  t["name"] + ".svg" 
            urllib.request.urlretrieve(flag_img, path) 
            t["path"] = path 
            writer.writerow(t)
            
        fixtures = get_fixtures_by_league_id(id)
        csvfile = open('../csv/matches.csv', 'w', newline='', encoding='utf-8')
        headers = list(fixtures["fixtures"][0].keys())
        headers.append('goalsHomeTeam')
        headers.append('goalsAwayTeam')
        headers.append('AccomGoalsHomeTeam')
        headers.append('AccomGoalsAwayTeam')
        headers.append('AccomTotalGoals')
        headers.append('gdX')
        headers.append('gdY')
        headers.append('rankX')
        headers.append('rankY')
        headers.append('extraTimeHomeGoals')
        headers.append('extraTimeAwayGoals') 
        headers.append('penaltyShootoutHomeGoals') 
        headers.append('penaltyShootoutAwayGoals')

 
        print(headers) 
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()
        teams = {}
        total_goals = 0
        for f in fixtures["fixtures"]:
            x = dict(f["result"])
            f['goalsHomeTeam'] = x['goalsHomeTeam']
            f['goalsAwayTeam'] = x['goalsAwayTeam']
            f['extraTimeHomeGoals'] = x.get("extraTime", {}).get("goalsHomeTeam", "NULL")
            f['extraTimeAwayGoals'] = x.get("extraTime", {}).get("goalsAwayTeam", "NULL")
            f['penaltyShootoutHomeGoals'] =  x.get("penaltyShootout", {}).get("goalsHomeTeam", "NULL")
            f['penaltyShootoutAwayGoals'] =  x.get("penaltyShootout", {}).get("goalsAwayTeam", "NULL")

            if x['goalsAwayTeam'] != None:
                if f['awayTeamId'] in teams:
                    teams[f['awayTeamId']] += int (x['goalsAwayTeam'])
                else:
                    teams[f['awayTeamId']] =  int(x['goalsAwayTeam'])
         
                if f['homeTeamId'] in teams:
                    teams[f['homeTeamId']] +=  int(x['goalsHomeTeam'])
                else:
                    teams[f['homeTeamId']] =  int(x['goalsHomeTeam'])

            f['AccomGoalsHomeTeam'] = teams[f['homeTeamId']] 
            f['AccomGoalsAwayTeam'] =  teams[f['awayTeamId']] 
            f['gdX'] = teamCoords [f['homeTeamId']]["gdX"] 
            f['gdY'] = teamCoords [f['homeTeamId']]["gdY"] 
            f['rankX'] = teamCoords [f['homeTeamId']]["rank"]
            f['rankY'] = teamCoords [f['awayTeamId']]["rank"]



            total_goals += teams[f['homeTeamId']] + teams[f['awayTeamId']]
            f['AccomTotalGoals'] =  total_goals
            writer.writerow(f)
              
main()     
