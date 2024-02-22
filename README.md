install packages -

```bash
  pip install tornado
```

Please run the command -

```bash

pip install -r requirements.txt

```

To run the project -
```bash
python test.py 
http://localhost:8888/
```


API Endpoints - 
```bash

http://localhost:8888/ (GET) - Main page
http://localhost:8888/about (GET) - return about information
http://localhost:8888/contact (POST) - send contact information
http://localhost:8888/services (GET, POST) - return all services, create a new service
http://localhost:8888/services/1 (GET, PUT, DELETE) - return service with id 1, update service with id 1, delete service with id 1

```
