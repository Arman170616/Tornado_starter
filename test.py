import sqlite3
import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is the Main page.")

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

    def get(self, service_id=None):
        if service_id:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM services WHERE id=?", (service_id,))
            service = cursor.fetchone()
            if service:
                self.write({"service": {"id": service[0], "name": service[1], "description": service[2]}})
            else:
                self.set_status(404)
                self.write({"error": "Service not found"})
        else:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM services")
            services = cursor.fetchall()
            self.write({"services": [{"id": service[0], "name": service[1], "description": service[2]} for service in services]})

    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO services (name, description) VALUES (?, ?)", (data['name'], data['description']))
            self.db_conn.commit()
            response_data = {"message": "Service created successfully.", "data_received": data}
            self.write(json.dumps(response_data))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

    def put(self, service_id):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE services SET name=?, description=? WHERE id=?", (data['name'], data['description'], service_id))
            self.db_conn.commit()
            response_data = {"message": "Service updated successfully.", "data_received": data}
            self.write(json.dumps(response_data))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

    def delete(self, service_id):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM services WHERE id=?", (service_id,))
            self.db_conn.commit()
            response_data = {"message": "Service deleted successfully."}
            self.write(json.dumps(response_data))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

            




def make_app():
    db_conn = sqlite3.connect("example.db")
    db_conn.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)")
    db_conn.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, name TEXT, description TEXT)")
    return tornado.web.Application([
        (r"/", MainHandler),  # Mapping root URL to MainHandler
        (r"/about", AboutHandler, dict(db_conn=db_conn)),
        (r"/contact", ContactHandler, dict(db_conn=db_conn)),
        (r"/services", ServiceHandler, dict(db_conn=db_conn)),
        (r"/services/([0-9]+)", ServiceHandler, dict(db_conn=db_conn)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()






    