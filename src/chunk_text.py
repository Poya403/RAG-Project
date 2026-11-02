
import re

def chunk_text(text, max_chunk_size=2000):
    chunks = []

    sections = re.split(r'(?m)(?=^پیوست شماره\s*\d+)', text)

    for section in sections:

        articles = re.split(
            r'(?m)(?=^ماده\s*[.٫]?\s*\d+\b)',
            section
        )

        for article in articles:
            article = article.strip()

            if not article:
                continue

            if len(article) <= max_chunk_size:
                chunks.append(article)
                continue

            title = article.split("\n")[0]

            sub_chunks = re.split(
                r'(?m)(?=^تبصره?\s*:?\s*\d+)',
                article
            )

            for index, sub_chunk in enumerate(sub_chunks):
                sub_chunk = sub_chunk.strip()

                if not sub_chunk:
                    continue

                if index > 0:
                    sub_chunk = title + "\n" + sub_chunk

                chunks.append(sub_chunk)

    return chunks
