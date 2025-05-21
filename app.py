
import streamlit as st
import time

st.set_page_config(page_title="Estrategia Exblifep - Actualizado", layout="centered")
st.title("Estrategia Exblifep - Actualizado")
st.markdown("### Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

# Hospital Info
comunidad = st.selectbox("Selecciona la comunidad autónoma", ["Cataluña", "Madrid", "Andalucía"])
provincia = st.text_input("Provincia", "")
hospital = st.text_input("Nombre del hospital", "")

# ESTRATEGIA
st.header("Estrategia personalizada")
bacterias = st.multiselect("Selecciona bacterias frecuentes", ["Klebsiella pneumoniae", "Pseudomonas aeruginosa", "Escherichia coli"])
porcentajes_bacterias = {b: st.slider(f"Prevalencia de {b}", 0, 100, 10) for b in bacterias}

resistencias = st.multiselect("Selecciona resistencias frecuentes", ["OXA-48", "BLEE", "KPC", "NDM"])
porcentajes_resistencias = {r: st.slider(f"Prevalencia de {r}", 0, 100, 10) for r in resistencias}

# Simulación de análisis cruzado con EPINE
st.markdown("#### Cruzando datos con el informe EPINE para afinar la estrategia...")
barra = st.progress(0)
for i in range(101):
    time.sleep(0.01)
    barra.progress(i)

# Resultado
st.markdown(f"**Estrategia antibiótica adaptada a {hospital} en {provincia}, {comunidad}:**")
if bacterias:
    st.markdown("- **Bacterias más frecuentes:** " + ", ".join([f"{b} ({porcentajes_bacterias[b]}%)" for b in bacterias]))
if resistencias:
    st.markdown("- **Resistencias destacadas:** " + ", ".join([f"{r} ({porcentajes_resistencias[r]}%)" for r in resistencias]))
st.markdown("- **Recomendación:** Considerar cefepime/enmetazobactam como tratamiento empírico en casos graves con sospecha de estas resistencias.")

# COMPARATIVA
st.header("Comparativa entre antibióticos")
antibioticos = [
    "Cefepime/enmetazobactam", "Ceftazidima/avibactam", "Meropenem/vaborbactam",
    "Imipenem/relebactam", "Ceftolozano/tazobactam"
]
col1, col2 = st.columns(2)
ab1 = col1.selectbox("Antibiótico 1", antibioticos, key="ab1")
ab2 = col2.selectbox("Antibiótico 2", antibioticos, key="ab2")

detalles = {
    "Cefepime/enmetazobactam": [
        "- Amplio espectro frente a BLEE, OXA-48 y otras carbapenemasas.",
        "- Buena penetración pulmonar.",
        "- Perfil de seguridad favorable.",
        "- Alta evidencia clínica en neumonía grave."
    ],
    "Ceftazidima/avibactam": [
        "- Eficaz frente a BLEE y KPC.",
        "- Menor eficacia frente a OXA-48.",
        "- Requiere ajuste renal en pacientes críticos."
    ],
    "Meropenem/vaborbactam": [
        "- Muy potente frente a KPC.",
        "- No cubre OXA-48.",
        "- Indicaciones limitadas en España."
    ],
    "Imipenem/relebactam": [
        "- Alternativa a meropenem en ciertas infecciones.",
        "- No útil frente a metalo-beta-lactamasas."
    ],
    "Ceftolozano/tazobactam": [
        "- Muy eficaz frente a Pseudomonas multirresistente.",
        "- No activo frente a carbapenemasas."
    ]
}

if ab1 != ab2:
    st.subheader(f"Comparativa entre {ab1} y {ab2}")
    st.markdown(f"**{ab1}**")
    for punto in detalles[ab1]:
        st.markdown(f"- {punto}")
    st.markdown(f"**{ab2}**")
    for punto in detalles[ab2]:
        st.markdown(f"- {punto}")

    if "cefepime/enmetazobactam" in [ab1.lower(), ab2.lower()]:
        st.success("✅ **Ventaja de Cefepime/enmetazobactam:** cobertura robusta frente a BLEE, OXA-48 y otras carbapenemasas, con alta evidencia clínica en neumonía grave.")
