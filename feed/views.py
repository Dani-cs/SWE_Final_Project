from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    sample_lists = [
        {
            'author': 'alex_j',
            'title': 'Top 5 Anime of All Time',
            'items': ['Fullmetal Alchemist: Brotherhood', 'Steins;Gate', 'Hunter x Hunter', 'Naruto', 'One Piece'],
            'likes': 142,
            'comments': 23,
        },
        {
            'author': 'maria_v',
            'title': 'Best Restaurants in McAllen',
            'items': ['Tacos El Rancho', 'Denny\'s on 10th', 'Las Fuentes', 'Cheddar\'s', 'Whataburger'],
            'likes': 89,
            'comments': 11,
        },
        {
            'author': 'jdoe99',
            'title': 'Must-Play Video Games 2024',
            'items': ['Elden Ring', 'Baldur\'s Gate 3', 'Hades II', 'Helldivers 2', 'Palworld'],
            'likes': 201,
            'comments': 45,
        },
    ]
    return render(request, 'feed/home.html', {'lists': sample_lists})