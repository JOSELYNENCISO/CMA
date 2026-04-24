import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Levantamiento de alturas")

# Subir archivo
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo is not None:

    df = pd.read_excel(archivo)

    # Limpiar altura
    df["Altura"] = pd.to_numeric(df["Altura"], errors='coerce')

    # Clasificación
    def clasificar(h):
        if pd.isna(h):
            return "Sin dato"
        elif h >= 14:
            return "Óptimo"
        elif h >= 10:
            return "Corto"
        elif h >= 6:
            return "Crítico"
        else:
            return "Tapado"

    df["Categoria"] = df["Altura"].apply(clasificar)

    # Tamaños automáticos
    n_puntos = len(df)

    if n_puntos > 150:
        size_punto = 6
        size_texto = 4
    elif n_puntos > 80:
        size_punto = 10
        size_texto = 6
    elif n_puntos > 40:
        size_punto = 25
        size_texto = 9
    else:
        size_punto = 40
        size_texto = 12

    # Colores
    colores = {
        "Óptimo": "green",
        "Corto": "yellow",
        "Crítico": "orange",
        "Tapado": "red",
        "Sin dato": "black"
    }

    nombres = {
        "Óptimo": "Óptimo (>=14 m)",
        "Corto": "Corto (10–14 m)",
        "Crítico": "Crítico (6–10 m)",
        "Tapado": "Tapado (<6 m)",
        "Sin dato": "Sin dato (-)"
    }

    if st.button("🔘 Generar gráfico"):

        fig, ax = plt.subplots(figsize=(10,10))

        for cat in colores:
            sub = df[df["Categoria"] == cat]
            cantidad = len(sub)

            ax.scatter(sub["X"], sub["Y"],
                       c=colores[cat],
                       label=f"{nombres[cat]} - {cantidad}",
                       s=size_punto)

        offset = (df["Y"].max() - df["Y"].min()) * 0.008

        for i, row in df.iterrows():
            ax.text(row["X"], row["Y"] + offset,
                    str(row["ID"]),
                    fontsize=size_texto,
                    ha='center',
                    va='bottom',
                    fontweight='bold')

        ax.legend()
        ax.set_title("Plano de Taladros")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(False)

        margen = (df["X"].max() - df["X"].min()) * 0.05

        ax.set_xlim(df["X"].min() - margen, df["X"].max() + margen)
        ax.set_ylim(df["Y"].min() - margen, df["Y"].max() + margen)

        ax.set_aspect('equal', adjustable='box')

        st.pyplot(fig)

        # Guardar y descargar
        fig.savefig("grafico.png", dpi=600, bbox_inches='tight')

        with open("grafico.png", "rb") as file:
            st.download_button("⬇️ Descargar imagen", file, "grafico_taladros.png")