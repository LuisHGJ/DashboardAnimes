import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar dados
df = pd.read_csv("anime.csv", sep=",", decimal=".")

df = df.drop_duplicates()

for col in ["episodes", "rating", "year", "members"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "episodes" in df.columns:
    df["episodes"] = df["episodes"].fillna(df["episodes"].median())

if "rating" in df.columns:
    df["rating"] = df["rating"].fillna(df["rating"].mean())

if "year" in df.columns:
    df["year"] = df["year"].fillna(df["year"].mode()[0])

if "members" in df.columns:
    df["members"] = df["members"].fillna(0)

if "genre" in df.columns:
    df["genre"] = df["genre"].str.strip().str.title()

if "type" in df.columns:
    df["type"] = df["type"].str.strip().str.title()

if "year" in df.columns:
    df = df[df["year"].between(1900, 2025, inclusive="both")]

if "rating" in df.columns:
    df = df[df["rating"].between(0, 10, inclusive="both")]

if "episodes" in df.columns:
    df = df[df["episodes"] >= 0]

if "members" in df.columns:
    df = df[df["members"] >= 0]

df["episodes"] = pd.to_numeric(df["episodes"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["members"] = pd.to_numeric(df["members"], errors="coerce")

# Preparar lista de gêneros únicos
genre_series = df["genre"].dropna().str.split(",").explode().str.strip()
unique_genres = sorted(genre_series.unique())

# Preparar lista de ratings inteiros únicos
unique_ratings_int = sorted(df["rating"].dropna().apply(lambda x: int(x)).unique())

# Filtros na barra lateral
selected_genres = st.sidebar.multiselect("Gênero", unique_genres)
selected_types = st.sidebar.multiselect("Tipo", df["type"].unique())
selected_ratings = st.sidebar.multiselect("Avaliação", unique_ratings_int)

# Aplicar filtros
if selected_genres:
    df = df[df["genre"].apply(lambda x: any(g in x.split(",") for g in selected_genres) if pd.notnull(x) else False)]

if selected_types:
    df = df[df["type"].isin(selected_types)]

if selected_ratings:
    df = df[df["rating"].apply(lambda x: int(x) in selected_ratings if pd.notnull(x) else False)]



st.title("Dashboard de Animes")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Animes", df.shape[0])

with col2:
    st.metric("Nota Média", round(df["rating"].mean(), 2))

with col3:
    st.metric("Média de Episódios", round(df["episodes"].mean(), 2))

with col4:
    if not df.empty:
        mais_popular = df.loc[df["members"].idxmax()]
        st.metric("Anime Mais Popular", mais_popular["name"])
    else:
        st.metric("Anime Mais Popular", "N/A")

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
