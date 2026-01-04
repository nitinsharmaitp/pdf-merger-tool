import streamlit as st
from pypdf import PdfWriter
from streamlit_sortables import sort_items
import io
import fitz  # PyMuPDF

# --- Functions ---

def get_file_size_str(bytes_data):
    """Returns a human-readable file size string."""
    size_in_bytes = bytes_data.getbuffer().nbytes
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"

def merge_pdfs(ordered_file_list):
    """Merges PDFs using pypdf."""
    merger = PdfWriter()
    for pdf in ordered_file_list:
        pdf.seek(0)
        merger.append(pdf)
    
    output_buffer = io.BytesIO()
    merger.write(output_buffer)
    merger.close()
    output_buffer.seek(0)
    return output_buffer

def compress_pdf_advanced(input_buffer, quality_val):
    """
    Compresses PDF by downsampling images and cleaning structure.
    quality_val: Integer (1-100) representing JPEG quality.
    """
    input_buffer.seek(0)
    doc = fitz.open(stream=input_buffer.read(), filetype="pdf")
    
    # 1. Optimize Images (The biggest factor in file size)
    # Iterate through every page
    for page in doc:
        image_list = page.get_images()
        
        for img in image_list:
            xref = img[0] # The reference ID of the image object
            
            # Extract the image
            pix = fitz.Pixmap(doc, xref)
            
            # If it's CMYK, convert to RGB to ensure we can save as JPEG
            if pix.n - pix.alpha > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            # Compress the image data to new JPEG quality
            # This is where the actual "Size Reduction" happens
            new_data = pix.tobytes("jpeg", jpg_quality=int(quality_val))
            
            # Replace the old large image with the new compressed one
            doc.update_stream(xref, new_data)

    # 2. Save with structural garbage collection (deflate)
    output_buffer = io.BytesIO()
    doc.save(output_buffer, garbage=4, deflate=True)
    doc.close()
    
    output_buffer.seek(0)
    return output_buffer

# --- Streamlit UI ---
st.set_page_config(page_title="PDF Merger & Compressor", page_icon="📄")
st.title("📄 PDF Merger & Compressor")

# Session State Initialization
if 'merged_pdf' not in st.session_state:
    st.session_state['merged_pdf'] = None
if 'compressed_pdf' not in st.session_state:
    st.session_state['compressed_pdf'] = None
if 'compression_stats' not in st.session_state:
    st.session_state['compression_stats'] = None

# 1. UPLOAD
uploaded_files = st.file_uploader("1. Upload Files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # 2. SORT
    st.write("---")
    st.subheader("2. Reorder Files")
    file_map = {file.name: file for file in uploaded_files}
    original_order = list(file_map.keys())
    sorted_names = sort_items(original_order)
    sorted_files = [file_map[name] for name in sorted_names]

    st.write("---")
    
    # 3. MERGE
    if st.button("Merge Files"):
        with st.spinner("Merging..."):
            st.session_state['compressed_pdf'] = None 
            st.session_state['compression_stats'] = None
            st.session_state['merged_pdf'] = merge_pdfs(sorted_files)
            st.success("Files Merged Successfully!")

    # 4. DOWNLOAD & COMPRESS OPTIONS
    if st.session_state['merged_pdf']:
        st.subheader("3. Download & Optimize")
        
        col1, col2 = st.columns([1, 1.2]) # Make right column slightly wider
        
        # --- LEFT: Standard ---
        with col1:
            st.info("⬇️ **Standard Version**")
            size_str = get_file_size_str(st.session_state['merged_pdf'])
            st.write(f"Size: **{size_str}**")
            
            st.download_button(
                label="Download Standard PDF",
                data=st.session_state['merged_pdf'],
                file_name="merged_document.pdf",
                mime="application/pdf"
            )

        # --- RIGHT: Reduced ---
        with col2:
            st.success("♻️ **Reduced Size Version**")
            
            # SLIDER for user control
            quality = st.slider(
                "Image Quality %", 
                min_value=10, 
                max_value=90, 
                value=50, 
                step=10,
                help="Lower value = Smaller file size but lower image quality."
            )

            if st.button("Apply Compression"):
                with st.spinner(f"Compressing with {quality}% quality..."):
                    try:
                        st.session_state['merged_pdf'].seek(0)
                        
                        # Run the advanced compression
                        compressed_buffer = compress_pdf_advanced(st.session_state['merged_pdf'], quality)
                        st.session_state['compressed_pdf'] = compressed_buffer
                        
                        # Calculate statistics
                        orig_bytes = st.session_state['merged_pdf'].getbuffer().nbytes
                        new_bytes = compressed_buffer.getbuffer().nbytes
                        ratio = ((orig_bytes - new_bytes) / orig_bytes) * 100
                        
                        st.session_state['compression_stats'] = {
                            "new_size": get_file_size_str(compressed_buffer),
                            "reduction": ratio
                        }
                    except Exception as e:
                        st.error(f"Error: {e}")

            # Show Result if available
            if st.session_state['compressed_pdf']:
                stats = st.session_state['compression_stats']
                
                # Visual Metric
                st.metric(
                    label="New Size", 
                    value=stats["new_size"], 
                    delta=f"-{stats['reduction']:.1f}% Reduction"
                )
                
                st.download_button(
                    label="Download Reduced PDF",
                    data=st.session_state['compressed_pdf'],
                    file_name=f"merged_compressed_{quality}percent.pdf",
                    mime="application/pdf",
                    key="dl_compressed"
                )

else:
    # Reset
    st.session_state['merged_pdf'] = None
    st.session_state['compressed_pdf'] = None