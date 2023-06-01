import sqlite3
from cogs.cogs_spy_fall import spyfall_db as sf

locations = sf.get_locations()

x = input()

sf.check_db()

for location in locations:
    sf.add_location(location)