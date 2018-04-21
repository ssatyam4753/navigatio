from flask import render_template
from urllib.request import urlopen
import json

def apology(message):
    return render_template("apology.html",message=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def grab(oName,dName):
    url = "http://free.rome2rio.com/api/1.4/json/Search?"
    key = "AjO7qTKZ"
    #add key to url
    url = url + "key=" + key
    #add origin and destination
    url = url + "&oName=" + oName + "&dName=" + dName
    print("url:",url)
    connection = urlopen(url)
    data = connection.read().decode()

    js = json.loads(data)
    #print(json.dumps(js,indent=4))
    return js


def listify(data):
    # list of places; each entry is a dictionary that contains shortName, lat and lng
    places = list()
    for place in data["places"]:
        places.append({'shortName':place.get('shortName',None),'longName':place.get('longName',None),'lat':place.get('lat',None),'lng':place.get('lng',None)})

    # list of vehicles each entry is a dictionary; which conains kind and name fields
    vehicles = list()
    for vehicle in data['vehicles']:
        vehicles.append({'kind':vehicle.get('kind',None),'name':vehicle.get('name',None)})

    #list of aircrafts
    aircrafts = list()
    for aircraft in data['aircrafts'] :
        aircrafts.append({'code':aircraft.get('code',None),'manufacturer':aircraft.get('manufacturer',None),'model':aircraft.get('model',None)})

    # list of airlines;each entry is a dictionary which contains code, name and url
    airlines = list()
    for airline in data['airlines']:
        airlines.append({'code':airline.get('code',None),'name':airline.get('name',None),'url':airline.get('url',None)})


    #list to store agencies; each entry contains a dictionary containing name and url field
    agencies = list()
    for agency in data["agencies"]:
        agencies.append({'name':agency.get('name',None),'url': agency.get('url',None)})

    routes = list()
    for route in data["routes"]:
        routes.append({'arrPlace':route.get('arrPlace',None),'depPlace':route.get('depPlace',None),'distance':route.get('distance',None),'name':route.get('name',None),
        'totalDuration':route.get('totalDuration',0),'price':route['indicativePrices'][0]['price'],'currency':route['indicativePrices'][0]['currency'],'segments':route.get('segments',None)})

    dct = {'places':places,'vehicles':vehicles,'aircrafts':aircrafts,'airlines':airlines,'agencies':agencies,'routes':routes}
    return dct

def to_paths(data):
    path = list()
    temp = list()
    for route in data["routes"]:
        for segment in route["segments"] :
            temp.append(str(segment.get('path','')))
        #print(temp)
        path.append(temp[:])
        temp[:] = []
    for p in path:
        if '' in p:
            p.remove('')
        #for j in p:
        #    for i in j:
        #        i.replace('\\','\\\\')
        #print(p)
        #print("\n\n")
    return path



def main():
    data = grab("bhavnagar","pune")
    to_paths(data)






if __name__ == "__main__" :
    main()
