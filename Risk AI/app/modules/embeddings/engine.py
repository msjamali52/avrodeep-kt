from sentence_transformers import SentenceTransformer

class stella_v5_400m():
    def __init__(self):
        self.model = SentenceTransformer(f'dunzhang/stella_en_400M_v5', trust_remote_code=True)
        self.model.save(f"embed_models\stella_en_400m_v5")

    def embed_query(self, query):
        return self.model.encode(query).tolist()
    
    def embed_documents(self, documents):
        document_embedding = [self.embed_query(document) for document in documents]
        return document_embedding
    
class gte_large_1p5():
    def __init__(self):
        self.model = SentenceTransformer(f"Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)
        self.model.save(f"embed_models\gte-large")

    def embed_query(self, query):
        return self.model.encode(query).tolist()
    
    def embed_documents(self, documents):
        document_embedding = [self.embed_query(document) for document in documents]
        return document_embedding