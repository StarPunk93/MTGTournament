#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from database import Database
from mtg import MTG
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

hostName = "localhost"
serverPort = 8080

primarycolor = '#DBDBDB'
secondarycolor = '#7A7A7A'
thirdcolor = '#A8A8A8'

def header(site):
    site = site + '<div style="display: flex; height: 50px" id="contenttable">'
    for route in app.routes_mapper.routelist:
        link = route.path
        link_name = link.strip('/').upper()
        if link_name == '':
            link_name = 'INDEX'
        site = site + f"<a href={link}><div style='padding: 3px; width: 200px; border-style: solid; border-color: { secondarycolor }; text-align: center; margin: 0 auto; background: { primarycolor }'>{link_name}</div></a>"
    site = site + '</div>'
    return(site)

def index(requests):
    site = header('')
    return Response(site)



def cards(request):
    cards = header('')
    for card in urls:
        cards = cards + f'<img src={card[0]}>'
    return Response(cards)

def players(request):
    site = header('')
    if 'delete' in request.GET:
        deleteplayer = request.GET['delete']
        mtg.delete_player(deleteplayer)
        site = site + ' ' + deleteplayer + ' wurde gelöscht.<br>'

    if 'Spielername' in request.GET:
        newplayer = request.GET['Spielername']
        addedplayer = mtg.add_player(newplayer)
        print(addedplayer)
        if addedplayer is True:
            site = site + f"<p class='notice'>{newplayer} wurde hinzugefügt.</p>"
        else:
            site = site + f"<p class='notice'>{newplayer} existiert bereits.</p>"

    player = mtg.get_players()
    site = site + f"<div id=playeradd style='display: flex'><form style='padding: 15px; background: {primarycolor}' id='playerform' action=players><input type='text' id='playername' name='Spielername' placeholder='Spielername'><br><br><input type='submit' value='Spieler hinzufügen'></form></div></br> "
    if player is not ():
        site = site + f'<div id=player><form action=players id="playerdelete"><table><tbody><tr style="background: {primarycolor}"><th style="padding-right: 10px">Spieler</th><th style="padding-right: 10px">Punkte</th><th/></tr>'
        color = secondarycolor
        for p in player:
            player_points = mtg.get_points(p[1])
            site = site + f"<tr style='background: {color}'><td style='padding-right: 20px'>{p[1]}</td><td style='padding-right: 20px'>{player_points}</td><td style='padding-right: 10px'><input type='radio' name='delete' value='{p[1]}'><label for={p[1]}'>Löschen</label></td></tr>"
            if color == secondarycolor:
                color = thirdcolor
            else:
                color = secondarycolor
        site = site + "<tr><td></td><td></td><td><input type='submit'></td></tr></tbody></table></div>"
        return  Response(site)
    else:
        return Response( site + '<p>Keine Spieler registriert.</p>' )

def matches(request):
    if 'CreateMatches' in request.GET:
        mtg.create_all_matches()

    if 'DeleteMatches' in request.GET:
        mtg.delete_all_matches()

    if 'winner' in request.GET:
        if 'player' in request.GET:
            winner = request.GET['player']
            matchid = request.GET['matchid']
            #print(winner)
            #print(matchid)
            mtg.set_matchwinner(matchid, winner)
    site = header('')
    matches = mtg.get_matches()
    matchnummer = 0
    rows = len(matches) / 3
    if not rows.is_integer():
        rows = rows + 1
    rows = int(rows)
    site = site + f'<div style="padding-left: 15px; padding-right: 15px;"><div style="background: {secondarycolor}; display: grid; grid-template-columns: auto auto auto; grid-row-gap: 25px; grid-column-gap: 25px; padding: 10px; grid-template-rows: ' +  "210px " * rows + '">'
    for match in matches:
        #print(match)
        matchnummer = matchnummer + 1
        site = site + f'<div class="match" style="background: { primarycolor }; padding-left: 3%"><h3>Match {matchnummer}</h3>'
        site = site + f'<table style="padding: 10px"><tr><th style="width: 150px">Spieler 1</th><th style="width: 150px">Spieler 2</th></tr><tr><td>{match[0]}</td><td>{match[1]}</td></tr>'
        if match[2] is not 0:
            site = site + f'<tr><td>Winner:</td><td><b>{match[match[2] - 1]}</b></td></tr>'
        else:
            site = site + f'<tr><td>Winner:</td><td>-</td></tr>'

            site = site + f'<tr></tr><form action=matches><tr><td><input type="hidden" name="matchid" value={match[3]}><input name="player" list="{match[3]}"><datalist id="{match[3]}"><option value={match[0]}><option value={match[1]}></datalist></td><td><input type="submit" name="winner" value="Match abschließen"></td></tr>'
            #site = site + f'<tr><td><input type="submit" name="winner" value="Match abschließen"></td><td></td></tr></form>'
        site = site + '</table></div>'
    site = site + '</div></div>'
    site = site + '<div style="display: flex"><form action=matches><input type="submit" name="CreateMatches" value="Matches erstellen"></form>'
    site = site + '<form action=matches><input type="submit" name="DeleteMatches" value="Matches löschen"></form></div>'
    return Response(site)

if __name__ == "__main__":
    db = Database()
    mtg = MTG(db)

    urls = mtg.get_card_urls()
    type(urls)

    with Configurator() as config:
        config.add_route('index', '/')
        config.add_view(index, route_name='index')
        config.add_route('cards', '/cards')
        config.add_view(cards, route_name='cards')
        config.add_route('players', '/players')
        config.add_view(players, route_name='players')
        config.add_route('matches', '/matches')
        config.add_view(matches, route_name='matches')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
