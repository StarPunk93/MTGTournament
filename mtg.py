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

    def delete_player(self, playername):
        if self.db.player_exists(playername) is True:
            self.db.query(f'DELETE FROM Players WHERE `name`="{playername}"')

    def get_points(self, playername):
        wins = self.db.get_wins(playername)
        points = wins
        return(points)

    def get_matches(self):
        ### Output format: tuple(player1, player2, winner)
        matches = self.db.query('SELECT `Players`.name, `match`.player2, `match`.winner, `match`.id FROM `Match` INNER JOIN `Players` ON `Match`.player1=`Players`.id')
        matches_with_names = []
        for match in matches:
            player2name = self.db.query(f'SELECT `Players`.name FROM `Players` WHERE `id`="{match[1]}"')
            matches_with_names.append([match[0], player2name[0][0], match[2], match[3] ])
        #print(matches_with_names)
        return(matches_with_names)

    def create_all_matches(self):
        playercounter = 0
        players = self.get_players()
        for player1 in players:
            playercounter = playercounter + 1
            for player2 in self.get_players():
                if player2 != player1:
                    if player2 not in players[0:playercounter]:
                        #print(str(player1) + ' ' + str(player2))
                        self.db.new_match(player1[0], player2[0])
        return(True)

    def delete_all_matches(self):
        self.db.delete_all_matches()
        return(True)

    def set_matchwinner(self, matchid, winner):
        winnerid = self.db.query(f'SELECT `Players`.id FROM `Players` WHERE name = "{winner}"')[0][0]
        self.db.set_matchwinner(matchid, winnerid)
