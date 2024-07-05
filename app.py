import openai
import streamlit as st
from lida import Manager, TextGenerationConfig , llm 
from dotenv import load_dotenv
import os
import io
from PIL import Image
from io import BytesIO
import base64

load_dotenv()

openai.api_key = os.getenv("Open_api_key")

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

lida = Manager(text_gen= llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5 , model="gpt-3.5-turbo-16k", use_cache= True)

menu = st.sidebar._selectbox("Choose an option", ["Summarize", "Question based Graph"])
if menu == "Summarize":
    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your file", type="csv")
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save , "wb")as f:
            f.write(file_uploader.getvalue())
            summary = lida.summarize("filename.csv" , summary_method="default", textgen_config=textgen_config)
            st.write(summary)
            goals = lida.goals(summary, n=2 , textgen_config=textgen_config)
            for goal in goals:
                st.write(goal)
            i = 0
            library = "matplotlib"
            textgen_config = TextGenerationConfig(n=1 , temperature=0.2, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)

            img_base64_string = charts[0].raster
            img =base64_to_image(img_base64_string)
            st.image(img)

elif menu == "Question based Graph":
    st.subheader("QUery your data to generate Graph")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save , "wb")as f:
            f.write(file_uploader.getvalue())

            text_area = st.text_area("Query your data to generate Graph", height=200)
            if st.button("Generate Graph"):
                if len(text_area) > 0:
                    st.info("Your query: "+ text_area)
                    lida = Manager(text_gen= llm("openai"))             
                    textgen_config = TextGenerationConfig(n=1 , temperature=0.2, use_cache=True)
                    summary = lida.summarize("filename.csv" , summary_method="default", textgen_config=textgen_config)
                    user_query = text_area
                    charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
                    charts[0]
                    image_base64 = charts[0].raster
                    img = base64_to_image(image_base64)
                    st.image(img)