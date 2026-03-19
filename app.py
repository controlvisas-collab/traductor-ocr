import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
from pdf2image import convert_from_bytes
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Traductor OCR a Word", layout="wide")
st.title("🌍 Traductor de Documentos con Exportación")

languages = {'Español': 'es', 'Inglés': 'en', 'Francés': 'fr', 'Alemán': 'de'}
target_lang = st.sidebar.selectbox("Idioma de destino", list(languages.keys()))

uploaded_file = st.file_uploader("Sube tu PDF o Imagen", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Creamos un objeto de documento Word en memoria
    doc_word = Document()
    doc_word.add_heading('Traducción de Documento', 0)
    
    paginas_imagenes = []
    if uploaded_file.type == "application/pdf":
        paginas_imagenes = convert_from_bytes(uploaded_file.read(), dpi=200)
    else:
        paginas_imagenes.append(Image.open(uploaded_file))

    translator = Translator()
    texto_completo_traducido = ""

    for i, pagina in enumerate(paginas_imagenes):
        with st.spinner(f'Procesando página {i+1}...'):
            # OCR y Traducción
            texto_original = pytesseract.image_to_string(pagina)
            if texto_original.strip():
                traduccion = translator.translate(texto_original, dest=languages[target_lang]).text
                
                # Añadir al documento Word
                doc_word.add_heading(f'Página {i+1}', level=1)
                doc_word.add_paragraph(traduccion)
                
                # Mostrar en pantalla
                st.subheader(f"Página {i+1}")
                st.write(traduccion)
            else:
                st.warning(f"Página {i+1} parece estar vacía.")

    # --- SECCIÓN DE DESCARGA ---
    st.divider()
    st.subheader("✅ Procesamiento completado")
    
    # Guardar el Word en un buffer (memoria) para que Streamlit lo descargue
    buffer = BytesIO()
    doc_word.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar todo en Word (.docx)",
        data=buffer,
        file_name="documento_traducido.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )