import lenguaje

import streamlit as st

l=lenguaje.tu_idioma()

st.title(f':material/sell: {l.phrase[1]}')