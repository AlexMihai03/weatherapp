import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging

def fetch_data():
    api_token = 'c789df7980c99453'

    url = 'http://api.wunderground.com/api/' + api_token + '/conditions/q/CA/San_Francisco.json'
    r = requests.get(url).json()
    data = r['current_observation']
    location = data['observation_location']['full']
    weather = data['weather']
    wind_str = data['wind_string']
    temp = data['temp_c']
    humidity = data['relative_humidity']
    precip = data['precip_today_string']
    icon_url = data['icon_url']
    observation_time = data['observation_time']

    try:
        conn = psycopg2.connect(dbname='weather', user='postgres', host='localhost', password='Awesomefifa13')
    except:
        print(datetime.now(), "Unable to connect to database")
        logging.exception("Unable to connect to database")
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("INSERT INTO station_reading(location, weather, wind_str, temp, humidity, precip, icon_url, observation_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (location, weather, wind_str, temp, humidity, precip, icon_url, observation_time))

    conn.commit()
    cur.close()
    conn.close()

    print("Data written", datetime.now())

fetch_data()