# import modules
from flask import *
from json import *
from urllib.request import *

# create a weather class to store city name, current temperature, minimum temperature, maximum temperature, weather conditions, and humidity
# give all properties default values, except for maximum temperature, as it shared a cell with minimum temperature
class Weather:
    def __init__(self, city="City not found", temp="N/A", min="N", max="A", weather="N/A", humidity="N/A", minmax=""):
        self.city = city
        self.temp = temp
        self.min = min
        self.max = max
        self.weather = weather
        self.humidity = humidity

        if self.min != "N":
            # create a string containing the minimum temperature and the maximum temperature
            self.minmax = "%s / %s" % (self.min, self.max)
        else:
            self.minmax = "N/A"

# create flask app
app = Flask("__main__")

# define base url
url = "https://api.openweathermap.org/data/2.5/weather?appid=f0f7ee41fa26c17841ec6551f4d4c3a7&units=imperial&q="

# create a list of cities
cities = ["new york", "los angeles", "delhi", "london", "tokyo", "beijing", "cairo", "paris", "moscow"]

# format for query
def query(s):
    return "+".join(s.split())

# send a request for the city, and get the weather data
def parse(city):

    # format it for url
    city = query(city)

    # create url
    url2 = url + city

    # try to read json data
    try:
        json = urlopen(url2).read().decode()

    # if unable to, create empty weather instance
    except:
        return False

    # parse json data
    data = loads(json)

    # retrieve city
    city = data["name"] + ", " + data["sys"]["country"]
    # retrieve current temperature
    temp = round(data["main"]["temp"])
    # retrieve minimum temperature
    min = round(data["main"]["temp_min"])
    # retrieve maximum temperature
    max = round(data["main"]["temp_max"])
    # retrieve weather conditions
    weather = data["weather"][0]["description"]
    # retrieve humidity
    humidity = data["main"]["humidity"]

    # return weather object
    return Weather(city, temp, min, max, weather, humidity)

# create homepage
@app.route("/")
def home():

    # create a list of weather info for cities
    weatherlst = list(cities)

    # loop through each city
    for i, city in enumerate(weatherlst):

        # if request for city is successful
        if parse(city):
            # create weather object
            weatherlst[i] = parse(city)
        else:
            # create empty weather object
            weatherlst[i] = Weather()

    # push to website
    return render_template("index.html", weatherlst=weatherlst)

# after user entered city
@app.route("/", methods=["POST"])
def home2():

    # add the city to the front of the list
    cities.insert(0, request.form["usr-city"])

    # if the number of cities in the list is greater than 10
    if len(cities) > 10:
        cities.remove(cities[10])

    # create a list of weather info for cities
    weatherlst = list(cities)

    # loop through each city
    for i, city in enumerate(weatherlst):

        # if request for city is successful
        if parse(city):
            # create weather object
            weatherlst[i] = parse(city)
        else:
            # create empty weather object with capitalized city name
            weatherlst[i] = Weather(city=" ".join([w.capitalize() for w in city.split()]))

    # push to website
    return render_template("index.html", weatherlst=weatherlst)

app.run()
