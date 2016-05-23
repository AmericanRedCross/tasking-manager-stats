#!/usr/bin/python

# This script creates statistics for OSM users of the
# OSM Tasking Manager database.
# Edit timestamps for each category of action arranged by project and user.
# Output is in JSON format and is uploaded directly to an Amazon S3 bucket.
#
# Usage
#
# python taskingDBendpoint.py

import psycopg2
import psycopg2.extras
import simplejson as json
from os import path, mkdir


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

    # translation dict for task completion categories
    stateLookup = {2: 'done', 3: 'validated', 1: 'invalidated'}

    # helper to append new project and append first timestamp to
    # project in proper category
    def appendFirstProject(r, users, user_id, proj_id, stateLookup):
        users[user_id][proj_id] = {'done': {'times': []},
                                   'validated': {'times': []},
                                   'invalidated': {'times': []}}
        users[user_id][proj_id][stateLookup[r.state]]['times'] \
            .append(str(r.date).split('.')[0])

    # build user dictionary with unique keys and subkeys for user_id and
    # project_id, and placeholders for edit type and times
    users = {}
    for r in records:
        user_id = str(r.user_id)
        proj_id = str(r.project_id)
        # if user exists...
        if user_id in users:
            # if user exists and project exists...
            if proj_id in users[user_id]:
                # ...append next timestamp to project in proper category.
                users[user_id][proj_id][stateLookup[r.state]]['times'] \
                    .append(str(r.date).split('.')[0])
            # if user exists but project doesn't exist...
            else:
                # ...append new project and append first timestamp to project
                # in proper category.
                appendFirstProject(r, users, user_id, proj_id, stateLookup)
        # if no user exists...
        else:
            # ...append new user and append new project and append first
            # timestamp to project in proper category.
            users[user_id] = {}
            appendFirstProject(r, users, user_id, proj_id, stateLookup)

    return users


def write(users):
    outdir = 'user_data'
    if not path.exists(outdir):
        mkdir(outdir)

    # for each individual user...
    for user_id, user_data in users.iteritems():
        # ...dump user's dict into minified json...
        fout = fout = json.dumps(user_data, separators=(',', ':'))
        # ...generate file of user's json.
        f = open(path.join(outdir, user_id + '.json'), 'wb')
        f.write(fout)
        f.close()


def main():
    users = getTaskstate()
    write(users)

if __name__ == '__main__':
    main()
