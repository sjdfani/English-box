import sqlite3


def connect():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS database (word text,meaning text,synonym text ,antonym text ,describe_txt text, example text ,group_num text )")
    conn.commit()
    conn.close()


def insert(word, meaning, synonym, antonym, describe, example, group_num):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO database VALUES (?,?,?,?,?,?,?)",
                (word, meaning, synonym, antonym, describe, example, group_num))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM database")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(word=""):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM database WHERE word=? ", (word,))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(word):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM database WHERE word=?", (word,))
    conn.commit()
    conn.close()


def update(word, meaning, synonym, antonym, describe, example, group_num):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE database SET meaning=?,synonym=?,antonym=?,describe_txt=?,example=?,group_num=? WHERE word=?",
                (meaning, synonym, antonym, describe, example, group_num, word))
    conn.commit()
    conn.close()


connect()

# insert("hi", "سلام", "", "", "", "", 3)
