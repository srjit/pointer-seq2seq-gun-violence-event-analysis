import os
import subprocess, threading

import connector

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


conn = connector._getpostgres_connection()

def kill_lynx(pid):
    os.kill(pid, signal.SIGKILL)
    os.waitpid(-1, os.WNOHANG)
    print("lynx killed")
 
def get_url(url):
    web_data = ""
 
    # import ipdb
    # ipdb.set_trace()

    cmd = "lynx -dump -nolist -notitle \"{0}\"".format(url)
    lynx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    t = threading.Timer(300.0, kill_lynx, args=[lynx.pid])
    t.start()
 
    web_data = lynx.stdout.read()
    t.cancel()
 
    web_data = web_data.decode("utf-8", 'replace')
    return web_data


# url = "http://www.johnsoncitypress.com/Courts/2017/10/23/Vehicular-homicide-Man-who-fled-hospital-due-today-in-Washington-Co-courtroom.html"
# text = get_url(url)
# print(text)
cur = conn.cursor()

delete = """Drop table if exists news_text"""
cur.execute(delete)

cur.execute("Create Table news_text(url text, article text);")


cur.execute("""SELECT url from page_downloads""")
rows = cur.fetchall()

TABLE = "news_text"

for url in rows:
    data = get_url(url[0])
    cur.execute("""INSERT INTO """ + TABLE + """ (url, article) 
    				values (%s, %s)""", 
    				(url, data))
    conn.commit()




