import sqlite3
import tornado.ioloop
import tornado.web
import json

class AboutHandler(tornado.web.RequestHandler):
    def initialize(self, db_conn):
        self.db_conn = db_conn

    def get(self):
        self.write({"message": "This is the About page."})

class ContactHandler(tornado.web.RequestHandler):
    def initialize(self, db_conn):
        self.db_conn = db_conn

    def get(self):
        self.write({"message": "This is the Contact page."})

    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (data['name'], data['email'], data['message']))
            self.db_conn.commit()
            response_data = {"message": "Contact information received successfully.", "data_received": data}
            self.write(json.dumps(response_data))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class ServiceHandler(tornado.web.RequestHandler):
    def initialize(self, db_conn):
        self.db_conn = db_conn

    def get(self):
        self.write({"message": "This is the Service page."})

def make_app():
    db_conn = sqlite3.connect("example.db")
    db_conn.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)")

    return tornado.web.Application([
        (r"/about", AboutHandler, dict(db_conn=db_conn)),
        (r"/contact", ContactHandler, dict(db_conn=db_conn)),
        (r"/service", ServiceHandler, dict(db_conn=db_conn)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()
