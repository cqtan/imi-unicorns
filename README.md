# ChasingUnicornsAndVampires

## Installation

This application contains 2 parts, one is the Flask server which will serve the http calls and the angular application.
The second part is the Angular 2 (Version 6 at this point) which will provide the frontend for this project.
To get the Application running follow the steps belowe.

### Download the Repository

```
git clone git@github.com:CouchCat/imi-unicorns.git
```

checkout backend (temporary)
```
git checkout backend
```

and go into the Application Folder

```
cd imi-unicorns
```

### Angular 2 (Web application)

Go into the Application Folder:

```
cd WebApp 
```

and install all dependencies

```
npm install
```

for development run:
```
npm start
```

for test purposes build the application once with:
```
ng build --prod
```

### Python Flask (Server)

Next go back into the root directory 
```
cd ..
```

and install the dependencies of python with:
```
pip install -r requirements.txt
```

export the flask application to a enviroment variable:
```
export FLASK_APP=app/__init__.py
```

and run the server with:
```
flask run
```

the server will be available on:
```
localhost:5000
```
