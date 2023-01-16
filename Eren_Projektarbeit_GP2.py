import streamlit as st
import pandas as pd
import mysql.connector


st.image("https://img.freepik.com/premium-vector/tourist-traditional-people-with-text-welcome-switzerland_18591-3759.jpg?w=2000")


URL = "https://raw.githubusercontent.com/gamba/swiss-geolocation/master/post-codes.csv"

st.title ("Schweizerische Postleitzahl")
st.header ("Suche Anhang von Ortsnamen")
@st.cache
def load_data():
    df_tmp = pd.read_csv(URL, header=3, dtype={"zip": str})
    df_tmp["DISTRICT"] = df_tmp.apply(lambda row: row.post_district.upper(), axis=1)
    return df_tmp

df = load_data()
# st.table(df.sample(10)) # Stichprobendaten anzeigen

lat = []
lon = []

#Verbindung zum mySQL Datenbank
dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456_",
    database = "swiss_data"
)

place = st.text_input("Ort einggeben: ")

df_result = df.query(f"DISTRICT.str.contains('{place.upper()}')", engine='python')

if len(df) == len(df_result):
    st.info("Bitte einen Ort eingeben")
else:
    if df_result.empty:
        st.warning("Ort nicht gefunden!")
    else:
        df_display = df_result.set_index('zip').rename_axis('PLZ', axis=1)
        df_display = df_display[["town"]]
        df_display.index.name = None

        # DB zugriff um mit dem Ortsnamen die lat und lon auszulesen
        # Die ausgelesenen Werte in die liste lat und long abfüllen
    
        place = [place]
        mycursor = dataBase.cursor()
        mycursor.execute("SELECT latitude, longitude from data_bereinigt where place = %s", place)

        whole_table = mycursor.fetchall()

        # Iteration über liste (for schleife)
        for result in whole_table:
            lat.append(result[0])
            lon.append(result[1])
            
 
        # List append nutzen, um werte der liste lon und att hinzuzufügen
        mycursor.close()
        st.table (whole_table)
        
        st.write(df_display.to_html(), unsafe_allow_html=True)


coordinates = pd.DataFrame ({
    "lat": lat,
    "lon": lon
    
})

st.write(coordinates)

st.map(coordinates)

import pydeck as pdk

@st.cache

def from_data_file(filename):
    url = ("https://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/%s" % filename)
    return pd.read_json(url)


st.header ("Gesamte Tabelle - Hauptübersicht")
data = pd.read_csv("data_bereinigt.csv") #path folder of the data file
st.write(data) #displays the table of data
