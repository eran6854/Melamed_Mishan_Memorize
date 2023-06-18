import sqlite3

# setup
conn = sqlite3.connect("database.db")
c = conn.cursor()

# execution
# c.execute("""""")
# conn.commit()

# close
conn.close()