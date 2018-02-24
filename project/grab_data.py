from urllib.request import urlopen
import json

def grab(oName,dName):
    url = "http://free.rome2rio.com/api/1.4/json/Search?"
    key = "AjO7qTKZ"
    #add key to url
    url = url + "key=" + key
    #add origin and destination
    url = url + "&oName=" + oName + "&dName=" + dName
    print(url)
    connection = urlopen(url)
    data = connection.read().decode()

    js = json.loads(data)
    print(json.dumps(js,indent=2))

def main():
    grab("bhavnagar","ahmedabad")

if __name__ == "__main__" :
    main()
