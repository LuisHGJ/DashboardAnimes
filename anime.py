import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar dados
df = pd.read_csv("anime.csv", sep=",", decimal=".")

if "episodes" in df.columns:
    df["episodes"] = pd.to_numeric(df["episodes"], errors="coerce")

# Nota
if "rating" in df.columns:
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Ano
if "year" in df.columns:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

df["episodes"] = pd.to_numeric(df["episodes"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["members"] = pd.to_numeric(df["members"], errors="coerce")

st.title("Dashboard de Animes")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Animes", df.shape[0])

with col2:
    st.metric("Nota Média", round(df["rating"].mean(), 2))

with col3:
    st.metric("Média de Episódios", round(df["episodes"].mean(), 2))

with col4:
    mais_popular = df.loc[df["members"].idxmax()]
    st.metric("Anime Mais Popular", mais_popular["name"])

st.markdown("---")

# Distribuição das notas
st.subheader("Distribuição das Notas")
fig1 = px.histogram(df, x="rating", nbins=20,
                    title="Distribuição de Notas dos Animes")
st.plotly_chart(fig1, use_container_width=True)

# Top 10 gêneros
st.subheader("Top 10 Gêneros Mais Frequentes")
genre_series = df["genre"].dropna().str.split(",").explode().str.strip()
genre_counts = genre_series.value_counts().head(10).reset_index()
genre_counts.columns = ["Gênero", "Quantidade"]

fig2 = px.bar(genre_counts, x="Gênero", y="Quantidade",
              title="Top 10 Gêneros de Animes")
st.plotly_chart(fig2, use_container_width=True)

# Tipos de anime
st.subheader("Distribuição por Tipo")
fig3 = px.pie(df, names="type", title="Proporção de Tipos de Anime")
st.plotly_chart(fig3, use_container_width=True)