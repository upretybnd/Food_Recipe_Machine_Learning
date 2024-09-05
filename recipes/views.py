import csv
import os

import warnings
from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from transformers import GPT2LMHeadModel, GPT2Tokenizer

warnings.filterwarnings("ignore", category=FutureWarning, message=r"`clean_up_tokenization_spaces` was not set")

CSV_FILE_PATH = os.path.join('recipes', 'data', 'recipes.csv')

data_path = 'recipes/data/recipes.csv'  # Adjust to your correct path
recipes_df = pd.read_csv(data_path)


def home(request):
    context = {'recipes': []}

    if request.method == 'POST':
        recipe = request.POST.get('recipe', '')
        min_cooking_time = request.POST.get('min_cooking_time', '')
        max_cooking_time = request.POST.get('max_cooking_time', '')
        preference = request.POST.get('preference', '')
        food_type = request.POST.get('food_type', '')
        min_cooking_time = int(min_cooking_time) if min_cooking_time else None
        max_cooking_time = int(max_cooking_time) if max_cooking_time else None

        with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    cooking_time = int(row['cooking_time'])
                except ValueError:
                    cooking_time = None

                if (not recipe or recipe in row['recipe']) and \
                        (min_cooking_time is None or (
                                cooking_time is not None and cooking_time >= min_cooking_time)) and \
                        (max_cooking_time is None or (
                                cooking_time is not None and cooking_time <= max_cooking_time)) and \
                        (not preference or preference in row['preference']) and \
                        (not food_type or food_type in row['food_type']):
                    context['recipes'].append(row)

    return render(request, 'recipes/home.html', context)


def search(request):
    recipes = []
    search_query = ''

    if request.method == 'POST':
        search_query = request.POST.get('search_query', '').strip().lower()

        with open('recipes/data/recipes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if search_query in row['recipe'].lower() or search_query in row['ingredients'].lower():
                    recipes.append({
                        'recipe': row['recipe'],
                        'cooking_time': row['cooking_time'],
                        'ingredients': row['ingredients'],
                        'preference': row['preference'],
                        'food_type': row['food_type'],
                        'instructions': row['instructions'],
                    })

    return render(request, 'recipes/search.html', {'recipes': recipes})





