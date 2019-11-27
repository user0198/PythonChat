import requests

print('Input username:')
username = input()
print('Input password:  #(must contain 4-16 cahracters, at least one number and one capitalize)')
password = input()

while True:
    text = input()
    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={'username': username, 'password': password, 'text': text}
    )

    if response.status_code == 200:
        print('Message sent')
        print()
