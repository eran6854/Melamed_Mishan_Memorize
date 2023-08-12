import sqlite3
import math
import datetime
import statistics
import time

import extraFunctions

"""
########################################################################################################################
Constants:
########################################################################################################################
"""
TEST_1_WEIGHT = 0.1
TEST_2_WEIGHT = 0.5
TEST_3_WEIGHT = 0.4

"""
########################################################################################################################
Database Operations:
########################################################################################################################
"""
# setup
# conn = sqlite3.connect("database.db")
# c = conn.cursor()

# execution
# ----------------------------------------------------------------------------------------------------------------------
# create table

# c.execute("""CREATE TABLE text(
#              id TEXT PRIMARY KEY UNIQUE,
#              text TEXT
# )""")
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# insert

# values = [
#     ("berakhot_1_2", mishnayotText.berakhot_1_2_text),
#     ("berakhot_1_3", mishnayotText.berakhot_1_3_text)
# ]
#
# # check table name is correct here
# c.executemany('INSERT INTO text (id, text) VALUES (?, ?)', values)
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# delete
# c.execute("DELETE FROM hierarchy WHERE id='berakhot_3_2'")
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# update
# new_value = 'berakhot_1_1, berakhot_1_2, berakhot_1_3'
# row_id = 'berakhot_1'
#
# # c.execute("UPDATE <table name> SET <column val to change> = ? WHERE id = ?", (new_value, row_id))
# c.execute("UPDATE hierarchy SET children = ? WHERE id = ?", (new_value, row_id))
# conn.commit()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# select
# c.execute("""SELECT * FROM hierarchy WHERE id='berakhot_8'""")
# c.execute("""SELECT * FROM grades""")
# for line in c.fetchall():
#     print(line)
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
# conn.close()

"""
########################################################################################################################
Database Functions:
########################################################################################################################
"""


def show_all_table_rows(table):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    for line in cursor.fetchall():
        print(line)
    connection.close()


def show_row(table, row_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE id = '{row_id}'")
    print(cursor.fetchone())
    connection.close()


def get_all_table_rows(table):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    lines = []
    for line in cursor.fetchall():
        lines.append(line)
    connection.close()
    return lines


def eval_final_grade(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM grades WHERE id = ?", (mishna_id,))
    row = list(cursor.fetchone())
    new_value = math.floor(TEST_1_WEIGHT * row[1] + TEST_2_WEIGHT * row[2] + TEST_3_WEIGHT * row[3])
    cursor.execute("UPDATE grades SET final_grade = ? WHERE id = ?", (new_value, mishna_id))
    connection.commit()
    connection.close()


def update_test_0(mishna_id, grade):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    new_value = grade
    row_id = mishna_id
    cursor.execute("UPDATE grades SET test_1_grade = ? WHERE id = ?", (new_value, row_id))
    connection.commit()
    connection.close()
    eval_final_grade(mishna_id)


def reset_test_0(mishna_id):
    update_test_0(mishna_id, 0)


def reset_all_test_0():
    rows = get_all_table_rows("grades")
    for row in rows:
        mishna_id = row[0]
        reset_test_0(mishna_id)


def update_test_1(mishna_id, grade):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    new_value = grade
    row_id = mishna_id
    cursor.execute("UPDATE grades SET test_2_grade = ? WHERE id = ?", (new_value, row_id))
    connection.commit()
    connection.close()
    eval_final_grade(mishna_id)


def reset_test_1(mishna_id):
    update_test_1(mishna_id, 0)


def reset_all_test_1():
    rows = get_all_table_rows("grades")
    for row in rows:
        mishna_id = row[0]
        reset_test_1(mishna_id)


def update_last_100_score_date(mishna_id, date_in_timestamp):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    new_value = date_in_timestamp
    row_id = mishna_id
    cursor.execute("UPDATE dates SET last_100_score = ? WHERE id = ?", (new_value, row_id))
    connection.commit()
    connection.close()


def update_last_100_score_date_now(mishna_id):
    dt = datetime.datetime.now()
    seconds = int(dt.timestamp())
    update_last_100_score_date(mishna_id, seconds)


def reset_last_100_score_date(mishna_id):
    update_last_100_score_date(mishna_id, None)


def reset_all_last_100_score_date():
    rows = get_all_table_rows("dates")
    for row in rows:
        mishna_id = row[0]
        reset_last_100_score_date(mishna_id)


def drop_table(table):
    if table in ["names", "hierarchy", "grades", "dates", "text"]:
        raise Exception("are you sure??")
    else:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE {table}")
        connection.commit()
        connection.close()


def get_text(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM text WHERE id='{mishna_id}'")
    text = cursor.fetchone()[1]
    connection.close()
    return text


def get_children(item_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM hierarchy WHERE id='{item_id}'")
    children = cursor.fetchone()[2]
    if children is not None:
        children = children.split(",")
        children = [e.strip() for e in children]
    connection.close()
    return children


def get_parent(item_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM hierarchy WHERE id='{item_id}'")
    parent = cursor.fetchone()[1]
    connection.close()
    return parent


def is_mishna(item_id):
    if get_children(item_id) is None:
        return True
    return False


def get_mishna_grade(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM grades WHERE id='{mishna_id}'")
    grade = cursor.fetchone()[4]
    connection.close()
    return grade


def get_test_0_grade(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM grades WHERE id='{mishna_id}'")
    grade = cursor.fetchone()[1]
    connection.close()
    return grade


def get_test_1_grade(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM grades WHERE id='{mishna_id}'")
    grade = cursor.fetchone()[2]
    connection.close()
    return grade


def get_test_2_grade(mishna_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM grades WHERE id='{mishna_id}'")
    grade = cursor.fetchone()[3]
    connection.close()
    return grade


def get_grade(item_id):
    children_ids = get_children(item_id)
    if children_ids is None:
        return get_mishna_grade(item_id)
    else:
        try:
            return math.floor(statistics.mean([get_grade(e) for e in children_ids]))
        # remove when everything is well-defined
        except Exception:
            return 0


def update_test_2(mishna_id, grade):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    new_value = grade
    row_id = mishna_id
    cursor.execute("UPDATE grades SET test_3_grade = ? WHERE id = ?", (new_value, row_id))
    connection.commit()
    update_last_100_score_date_now(mishna_id)
    connection.close()
    eval_final_grade(mishna_id)


def reset_test_2(mishna_id):
    update_test_2(mishna_id, 0)
    reset_last_100_score_date(mishna_id)


def reset_all_test_2():
    rows = get_all_table_rows("grades")
    for row in rows:
        mishna_id = row[0]
        reset_test_2(mishna_id)


def reset_item(item_id):
    children_ids = get_children(item_id)
    if children_ids is None:
        reset_test_0(item_id)
        reset_test_1(item_id)
        reset_test_2(item_id)
    else:
        for child_id in children_ids:
            reset_item(child_id)


def get_name(item_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM names WHERE id='{item_id}'")
    name = cursor.fetchone()[1]
    connection.close()
    return name


def get_date(item_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM dates WHERE id='{item_id}'")
    date = cursor.fetchone()[1]
    connection.close()
    return date


def get_date_check_list(item_id, list1):
    children_ids = get_children(item_id)
    if children_ids is None:
        last_date = get_date(item_id)
        if last_date is None:
            return [None]
        else:
            date_check = extraFunctions.check_time_gap(last_date)
            list1.append(date_check)
            return [date_check]
    else:
        for child_id in children_ids:
            list1.extend(get_date_check_list(child_id, list1))
    return list1


def get_date_check(item_id):
    # return options:
    # None - wasn't touched
    # 1 - less than a month
    # 2 - between a month and 2 months
    # 3 - over 2 months
    lst = list()
    list1 = get_date_check_list(item_id, lst)
    if None in list1:
        return None
    else:
        return max(list1)


# update_last_100_score_date_now("berakhot_1_1")
# update_last_100_score_date_now("berakhot_1_2")
# update_last_100_score_date_now("berakhot_1_3")
# update_last_100_score_date_now("berakhot_1_4")
# update_last_100_score_date_now("berakhot_1_5")
# update_last_100_score_date_now("berakhot_2_1")
# update_last_100_score_date_now("berakhot_2_2")
# update_last_100_score_date_now("berakhot_2_3")
# update_last_100_score_date_now("berakhot_2_4")
# update_last_100_score_date_now("berakhot_2_5")
# update_last_100_score_date_now("berakhot_2_6")
# update_last_100_score_date_now("berakhot_2_7")
# update_last_100_score_date_now("berakhot_2_8")
# update_last_100_score_date_now("berakhot_3_1")
# update_last_100_score_date_now("berakhot_3_2")
# update_last_100_score_date_now("berakhot_3_3")
# update_last_100_score_date_now("berakhot_3_4")
# update_last_100_score_date_now("berakhot_3_5")
# update_last_100_score_date_now("berakhot_3_6")
# update_last_100_score_date_now("berakhot_4_1")
# update_last_100_score_date_now("berakhot_4_2")
# update_last_100_score_date_now("berakhot_4_3")
# update_last_100_score_date_now("berakhot_4_4")
# update_last_100_score_date_now("berakhot_4_5")
# update_last_100_score_date_now("berakhot_4_6")
# update_last_100_score_date_now("berakhot_4_7")
# update_last_100_score_date_now("berakhot_5_1")
# update_last_100_score_date_now("berakhot_5_2")
# update_last_100_score_date_now("berakhot_5_3")
# update_last_100_score_date_now("berakhot_5_4")
# update_last_100_score_date_now("berakhot_5_5")
# update_last_100_score_date_now("berakhot_6_1")
# update_last_100_score_date_now("berakhot_6_2")
# update_last_100_score_date_now("berakhot_6_3")
# update_last_100_score_date_now("berakhot_6_4")
# update_last_100_score_date_now("berakhot_6_5")
# update_last_100_score_date_now("berakhot_6_6")
# update_last_100_score_date_now("berakhot_6_7")
# update_last_100_score_date_now("berakhot_6_8")
# update_last_100_score_date_now("berakhot_7_1")
# update_last_100_score_date_now("berakhot_7_2")
# update_last_100_score_date_now("berakhot_7_3")
# update_last_100_score_date_now("berakhot_7_4")
# update_last_100_score_date_now("berakhot_7_5")
# update_last_100_score_date_now("berakhot_8_1")
# update_last_100_score_date_now("berakhot_8_2")
# update_last_100_score_date_now("berakhot_8_3")
# update_last_100_score_date_now("berakhot_8_4")
# update_last_100_score_date_now("berakhot_8_5")
# update_last_100_score_date_now("berakhot_8_6")
# update_last_100_score_date_now("berakhot_8_7")
# update_last_100_score_date_now("berakhot_8_8")
# update_last_100_score_date_now("berakhot_9_1")
# update_last_100_score_date_now("berakhot_9_2")
# update_last_100_score_date_now("berakhot_9_3")
# update_last_100_score_date_now("berakhot_9_4")
# update_last_100_score_date_now("berakhot_9_5")

# for show
# update_test_0("berakhot_1_1", 100)
# update_test_1("berakhot_1_1", 100)
# update_test_2("berakhot_1_1", 100)
# update_test_0("berakhot_1_2", 100)
# update_test_1("berakhot_1_2", 100)
# update_test_2("berakhot_1_2", 100)
# update_test_0("berakhot_1_3", 100)
# update_test_1("berakhot_1_3", 100)
# update_test_2("berakhot_1_3", 100)
# update_test_0("berakhot_1_4", 100)
# update_test_1("berakhot_1_4", 100)
# update_test_2("berakhot_1_4", 100)
# update_test_0("berakhot_1_5", 100)
# update_test_1("berakhot_1_5", 100)
# update_test_2("berakhot_1_5", 100)
#
# update_last_100_score_date("berakhot_1_1", time.time() - 30 * 24 * 60 * 60 + 20)
# update_last_100_score_date("berakhot_1_2", time.time() - 60 * 24 * 60 * 60 + 800)
# update_last_100_score_date("berakhot_1_3", time.time() - 60 * 24 * 60 * 60 - 800)
show_all_table_rows("hierarchy")
"""
########################################################################################################################
Notes:
########################################################################################################################
"""

"""
Tables (static means it's values shouldn't be changed):
1) names (static): cols = id (unique), name
2) hierarchy (static): cols = id (unique), parent, children
3) grades (dynamic): cols = id (unique), test_1_grade, test_2_grade, test_3_grade, final_grade
4) dates (dynamic): cols = id (unique), last_100_score
5) text (static): cols = id (unique), text
"""

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

"""
#     ("berakhot_1_1", None),
#     ("berakhot_1_2", None),
#     ("berakhot_1_3", None),
#     ("berakhot_1_4", None),
#     ("berakhot_1_5", None),
#     ("berakhot_2_1", None),
#     ("berakhot_2_2", None),
#     ("berakhot_2_3", None),
#     ("berakhot_2_4", None),
#     ("berakhot_2_5", None),
#     ("berakhot_2_6", None),
#     ("berakhot_2_7", None),
#     ("berakhot_2_8", None),
#     ("berakhot_3_1", None),
#     ("berakhot_3_2", None),
#     ("berakhot_3_3", None),
#     ("berakhot_3_4", None),
#     ("berakhot_3_5", None),
#     ("berakhot_3_6", None),
#     ("berakhot_4_1", None),
#     ("berakhot_4_2", None),
#     ("berakhot_4_3", None),
#     ("berakhot_4_4", None),
#     ("berakhot_4_5", None),
#     ("berakhot_4_6", None),
#     ("berakhot_4_7", None),
#     ("berakhot_5_1", None),
#     ("berakhot_5_2", None),
#     ("berakhot_5_3", None),
#     ("berakhot_5_4", None),
#     ("berakhot_5_5", None),
#     ("berakhot_6_1", None),
#     ("berakhot_6_2", None),
#     ("berakhot_6_3", None),
#     ("berakhot_6_4", None),
#     ("berakhot_6_5", None),
#     ("berakhot_6_6", None),
#     ("berakhot_6_7", None),
#     ("berakhot_6_8", None),
#     ("berakhot_7_1", None),
#     ("berakhot_7_2", None),
#     ("berakhot_7_3", None),
#     ("berakhot_7_4", None),
#     ("berakhot_7_5", None),
#     ("berakhot_8_1", None),
#     ("berakhot_8_2", None),
#     ("berakhot_8_3", None),
#     ("berakhot_8_4", None),
#     ("berakhot_8_5", None),
#     ("berakhot_8_6", None),
#     ("berakhot_8_7", None),
#     ("berakhot_8_8", None),
#     ("berakhot_9_1", None),
#     ("berakhot_9_2", None),
#     ("berakhot_9_3", None),
#     ("berakhot_9_4", None),
#     ("berakhot_9_5", None)
"""
"""
hierarchy:
('shas', None, 'zeraim, moed, nashim, nezikin, kodashim, tohorot')
('zeraim', 'shas', 'berakhot, peah, demai, kilayim, sheviit, terumot, maaserot, maaser_sheni, challah, orlah, bikkurim')
"""

"""
for show:
update_test_0("berakhot_1_1", 100)
update_test_1("berakhot_1_1", 100)
update_test_2("berakhot_1_1", 100)
update_test_0("berakhot_1_2", 100)
update_test_1("berakhot_1_2", 100)
update_test_2("berakhot_1_2", 100)
update_test_0("berakhot_1_3", 100)
update_test_1("berakhot_1_3", 100)
update_test_2("berakhot_1_3", 100)
update_test_0("berakhot_1_4", 100)
update_test_1("berakhot_1_4", 100)
update_test_2("berakhot_1_4", 100)
update_test_0("berakhot_1_5", 100)
update_test_1("berakhot_1_5", 100)
update_test_2("berakhot_1_5", 100)

update_last_100_score_date("berakhot_1_1", time.time() - 30 * 24 * 60 * 60 + 800)
update_last_100_score_date("berakhot_1_2", time.time() - 60 * 24 * 60 * 60 + 800)
update_last_100_score_date("berakhot_1_3", time.time() - 60 * 24 * 60 * 60 - 800)
show_all_table_rows("dates")
"""

"""
('shas', None, 'zeraim')
('zeraim', 'shas', 'berakhot')
('berakhot', 'zeraim', 'berakhot_1, berakhot_2, berakhot_3, berakhot_4, berakhot_5, berakhot_6, berakhot_7, berakhot_8, berakhot_9')
('berakhot_1', 'berakhot', 'berakhot_1_1, berakhot_1_2, berakhot_1_3, berakhot_1_4, berakhot_1_5')
('berakhot_2', 'berakhot', 'berakhot_2_1, berakhot_2_2, berakhot_2_3, berakhot_2_4, berakhot_2_5, berakhot_2_6, berakhot_2_7, berakhot_2_8')
('berakhot_3', 'berakhot', 'berakhot_3_1, berakhot_3_2, berakhot_3_3, berakhot_3_4, berakhot_3_5, berakhot_3_6')
('berakhot_4', 'berakhot', 'berakhot_4_1, berakhot_4_2, berakhot_4_3, berakhot_4_4, berakhot_4_5, berakhot_4_6, berakhot_4_7')
('berakhot_5', 'berakhot', 'berakhot_5_1, berakhot_5_2, berakhot_5_3, berakhot_5_4, berakhot_5_5')
('berakhot_6', 'berakhot', 'berakhot_6_1, berakhot_6_2, berakhot_6_3, berakhot_6_4, berakhot_6_5, berakhot_6_6, berakhot_6_7, berakhot_6_8')
('berakhot_7', 'berakhot', 'berakhot_7_1, berakhot_7_2, berakhot_7_3, berakhot_7_4, berakhot_7_5')
('berakhot_8', 'berakhot', 'berakhot_8_1, berakhot_8_2, berakhot_8_3, berakhot_8_4, berakhot_8_5, berakhot_8_6, berakhot_8_7, berakhot_8_8')
('berakhot_9', 'berakhot', 'berakhot_9_1, berakhot_9_2, berakhot_9_3, berakhot_9_4, berakhot_9_5')
('berakhot_1_1', 'berakhot_1', None)
('berakhot_1_2', 'berakhot_1', None)
('berakhot_1_3', 'berakhot_1', None)
('berakhot_1_4', 'berakhot_1', None)
('berakhot_1_5', 'berakhot_1', None)
('berakhot_2_1', 'berakhot_2', None)
('berakhot_2_2', 'berakhot_2', None)
('berakhot_2_3', 'berakhot_2', None)
('berakhot_2_4', 'berakhot_2', None)
('berakhot_2_5', 'berakhot_2', None)
('berakhot_2_6', 'berakhot_2', None)
('berakhot_2_7', 'berakhot_2', None)
('berakhot_2_8', 'berakhot_2', None)
('berakhot_3_1', 'berakhot_3', None)
('berakhot_3_2', 'berakhot_3', None)
('berakhot_3_3', 'berakhot_3', None)
('berakhot_3_4', 'berakhot_3', None)
('berakhot_3_5', 'berakhot_3', None)
('berakhot_3_6', 'berakhot_3', None)
('berakhot_4_1', 'berakhot_4', None)
('berakhot_4_2', 'berakhot_4', None)
('berakhot_4_3', 'berakhot_4', None)
('berakhot_4_4', 'berakhot_4', None)
('berakhot_4_5', 'berakhot_4', None)
('berakhot_4_6', 'berakhot_4', None)
('berakhot_4_7', 'berakhot_4', None)
('berakhot_5_1', 'berakhot_5', None)
('berakhot_5_2', 'berakhot_5', None)
('berakhot_5_3', 'berakhot_5', None)
('berakhot_5_4', 'berakhot_5', None)
('berakhot_5_5', 'berakhot_5', None)
('berakhot_6_1', 'berakhot_6', None)
('berakhot_6_2', 'berakhot_6', None)
('berakhot_6_3', 'berakhot_6', None)
('berakhot_6_4', 'berakhot_6', None)
('berakhot_6_5', 'berakhot_6', None)
('berakhot_6_6', 'berakhot_6', None)
('berakhot_6_7', 'berakhot_6', None)
('berakhot_6_8', 'berakhot_6', None)
('berakhot_7_1', 'berakhot_7', None)
('berakhot_7_2', 'berakhot_7', None)
('berakhot_7_3', 'berakhot_7', None)
('berakhot_7_4', 'berakhot_7', None)
('berakhot_7_5', 'berakhot_7', None)
('berakhot_8_1', 'berakhot_8', None)
('berakhot_8_2', 'berakhot_8', None)
('berakhot_8_3', 'berakhot_8', None)
('berakhot_8_4', 'berakhot_8', None)
('berakhot_8_5', 'berakhot_8', None)
('berakhot_8_6', 'berakhot_8', None)
('berakhot_8_7', 'berakhot_8', None)
('berakhot_8_8', 'berakhot_8', None)
('berakhot_9_1', 'berakhot_9', None)
('berakhot_9_2', 'berakhot_9', None)
('berakhot_9_3', 'berakhot_9', None)
('berakhot_9_4', 'berakhot_9', None)
('berakhot_9_5', 'berakhot_9', None)

"""