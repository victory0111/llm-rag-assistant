from enum import Enum


class PromptTask(str, Enum):

    CHAT = "chat"

    RAG = "rag"

    SUMMARY = "summary"

    REVIEW = "review"

    TRANSLATION = "translation"

    REPORT = "report"