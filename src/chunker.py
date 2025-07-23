import re
from typing import List

def recursive_character_text_splitter(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Splits text into chunks using a recursive character splitting strategy,
    prioritizing sentence and paragraph boundaries for better semantic coherence. 

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of characters to overlap between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text:
        return []

    # Define separators in order of preference for semantic splitting
    separators = [
        r"(?<=[।?!])\s+",  # Bangla sentence endings
        r"\n\n+",         # Multiple newlines for paragraphs
        r"\n",            # Single newline
        r"\s",            # Whitespace
        ""                # Fallback to character-level splitting
    ]

    # Clean up multiple spaces and newlines before splitting
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\n\s*\n', '\n\n', text) # Normalize multiple newlines

    # Function to recursively split a segment of text
    def _split_recursively(segment: str, current_separators: List[str]) -> List[str]:
        if not current_separators or len(segment) <= chunk_size:
            # Base case: no more separators or segment is small enough
            return [segment]

        separator_pattern = current_separators[0]
        remaining_separators = current_separators[1:]

        # Split the segment by the current separator pattern
        parts = re.split(separator_pattern, segment)
        
        chunks_from_parts = []
        for i, part in enumerate(parts):
            if not part.strip(): # Skip empty parts resulting from splits
                continue

            # Add back the separator if it's not the last part
            if i < len(parts) - 1 and separator_pattern != "":
                if separator_pattern == r"(?<=[।?!])\s+":
                    part += " "
                elif separator_pattern == r"\n\n+":
                    part += "\n\n"
                elif separator_pattern == r"\n":
                    part += "\n"
                elif separator_pattern == r"\s":
                    part += " "


            if len(part) > chunk_size:
                chunks_from_parts.extend(_split_recursively(part, remaining_separators))
            else:
                chunks_from_parts.append(part)
        return chunks_from_parts

    # Perform the initial recursive splitting
    raw_chunks = _split_recursively(text, separators)
    final_chunks = []
    current_chunk_content = ""

    for part in raw_chunks:
        if len(current_chunk_content) + len(part) + (len(final_chunks) > 0 and chunk_overlap > 0) > chunk_size:
            if current_chunk_content.strip():
                final_chunks.append(current_chunk_content.strip())

            # Start a new chunk with overlap from the end of the previous chunk
            if chunk_overlap > 0 and len(current_chunk_content) > chunk_overlap:
                current_chunk_content = current_chunk_content[-chunk_overlap:].strip() + " " + part.strip()
            else:
                current_chunk_content = part.strip()
        else:
            # Add part to current_chunk_content
            if current_chunk_content:
                current_chunk_content += " " # Add a space between parts
            current_chunk_content += part.strip()

    # Add the last chunk if it's not empty
    if current_chunk_content.strip():
        final_chunks.append(current_chunk_content.strip())

    refined_chunks = []
    for chunk in final_chunks:
        while len(chunk) > chunk_size:
            refined_chunks.append(chunk[:chunk_size])
            chunk = chunk[chunk_size - chunk_overlap:] # Apply overlap for the remainder
        if chunk: # Add the remaining part if any
            refined_chunks.append(chunk)

    # Filter out any empty strings that might have resulted from stripping or splitting
    return [c for c in refined_chunks if c.strip()]

if __name__ == '__main__':
    
    long_text = """
    প্রথম পরিচ্ছেদ: বাংলা ভাষার উদ্ভব ও বিকাশ। বাংলা ভাষা ইন্দো-ইউরোপীয় ভাষা পরিবারের সদস্য। এর উদ্ভব হয়েছে প্রাচীন ভারতীয় আর্য ভাষা থেকে। প্রাচীন ভারতীয় আর্য ভাষার তিনটি স্তর রয়েছে: বৈদিক, সংস্কৃত এবং প্রাকৃত। প্রাকৃত ভাষা থেকে মাগধী প্রাকৃতের মাধ্যমে বাংলা ভাষার জন্ম।

    দ্বিতীয় পরিচ্ছেদ: বাংলা সাহিত্যের যুগ বিভাগ। বাংলা সাহিত্যের ইতিহাসকে প্রধানত তিনটি যুগে ভাগ করা হয়: প্রাচীন যুগ, মধ্যযুগ এবং আধুনিক যুগ। প্রাচীন যুগের নিদর্শন হলো চর্যাপদ। এটি দশম থেকে দ্বাদশ শতাব্দীর মধ্যে রচিত। মধ্যযুগ শুরু হয় ত্রয়োদশ শতাব্দী থেকে এবং শেষ হয় আঠারো শতাব্দীর মাঝামাঝি। আধুনিক যুগ উনিশ শতকের শুরু থেকে বর্তমান পর্যন্ত বিস্তৃত।
    """
    
    # Test with different chunk sizes and overlaps
    print("--- Testing Chunker ---")
    
    # Test 1: Small chunks, no overlap
    chunks1 = recursive_character_text_splitter(long_text, chunk_size=50, chunk_overlap=0)
    print(f"\nChunks (size=50, overlap=0): {len(chunks1)} chunks")
    for i, chunk in enumerate(chunks1):
        print(f"Chunk {i+1} (len {len(chunk)}): {chunk[:50]}...")

    # Test 2: Larger chunks, with overlap, specifically targeting the "অনুপম" sentence
    chunks2 = recursive_character_text_splitter(long_text, chunk_size=150, chunk_overlap=30)
    print(f"\nChunks (size=150, overlap=30): {len(chunks2)} chunks")
    for i, chunk in enumerate(chunks2):
        print(f"Chunk {i+1} (len {len(chunk)}): {chunk[:100]}...")
        if "অনুপমের ভাষায় শুম্ভুনাথকে সুপুরুষ বলা হয়েছে" in chunk:
            print(f"  --> Found 'অনুপম' sentence in Chunk {i+1}!")

    # Test 3: Empty text
    chunks3 = recursive_character_text_splitter("", chunk_size=100, chunk_overlap=20)
    print(f"\nChunks (empty text): {len(chunks3)} chunks")

    # Test 4: Text shorter than chunk size
    short_text = "বিয়ের সময় কল্যাণীর প্রকৃত বয়স ১৫ বছর ছিল।"
    chunks4 = recursive_character_text_splitter(short_text, chunk_size=100, chunk_overlap=20)
    print(f"\nChunks (short text): {len(chunks4)} chunks")
    for i, chunk in enumerate(chunks4):
        print(f"Chunk {i+1} (len {len(chunk)}): {chunk}")
