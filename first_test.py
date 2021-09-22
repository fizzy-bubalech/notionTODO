from pprint import pprint
from notion_client import Client
import os

print(f'test\n{os.getenv("NOTION_TOKEN", "")}\nend test')
notion = Client(auth="secret_WD4B9AglheWESUhhOUFap613gyhDh3MRV3vUTqeEt1Q")

database_id = "3ec47b5d6202464ab9b831a099b4aa35"

'''my_page = notion.pages.retrieve(
    **{
        "page_id": "7713dada-b790-49a3-9fad-adfd-821008e9"
    }
)'''
results = notion.pages.retrieve(
    **{
        "page_id": database_id
    }
)
pprint(results)