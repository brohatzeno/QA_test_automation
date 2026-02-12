from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import sys
import inspect

# Get the current file's directory and add the parent directory to the path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.utils.qdrant_utils import get_qdrant_client


def create_qdrant_collection():
    '''
    Create the faqs collection in Qdrant with appropriate vector settings
    '''
    try:
        # Initialize Qdrant client using the centralized function
        qdrant_client = get_qdrant_client()

        if qdrant_client is None:
            print("Failed to initialize Qdrant client")
            return None

        # Create the collection with 768-dimensional vectors and Cosine distance
        qdrant_client.recreate_collection(
            collection_name='faqs',
            vectors_config=models.VectorParams(
                size=768,  # Size of the vectors (matching EmbeddingGemma)
                distance=models.Distance.COSINE  # Distance metric
            )
        )

        print('Collection \'faqs\' created successfully in Qdrant!')
        print('Configuration: 768-dimensional vectors with Cosine distance')
        return qdrant_client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        print("Make sure Qdrant is running at the specified host ('172.20.103.184')")
        print("If running locally, you can start Qdrant with Docker:")
        print("  docker run -p 6333:6333 qdrant/qdrant")
        return None


if __name__ == '__main__':
    create_qdrant_collection()
