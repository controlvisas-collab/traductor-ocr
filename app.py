import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Traductor Sin Registro", layout="wide")
st.title("🌍 Traductor de PDF (Sin API Key)")
st.write("Esta versión no requiere tarjetas ni registros. Mantiene párrafos y estructura básica.")

languages_dict = {'Español': 'es', 'Inglés': 'en', 'Francés': 'fr', 'Alemán': 'de'}
target_lang = st.sidebar.selectbox("Idioma de destino", list(languages_dict.keys()))

uploaded_file = st.file_uploader("Sube tu PDF", type=["pdf"])

if uploaded_file is not None:
    doc_word = Document()
    
    with pdfplumber.open(uploaded_file) as pdf:
        total_paginas = len(pdf.pages)
        progreso = st.progress(0)
        
        for i, pagina in enumerate(pdf.pages):
            st.subheader(f"Pagina {i+1}")
            
            # Extraemos el texto manteniendo la disposición visual
            texto_pagina = pagina.extract_text()
            
            if texto_pagina:
                # Traducir por bloques para no saturar el servidor
                lineas = texto_pagina.split('\n')
                texto_traducido_pag = []
                
                for linea in lineas:
                    if linea.strip():
                        trad = GoogleTranslator(source='auto', target=languages_dict[target_lang]).translate(linea)
                        texto_traducido_pag.append(trad)
                
                resultado_final = "\n".join(texto_traducido_pag)
                
                # Mostrar en la web
                st.text_area(f"Resultado Pág {i+1}", resultado_final, height=200)
                
                # Guardar en el Word
                doc_word.add_heading(f'Página {i+1}', level=1)
                doc_word.add_paragraph(resultado_final)
            
            progreso.progress((i + 1) / total_paginas)

    # Botón de descarga
    st.divider()
    buffer = BytesIO()
    doc_word.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar Documento en Word",
        data=buffer,
        file_name="traduccion_formato_basico.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
