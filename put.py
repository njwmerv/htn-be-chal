import requests

url = "http://127.0.0.1:5000/users/123"
data = {'company': 'Apple',
        'name': 'Hisa Lo',
        'skills': [
            {'skill': 'Prolog', 'rating': '3'},
            {'skill': 'Flask', 'rating': '2'}
        ],
        'events': [
            {'event': 'Coding Workshop', 'rating': 5},
            {'event': 'Boring Talk'}
        ]
}
response = requests.put(url, json=data)

url = "http://127.0.0.1:5000/users/124"
data = {'name': 'Johnathan Smitherston',
        'phone': '123-456-987',
        'skills': [
            {'skill': 'Godot', 'rating': '10'},
            {'skill': 'Typing', 'rating': '3'}
        ],
        'events': [
            {'event': 'Coding Workshop', 'rating': 10},
            {'event': 'Boring Talk', 'rating': 2},
            {'event': 'Cool Talk', 'rating': 7}
        ]
}
response = requests.put(url, json=data)