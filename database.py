from config import Config
import MySQLdb


class Database:
    def __init__(self):
        self.db=MySQLdb.connect(
            Config.DATABASE_CONFIG['server'],
            Config.DATABASE_CONFIG['user'],
            Config.DATABASE_CONFIG['password'],
            Config.DATABASE_CONFIG['name']
            )
        self.cursor = self.db.cursor()

    def query(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def player_exists(self, playername):
        print(f'SELECT * FROM Players WHERE `name`=`{playername}`')
        self.cursor.execute(f'SELECT * FROM Players WHERE `name`="{playername}"')
        existingplayer = self.cursor.fetchone()
        print(existingplayer)
        if existingplayer is None:
            return(False)
        else:
            return(True)

    def add_player(self, playername):
        self.cursor.execute(f'INSERT INTO `Players` (`name`) VALUES ("{playername}")')
        self.db.commit()
        return(True)

    def delete_player(self, playername):
        self.cursor.execute(f'DELETE FROM Players WHERE `name`="{playername}"')
        self.db.commit()
        return(True)

    def get_wins(self, playername):
        wins = self.query(f'SELECT COUNT(`Match`.player1) FROM `Match` INNER JOIN `Players` ON `Match`.player1=`Players`.id WHERE `Players`.name = "{playername}" AND `Match`.winner = "1"')[0][0]
        wins = wins + self.query(f'SELECT COUNT(`Match`.player2) FROM `Match` INNER JOIN `Players` ON `Match`.player2=`Players`.id WHERE `Players`.name = "{playername}" AND `Match`.winner = "2"')[0][0]
        print(wins)
        #self.cursor.execute(f'SELECT COUNT(`Match`.`winner`) from `Match` INNER JOIN `Players` ON `Match`.`winner`=`Players`.id WHERE `Players`.name = "{playername}"')
        return(wins)

    def new_match(self, player1id, player2id):
        self.cursor.execute(f'INSERT INTO `Match` (`player1`, `winner`, `player2`) VALUES ({player1id}, 0, {player2id})')
        self.db.commit()
        return(True)

    def delete_all_matches(self):
        self.cursor.execute('TRUNCATE `Match`')
        self.db.commit()
        return(True)

    def set_matchwinner(self, matchid, winnerid):
        #print(winnerid)
        #print(matchid)
        #print(self.query(f'SELECT player1 FROM `Match` WHERE player1 = "{winnerid}" AND id = "{matchid}"'))
        if self.query(f'SELECT player1 FROM `Match` WHERE player1 = "{winnerid}" AND id = "{matchid}"') is not ():
            self.cursor.execute(f'UPDATE `Match` SET winner = "1" WHERE id = "{matchid}"')
        if self.query(f'SELECT player2 FROM `Match` WHERE player2 = "{winnerid}" AND id = "{matchid}"') is not ():
            self.cursor.execute(f'UPDATE `Match` SET winner = "2" WHERE id = "{matchid}"')
        self.db.commit()
