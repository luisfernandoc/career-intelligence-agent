import chromadb
from chromadb.utils import embedding_functions
from app.services.llm_service import LLMService


class MemoryService:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name="career_memory",
            embedding_function=self.embedding_function,
        )

        self.llm_service = LLMService()

    def upload_document(
        self,
        title: str,
        content: str,
        document_type: str,
    ):
        document_id = title.lower().replace(" ", "_")

        self.collection.add(
            ids=[document_id],
            documents=[content],
            metadatas=[
                {
                    "title": title,
                    "document_type": document_type,
                }
            ],
        )

        return {
            "document_id": document_id,
            "title": title,
            "document_type": document_type,
            "status": "stored",
        }

    def upload_file(
        self,
        file_name: str,
        content: bytes,
        document_type: str = "general",
    ):
        allowed_extensions = [
            ".txt",
            ".md",
            ".py",
            ".js",
            ".ts",
            ".json",
            ".csv",
        ]

        if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_name}",
            }

        try:
            text_content = content.decode("utf-8")
        except UnicodeDecodeError:
            text_content = content.decode("latin-1")

        document_id = file_name.lower().replace(" ", "_")

        self.collection.add(
            ids=[document_id],
            documents=[text_content],
            metadatas=[
                {
                    "title": file_name,
                    "document_type": document_type,
                    "source": "file_upload",
                }
            ],
        )

        return {
            "document_id": document_id,
            "file_name": file_name,
            "document_type": document_type,
            "characters_stored": len(text_content),
            "status": "stored",
        }

    def ask_career_memory(self, question: str):
        results = self.collection.query(
            query_texts=[question],
            n_results=3,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        context = "\n\n".join(documents)

        system_prompt = """
You are a career memory assistant.
Answer using only the provided career memory context.
If the answer is not found in the context, say that there is not enough information.
"""

        user_prompt = f"""
Question:
{question}

Career memory context:
{context}

Answer clearly and cite the relevant document titles when possible.
"""

        answer = self.llm_service.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
        )

        sources = [
            {
                "title": metadata.get("title"),
                "document_type": metadata.get("document_type"),
            }
            for metadata in metadatas
        ]

        return {
            "answer": answer,
            "sources": sources,
        }
