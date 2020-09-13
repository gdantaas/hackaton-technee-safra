import pyodbc

class dbData:
    def __init__(self, server='localhost\SQLEXPRESS01', db='SafraHubDB', usr='technee', pwd='123456'):
        self.conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                   f'Server={server};'
                                   f'Database={db};'
                                   f'UID={usr};'
                                   f'PWD={pwd};')
        self.cursor = self.conn.cursor()

    def selectData(self, table, filters='', columns='*', order='', group='', join=''):
        sel = f'SELECT {columns} FROM {table} '
        joi = join + ' '
        fil = f'WHERE {filters} ' if len(filters) > 0 else ' '
        ord = f'ORDER BY {order} ' if len(order) > 0 else ' '
        grp = f'GROUP BY {group} ' if len(group) > 0 else ' '

        # print(sel + joi + fil + ord + grp)
        self.cursor.execute(sel + joi + fil + ord + grp)
        return [row for row in self.cursor]
