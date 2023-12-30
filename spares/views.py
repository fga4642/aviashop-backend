from django.shortcuts import render, redirect

from spares.models import *


def index(request):
    query = request.GET.get("query")
    spares = Spare.objects.filter(name__icontains=query).filter(status=1) if query else Spare.objects.filter(status=1)

    context = {
        "search_query": query if query else "",
        "spares": spares
    }

    return render(request, "home_page.html", context)


def spare_detail(request, spare_id):
    context = {
        "spare": Spare.objects.get(id=spare_id)
    }

    return render(request, "order_page.html", context)


def delete(request, spare_id):
    spare = Spare.objects.get(id=spare_id)
    spare.delete()

    return redirect("/")