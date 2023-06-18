import sqlite3

"""
Tables (static means it's values shouldn't be changed):
names (static): cols = id (unique), name,
hierarchy (static): cols = id (unique), parent, children,
"""

# setup
conn = sqlite3.connect("database.db")
c = conn.cursor()

# execution
# ----------------------------------------------------------------------------------------------------------------------
# create table

# c.execute("""CREATE TABLE hierarchy(
#              id TEXT PRIMARY KEY UNIQUE,
#              parent TEXT,
#              children TEXT
# )""")
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# insert

# values = [
#     ("shas", None, 'zeraim, moed, nashim, nezikin, kodashim, tohorot'),
# ]
#
# # check table name is correct here
# c.executemany('INSERT INTO <hierarchy> (id, parent, children) VALUES (?, ?, ?)', values)
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# delete
# c.execute("DELETE FROM names WHERE id='berakhot_1'")
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# update
# new_value = "zeraim"
# row_id = 'Zeraim'
#
# c.execute("UPDATE <table name> SET <column val to change> = ? WHERE id = ?", (new_value, row_id))
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# select
c.execute("""SELECT * FROM hierarchy WHERE id!='1'""")
for line in c.fetchall():
    list_children = line[2].split(",")
    list_children = [e.strip() for e in list_children]
    for child in list_children:
        print(child)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# drop table
# c.execute('DROP TABLE <table name>')
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# copy data into <table 1> table to <table 2>
# c.execute('INSERT INTO <table 1> SELECT * FROM <table 2>')
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# rename table
# c.execute('ALTER TABLE <old table name> RENAME TO <new table name>')
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------


# close
conn.close()

"""
id values to remember:
shas
orders: zeraim, moed, nashim, nezikin, kodashim, tohorot
berakhot
"""

"""
select to remember:
c.execute(""SELECT * FROM hierarchy WHERE id!='1'"")
for line in c.fetchall():
    list_children = line[2].split(",")
    list_children = [e.strip() for e in list_children]
    for child in list_children:
        print(child)
"""
