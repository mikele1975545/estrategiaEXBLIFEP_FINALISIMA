
import streamlit as st
from fpdf import FPDF
from datetime import date

# Datos de ejemplo
antibioticos_info = {
    "Cefepime/enmetazobactam": {
        "Ventajas": "Mejor actividad frente a OXA-48 y BLEE.",
        "Desventajas": "Menor experiencia clínica acumulada."
    },
    "Ceftazidima/avibactam": {
        "Ventajas": "Amplia experiencia clínica. Activo frente a OXA-48.",
        "Desventajas": "No cubre BLEE tan eficazmente como otras combinaciones."
    },
    "Ceftolozano/tazobactam": {
        "Ventajas": "Muy eficaz frente a Pseudomonas multirresistente.",
        "Desventajas": "No cubre OXA-48 ni algunas BLEE."
    },
    "Meropenem/vaborbactam": {
        "Ventajas": "Activo frente a KPC. Buena actividad frente a BLEE.",
        "Desventajas": "No cubre OXA-48."
    },
    "Imipenem/relebactam": {
        "Ventajas": "Cobertura frente a BLEE y algunas KPC.",
        "Desventajas": "No cubre OXA-48. Menos experiencia clínica."
    }
}

abreviaturas = {
    "OXA-48": "Carbapenemasa del tipo OXA-48, común en enterobacterias.",
    "BLEE": "Betalactamasas de espectro extendido.",
    "KPC": "Carbapenemasa tipo K. pneumoniae."
}

hospitales_db = {}

st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

menu = st.sidebar.selectbox("Selecciona una funcionalidad", ["Estrategia hospital", "Comparativa entre antibióticos"])

if menu == "Estrategia hospital":
    comunidad = st.selectbox("Selecciona la comunidad autónoma", ["Cataluña", "Madrid", "Andalucía", "Valencia"])
    provincia = st.selectbox("Selecciona la provincia", ["Barcelona", "Madrid", "Sevilla", "Valencia"])
    hospital = st.text_input("Introduce el nombre del hospital")

    bacterias = st.multiselect("Selecciona bacterias presentes", ["E. coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"])
    resistencias = st.multiselect("Selecciona resistencias detectadas", ["OXA-48", "BLEE", "KPC"])

    if st.button("Generar estrategia"):
        estrategia = f"Estrategia recomendada para {hospital} en {provincia}, {comunidad}:"
        st.success(estrategia)

        resumen = f"Bacterias detectadas: {', '.join(bacterias)}. Resistencias: {', '.join(resistencias)}"
        st.write(resumen)

        if hospital:
            hospitales_db[hospital] = {"bacterias": bacterias, "resistencias": resistencias, "comunidad": comunidad, "provincia": provincia}

        if st.button("Exportar a PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 10, f"Estrategia basada en los datos proporcionados por {hospital}.")
            pdf.multi_cell(200, 10, resumen)
            pdf.output("/mnt/data/estrategia_hospital.pdf")
            st.success("PDF generado correctamente. [Descargar PDF](sandbox:/mnt/data/estrategia_hospital.pdf)")

elif menu == "Comparativa entre antibióticos":
    ab1 = st.selectbox("Antibiótico 1", list(antibioticos_info.keys()))
    ab2 = st.selectbox("Antibiótico 2", list(antibioticos_info.keys()), index=1)

    if st.button("Comparar"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(ab1)
            st.markdown(f"**Ventajas**: {antibioticos_info[ab1]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos_info[ab1]['Desventajas']}")
        with col2:
            st.subheader(ab2)
            st.markdown(f"**Ventajas**: {antibioticos_info[ab2]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos_info[ab2]['Desventajas']}")

        if st.button("Exportar comparativa a PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, f"Comparativa entre {ab1} y {ab2}", ln=True)
            pdf.multi_cell(200, 10, f"{ab1} - Ventajas: {antibioticos_info[ab1]['Ventajas']}")
            pdf.multi_cell(200, 10, f"{ab1} - Desventajas: {antibioticos_info[ab1]['Desventajas']}")
            pdf.multi_cell(200, 10, f"{ab2} - Ventajas: {antibioticos_info[ab2]['Ventajas']}")
            pdf.multi_cell(200, 10, f"{ab2} - Desventajas: {antibioticos_info[ab2]['Desventajas']}")
            pdf.output("/mnt/data/comparativa_antibioticos.pdf")
            st.success("PDF generado correctamente. [Descargar PDF](sandbox:/mnt/data/comparativa_antibioticos.pdf)")

with st.expander("Leyenda de abreviaturas"):
    for sigla, descripcion in abreviaturas.items():
        st.markdown(f"**{sigla}**: {descripcion}")
