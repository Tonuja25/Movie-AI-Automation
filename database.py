
import sqlite3

def getConnection():
    con = sqlite3.connect(
        "./moviedb1.sqlite3",
        check_same_thread=False
    )

    cursor = con.cursor()
    return con, cursor
