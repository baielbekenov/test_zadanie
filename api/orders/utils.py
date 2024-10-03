from math import radians, sin, cos, sqrt, atan2

from apps.orders.models import Address, Coordinates

# import requests

def get_coordinates_from_address(address):
    # url = "https://nominatim.openstreetmap.org/search"
    # params = {
    #     'q': address,
    #     'format': 'json',
    #     'limit': 1  # Нам нужны только первые координаты
    # }
    # # response = requests.get(url, params=params)
    # print(params)
    # if response.status_code == 200:
    #     data = response.json()
    #     if data:
    #         # Получаем широту и долготу из первого результата
    #         return float(data[0]['lat']), float(data[0]['lon'])
    return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    # Преобразование decimal.Decimal в float
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    # Преобразование градусов в радианы
    R = 6371.0  # Радиус Земли в километрах
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def find_nearest_pickup_point(delivery_address):
    if not delivery_address.coordinates:
        lat, lon = get_coordinates_from_address(f"{delivery_address.streetName}, {delivery_address.cityName}")
        if lat and lon:
            delivery_address.coordinates = Coordinates.objects.create(latitude=lat, longitude=lon)
        else:
            return None

    pickup_points = Address.objects.filter(pickup=True)
    nearest_point = None
    shortest_distance = float('inf')

    for point in pickup_points:
        # Доступ к координатам через связанную модель coordinates
        if point.coordinates and delivery_address.coordinates:
            distance = calculate_distance(
                delivery_address.coordinates.latitude, delivery_address.coordinates.longitude,
                point.coordinates.latitude, point.coordinates.longitude
            )
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_point = point

    return nearest_point