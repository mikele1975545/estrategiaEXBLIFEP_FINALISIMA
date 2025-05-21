
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Variables simuladas para ejemplo
hospital = "Hospital General"
provincia = "Barcelona"
comunidad = "Cataluña"

# Crear el contenido corregido
resultado = f"Estrategia antibiótica adaptada a {hospital} en {provincia}, {comunidad}:"
st.write(resultado)
