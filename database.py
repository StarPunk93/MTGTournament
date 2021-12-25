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

    def get_wins(self, playername):
        self.cursor.execute(f'SELECT COUNT(`Match`.`winner`) from `Match` INNER JOIN `Players` ON `Match`.`winner`=`Players`.id WHERE `Players`.name = "{playername}"')
        return self.cursor.fetchall()
