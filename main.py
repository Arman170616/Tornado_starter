import sqlite3
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db_conn):
        self.db_conn = db_conn

    def get(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        self.write({"users": users})

def make_app():
    db_conn = sqlite3.connect("example.db")
    db_conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    return tornado.web.Application([
        (r"/", MainHandler, dict(db_conn=db_conn)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()
