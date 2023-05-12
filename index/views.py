from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import MyForm
from .controller import base_router

import pandas as pd
import json

def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            text_input = form.cleaned_data['text_input']
            request.session['vega_lite_spec'] = text_input
            checkbox = form.cleaned_data['check_box']

            if checkbox:
                csv_upload = form.cleaned_data['csv_upload']
                csv_df = pd.read_csv(csv_upload)
                base_router(text_input=text_input, check_box=checkbox, data=csv_df)
            else:
                base_router(text_input=text_input, check_box=checkbox)
            return redirect('index')
    else:
        form = MyForm()
        vega_lite_spec = request.session.get('vega_lite_spec', None)  # Retrieve the spec from the session
        return render(request, 'index.html', {'form': form, 'vega_lite_spec': vega_lite_spec})