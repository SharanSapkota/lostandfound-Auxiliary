from api_client import ApiClient

client = ApiClient()
client.login()

items = client.get_all_items()
print("Items:", len(items))

pickups = client.get_all_pickups()
print("Pickups:", len(pickups))