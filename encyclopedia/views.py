from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse  
from . import util
from markdown2 import Markdown
from random import choice

markdowner = Markdown()
class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    markdown = forms.CharField(widget=forms.Textarea, label="Markdown")

class EditEntryForm(forms.Form):
    new_markdown = forms.CharField(widget=forms.Textarea, label="New Markdown")


def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            entries = []
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))
                elif title.lower() in entry.lower():
                    entries.append(entry)
            return render(request, "encyclopedia/results.html", {
                "entries" : entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdowner.convert(util.get_entry(title)),
            "title" : title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "massage" : "Requested page was not found"
        })


def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            markdown = form.cleaned_data['markdown']
            if title not in util.list_entries():
                util.save_entry(title, markdown)
                return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/error.html", {
                    "massage" : "An encyclopedia entry with the provided title already exists"
                })
        
    return render(request, "encyclopedia/create.html")


def random(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))


def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_markdown = form.cleaned_data['new_markdown']
            util.save_entry(title, new_markdown)
            return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))

    return render(request, "encyclopedia/edit.html", {
            "entry" : util.get_entry(title),
            "title" : title
        })