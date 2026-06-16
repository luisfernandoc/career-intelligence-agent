import chromadb
from chromadb.utils import embedding_functions
import uuid
from app.services.llm_service import LLMService
from app.db.models import Document


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
        db,
        title: str,
        content: str,
        document_type: str,
    ):
        chroma_id = str(uuid.uuid4())

        self.collection.add(
            ids=[chroma_id],
            documents=[content],
            metadatas=[
                {
                    "title": title,
                    "document_type": document_type,
                }
            ],
        )

        document = self.save_document_metadata(
            db=db,
            title=title,
            document_type=document_type,
            source="manual",
            chroma_id=chroma_id,
        )

        return {
            "id": document.id,
            "chroma_id": chroma_id,
            "title": document.title,
            "document_type": document.document_type,
            "source": document.source,
            "status": "stored",
        }

    def upload_file(
        self,
        db,
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

        chroma_id = str(uuid.uuid4())

        self.collection.add(
            ids=[chroma_id],
            documents=[text_content],
            metadatas=[
                {
                    "title": file_name,
                    "document_type": document_type,
                    "source": "file_upload",
                }
            ],
        )

        document = self.save_document_metadata(
            db=db,
            title=file_name,
            document_type=document_type,
            source="file_upload",
            chroma_id=chroma_id,
        )

        return {
            "id": document.id,
            "chroma_id": chroma_id,
            "file_name": file_name,
            "document_type": document.document_type,
            "source": document.source,
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

    def get_document_by_id(
        self,
        db,
        document_id: int,
    ):
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return {
                "status": "error",
                "message": "Document not found",
            }

        return {
            "id": document.id,
            "title": document.title,
            "document_type": document.document_type,
            "source": document.source,
            "chroma_id": document.chroma_id,
            "created_at": document.created_at,
        }

    def save_document_metadata(
        self,
        db,
        title,
        document_type,
        source,
        chroma_id,
    ):
        document = Document(
            title=title,
            document_type=document_type,
            source=source,
            chroma_id=chroma_id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def delete_document(
        self,
        db,
        document_id: int,
    ):
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return {
                "status": "error",
                "message": "Document not found",
            }

        try:
            self.collection.delete(
                ids=[document.chroma_id]
            )
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete from Chroma: {str(e)}",
            }

        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "title": document.title,
        }
