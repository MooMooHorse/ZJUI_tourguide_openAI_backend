import fitz  # PyMuPDF

# Open the PDF file
pdf_path = '/mnt/data/service-booklet.pdf'
pdf_document = fitz.open(pdf_path)

# Read and concatenate text from each page
full_text = ""
for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    full_text += page.get_text("text")

# Close the PDF after reading
pdf_document.close()

# The 'full_text' variable now contains all the text extracted from the PDF
