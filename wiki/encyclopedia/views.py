from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .util import list_entries, get_entry, save_entry
from markdown2 import markdown
from django.views.generic import View
from django.urls import reverse
import random

def index(request):
    entries = list_entries()
    return render(request, 'encyclopedia/index.html', {'entries': entries})

def entry(request, title):
    content = get_entry(title)
    if content is None:
        raise Http404("Page not found.")
    html_content = markdown(content)
    return render(request, 'encyclopedia/entry.html', {'title': title, 'content': html_content})

def search(request):
    query = request.GET.get('query')
    if not query:  
        return render(request, 'encyclopedia/no_results.html', {'query': ''})

    try:
        entries = list_entries()  
    except Exception as e:

        print(e)  
        return render(request, 'encyclopedia/no_results.html', {'query': query})

    # 过滤出包含查询字符串的条目，确保列表中的每个元素都是字符串
    filtered_entries = [entry for entry in entries if isinstance(entry, str) and query.lower() in entry.lower()]
    
    if filtered_entries:  
        return render(request, 'encyclopedia/search_results.html', {'entries': filtered_entries, 'query': query})
    else:  
        return render(request, 'encyclopedia/no_results.html', {'query': query})

def new_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            save_entry(title, content)
            return redirect('entry', title=title)
    return render(request, 'encyclopedia/new_entry.html')

def edit_entry(request, title):
    content = get_entry(title)
    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            save_entry(title, new_content)
            return redirect('entry', title=title)
    return render(request, 'encyclopedia/edit_entry.html', {'title': title, 'content': content})

def random_entry(request):
    entries = list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry', title=random_entry)
    raise Http404("No entries available.")