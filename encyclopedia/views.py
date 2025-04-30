from django.shortcuts import render, redirect
from django import forms
import random as rand

from . import util

class Entry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        entries = util.list_entries()

        if any(existing.lower() == title.lower() for existing in entries):
            raise forms.ValidationError(f"An entry with the title '{title}' already exists.")

        return title
    

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
    if request.method == "POST":
        form = Entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "name": title,
                "content": content
            })
    else:
        form = Entry()

    return render(request, "encyclopedia/create.html", {
        "form": form
    })

def edit(request, name):
    if request.method == "POST":
        form = Entry(request.POST)
        title = form.data.get('title')
        content = form.data.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "name": title,
            "content": content
        })
    else:
        content = util.get_entry(name)
        form = Entry(initial={"title": name, "content": content})
        form.fields['title'].widget.attrs['readonly'] = True

        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": name
        })

def random(request):
    names = util.list_entries()
    name = rand.choice(names)
    content = util.get_entry(name)
    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "content": content
    })

