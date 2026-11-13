import re

def chunk_text(text, max_chunk_size=2000):
    chunks = []

    # Separate the appendix from the main text
    sections = re.split(
        r'(?m)(?=^پیوست شماره\s*\d+)',
        text
    )

    for section in sections:
        section = section.strip()

        if not section:
            continue

        # Process the appendix separately
        if section.startswith("پیوست شماره"):
            chunks.extend(chunk_appendix(section))
            continue

        # Split the main text by article numbers
        articles = re.split(
            r'(?m)(?=^\s*ماده\s*[.٫]?\s*\d+)',
            section
        )

        for article in articles:
            article = article.strip()

            if not article:
                continue

            # Keep short articles as they are
            if len(article) <= max_chunk_size:
                chunks.append(article)
            else:
                chunks.extend(chunk_long_article(article))

    return chunks


def chunk_long_article(article):
    # Handle article 12 separately
    if re.match(r'^\s*ماده\s*[.٫]?\s*12\b', article):
        split_position = re.search(
            r'(?m)^\s*ج\s*[\)]',
            article
        )

        if split_position:
            first_chunk = article[:split_position.start()].strip()

            second_chunk = (
                "ماده ۱۲ (ادامه):\n" +
                article[split_position.start():].strip()
            )

            return [first_chunk, second_chunk]

    # Find all note boundaries
    notes = re.split(
        r'(?m)(?=^\s*تبصره\s*[:：]?\s*(?:شماره\s*)?[\d۰-۹٠-٩]+)',
        article
    )

    # Keep the article unchanged if it has no notes
    if len(notes) < 2:
        return [article]

    introduction = notes[0].strip()

    # Keep articles with lettered clauses unchanged
    clause_pattern = r'(?m)^\s*(?:الف|ب|ج|د|ه|و|ز|ح|ط)\s*[\)]'

    if re.search(clause_pattern, introduction):
        return [article]

    chunks = []

    # Combine the article introduction with the first note
    first_chunk = introduction + "\n" + notes[1].strip()
    chunks.append(first_chunk)

    # Keep the remaining notes in separate chunks
    article_title = introduction.split("\n")[0]

    for note in notes[2:]:
        note = note.strip()

        if note:
            chunks.append(article_title + "\n" + note)

    return chunks

def chunk_appendix(appendix):
    # Separate document information from the definitions
    metadata_pattern = r'(?m)(?=^\s*عنوان\s*سند\s*:)'

    parts = re.split(metadata_pattern, appendix)

    definitions_text = parts[0]
    metadata = parts[1:]

    # Identify the beginning of each definition
    definitions_pattern = (
        r'(?m)(?=^\s*(?:'
        r'وزارت|'
        r'شورای عالی برنامه ریزی آموزشی|'
        r'آموزش رایگان|'
        r'مدرس|'
        r'دانشـجـو|'
        r'دانش آموخته|'
        r'دانشجوی قهرمان|'
        r'حضوری|'
        r'نیمسال تحصیلی|'
        r'برنامه درسی|'
        r'واحد درسی|'
        r'مشروطی|'
        r'رشته تحصیلی|'
        r'کارشناسی پیوسته|'
        r'گروه آزمایشی|'
        r'گروه آموزشی|'
        r'مجموعه امتحانی|'
        r'شورای آموزشی|'
        r'راهنمای آموزشی'
        r')\s*:)'
    )

    definitions = re.split(definitions_pattern, definitions_text)

    chunks = []

    for definition in definitions:
        definition = definition.strip()

        if definition:
            chunks.append(definition)

    # Add document information as a separate chunk
    for item in metadata:
        item = item.strip()

        if item:
            chunks.append(item)

    return chunks
