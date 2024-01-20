import sqlite3 as db

conn = db.connect('Scraper.db')
cursor = conn.cursor()

# enables foreign keys
cursor.execute("""
    PRAGMA foreign_keys = ON;
""")

# create tables 
cursor.execute("""
    CREATE TABLE Stocks (
        ticker_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_desc TEXT
    );
""")

cursor.execute("""
    CREATE TABLE OptTypes (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_desc TEXT
    );
""")

cursor.execute("""

    CREATE TABLE Strategy (
        strategy_id INTEGER PRIMARY KEY AUTOINCREMENT,
        strategy_desc TEXT    
    );
""")

cursor.execute("""
    CREATE TABLE ActiveOptions (
        option_id INTEGER,

        CONSTRAINT fks
            FOREIGN KEY (option_id) REFERENCES Options(option_id)  
    );
""")

cursor.execute("""
    CREATE TABLE Options (
        option_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_id INTEGER,
        strike INTEGER,
        exp_date TEXT,
        strategy_id INTEGER,
        type_id INTEGER,
        opt_desc TEXT,
        qnty INTEGER,
        bp NUMERIC,
        open_interest INTEGER,
        volume INTEGER,
        iv NUMERIC,
        cpl NUMERIC,
        cps NUMERIC,
        gamma NUMERIC,
        delta NUMERIC,
        theta NUMERIC,
        rho NUMERIC,
        vega NUMERIC,
        
        CONSTRAINT fks
            FOREIGN KEY (ticker_id) REFERENCES Stocks(ticker_id),
            FOREIGN KEY (strategy_id) REFERENCES Strategy(strategy_id),
            FOREIGN KEY (type_id) REFERENCES OptTypes(type_id)
    );
""")

cursor.execute("""
    CREATE TABLE Prices (
        option_id INTEGER,
        price NUMERIC,
        tmstp INTEGER,

        CONSTRAINT fks
            FOREIGN KEY (option_id) REFERENCES Options(option_id)        
    );
""")

cursor.execute("""
    INSERT INTO Strategy (strategy_desc)
        VALUES ('self'),
               ('optionsful');
""")

cursor.execute("""
    INSERT INTO OptTypes (type_desc)
        VALUES ('call'),
                ('put');
""")

conn.commit()
conn.close()