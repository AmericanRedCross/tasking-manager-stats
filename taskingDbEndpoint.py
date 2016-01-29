import psycopg2
import psycopg2.extras
from flask import Flask, jsonify


def connectDB():
    # login info
    host = 'localhost'
    database = 'osmtm'
    user = 'postgres'
    # define connection string
    conn_string = "host='%s' dbname='%s' user='%s'" % (host, database, user)
    # get a connection
    conn = psycopg2.connect(conn_string)
    # initialize a cursor
    return conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

# returns dictionary of users, their projects, the categories of edits
# made by them, and the times they made those edits
def getTaskstate():
    # connect to database
    cur = connectDB()
    # cursor to select all relevant task_state columns
    cur.execute(' SELECT user_id, project_id, state, date \
                  FROM task_state \
                  WHERE user_id IS NOT NULL \
                  AND state IN (1, 2, 3) ')
    records = cur.fetchall()
    # build user dictionary with unique keys and subkeys for user_id and
    # project_id, and placeholders for edit type and times
    stateLookup = {2: 'done', 3: 'validated', 1: 'invalidated'}
    users = {}
    for r in records:
        user_id = str(r.user_id)
        proj_id = str(r.project_id)
        if user_id in users:
            if proj_id in users[user_id]:
                users[user_id][proj_id][stateLookup[r.state]]['times']\
                    .append(r.date)
            else:
                users[user_id][proj_id] = {'done': {'times': []},
                                           'validated': {'times': []},
                                           'invalidated': {'times': []}}
        else:
            users[user_id] = {}

    return users


app = Flask(__name__)


# route definitions
# posts dictionary from getUserdata function as JSON
@app.route('/')
def userdata():
    users = getTaskstate()
    return jsonify(users)

if __name__ == '__main__':
    app.debug = True
    app.run()
