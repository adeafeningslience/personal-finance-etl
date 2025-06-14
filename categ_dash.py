import streamlit as st
import psycopg2
import pandas as pd

@st.cache_data
def get_categories():
    conn = psycopg2.connect(dbname="postgres", user="claytonwells", password="K%$h3lle", host="localhost")
    df = pd.read_sql("SELECT * FROM ref.categories ORDER BY id", conn)
    conn.close()
    return df

st.title("Personal Finance Categories")

df = get_categories()
st.dataframe(df)

new_id = st.number_input("New Category ID", min_value=1, step=1)
new_name = st.text_input("New Category Name")

if st.button("Add / Update Category"):
    conn = psycopg2.connect(dbname="postgres", user="claytonwells", password="K%$h3lle", host="localhost")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ref.categories (id, name)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
    """, (new_id, new_name))
    conn.commit()
    cursor.close()
    conn.close()
    st.success(f"Category '{new_name}' added/updated!")
    st.rerun()
