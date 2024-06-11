import json
import os.path

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Мне лень поэтому нормальной бд не будет. хЫ!
FILENAME = "bd.json"
PRICE = 15


def get_data():
    if not os.path.isfile(FILENAME):
        with open(FILENAME, "w") as f:
            json.dump({"temperature": 0, "humidity": 0, "price": PRICE, "collected": 0, "non_used": 0}, f)

    with open(FILENAME) as f:
        return json.load(f)


def set_data(data):
    with open(FILENAME, "w") as f:
        return json.dump(data, f)


def set_info(request):
    print(request.GET)
    temperature, humidity = request.GET.get("temperature"), request.GET.get("humidity")
    if temperature is not None:
        d = get_data()
        d["temperature"] = temperature
        set_data(d)
    if humidity is not None:
        d = get_data()
        d["humidity"] = humidity
        set_data(d)
    return HttpResponse("OK")


def get_info(request):
    return JsonResponse(get_data())


def get_drop(request):
    d = get_data()
    n = d["non_used"]
    d["non_used"] = n % PRICE
    set_data(d)
    return HttpResponse(n)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def donate_webhook(request):
    if request.method == "POST":
        try:
            data: dict = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse({'error': '0', })
        print(data)
        if data.get("type") == "confirm":
            return HttpResponse("ONoppDhJXM")
        s = int(data.get("sum", 0))
        if s:
            d = get_data()
            d["non_used"] += s
            d["collected"] += s
            set_data(d)
            return HttpResponse("OK")
    return HttpResponseNotFound()


def add(request):
    s = 100
    # if s:
    d = get_data()
    d["non_used"] += s
    d["collected"] += s
    set_data(d)
    return HttpResponse("OK")
