import csv
import re
import random
import math
import simplekml


LOCATION_REGEX = r"(\d+.\d+(?=K)|\d+(?=K)|\d+.\d+(?=公里)|\d+(?=公里))"
MILEAGE_SIGN = None


def get_mileage_sign():
    mileage_sign = {}
    with open('t7b_mileage_sign.csv') as f:
        reader = csv.reader(f)
        for r in reader:
            km, meter = map(int, r[0].split('K+'))
            kmm = float(f'{km}.{meter}')
            lat = float(r[3])
            lng = float(r[2])
            mileage_sign[kmm] = (lat, lng)
    return mileage_sign


def midpoint(lat1, long1, lat2, long2, percentage):
    lat1 = float(lat1)
    long1 = float(long1)
    lat2 = float(lat2)
    long2 = float(long2)
    return (lat1 + (lat2 - lat1) * percentage,
            long1 + (long2 - long1) * percentage)


def get_gps_points(loc):
    if loc in MILEAGE_SIGN:
        return MILEAGE_SIGN[loc]
    return (0, 0)


def get_random_gps_nearby(lat, lng, radius):
    radius_in_degrees = radius / 111000

    u = random.random()
    v = random.random()
    w = radius_in_degrees * (u ** .5)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    new_x = x / math.cos(math.radians(lat))
    nlat = new_x + lat
    nlng = y + lng
    return float(f'{nlat:.6f}'), float(f'{nlng:.6f}')


def main(path):
    locations = []
    reader = csv.reader(open(path), delimiter=',')
    for r in reader:
        location_re = re.search(LOCATION_REGEX, r[1])
        if location_re:
            locations.append((float(location_re.group()), r))

    locations.sort()
    kml = simplekml.Kml()
    for loc in locations:
        lat, lng = get_random_gps_nearby(*get_gps_points(loc[0]), 10)
        pt = kml.newpoint(name=f'{loc[0]} - {loc[1][0]}', coords=[(lng, lat)])
        pt.description = '\n'.join(loc[1])
        if not loc[1][2].endswith('0'):
            pt.style.labelstyle.color = 'ff0000ff'

    kml.save('t7b_incident.kml')


if __name__ == '__main__':
    MILEAGE_SIGN = get_mileage_sign()
    main('data.csv')
