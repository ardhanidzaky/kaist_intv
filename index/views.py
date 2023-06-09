from django.shortcuts import render, redirect
from .forms import MyForm
from .controller import base_router
from .utils import update_data

import pandas as pd
import altair as alt
import altair_viewer
import json

def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            text_input = form.cleaned_data['text_input']
            checkbox = form.cleaned_data['check_box']

            if checkbox:
                csv_upload = form.cleaned_data['csv_upload']
                csv_df = pd.read_csv(csv_upload)
                # chart = alt.Chart.from_json(update_data(text_input, csv_df))
                # chart = altair_viewer.display(chart)
                return base_router(text_input=text_input, check_box=checkbox, data=csv_df)
            else:
                # chart = alt.Chart.from_json(text_input)
                # chart = altair_viewer.display(chart)
                return base_router(text_input=text_input, check_box=checkbox)
        return redirect('index')
    else:
        form = MyForm()
        return render(request, 'index.html', {'form': form})