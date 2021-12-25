class MTG:
    def __init__(self, database):
        self.db = database

    def get_card_urls(self):
        urls = self.db.query('SELECT imageUrl from cards')
        return(urls)

    def get_players(self):
        players = self.db.query('SELECT * FROM Players')
        return(players)

    def add_player(self, playername):
        if self.db.player_exists(playername) is True:
            return(False)
        else:
            self.db.add_player(playername)
            return(True)

    def get_points(self, playername):
        wins = self.db.get_wins(playername)
        points = wins[0][0]
        return(points)
