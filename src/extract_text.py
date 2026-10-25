
import pymupdf
import os

pdf_path = "data/raw/regulations.pdf"
output_path = "data/processed/regulations.txt"

# Open the PDF file
pdf = pymupdf.open(pdf_path)

# Extract text from all pages
text = ""

for page in pdf:
    text += page.get_text() + "\n"

# Close the PDF file
pdf.close()

# Create the output folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Save the extracted text
with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

print("Text extracted successfully!")
print("Number of characters:", len(text))
