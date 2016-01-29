# tasking-manager-stats

This script is intended to provide an API endpoint to relevant OSM user statistics contained in the HOTOSM tasking manager database. Specifically, edit timestamps in the categories of done, validated, and invalidated, arranged by project and by user. For example:

```
"2156(userid)": {
  "167(projectid)": {
    "done": {
      "times": [
        "Sat Feb 13 2016 04:58:03 GMT"
        "Sat Feb 20 2016 04:02:20 GMT"
        "Sat Jan 30 2016 17:50:38 GMT"
      ]
    },
    "invalidated": {
      "times": [
        "Sun Apr 10 2016 08:24:42 GMT"
        "Thu Mar 03 2016 06:17:58 GMT"
      ]
    },
    "validated": {
      "times": [
        "Sun Jan 31 2016 07:16:41 GMT"
        "Thu Feb 11 2016 08:09:27 GMT"
        "Mon May 09 2016 02:25:27 GMT"
        "Thu Apr 14 2016 06:37:59 GMT"
        "Wed Mar 09 2016 19:44:51 GMT"
        "Wed May 25 2016 04:40:04 GMT"
      ]
    }
  }
}
```

In the current implementation, while the script is running and a database is being served, this information is provided at http://localhost:5000/.

## Dependencies
- pip install psycopg2 (SQL connection for Python) and flask (lightweight endpoint server) if necessary.
- This script depends on a running version of the HOTOSM Tasking Manager pgsql database schema, a clean copy of which can be downloaded along with the HOTOSM Tasking Server itself from https://github.com/hotosm/osm-tasking-manager2.
