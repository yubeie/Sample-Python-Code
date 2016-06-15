import re
import os
import sqlite3
import shutil

fhandle1 = open('D1.txt')
fhandle2 = open('D2.txt')

dbconnection = sqlite3.connect('dinosaur.db')
dbcur = dbconnection.cursor()

dbcur.execute('DROP TABLE IF EXISTS dname')
dbcur.execute('DROP TABLE IF EXISTS catname')
dbcur.execute('DROP TABLE IF EXISTS leg')
dbcur.execute('DROP TABLE IF EXISTS dsplenlegcat')

dbcur.execute('CREATE TABLE dname(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,dinosaur_name CHAR(10) UNIQUE)')
dbcur.execute('CREATE TABLE catname(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,category_name TEXT UNIQUE)')
dbcur.execute('CREATE TABLE leg(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,leg TEXT UNIQUE)')
dbcur.execute('CREATE TABLE dsplenlegcat(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,dinosaur_id INTEGER,leg_id INTEGER,cat_id INTEGER,speed INTEGER,length INTEGER)')


for line in fhandle1:
    line.strip()
    word_list = line.split()
    dbcur.execute('INSERT OR IGNORE INTO dname(dinosaur_name) VALUES (?)',(word_list[0],))
    dbcur.execute('INSERT OR IGNORE INTO catname(category_name) VALUES (?)',(word_list[2],))
    dbcur.execute('INSERT OR IGNORE INTO leg(leg) VALUES (?)',(word_list[1],))
    dbconnection.commit()

fhandle1.close()

for line in fhandle2:
    line.strip()
    word_list = line.split()
    din_name = word_list[0]
    dbcur.execute('SELECT id FROM dname WHERE dinosaur_name = ?', (din_name,))
    din_id = dbcur.fetchone()[0]
    dbcur.execute('INSERT INTO dsplenlegcat(dinosaur_id,speed,length) VALUES (?,?,?)',(din_id,word_list[1],word_list[2]))
    dbconnection.commit()

fhandle2.close()
fhandle1 = open('D1.txt')
  
for line in fhandle1:
    line.strip()
    word_list = line.split()
    dino_name = word_list[0]
    legs_name = word_list[1]
    cat = word_list[2]
    dbcur.execute('SELECT id FROM dname WHERE dinosaur_name = ?', (word_list[0],))
    dino_id = dbcur.fetchone()[0]
    dbcur.execute('SELECT id FROM leg WHERE leg = ?', (word_list[1],))
    legs_id = dbcur.fetchone()[0]
    dbcur.execute('SELECT id FROM catname WHERE category_name = ?', (word_list[2],))
    cats_id = dbcur.fetchone()[0]
    print dino_id 
    print legs_id
    print cats_id
    dbcur.execute('UPDATE dsplenlegcat SET leg_id=?,cat_id=? WHERE dinosaur_id = ?',(legs_id,cats_id,dino_id))
    dbconnection.commit()



def query(category,legged):
    print 'entering query function....'
    all_rows = list()
    dbcur.execute('SELECT dsplenlegcat.speed,leg.leg,catname.category_name,dname.dinosaur_name FROM dsplenlegcat JOIN leg JOIN catname JOIN dname ON dsplenlegcat.dinosaur_id=dname.id AND dsplenlegcat.leg_id=leg.id AND dsplenlegcat.cat_id=catname.id WHERE category_name=? AND leg=?',(category,legged))
    all_rows=dbcur.fetchall()
    print all_rows


while True:
    try:
        legged = raw_input('Enter two-legged (or) four-legged: ')
        legged = str(legged)
        if legged == 'quit':
            break
        elif legged =='two-legged' or legged =='four-legged':
            category = raw_input('Enter cat1 (or) cat2 (or) cat3: ')
            category = str(category)
            if category =='quit':
                break
            elif (category == 'cat1'):
                query(category,legged)
            elif (category == 'cat2'):
                query(category,legged)
            elif (category == 'cat3'):
                query(category,legged)
            else:
                print 'enter correct value or enter quit'
                continue
        else:
            print 'enter the correct value or enter quit'
            continue
    except:
        print 'quitting the program due to issues..'
        break
    