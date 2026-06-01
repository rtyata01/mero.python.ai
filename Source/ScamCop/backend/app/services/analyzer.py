from app.services.retriever import retrieve_similar_scams
from app.services.llm import generate_explanation

def analyze_message(message:str):
    retrieved=retrieve_similar_scams(message)
    risk='HIGH' if any(w in message.lower() for w in ['urgent','verify','password','bank','click']) else 'LOW'
    return {'risk_level':risk,'explanation':generate_explanation(message,retrieved),'similar_scams':retrieved}
