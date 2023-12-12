from django.shortcuts import render


def index(request):
    return render(request, "index.html")


# def room(request, id):
#     return render(request, "room.html", {"room_name": id})