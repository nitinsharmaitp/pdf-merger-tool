# 📄 PDF Merger & Optimizer Tool

A powerful, user-friendly web application to merge multiple PDF files, reorder them, and significantly reduce their file size using advanced compression techniques. Built with Python and Streamlit.

## 🚀 Live Demo
[Insert your Streamlit Share URL here once deployed]

## ✨ Features

### 1. 📂 Merge Multiple PDFs
* Upload an unlimited number of PDF files at once.
* **Drag & Drop Reordering:** Easily arrange your files in the exact sequence you need before merging.
* Merges files instantly into a single document.

### 2. ♻️ Advanced Compression (Size Reduction)
Unlike standard mergers that often increase file size, this tool includes a dedicated compression engine.
* **Smart Compression:** Reduces file size by optimizing internal structures and removing unused data.
* **Image Optimization:** Detects images inside the PDF and re-encodes them to save space.
* **Custom Quality Slider:** You control the balance between quality and size (10% to 90%).
* **Live Feedback:** Shows the original size, new size, and exact percentage reduction (e.g., "-45% Reduction").

### 3. 🔒 Privacy Focused
* Files are processed in-memory.
* No files are permanently stored on any server.
* Everything is wiped from memory as soon as you refresh or close the page.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **PDF Processing:** [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) and [pypdf](https://pypdf.readthedocs.io/)
* **UI Components:** [Streamlit-Sortables](https://github.com/ohtaman/streamlit-sortables)

## 📦 Local Installation

If you prefer to run this tool on your own machine instead of using the web version:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/pdf-merger-tool.git](https://github.com/your-username/pdf-merger-tool.git)
    cd pdf-merger-tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📋 Requirements
The project relies on the following Python libraries (included in `requirements.txt`):
* `streamlit`
* `pypdf`
* `pymupdf`
* `streamlit-sortables`

## 🤝 Contributing
Feel free to open issues or submit pull requests if you have suggestions for improvements!

---
*Created with ❤️ by [Your Name]*
