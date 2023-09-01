import mysql.connector

 # TODO: add columns for email (maybe even level and exp)

class Accounts_msa():

    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.mydb = mysql.connector.connect(
            user         = '',
            password     = '',
            host         = 'tetradats-db1.mysql.database.azure.com',
            port         = 3306,
            database     = self.database,
            ssl_ca       = 'DigiCertGlobalRootCA.crt.pem',
            ssl_disabled = False
        )
        self.cursor = self.mydb.cursor()
        self.user_info_names = ['username']
        self.binding_names   = ['quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop']
        self.handling_names  = ['DAS', 'ARR', 'SDF']
    
    def login(self, username, password):
        self.cursor.execute(f'SELECT * FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
        acct_info = [x for x in self.cursor]
        if acct_info:
            user_info = {k: acct_info[0][i] for i, k in enumerate(self.user_info_names)}
            bindings  = {k: acct_info[0][i + 2] for i, k in enumerate(self.binding_names)}
            handling  = {k: acct_info[0][i + 12] for i, k in enumerate(self.handling_names)}
            return user_info, bindings, handling

    def sign_up(self, username, password, datetime, timezone):
        self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        if not acct_info:
            self.cursor.execute(f'INSERT INTO {self.table} VALUES ("{username}", "{password}", "{datetime}", "{timezone}", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
            return self.login(username, password)

    def settings(self, username, password, changes):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{changes["username"]}"')
            acct_info = [x for x in self.cursor]
            if acct_info:
                valid = False
        if 'password' in changes.keys(): # password required for changing password
            self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
            acct_info = [x for x in self.cursor]
            if not acct_info:
                valid = False
        if valid:
            changes_string = ", ".join([f'{k} = "{v}"' if k in ['username', 'password'] else f'{k} = {v}' for k, v in changes.items()])
            self.cursor.execute(f'UPDATE {self.table} SET {changes_string} WHERE username = "{username}"')
            self.mydb.commit()
            return True
        else:
            return False
        
    def username_available(self, username):
        self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        return not acct_info

class Accounts_sql():

    def __init__(self, database, table, header, datatype):
        self.database = database
        self.table = table
        self.mydb = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = 'pass'
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SHOW DATABASES;')
        if (self.database,) not in self.cursor:
            self.cursor.execute('CREATE DATABASE tetris;')
        self.mydb = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = 'pass',
            database = self.database
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SHOW TABLES;')
        if (self.table,) not in [x for x in self.cursor]:
            query = f'CREATE TABLE {self.table}('
            for i in range(len(header)):
                column = header[i].replace(" ", "_").replace("-", "_")
                query += f'{column} {datatype[i]}, '
            query = query[:-2] + ');'
            self.cursor.execute(query)
        self.user_info_names = ['username']
        self.binding_names   = ['quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop']
        self.handling_names  = ['DAS', 'ARR', 'SDF']

    def login(self, username, password):
        self.cursor.execute(f'SELECT * FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
        acct_info = [x for x in self.cursor]
        if acct_info:
            user_info = {k: acct_info[0][i] for i, k in enumerate(self.user_info_names)}
            bindings  = {k: acct_info[0][i + 2] for i, k in enumerate(self.binding_names)}
            handling  = {k: acct_info[0][i + 12] for i, k in enumerate(self.handling_names)}
            return user_info, bindings, handling

    def sign_up(self, username, password, datetime, timezone):
        self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        if not acct_info:
            self.cursor.execute(f'INSERT INTO {self.table} VALUES ("{username}", "{password}", "{datetime}", "{timezone}", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
            return self.login(username, password)

    def settings(self, username, password, changes):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{changes["username"]}"')
            acct_info = [x for x in self.cursor]
            if acct_info:
                valid = False
        if 'password' in changes.keys(): # password required for changing password
            self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
            acct_info = [x for x in self.cursor]
            if not acct_info:
                valid = False
        if valid:
            changes_string = ", ".join([f'{k} = "{v}"' if k in ['username', 'password'] else f'{k} = {v}' for k, v in changes.items()])
            self.cursor.execute(f'UPDATE {self.table} SET {changes_string} WHERE username = "{username}"')
            self.mydb.commit()
            return True
        else:
            return False
        
    def username_available(self, username):
        self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        return not acct_info