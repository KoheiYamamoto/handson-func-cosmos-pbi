import os
import logging
import azure.functions as func
from azure.cosmos import CosmosClient

endpoint = os.environ['CosmosDBEndpoint']
key = os.environ['CosmosDBKey']

def main(documents: func.DocumentList) -> str:
    if documents:
        # 格納先のデータベースのインスタンス作成
        client = CosmosClient(endpoint, key)
        database = client.get_database_client("Refined")
        container = database.get_container_client('Items')
        for document in documents:
            # Inferences の中身取得
            inferences = document.get('Inferences')
            if inferences:
                # Inferences の中身をリストで取得
                inference_results = inferences['inferenceResults']  
                counter = 0
                # リストの中身ごとに取り出して、Cosmos DB に格納
                for result in inference_results:
                    item = {
                        'id': document.get('id') + '-' + str(counter),
                        'DeviceID': document.get('DeviceID'),
                        'ModelID': document.get('ModelID'),
                        'Class': 'Banana' if result.get('C') == 1 else 'Apple', # 1: Banana, 0: Apple
                        'P': result.get('P'),
                        'Left': result.get('Left'),
                        'Top': result.get('Top'),
                        'Right': result.get('Right'),
                        'Bottom': result.get('Bottom')
                    }
                    container.create_item(body=item)
                    logging.info('Inference results inserted into Refined')
                    counter += 1