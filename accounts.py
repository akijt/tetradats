import mysql.connector
import os
import csv

 # TODO: add columns for email (maybe even level and exp)

class Accounts_msa():

    def __init__(self, database, table, header):
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
        ) # enter correct user, password, host, and ssl_ca
        self.cursor = self.mydb.cursor()
        self.user_info_names = header[0:1]
        self.binding_names   = header[4:14]
        self.handling_names  = header[14:17]

    def login(self, username, password):
        self.cursor.execute(f'SELECT * FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
        acct_info = [x for x in self.cursor]
        if acct_info:
            user_info = {k: acct_info[0][i] for i, k in enumerate(self.user_info_names)}
            bindings  = {k: acct_info[0][i + 4] for i, k in enumerate(self.binding_names)}
            handling  = {k: acct_info[0][i + 14] for i, k in enumerate(self.handling_names)}
            return user_info, bindings, handling

    def sign_up(self, username, password, datetime, timezone):
        if self.username_available(username):
            self.cursor.execute(f'INSERT INTO {self.table} VALUES ("{username}", "{password}", "{datetime}", "{timezone}", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
            return self.login(username, password)

    def settings(self, username, changes, password=''):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            if not self.username_available(changes["username"]):
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
            self.cursor.execute(f'INSERT INTO {self.table} VALUES ("guest", "", "2023/01/01 00:00:00", "0000", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
        self.user_info_names = header[0:1]
        self.binding_names   = header[4:14]
        self.handling_names  = header[14:17]

    def login(self, username, password):
        self.cursor.execute(f'SELECT * FROM {self.table} WHERE username = "{username}" AND password = "{password}"')
        acct_info = [x for x in self.cursor]
        if acct_info:
            user_info = {k: acct_info[0][i] for i, k in enumerate(self.user_info_names)}
            bindings  = {k: acct_info[0][i + 4] for i, k in enumerate(self.binding_names)}
            handling  = {k: acct_info[0][i + 14] for i, k in enumerate(self.handling_names)}
            return user_info, bindings, handling

    def sign_up(self, username, password, datetime, timezone):
        if self.username_available(username):
            self.cursor.execute(f'INSERT INTO {self.table} VALUES ("{username}", "{password}", "{datetime}", "{timezone}", 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20);')
            self.mydb.commit()
            return self.login(username, password)

    def settings(self, username, changes, password=''):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            if not self.username_available(changes["username"]):
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

    def username_available(self, username):
        self.cursor.execute(f'SELECT username FROM {self.table} WHERE username = "{username}"')
        acct_info = [x for x in self.cursor]
        return not acct_info

class Accounts_csv():

    def __init__(self, file, header):
        self.file_path = f'{file}.csv'
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
        self.user_info_names = header[0:1]
        self.binding_names   = header[1:11]
        self.handling_names  = header[11:14]

    def login(self, username):
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                if line[0] == username:
                    user_info = {k: line[i] for i, k in enumerate(self.user_info_names)}
                    bindings  = {k: int(line[i + 1]) for i, k in enumerate(self.binding_names)}
                    handling  = {k: int(line[i + 11]) for i, k in enumerate(self.handling_names)}
                    return user_info, bindings, handling

    def sign_up(self, username):
        if self.username_available(username):
            with open(self.file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                row = [username, 27,  114, 99, 1073741904, 1073741903, 120, 1073742049, 122, 1073741905, 32, 300, 50, 20]
                writer.writerow(row)
            return self.login(username)

    def settings(self, username, changes):
        valid = True
        if 'username' in changes.keys(): # check if new username is unique
            if not self.username_available(changes["username"]):
                valid = False
        if valid:
            with open(self.file_path, 'r', newline='') as f:
                reader = csv.reader(f)
                accounts = [next(reader)]
                for line in reader:
                    if line[0] == username:
                        for k, v in changes.items():
                            line[accounts[0].index(k)] = v
                        accounts.append(line)
                        break
                    accounts.append(line)
                for line in reader:
                    accounts.append(line)
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                for line in accounts:
                    writer.writerow(line)
            return True

    def username_available(self, username):
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                if line[0] == username:
                    return False
        return True