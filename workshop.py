import pandas as pd
import streamlit as st
from streamlit import write
from transformers import pipeline
from google.cloud import firestore
import os


def app():
    db = firestore.Client.from_service_account_info(st.secrets["gcp_service_account"])
    st.text("Le meilleur workshop de l'année !!")
    sentence = st.text_input('Fill in the sentence you want to try then press enter:', 'Data science is [MASK].')
    unmasker = pipeline('fill-mask', model='distilbert-base-uncased')
    if "[MASK]" in sentence:
        result = unmasker(sentence)
        st.write(pd.DataFrame(result))
    else:
        st.warning("The sentence needs to contains [MASK]")
        
    if st.button("Store result in the database"):
        data = {
            u"table_results": result
        }
        db.collection("posts").document(sentence).set(data)
        st.success('Well Done !! ')
    

if __name__ == '__main__':

    app()

