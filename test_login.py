from api_client import ApiClient

client = ApiClient()
client.login()

print("Login successful")
print(client.token)