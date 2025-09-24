import requests
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
api_key = os.environ.get('NEWSAPI_ORG_KEY')
mongo_uri = os.environ.get("MONGODB_CONNECTIONSTRING")

# Connect to MongoDB
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client.get_database("newsdb")  # You can name this anything
collection = db.get_collection("articles")  # Target collection

# Ping MongoDB to confirm connection
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    exit()

# NewsAPI setup
base_url = 'https://newsapi.org/v2/'
endpoint = 'everything'
queries = ['USD', 'socgen', 'dbs', 'stanchart', 'INR', 'Ship']

# Fetch and store articles
for query in queries:
    print(f"\n🔍 Fetching news for: {query}")
    parameters = {
        'q': query,
        'apiKey': api_key,
    }

    response = requests.get(f"{base_url}{endpoint}", params=parameters)

    if response.status_code == 200:
        data = response.json()
        for article in data.get('articles', []):
            payload = {
                "query": query,
                "source": "NewsAPI.org",
                "title": article.get('title', 'N/A'),
                "description": article.get('description', 'N/A'),
                "url": article.get('url', 'N/A'),
                "publishedTime": article.get('publishedAt', 'N/A'),
                "sourcename": article.get("source", {}).get("name", "N/A"),
                "author": article.get('author', 'N/A')
            }
            try:
                collection.insert_one(payload)
                print(f"📝 Stored article: {payload['title']}")
            except Exception as e:
                print(f"⚠️ Failed to store article: {e}")
    else:
        print(f"❌ Failed to fetch news for {query}: {response.status_code}")
