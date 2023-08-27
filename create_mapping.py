from elasticsearch import Elasticsearch
import time

# Connect to Elasticsearch
# es = Elasticsearch("http://78.110.122.137:9200")
es = Elasticsearch('http://localhost:9200')

# Ensure Elasticsearch is up
while True:
    try:
        if es.ping():
            print("Connected to Elasticsearch.")
            break
    except Exception as e:
        print(f"Waiting for Elasticsearch... Error: {e}")
        time.sleep(5)
settings = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0,
        "similarity": {
            "title_fa_similarity": {
                "type": "BM25",
                "k1": 1.2,
                "b": 0.0
            },
            "category_similarity": {
                "type": "BM25",
                "k1": 1.2,
                "b": 1.0
            }
        },
        "analysis": {
            "char_filter": {
                "zero_width_spaces": {
                    "type": "mapping",
                    "mappings": ["\\u200C => \\u0020"]
                }
            },
            "filter": {
                "persian_stop": {
                    "type": "stop",
                    "stopwords": "_persian_"
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "custom_stop":{
                    "type":"stop",
                    "stopwords_path":"/usr/share/elasticsearch/config/stop_words.txt"
                },
                "synonym_words":{
                    "type": "synonym",
                    "synonyms_path": "/usr/share/elasticsearch/config/synonyms/synonym.txt"
                }
            },
            "analyzer": {
                "persian_analyzer": {
                    "tokenizer": "standard",
                    "char_filter": ["zero_width_spaces"],
                    "filter": [
                        "lowercase",
                        "decimal_digit",
                        "arabic_normalization",
                        "persian_normalization",
                        "persian_stop",
                        "custom_stop",
                        "synonym_words",
                        "unique"
                    ]
                },
                "english_analyzer":{
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "unique",
                        "synonym_words",
                    ]   

                }
            }
        }
    },
    "mappings": {
        "dynamic": False,
        "properties": {
            "id" : { "type": "integer" },
            "title_fa" : { 
                "type": "text",
                "analyzer": "persian_analyzer",
                "similarity": "title_fa_similarity"
                },
            "title_en" : {"type": "text", "analyzer": "english_analyzer" },
            "category1" : {
                "type": "text",
                "analyzer": "persian_analyzer",
                "similarity": "category_similarity"
                },
            "brand":{"type":"text", "analyzer":"persian_analyzer"},
            "website" : { "enabled": "false" },
            "website_url" :{ "enabled": "false" },
            "website_id": { "type": "integer" },
            "is_fake": { "type": "boolean"},
            "home_show": { "type": "boolean"},
            "url" : { "enabled": "false"},
            "write_date" : {"enabled": "false"},
            "is_active" : { "type": "boolean"},
            "image" : { "enabled": "false" },
            "discount_price" : { "type": "float" },
            "selling_price" : { "type": "float" },
            "rrp_price" : { "type": "float" },
            "discount_percent" : { "type": "float" },
        }
    }
}

es.indices.create(index="blackeveryday_product", body=settings, ignore=400)
# es.indices.create(index="test", body=settings, ignore=400)
