import sqlite3
from dataclasses import dataclass

connection = sqlite3.connect('cats.db')
cursor = connection.cursor()
connection.execute("""CREATE TABLE "breeds" (
    "breedid"   INTEGER NOT NULL,
    "name"  TEXT NOT NULL,
    "description"   TEXT,
    PRIMARY KEY("breedid" AUTOINCREMENT)
)
""")
connection.execute("""CREATE TABLE "catperson" (
    "personid"  INTEGER NOT NULL,
    "name"  TEXT NOT NULL,
    "breedid"   INTEGER NOT NULL,
    "birth" TEXT,
    "description"   TEXT,
    "subbreedid"    INT,
    PRIMARY KEY("personid" AUTOINCREMENT)
    FOREIGN KEY (breedid)  REFERENCES breeds (breedid)
    FOREIGN KEY (subbreedid)  REFERENCES subbreeds (subbreedid)
)
""")
connection.execute("""CREATE TABLE "subbreeds" (
    "subbreedid"    INTEGER NOT NULL,
    "name"  TEXT NOT NULL,    
    "breedid"   INTEGER,
    "description"   TEXT,
    PRIMARY KEY("subbreedid" AUTOINCREMENT)
    FOREIGN KEY (breedid)  REFERENCES breeds (breedid)
)
""")

connection.commit()



