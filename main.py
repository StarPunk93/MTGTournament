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


def index(requests):
    site = ''
    for route in app.routes_mapper.routelist:
        site = site + f"<a href={route.path}>{route.path}</a><br>"
    return Response(site)



def cards(request):
    cards = ''
    for card in urls:
        cards = cards + f'<img src={card[0]}>'
    return Response(cards)

def players(request):
    site = ''
    if 'Spielername' in request.GET:
        newplayer = request.GET['Spielername']
        addedplayer = mtg.add_player(newplayer)
        print(adddedplayer)
        if addedplayer is True:
            site = site + f"<p class='notice'>{newplayer} wurde hinzugefügt.</p>"
        else:
            site = site + f"<p class='notice'>{newplayer} existiert bereits.</p>"
    player = mtg.get_players()
    site = site + "<form action=players><input type='text' id='playername' name='Spielername'><br><input type='submit' value='Spieler hinzufügen'></form></br> "
    if player is not ():
        site = site + "<div id=player><table><tr><th>Spieler</th><th>Punkte</th></tr>"
        for p in player:
            site = site + f"<tr><td>{p[1]}</td><td>#TODO PUNKTE</td></tr>"
        site = site + "</table></div>"
        return  Response(site)
    else:
        return Response('<p>Keine Spieler registriert.</p>' + site)

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
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
