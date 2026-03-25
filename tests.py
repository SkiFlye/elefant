import requests

BASE_URL = "https://elefant--matveynikiforof.replit.app"
POST_URL = f"{BASE_URL}/post"

response = requests.get(BASE_URL)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

payload = {
    "session": {
        "new": True,
        "message_id": 1,
        "session_id": "test-001",
        "user_id": "test-user",
        "skill_id": "test"
    },
    "version": "1.0",
    "request": {
        "command": "",
        "original_utterance": "",
        "type": "SimpleUtterance"
    }
}
response = requests.post(POST_URL, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")
session_data = response.json()

payload = {
    "session": {
        "new": False,
        "message_id": session_data['session']['message_id'] + 1,
        "session_id": session_data['session']['session_id'],
        "user_id": session_data['session']['user_id'],
        "skill_id": "test"
    },
    "version": "1.0",
    "request": {
        "command": "не хочу",
        "original_utterance": "не хочу",
        "type": "SimpleUtterance"
    }
}
response = requests.post(POST_URL, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")
session_data = response.json()

payload = {
    "session": {
        "new": False,
        "message_id": session_data['session']['message_id'] + 1,
        "session_id": session_data['session']['session_id'],
        "user_id": session_data['session']['user_id'],
        "skill_id": "test"
    },
    "version": "1.0",
    "request": {
        "command": "куплю",
        "original_utterance": "куплю",
        "type": "SimpleUtterance"
    }
}
response = requests.post(POST_URL, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")