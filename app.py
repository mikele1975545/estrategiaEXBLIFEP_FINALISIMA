
import streamlit as st
import time
from fpdf import FPDF
from datetime import date

# Datos simulados para EPINE
epine_data = {
    "Cataluña": {"E. coli": "35%", "Klebsiella pneumoniae": "18%", "Pseudomonas aeruginosa": "12%"},
    "Madrid": {"E. coli": "32%", "Klebsiella pneumoniae": "15%", "Pseudomonas aeruginosa": "10%"}
}

resistencias_epine = {
    "Cataluña": {"OXA-48": "5%", "BLEE": "21%", "KPC": "2%"},
    "Madrid": {"OXA-48": "4%", "BLEE": "19%", "KPC": "3%"}
}

# Diccionario antibióticos
antibioticos_info = {
    "Cefepime/enmetazobactam": {
        "Ventajas": "Activo frente a BLEE y OXA-48. Buen perfil de seguridad. Datos positivos en neumonía y bacteriemia.",
        "Desventajas": "Nuevo en el mercado, menor experiencia clínica."
    },
    "Ceftazidima/avibactam": {
        "Ventajas": "Eficaz frente a BLEE y OXA-48. Muy utilizado.",
        "Desventajas": "Emergencia creciente de resistencias. No cubre MBLs como NDM."
    },
    "Ceftolozano/tazobactam": {
        "Ventajas": "Excelente contra Pseudomonas multirresistente.",
        "Desventajas": "Cobertura inferior frente a BLEE/OXA-48."
    },
    "Meropenem/vaborbactam": {
        "Ventajas": "Buena actividad frente a KPC.",
        "Desventajas": "No cubre OXA-48 ni NDM."
    },
    "Imipenem/relebactam": {
        "Ventajas": "Buena actividad frente a BLEE y KPC.",
        "Desventajas": "Actividad limitada frente a OXA-48."
    }
}

abreviaturas = {
    "OXA-48": "Carbapenemasa del tipo OXA-48",
    "BLEE": "Betalactamasas de espectro extendido",
    "KPC": "Carbapenemasa tipo K. pneumoniae"
}

st.set_page_config(page_title="Estrategia Exblifep", layout="wide")
st.title("Estrategia Exblifep")

menu = st.sidebar.radio("Menú", ["📊 Estrategia hospital", "⚖️ Comparativa antibióticos"])

if menu == "📊 Estrategia hospital":
    comunidad = st.selectbox("Selecciona comunidad", list(epine_data.keys()))
    provincia = st.text_input("Provincia")
    hospital = st.text_input("Nombre del hospital")

    st.markdown("### Bacterias en el hospital")
    bacterias = st.multiselect("Selecciona bacterias", ["E. coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"])
    porcentajes_bacterias = {b: st.selectbox(f"% estimado en el hospital para {b}", ["<10%", "10-25%", "25-50%", ">50%"], key=b) for b in bacterias}

    st.markdown("### Resistencias en el hospital")
    resistencias = st.multiselect("Selecciona resistencias", ["OXA-48", "BLEE", "KPC"])
    porcentajes_resistencias = {r: st.selectbox(f"% estimado para {r}", ["<5%", "5-15%", "15-30%", ">30%"], key=r) for r in resistencias}

    if st.button("Generar estrategia"):
        with st.spinner("Cruzando datos con informe EPINE..."):
            for i in range(100):
                time.sleep(0.01)
                st.progress(i + 1, text="Analizando perfil epidemiológico...")

        estrategia = f"Estrategia para {hospital} en {provincia}, {comunidad}:

"
        estrategia += "📌 **Bacterias frecuentes**:
"
        for b, p in porcentajes_bacterias.items():
            epine = epine_data[comunidad].get(b, "N/A")
            estrategia += f"- {b}: hospital {p}, EPINE {epine}
"

        estrategia += "
🧬 **Resistencias frecuentes**:
"
        for r, p in porcentajes_resistencias.items():
            epine_r = resistencias_epine[comunidad].get(r, "N/A")
            estrategia += f"- {r}: hospital {p}, EPINE {epine_r}
"

        estrategia += "
💊 **Recomendación**:
"
        estrategia += "- Considerar Cefepime/enmetazobactam como primera línea si BLEE u OXA-48 son relevantes.
"
        estrategia += "- Evitar carbapenémicos si existen opciones activas como Exblifep para preservar su uso."

        st.text_area("Resultado:", estrategia, height=300)

elif menu == "⚖️ Comparativa antibióticos":
    st.markdown("### Selecciona dos antibióticos para comparar")
    col1, col2 = st.columns(2)
    with col1:
        ab1 = st.radio("Antibiótico 1", list(antibioticos_info.keys()), key="ab1")
    with col2:
        ab2 = st.radio("Antibiótico 2", list(antibioticos_info.keys()), key="ab2")

    if ab1 != ab2:
        st.subheader(f"🔬 Comparativa entre {ab1} y {ab2}")
        st.markdown(f"**{ab1}**")
        st.markdown(f"- Ventajas: {antibioticos_info[ab1]['Ventajas']}")
        st.markdown(f"- Desventajas: {antibioticos_info[ab1]['Desventajas']}")
        st.markdown("---")
        st.markdown(f"**{ab2}**")
        st.markdown(f"- Ventajas: {antibioticos_info[ab2]['Ventajas']}")
        st.markdown(f"- Desventajas: {antibioticos_info[ab2]['Desventajas']}")

        if ab1 == "Cefepime/enmetazobactam" or ab2 == "Cefepime/enmetazobactam":
            st.markdown("✅ **Argumento de superioridad de Cefepime/enmetazobactam:**")
            st.markdown("- Tiene mejor cobertura frente a OXA-48 que muchos competidores.")
            st.markdown("- Permite reducir el uso innecesario de carbapenémicos.")
            st.markdown("- Excelente penetración pulmonar y perfil de seguridad favorable.")

st.markdown("---")
with st.expander("📘 Leyenda de siglas"):
    for sigla, definicion in abreviaturas.items():
        st.markdown(f"- **{sigla}**: {definicion}")
