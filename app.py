import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from pdf2image import convert_from_bytes
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Traductor OCR Pro", layout="wide")
st.title("🌍 Traductor de Documentos Pro (Versión Estable)")

# Configuración de idiomas
languages_dict = {'Español': 'es', 'Inglés': 'en', 'Francés': 'fr', 'Alemán': 'de', 'Italiano': 'it'}
target_lang = st.sidebar.selectbox("Selecciona idioma de destino", list(languages_dict.keys()))

uploaded_file = st.file_uploader("Sube tu PDF o Imagen", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    doc_word = Document()
    doc_word.add_heading('Traducción de Documento', 0)
    
    paginas_imagenes = []
    if uploaded_file.type == "application/pdf":
        with st.spinner('Convirtiendo PDF...'):
            paginas_imagenes = convert_from_bytes(uploaded_file.read(), dpi=200)
    else:
        paginas_imagenes.append(Image.open(uploaded_file))

    # Usamos el nuevo traductor que no falla en Python 3.14
    translator = GoogleTranslator(source='auto', target=languages_dict[target_lang])

    for i, pagina in enumerate(paginas_imagenes):
        with st.spinner(f'Procesando página {i+1}...'):
            texto_original = pytesseract.image_to_string(pagina)
            
            if texto_original.strip():
                # Nueva forma de traducir
                traduccion = translator.translate(texto_original)
                
                doc_word.add_heading(f'Página {i+1}', level=1)
                doc_word.add_paragraph(traduccion)
                
                st.subheader(f"Página {i+1}")
                col1, col2 = st.columns(2)
                with col1: st.image(pagina, use_column_width=True)
                with col2: st.write(traduccion)
            else:
                st.warning(f"No se detectó texto en la página {i+1}")

    st.divider()
    buffer = BytesIO()
    doc_word.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar todo en Word (.docx)",
        data=buffer,
        file_name="traduccion_final.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
