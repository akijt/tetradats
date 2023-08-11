import mysql.connector

# TODO: save into online database

class Accounts_sql(): # TODO: add columns for email, and datetime and timezone for when created (maybe even level and exp)

    def __init__(self, header, datatype):
        self.mydb = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = 'pass'
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SHOW DATABASES;')
        if ('tetris',) not in self.cursor:
            self.cursor.execute('CREATE DATABASE tetris;')
        self.mydb = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = 'pass',
            database = 'tetris'
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SHOW TABLES;')
        if ('accounts',) not in [x for x in self.cursor]:
            query = 'CREATE TABLE accounts('
            for i in range(len(header)):
                column = header[i].replace(" ", "_").replace("-", "_")
                query += f'{column} {datatype[i]}, '
            query = query[:-2] + ');'
            self.cursor.execute(query)
        self.user_info_names = ['username']
        self.binding_names   = ['quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop']
        self.handling_names  = ['DAS', 'ARR', 'SDF']

    def login(self, username, password):
        self.cursor.execute(f'SELECT * FROM accounts WHERE username = "{username}" AND password = "{password}"')
        acct_info = [x for x in self.cursor]
        if acct_info:
            user_info = {k: acct_info[0][i] for i, k in enumerate(self.user_info_names)}
            bindings  = {k: acct_info[0][i + 2] for i, k in enumerate(self.binding_names)}
            handling  = {k: acct_info[0][i + 12] for i, k in enumerate(self.handling_names)}
            return user_info, bindings, handling

    def sign_up(self, username, password):
        self.cursor.execute(f'SELECT username FROM accounts WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        if not acct_info:
            self.cursor.execute(f'INSERT INTO accounts VALUES ("{username}", "{password}", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
            return self.login(username, password)

    def settings(self, username, password, changes):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            self.cursor.execute(f'SELECT username FROM accounts WHERE username = "{changes["username"]}"')
            acct_info = [x for x in self.cursor]
            if acct_info:
                valid = False
        if 'password' in changes.keys(): # password required for changing password
            self.cursor.execute(f'SELECT username FROM accounts WHERE username = "{username}" AND password = "{password}"')
            acct_info = [x for x in self.cursor]
            if not acct_info:
                valid = False
        if valid:
            changes_string = ", ".join([f'{k} = "{v}"' if k in ['username', 'password'] else f'{k} = {v}' for k, v in changes.items()])
            self.cursor.execute(f'UPDATE accounts SET {changes_string} WHERE username = "{username}"')
            self.mydb.commit()
            return True
        else:
            return False
        
    def username_available(self, username):
        self.cursor.execute(f'SELECT username FROM accounts WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        return not acct_info