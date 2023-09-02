import mysql.connector
import os
import csv

class Records_msa():

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

    def save(self, row, order_by):
        query = f'INSERT INTO {self.table} VALUES({("%s, " * len(row))[:-2]});'
        self.cursor.execute(query, row)
        self.mydb.commit()
        query = f'SELECT datetime, RANK() OVER(ORDER BY {order_by}) AS "rank" FROM {self.table} WHERE username = "{row[0]}" and mode = "{row[3]}"'
        query = f'SELECT q.rank FROM ({query}) AS q WHERE datetime = "{row[1]}"'
        self.cursor.execute(query)
        position_local = [x for x in self.cursor][0][0]
        query = f'SELECT username, datetime, RANK() OVER(ORDER BY {order_by}) AS "rank" FROM {self.table} WHERE mode = "{row[3]}"'
        query = f'SELECT q.rank FROM ({query}) as q WHERE username = "{row[0]}" and datetime = "{row[1]}"'
        self.cursor.execute(query)
        position_global = [x for x in self.cursor][0][0]
        return (position_local, position_global)

    def load(self, username, mode, order_by, n):
        self.cursor.execute(f'SHOW COLUMNS FROM {self.table};')
        top_n = [tuple([''] + [x[0] for x in self.cursor])]
        if username:
            query = f'SELECT RANK() OVER(ORDER BY {order_by}) AS "rank", {self.table}.* FROM {self.table} WHERE username = "{username}" and mode = "{mode}" ORDER BY {order_by} LIMIT {n}'
        else:
            query = f'SELECT RANK() OVER(ORDER BY {order_by}) AS "rank", {self.table}.* FROM {self.table} WHERE mode = "{mode}" ORDER BY {order_by} LIMIT {n}'
        self.cursor.execute(query)
        top_n += [x for x in self.cursor]
        return top_n

class Records_sql():

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
        if (f'{self.database}',) not in self.cursor:
            self.cursor.execute(f'CREATE DATABASE {self.database};')
        self.mydb = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = 'pass',
            database = f'{self.database}'
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SHOW TABLES;')
        if (f'{self.table}',) not in [x for x in self.cursor]:
            query = f'CREATE TABLE {self.table}('
            for i in range(len(header)):
                column = header[i].replace(" ", "_").replace("-", "_")
                if column in ['lines', 'keys', 'double']:
                    column += '_'
                query += f'{column} {datatype[i]}, '
            query = query[:-2] + ');'
            self.cursor.execute(query)

    def edit(self):
        '''
        used to make changes to the database
        '''
        pass

        # # convert datetime from float to datetime datatype
        # import time
        # self.cursor.execute(f'ALTER TABLE {self.table} DROP COLUMN datetime2;')
        # self.cursor.execute(f'ALTER table {self.table} add column datetime2 DATETIME AFTER datetime')
        # self.cursor.execute(f'SELECT * FROM {self.table};')
        # q = [x for x in self.cursor]
        # switches = dict()
        # for r in q:
        #     switches[r[1]] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(r[1]))
        # for k, v in switches.items():
        #     self.cursor.execute(f'UPDATE {self.table} SET datetime2 = "{v}" WHERE datetime = {k}')
        # self.cursor.execute(f'ALTER TABLE {self.table} DROP COLUMN datetime;')
        # self.cursor.execute(f'ALTER TABLE {self.table} RENAME COLUMN datetime2 to datetime;')
        # self.mydb.commit()

        # # convert datetime from local time to gm time
        # import time
        # self.cursor.execute(f'SELECT * FROM {self.table};')
        # q = [x for x in self.cursor]
        # switches = dict()
        # for r in q:
        #     gm_timestamp = time.gmtime(time.mktime(r[1].timetuple()))
        #     local_timestamp = time.localtime(time.mktime(r[1].timetuple()))
        #     local_timestamp = time.strftime('%Y/%m/%d %H:%M:%S', local_timestamp)
        #     switches[local_timestamp] = time.strftime('%Y/%m/%d %H:%M:%S', gm_timestamp)
        # for k, v in switches.items():
        #     self.cursor.execute(f'UPDATE {self.table} SET datetime = "{v}" WHERE datetime = "{k}"')
        # self.mydb.commit()

    def save(self, row, order_by):
        query = f'INSERT INTO {self.table} VALUES({("%s, " * len(row))[:-2]});'
        self.cursor.execute(query, row)
        self.mydb.commit()
        query = f'SELECT datetime, RANK() OVER(ORDER BY {order_by}) AS "rank" FROM {self.table} WHERE username = "{row[0]}" and mode = "{row[3]}"'
        query = f'SELECT q.rank FROM ({query}) AS q WHERE datetime = "{row[1]}"'
        self.cursor.execute(query)
        position_local = [x for x in self.cursor][0][0]
        query = f'SELECT username, datetime, RANK() OVER(ORDER BY {order_by}) AS "rank" FROM {self.table} WHERE mode = "{row[3]}"'
        query = f'SELECT q.rank FROM ({query}) as q WHERE username = "{row[0]}" and datetime = "{row[1]}"'
        self.cursor.execute(query)
        position_global = [x for x in self.cursor][0][0]
        return (position_local, position_global)

    def load(self, username, mode, order_by, n):
        self.cursor.execute(f'SHOW COLUMNS FROM {self.table};')
        top_n = [tuple([''] + [x[0] for x in self.cursor])]
        if username:
            query = f'SELECT RANK() OVER(ORDER BY {order_by}) AS "rank", {self.table}.* FROM {self.table} WHERE username = "{username}" and mode = "{mode}" ORDER BY {order_by} LIMIT {n}'
        else:
            query = f'SELECT RANK() OVER(ORDER BY {order_by}) AS "rank", {self.table}.* FROM {self.table} WHERE mode = "{mode}" ORDER BY {order_by} LIMIT {n}'
        self.cursor.execute(query)
        top_n += [x for x in self.cursor]
        return top_n

class Records_csv():

    def __init__(self, directory, modes, header):
        self.directory = directory
        if not os.path.isdir(f'{self.directory}'):
            os.makedirs(f'{self.directory}')
        for mode in modes:
            record_path = os.path.join(f'{self.directory}', f'{mode}.csv')
            if not os.path.isfile(record_path):
                with open(record_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)

    def save(self, row, mode, order):
        record_path = os.path.join(f'{self.directory}', f'{mode}.csv')
        with open(record_path, 'r', newline='') as f:
            reader = csv.reader(f)
            records = [next(reader)]
            position_local = 1
            position_global = 1
            for line in reader:
                if (order[1] == 'asc' and row[order[0]] < float(line[order[0]]) or
                    order[1] == 'desc' and row[order[0]] > float(line[order[0]])):
                    records.append(row)
                    records.append(line)
                    for line in reader:
                        records.append(line)
                    break
                records.append(line)
                if line[0] == row[0]:
                    position_local += 1
                position_global += 1
            else:
                records.append(row)
        with open(record_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for line in records:
                writer.writerow(line)
        return (position_local, position_global)

    def load(self, username, mode, n):
        record_path = os.path.join(f'{self.directory}', f'{mode}.csv')
        with open(record_path, 'r', newline='') as f:
            reader = csv.reader(f)
            top_n = [next(reader)]
            for line in reader:
                if username == '' or line[0] == username:
                    top_n.append(line)
                    if len(top_n) > n:
                        break
        return top_n