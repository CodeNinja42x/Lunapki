import base64

with open('bot_log.log', 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')

print(encoded_string)