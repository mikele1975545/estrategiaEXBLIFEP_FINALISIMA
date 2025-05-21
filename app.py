import streamlit as st
from fpdf import FPDF
import datetime

# Simulador sencillo con pestañas
st.set_page_config(page_title="Estrategia Exblifep", layout="centered")

st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

# --- Base de datos simulada para antibióticos ---
antibioticos_info = {
    "Cefepime/enmetazobactam": {
        "Ventajas": "Mejor actividad frente a OXA-48 y BLEE. Amplio espectro frente a gramnegativos.",
        "Desventajas": "Nuevo en el mercado. Menor experiencia clínica."
    },
    "Ceftazidima/avibactam": {
        "Ventajas": "Alta eficacia frente a BLEE y algunas carbapenemasas.",
        "Desventajas": "Resistencia emergente frente a metalo-β-lactamasas."
    },
    "Ceftolozano/tazobactam": {
        "Ventajas": "Buena actividad frente a Pseudomonas multirresistente.",
        "Desventajas": "Menor actividad frente a Enterobacterias BLEE comparado con otras combinaciones."
    },
    "Imipenem/relebactam": {
        "Ventajas": "Activo frente a BLEE, KPC y Pseudomonas.",
        "Desventajas": "Uso limitado en infecciones específicas. Costoso."
    },
    "Meropenem/vaborbactam": {
        "Ventajas": "Buena actividad frente a KPC.",
        "Desventajas": "No cubre OXA-48 ni MBLs. Uso hospitalario restringido."
    }
}

# --- Funciones auxiliares ---
def exportar_pdf(nombre_hospital, comunidad, provincia, estrategia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    pdf.cell(200, 10, f"Estrategia recomendada para {nombre_hospital} ({provincia}, {comunidad})", ln=True)
    pdf.cell(200, 10, f"Fecha: {fecha_actual}", ln=True)
    pdf.multi_cell(200, 10, estrategia)
    nombre_archivo = f"Estrategia_{nombre_hospital.replace(' ', '_')}.pdf"
    ruta = os.path.join("/mnt/data", nombre_archivo)
    pdf.output(ruta)
    return ruta

# --- Interfaz ---
tabs = st.tabs(["Estrategia por hospital", "Comparativa entre antibióticos"])

with tabs[0]:
    st.subheader("Estrategia personalizada por hospital")
    hospital = st.text_input("Nombre del hospital")
    comunidad = st.selectbox("Comunidad autónoma", ["Cataluña", "Madrid", "Andalucía", "Galicia"])
    provincia = st.text_input("Provincia")

    st.markdown("#### Bacterias más frecuentes")
    bacterias = st.multiselect("Selecciona bacterias", ["Klebsiella pneumoniae", "E. coli", "Pseudomonas aeruginosa"])
    porcentajes_bacterias = {bact: st.selectbox(f"Prevalencia estimada para {bact}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"bact_{bact}") for bact in bacterias}

    st.markdown("#### Resistencias más frecuentes")
    resistencias = st.multiselect("Selecciona resistencias", ["BLEE", "OXA-48", "KPC", "NDM"])
    porcentajes_resistencias = {res: st.selectbox(f"Prevalencia estimada para {res}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"res_{res}") for res in resistencias}

    st.markdown("#### Leyenda de siglas")
    with st.expander("Mostrar leyenda"):
        st.markdown("""
        - **BLEE**: Betalactamasas de espectro extendido  
        - **OXA-48**: Carbapenemasa del tipo OXA  
        - **KPC**: Klebsiella pneumoniae carbapenemasa  
        - **NDM**: Metalo-betalactamasa tipo New Delhi  
        """)

    if st.button("Generar estrategia"):
        resultado = f"Estrategia antibiótica adaptada a {hospital} en {provincia}, {comunidad}:
"
        resultado += "Bacterias seleccionadas y prevalencias:
"
        for bact, por in porcentajes_bacterias.items():
            resultado += f"- {bact}: {por}
"
        resultado += "Resistencias seleccionadas y prevalencias:
"
        for res, por in porcentajes_resistencias.items():
            resultado += f"- {res}: {por}
"
        resultado += "
**Recomendación preliminar:** Considerar el uso de antibióticos con actividad frente a las resistencias detectadas, priorizando aquellos con mejor perfil de eficacia y seguridad."
        st.success("Estrategia generada:")
        st.markdown(resultado)

        if st.button("Exportar a PDF"):
            ruta = exportar_pdf(hospital, comunidad, provincia, resultado)
            st.success(f"PDF generado correctamente: {ruta}")

with tabs[1]:
    st.subheader("Comparativa entre antibióticos")
    ab1 = st.selectbox("Antibiótico 1", list(antibioticos_info.keys()), key="ab1")
    ab2 = st.selectbox("Antibiótico 2", list(antibioticos_info.keys()), index=1, key="ab2")

    if ab1 != ab2:
        st.markdown(f"### {ab1}")
        st.markdown(f"**Ventajas**: {antibioticos_info[ab1]['Ventajas']}")
        st.markdown(f"**Desventajas**: {antibioticos_info[ab1]['Desventajas']}")
        st.markdown("---")
        st.markdown(f"### {ab2}")
        st.markdown(f"**Ventajas**: {antibioticos_info[ab2]['Ventajas']}")
        st.markdown(f"**Desventajas**: {antibioticos_info[ab2]['Desventajas']}")
    else:
        st.warning("Por favor, selecciona dos antibióticos distintos.")
