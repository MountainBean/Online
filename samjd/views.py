from datetime import date
from django.shortcuts import render, get_object_or_404
from feedparser import parse


def starting_page(request):
    print("parsing for blog posts")
    feed = parse("https://blog.mountainbean.online/rss.xml")
    print(f"{feed.status=}")
    top_five = feed.entries[:5]
    return render(request, "samjd/index.html", {
        "entries": top_five
    })
