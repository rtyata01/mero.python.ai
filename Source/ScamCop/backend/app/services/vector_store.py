import faiss, numpy as np


class VectorStore:
    def __init__(self,dimension:int):
        self.index=faiss.IndexFlatL2(dimension)
        self.documents=[]

    def add(self,texts,embeddings):
        self.index.add(np.array(embeddings,dtype='float32')) # type: ignore
        self.documents.extend(texts)
        
    def search(self,embedding,k=3):
        _,idx=self.index.search(np.array([embedding],dtype='float32'),k) # type: ignore
        return [self.documents[i] for i in idx[0]]
