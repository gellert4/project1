"""
Query engine for RAG.

Retrieves relevant document chunks and generates an answer that is based
strictly on the uploaded evidence.
"""

import logging
from pathlib import Path

from config import Config

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


logger = logging.getLogger(__name__)

INSUFFICIENT_EVIDENCE = "I don't have enough evidence to answer that."


class QueryEngine:
    """RAG query engine using semantic retrieval and Gemini."""

    def __init__(self, vector_store):
        """
        Initialize the query engine.

        Args:
            vector_store: FAISS vector store containing document embeddings.
        """
        self.vector_store = vector_store
        self.client = None
        self.llm_available = False

        # Try these models in order.
        # If one is unavailable for the API key, the next one is attempted.
        self.model_names = [
            "gemini-flash-latest",
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]

        if not Config.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY is missing.")
            return

        if genai is None:
            logger.warning(
                "google-genai is not installed. "
                "Run: pip install -U google-genai"
            )
            return

        try:
            self.client = genai.Client(
                api_key=Config.GOOGLE_API_KEY
            )
            self.llm_available = True
            logger.info("Gemini client initialized successfully.")

        except Exception:
            logger.exception("Failed to initialize Gemini client.")
            self.client = None
            self.llm_available = False

    def query(self, question, top_k=4):
        """
        Answer a question using retrieved document evidence.

        Args:
            question: User question.
            top_k: Number of relevant chunks to retrieve.

        Returns:
            Dictionary containing answer, sources and confidence.
        """
        question = (question or "").strip()

        if not question:
            return {
                "answer": "Please enter a question.",
                "sources": [],
                "confidence": 0.0,
            }

        if not self.vector_store:
            return {
                "answer": "I don't have any case files loaded yet.",
                "sources": [],
                "confidence": 0.0,
            }

        try:
            results = self.vector_store.similarity_search(
                question,
                k=top_k,
            )

            if not results:
                return {
                    "answer": INSUFFICIENT_EVIDENCE,
                    "sources": [],
                    "confidence": 0.0,
                }

            context = self._prepare_context(results)
            answer = self._generate_answer(question, context)

            sources = sorted(
                {
                    self._clean_source_name(
                        document.metadata.get(
                            "source",
                            "Unknown",
                        )
                    )
                    for document in results
                }
            )

            error_messages = (
                "The language model is currently unavailable.",
                "Gemini could not generate an answer.",
            )

            if (
                answer == INSUFFICIENT_EVIDENCE
                or answer.startswith(error_messages)
            ):
                confidence = 0.0
            else:
                confidence = 0.85

            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
            }

        except Exception as error:
            logger.exception("Error while processing query.")

            return {
                "answer": f"Query processing failed: {error}",
                "sources": [],
                "confidence": 0.0,
            }

    def _prepare_context(self, documents):
        """Create structured evidence context for the LLM."""
        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            source = self._clean_source_name(
                document.metadata.get(
                    "source",
                    "Unknown",
                )
            )

            page = document.metadata.get("page")
            page_text = ""

            if isinstance(page, int):
                page_text = f", page {page + 1}"

            context_parts.append(
                f"[Evidence {index} | "
                f"{source}{page_text}]\n"
                f"{document.page_content.strip()}"
            )

        return "\n\n".join(context_parts)

    def _generate_answer(self, question, context):
        """
        Generate a concise answer using only retrieved evidence.
        """
        if (
            not self.llm_available
            or self.client is None
        ):
            logger.error(
                "Gemini is unavailable. "
                "Check the API key and google-genai package."
            )

            return (
                "The language model is currently unavailable. "
                "Check the backend terminal for details."
            )

        prompt = f"""
You are Sherlock, an evidence analysis assistant.

Answer the user's question using only the evidence supplied below.

Rules:
1. Do not use outside knowledge.
2. Do not guess or invent information.
3. Ignore evidence unrelated to the question.
4. Give a direct and natural answer.
5. Prefer one to three concise sentences.
6. Do not repeat raw evidence chunks.
7. Do not include a separate sources section.
8. If the evidence does not directly answer the question, respond exactly:
"{INSUFFICIENT_EVIDENCE}"

Question:
{question}

Evidence:
{context}

Answer:
""".strip()

        last_error = None

        for model_name in self.model_names:
            try:
                logger.info(
                    "Trying Gemini model: %s",
                    model_name,
                )

                response = (
                    self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.0,
                            max_output_tokens=250,
                        ),
                    )
                )

                answer = (
                    response.text or ""
                ).strip()

                if not answer:
                    logger.warning(
                        "Gemini model %s returned "
                        "an empty answer.",
                        model_name,
                    )
                    continue

                logger.info(
                    "Gemini response generated "
                    "with model: %s",
                    model_name,
                )

                if self._contains_uncertain_language(
                    answer
                ):
                    return INSUFFICIENT_EVIDENCE

                return answer

            except Exception as error:
                last_error = error

                logger.warning(
                    "Gemini model %s failed: %s",
                    model_name,
                    error,
                )

        logger.error(
            "All configured Gemini models failed.",
            exc_info=last_error,
        )

        return (
            "Gemini could not generate an answer. "
            "Check the backend terminal for the API error."
        )

    @staticmethod
    def _clean_source_name(source):
        """
        Return only the filename instead of its full path.
        """
        source = str(source).replace("\\", "/")
        return Path(source).name

    @staticmethod
    def _contains_uncertain_language(answer):
        """
        Reject answers that appear clearly speculative.
        """
        indicators = [
            "presumably",
            "it is possible that",
            "it's possible that",
            "could have",
            "might have",
            "probably",
            "perhaps",
            "unclear from the evidence",
        ]

        lower_answer = answer.lower()

        return any(
            indicator in lower_answer
            for indicator in indicators
        )