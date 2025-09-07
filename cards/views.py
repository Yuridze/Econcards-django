
import random
from typing import List, Tuple
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import UploadForm, CardForm
from .utils import read_cards, parse_lines, overwrite_cards, append_card

def home_redirect(request):
    return redirect('cards:cards_list')

def cards_list(request):
    pairs = read_cards(settings.CARDS_FILE)
    return render(request, 'cards/list.html', {'pairs': pairs})

def quiz(request):
    pairs: List[Tuple[str, str]] = read_cards(settings.CARDS_FILE)
    if not pairs:
        messages.info(request, 'Сначала загрузите или добавьте карточки.')
        return redirect('cards:upload_cards')

    # State in session: current index and show flag
    if 'next' in request.GET or 'reset' in request.GET:
        request.session.pop('quiz_idx', None)
        request.session.pop('show', None)

    idx = request.session.get('quiz_idx')
    if idx is None or idx >= len(pairs):
        idx = random.randrange(len(pairs))
        request.session['quiz_idx'] = idx
        request.session['show'] = False

    show = request.session.get('show', False)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'show':
            show = True
            request.session['show'] = True
        elif action == 'next':
            idx = random.randrange(len(pairs))
            request.session['quiz_idx'] = idx
            show = False
            request.session['show'] = False

    question, answer = pairs[idx]
    context = {'question': question, 'answer': answer, 'show': show, 'count': len(pairs)}
    return render(request, 'cards/quiz.html', context)

def upload_cards(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES['file'].read().decode('utf-8', errors='ignore')
            pairs = parse_lines(content)
            if not pairs:
                form.add_error('file', 'Файл не содержит корректных карточек.')
            else:
                overwrite_cards(settings.CARDS_FILE, pairs)
                messages.success(request, f'Загружено карточек: {len(pairs)}')
                return redirect('cards:cards_list')
    else:
        form = UploadForm()
    return render(request, 'cards/upload.html', {'form': form})

def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['question']
            a = form.cleaned_data['answer']
            append_card(settings.CARDS_FILE, q, a)
            messages.success(request, 'Карточка добавлена.')
            return redirect('cards:add_card')
    else:
        form = CardForm()
    return render(request, 'cards/add.html', {'form': form})
