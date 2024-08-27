from datetime import date
from django.shortcuts import render
from ipware import get_client_ip
import requests
import json

blog_query = '''
query Publication {
    publication(host: "blog.mountainbean.online") {
        id
        posts(first: 5) {
            edges {
                node {
                    id
                    title
                    brief
                    url
                }
            }
        }
    }
}
'''


def starting_page(request):
    five_latest = None
    ip, isroutable = get_client_ip(request)
    if isroutable or ip == "127.0.0.1":
        print("parsing for blog posts")
        blog_response = requests.post(
            url="https://gql.hashnode.com",
            json={"query": blog_query})
        five_latest = json.loads(
            blog_response.content
        )['data']['publication']['posts']['edges']
    else:
        print(f"Unable to fetch blog posts. {ip=}, {isroutable=}")
    return render(request, "samjd/index.html", {
        "entries": five_latest
    })


# def projects_page(request):
#     return render(request, "samjd/projects.html")
