import streamlit as st
import requests
from elasticsearch import Elasticsearch
import time

with open('./style.css','r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

client = Elasticsearch("http://localhost:9200",)


def check_server(client):
    if client.ping() == False:
        st.toast("Elastic Search Server Is Not Running!")

def display_results(query,searchtype):
    check_server(client)
    getreq = {
            searchtype: {"tags":query}
    }
    results = client.search(index="flicker", query=getreq) 
    cols = st.columns(2)
    col_heights = [0, 0]
    displayed_images = 0
    for hit in results["hits"]['hits']:
        if displayed_images >= 10:
            break
        image_data = hit["_source"]
        image= "http://farm"+image_data['flickr_farm']+".staticflickr.com/"+image_data['flickr_server']+"/"+image_data["id"]+"_"+image_data['flickr_secret']+".jpg"
        col_id = 0 if col_heights[0] <= col_heights[1] else 1
        with st.spinner("Loading Image"):
            response = requests.get(image)
            if response.status_code == 200:
                cols[col_id].image(image)
                col_heights[col_id] += 1
                displayed_images += 1
 
#__main__

if __name__ == "__main__" : 
 
    st.write('## Textual Search Bar')
    st.sidebar.write('# Search Features ')
    searchType = st.sidebar.selectbox('Select Search Type:', ['match','fuzzy'])

    with st.form("my_form"):
        query = st.text_input('Enter some text')
        submit = st.form_submit_button("Search")
        if submit :
            display_results(query,searchType)


