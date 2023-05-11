from django.shortcuts import render, redirect
from .forms import MyForm
from .controller import base_router

import pandas as pd

def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            text_input = form.cleaned_data['text_input']
            checkbox = form.cleaned_data['check_box']

            if checkbox:
                csv_upload = form.cleaned_data['csv_upload']
                base_router(text_input=text_input, check_box=checkbox, data=pd.read_csv(csv_upload))
                pd.read_csv(csv_upload).to_excel('uploaded.xlsx')

            base_router(text_input=text_input, check_box=checkbox)
            return redirect('index')
    else:
        form = MyForm()
    return render(request, 'index.html', {'form': form})