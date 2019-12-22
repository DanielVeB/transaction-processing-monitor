import psycopg2

def begin_tran(cursor):
    cursor.execute('begin;')

def commit_tran(cursor):
    cursor.execute('commit')
    
def rollback(cursor):
    cursor.execute('rollback;')

def select(cursor,table):
    cursor.execute('select * from ' + table)
    records = cursor.fetchall()
    print(records)


connUsers = psycopg2.connect(dbname='cqgylhta', user='cqgylhta', 
                        password='znCG_b7Z1YZKMvtLLKc8x6K-N-22DrB-', host='rajje.db.elephantsql.com')
cursorU = connUsers.cursor()

connBooks = psycopg2.connect(dbname='rprwtdlf', user='rprwtdlf', 
                        password='gckeLMLWQYaD5YEZOPhhItLIifuZUz48', host='rajje.db.elephantsql.com')
cursorB = connBooks.cursor()

'-----------------------------------------------------------------------------------------------------'

print('Begin transaction')

begin_tran(cursorU)
begin_tran(cursorB)
select(cursorB,'books')
select(cursorU,'users')

print('---------------------------------')

print('some changes')

cursorU.execute('delete from users where name = \'Andrii\'')
cursorB.execute('delete from books where book = \'book_1\'')
select(cursorB,'books')
select(cursorU,'users')

print('---------------------------------')

print('roollback')

rollback(cursorU)
rollback(cursorB)
select(cursorB,'books')
select(cursorU,'users')

print('---------------------------------')



'-----------------------------------------------------------------------------------------------------'
cursorU.close()
cursorB.close()
connBooks.close()
connUsers.close()