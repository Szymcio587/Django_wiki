from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if name in util.list_entries():
        content = util.get_entry(name)
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{name}' was not found."
        }, status=404)
    
def search(request):
    entries = util.list_entries()
    prompt = request.GET.get('q', '').strip()
    print(f"Entries: {entries}")
    print(f"Prompt: {prompt}")
    if next((entry for entry in entries if entry.lower() == prompt.lower()), None):
        content = util.get_entry(prompt)
        return render(request, "encyclopedia/entry.html", {
            "name": prompt,
            "content": content
        })
    else:
        matches = [s for s in entries if (prompt.lower() in s.lower())]
        return render(request, "encyclopedia/index.html", {
            "entries": matches
        })

def create(request):
    return render(request, "encyclopedia/create.html")

def add(request):
    title = request.GET.get('title', '').strip()
    content = request.GET.get('content', '').strip()