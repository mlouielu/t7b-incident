# -*- coding: utf-8 -*-
import csv
import datetime
import re

from flask import Flask, jsonify
from flask_cors import CORS

import main


LOCATION_REGEX = r"(\d+.\d+(?=K)|\d+(?=K)|\d+.\d+(?=公里)|\d+(?=公里))"
DATA = []


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


def get_incident_metadata(r, location, lat, lng):
    date, time = r[0].split()
    date = date.replace('年', '-').replace('月', '-').replace('日', '')
    dead = int(r[2][2:])
    injury = int(r[3][2:])
    contributing = list(filter(lambda x: x, r[4:]))
    involve_normal_motorcycle = len(list(filter(
        lambda x: x.startswith('普通重型-機車'), contributing))) > 0
    involve_big_motorcycle = len(list(filter(
        lambda x: x.startswith('大型重型'), contributing))) > 0
    involve_light_motorcycle = len(list(filter(
        lambda x: x.startswith('普通輕型-機車'), contributing))) > 0
    involve_car = len(list(filter(
        lambda x: x.startswith('自用-小客車'), contributing))) > 0
    return {
        'description': '\n'.join(r).strip(),
        'date': date,
        'weekend': datetime.datetime.strptime(date, '%Y-%m-%d').weekday() > 4,
        'time': time,
        'minutes': int(time.split(':')[0]) * 60 + int(time.split(':')[1]),
        'dead': dead,
        'injuries': injury,
        'contributing': contributing,
        'involve_big_motorcycle': involve_big_motorcycle,
        'involve_normal_motorcycle': involve_normal_motorcycle,
        'involve_light_motorcycle': involve_light_motorcycle,
        'involve_car': involve_car,
        'location': location,
        'position': {'lat': lat, 'lng': lng}
    }


def load_incident_data():
    reader = csv.reader(open('data.csv'))
    for r in reader:
        location_re = re.search(LOCATION_REGEX, r[1])
        if location_re:
            location = float(location_re.group())
            lat, lng = main.get_random_gps_nearby(
                *main.get_gps_points(location), 10)
            metadata = get_incident_metadata(r, location, lat, lng)
            DATA.append(metadata)


@app.route('/incidents')
def incidents():
    return jsonify({'data': DATA})


if __name__ == '__main__':
    main.init_mileage_sign()
    load_incident_data()
    app.run(debug=True)
