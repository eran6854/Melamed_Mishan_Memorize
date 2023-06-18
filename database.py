import sqlite3

"""
Tables (static means it's values shouldn't be changed):
1) names (static): cols = id (unique), name,
2) hierarchy (static): cols = id (unique), parent, children,
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
#     ("berakhot_1_1", "berakhot_1", None)
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
# new_value = 'berakhot_4_1, berakhot_4_2, berakhot_4_3, berakhot_4_4, berakhot_4_5, berakhot_4_6, berakhot_4_7'
# row_id = 'berakhot_4'
#
# c.execute("UPDATE <table name> SET <column val to change> = ? WHERE id = ?", (new_value, row_id))
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# select
# c.execute("""SELECT * FROM hierarchy WHERE id='berakhot_8'""")
# c.execute("""SELECT * FROM hierarchy""")
# for line in c.fetchall():
#     print(line)
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
zeraim: berakhot, peah, demai, kilayim, sheviit, terumot, maaserot, maaser_sheni, challah, orlah, bikkurim     
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
