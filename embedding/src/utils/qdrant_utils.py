# qdrant_utils.py
from qdrant_client import QdrantClient

def get_qdrant_client():
    """
    Initialize and return Qdrant client
    """
    # Use hardcoded host and port values
    qdrant_client = QdrantClient(
        host='172.20.103.184',
        port=6333
    )

    return qdrant_client
