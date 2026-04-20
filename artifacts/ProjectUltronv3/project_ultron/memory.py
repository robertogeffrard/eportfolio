import chromadb
from datetime import datetime

class Memory:
    def __init__(self, persist_dir="./memory"):
        self.client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory=persist_dir
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="ultron_memory"
        )

    def add(self, text):
        try:
            self.collection.add(
                documents=[text],
                ids=[str(datetime.now().timestamp())]
        )
        except Exception as e:
            print(f"[Memory Add Error]: {e}")

    def search(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results["documents"][0] if results["documents"] else []