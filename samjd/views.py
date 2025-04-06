from datetime import date
from django.shortcuts import render, get_object_or_404
from ipware import get_client_ip
from .models import Project, Cert
import json
import requests

class PostEntry:

    id = 0
    def __init__(self) -> None:
        self.id = PostEntry.id
        PostEntry.id = PostEntry.id + 1
        self.title = f"New Post {self.id}", 
        self.brief = "lorem ipsum..."
        self.url = "#"


blog_query = '''
query Publication {
    publication(host: "blog.samjdrew.com") {
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


def projects_page(request):
    active_projects = Project.objects.filter(status="active").order_by("-published_date")
    old_projects = Project.objects.filter(status="inactive").order_by("-published_date")

    return render(request, "samjd/projects.html", {
        "active_projects": active_projects,
        "old_projects": old_projects
    })


def project_detail(request, slug):
    target_project = get_object_or_404(Project, slug=slug)
    index_body = ""
    if target_project.title == "Experimental OpenGL":
        index_html = requests.get("https://webgl.samjdrew.com/").text
        index_body = index_html[index_html.find("<body>")+6:index_html.find("</body>")]
    elif target_project.title == "LearnOpenGL.com Examples":
        index_html = requests.get("https://webgl.samjdrew.com/webdata/demos_index").text
        index_body = index_html[index_html.find("<body>")+6:index_html.find("</body>")]

    return render(request, "samjd/project_detail.html", {
        "project": target_project,
        "data": index_body
    })

def certs(request):
    
    return render(request, "samjd/certs.html", {
        "certs": Cert.objects.all(),
    })

