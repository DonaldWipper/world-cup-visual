import json
import requests
import csv

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
    #print()
    YEAR = 2018
    resp = requests.get(main_url + '/v1/competitions/?season=' + str(YEAR),  headers = myheaders)
    wdata = resp.json()


    csvfile = open('../csv/tournaments.csv', 'w', newline='', encoding='utf-8')
        
    while YEAR <= 2018: 
        for data in wdata:
            if data["caption"].lower().find('world') > -1:
                ids_tournaments.append(data["id"])
                headers = data.keys()
                writer = csv.DictWriter(csvfile, headers,  delimiter=',')
                writer.writeheader()
                writer.writerow(data)
        YEAR += 4
        resp = requests.get(main_url + '/v1/competitions/?season=' + str(YEAR),  headers = myheaders)
        wdata = resp.json()
        
 

    a = []
    teams_WC = {}

    for id in ids_tournaments:
                
        table = get_table_by_league_id(id)
        csvfile = open('../csv/standings.csv', 'w', newline='', encoding='utf-8')
        headers = table["standings"]["A"][0].keys()  
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()    
        for l in table["standings"]:
            for pos_t in table["standings"][l]:
                writer.writerow(pos_t)    
                             
        
                
        teams = get_teams_by_league_id(id)
        
        csvfile = open('../csv/teams_wc.csv', 'w', newline='', encoding='utf-8')
        headers = teams["teams"][0].keys()
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()
        for t in teams["teams"]:
            writer.writerow(t)
            
        fixtures = get_fixtures_by_league_id(id)
        csvfile = open('../csv/matches.csv', 'w', newline='', encoding='utf-8')
        headers = fixtures["fixtures"][0].keys()
        print(headers) 
        writer = csv.DictWriter(csvfile, headers,  delimiter=',')
        writer.writeheader()
        for f in fixtures["fixtures"]:
            writer.writerow(f)  

       
main()     
