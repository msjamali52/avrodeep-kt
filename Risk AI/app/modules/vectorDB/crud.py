from app.modules.embeddings.engine import gte_large_1p5
import shutil

import chromadb
import os

class vectorDB_crud():
    def __init__(self, embed_model = gte_large_1p5()):
        self.client = chromadb.PersistentClient(path=f"chromadb/")
        self.embed_model = embed_model

    def add_data(self, collection_name:str, documents: list[dict]):
        collection = self.client.get_or_create_collection(collection_name, metadata={"hnsw:space": "cosine"})
        info = {"ids_added": [], "ids_already_existed": []}
        for doc in documents:
            doc_id = [str(doc["id"])]
            query = doc["name"]

            id_list = collection.get(ids=doc_id)
            if len(id_list['documents']) == 0:
                embeddings = [self.embed_model.embed_query(query=query)]
            
                collection.add(
                    embeddings = embeddings,
                    documents = query,
                    ids = doc_id
                )
                info["ids_added"].append(doc_id[0])
            else:
                info["ids_already_existed"].append(doc_id[0])

        return info

    def get_query_similarity(self,collection_name:str, query: str, result_limit:int = 5, threshold:int = None):
        
        query_embedding = self.embed_model.embed_query(query)

        collection = self.client.get_collection(name=collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=result_limit
        )

        if threshold is not None:
            distances = results['distances'][0]
            ids = results['ids'][0]
            documents = results['documents'][0]

            filtered_result = {"ids": [[]], "documents": [[]], "distances": [[]]}
            for i in range(len(distances)):
                if distances[i] < threshold:
                    filtered_result["ids"][0].append(ids[i])
                    filtered_result["documents"][0].append(documents[i])
                    filtered_result["distances"][0].append(distances[i])
                
            results = filtered_result
        return results
    
    def delete_collection(self, collection_name:str):
        try:
            collection = self.client.get_collection(name=collection_name)
            collection.delete(ids=collection.get()["ids"])

            folder_path = f"db/{collection.id}"
            self.client.delete_collection(name=collection_name)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

            return {"success": True, "response": f"{collection_name} deleted. Folder path: {folder_path} Removed."}
        except Exception as e:
            print("Delete Exception Occured: ", e)

    def see_collections(self, target_id=None):
        result = []
        collections = self.client.list_collections()

        for collection in collections:
            if target_id is None or str(collection.id) == target_id:
                collection_obj = self.client.get_collection(collection.name)
                collection_data = {"collection_id":collection.id, "collection_name": collection.name, "collection_details": collection_obj.get()}

                result.append(collection_data)
                               
        return result

