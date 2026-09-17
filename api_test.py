import requests

params = {
    "userId": 1
}

response = requests.get(
    "https://jsonplaceholder.typicode.com/todos",
    params=params
)

print(response.status_code)

data = response.json()

for todo in data:
    if todo["completed"] == False:
        print(f"{todo['id']}: {todo['title']}")