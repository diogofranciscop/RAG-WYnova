import os
from groq import Groq
from typing import List
from app.embeddings import get_relevant_snippets, extract_and_split_pdf, store_embeddings_in_chroma
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client with the api from the .env file
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Function to retrieve snippets and generate an answer
def generate_rag_answer(query: str, snippets: List[str]) -> str:
    """
    Generate an answer using Groq's generative model with the retrieved snippets as context.
    
    Args:
        query (str): The user's question.
        snippets (List[str]): Relevant snippets retrieved from the database.

    Returns:
        str: A generated answer from the Groq model.
    """
    # Combine snippets into a single context string
    context = " ".join(snippets)

    # Generate response with Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": """
             You are an AI assistant providing concise and accurate answers about the Fundamental Rights in the European Union.
             If a user prompted you with a question not related to fundamental rights, you should answer with "I'm sorry, I can only provide information about the Fundamental Rights in the European Union.".
             """},
            {"role": "user", "content": f"Query: {query}\nContext: {context}"},
        ],
        model="llama-3.3-70b-versatile",
    )

    # Return the generated answer
    return chat_completion.choices[0].message.content

