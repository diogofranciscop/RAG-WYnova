import pdfplumber
import re
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

# Initialize the Chroma client and embedding model
client = chromadb.Client()
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="european_rights_sections")

# Step 1: Extract and Split the Document
def extract_and_split_pdf(pdf_path: str, skip_pages: int = 4, output_file: str = "clean_pdf.txt") -> List[str]:
    """
    Extracts text from a PDF, skipping the first `skip_pages` pages (because there is no content there), splits it into cleaned sections,
    adds a colon after "Article <number>", ensures a dot and a space after the title.
    The output file is just to check how the file looked after being split and cleaned.

    Args:
        pdf_path (str): Path to the PDF file.
        skip_pages (int): Number of pages to skip.
        output_file (str): Path to save the cleaned sections.

    Returns:
        List[str]: List of cleaned sections split by "Article <number>".
    """
    def clean_text(text: str) -> str:
        """
        Cleans the extracted text by:
        - Adding a colon after "Article <number>".
        - Adding a comma after the title following "Article <number>".
        - Removing numbers followed by a period (e.g., "1." or "2.").
        - Removing extra whitespace and newlines.

        Args:
            text (str): The raw text to clean.

        Returns:
            str: The cleaned text.
        """
        # Add colon after "Article <number>"
        text = re.sub(r"(?i)(Article\s+\d+)", r"\1:", text)
        # Add a period and a space after the title following "Article <number>"
        text = re.sub(r"(?i)(Article\s+\d+:)\s*(.*?)\n", r"\1 \2. ", text)
        # Remove numbers followed by a period (e.g., "1." or "2.")
        text = re.sub(r"\b\d+\.\s*", "", text)
        # Remove excessive newlines
        text = re.sub(r"\n+", " ", text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Replace multiple spaces with a single space
        text = re.sub(r"\s{2,}", " ", text)
        # Remove text that is entirely in uppercase
        text = re.sub(r"\b[A-Z\s]{2,}\b", "", text)

        return text

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for i in range(skip_pages, len(pdf.pages)):  # Skip specified pages
                try:
                    page_text = pdf.pages[i].extract_text()
                    if page_text:  # Only process if text exists on the page
                        text += page_text + "\n"
                except Exception as e:
                    print(f"Skipping page {i} due to error: {e}")

        # Use regex to split by "Article <number>"
        sections = re.split(r"(?i)(?=Article\s+\d+)", text)
        # Clean each section and remove empty ones
        cleaned_sections = [clean_text(section) for section in sections if section.strip()]
        
        # Save sections to a file for inspection
        with open(output_file, "w", encoding="utf-8") as file:
            for idx, section in enumerate(cleaned_sections, start=1):
                file.write(f"Section {idx}:\n{section}\n{'-'*50}\n")

        print(f"Sections saved to {output_file}")
        return cleaned_sections
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []


# Step 2: Create Embeddings and Store in Chroma
def store_embeddings_in_chroma(sections: List[str]) -> None:
    """
    Store the cleaned and splitted text in Chroma.
    
    Args:
        sections (List[str]): List of document sections.
    """
    
    # Store each section in Chroma
    for idx, section in enumerate(sections):
        embedding = embedding_model.encode(section)  # Generate vector embedding
        collection.add(
            ids=[f"paragraph_{idx + 1}"],  # Unique ID for each paragraph
            documents=[section],  
            embeddings=[embedding.tolist()], 
            metadatas=[{"paragraph_id": idx + 1}]  
        )




def get_relevant_snippets(query: str) -> List[str]:
    """
    Retrieves up to the top 3 relevant paragraphs for a given query.
    
    Args:
        query (str): The user's query.

    Returns:
        List[str]: A list of the most relevant paragraphs (1–3 paragraphs).
    """
    # Compute the embedding for the query
    query_embedding = embedding_model.encode(query).tolist()
    
    # Query for up to 3 paragraphs
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # If no documents are returned, provide a message to the user
    if not results.get("documents"):
        return ["No relevant sections found."]
    
    # results["documents"][0] is a list of up to 3 paragraphs
    return results["documents"][0]

