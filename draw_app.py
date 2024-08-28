# pip install streamlit streamlit_drawable_canvas

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import google.generativeai as genai
import json
import random



f = open("gemini_secret_key.txt")
KEY = f.read()
genai.configure(api_key=KEY)

model = genai.GenerativeModel(model_name='models/gemini-1.5-flash', system_instruction="""
                              Please analyze the given image and identify the object it represents. Your task is to classify the image into one of the following categories: Fish, Snake, Elephant, Sun, Moon, Star, Tree, Flower, House, Apple, Banana, Cake, Pizza, Ice Cream, Cookie, Donut, Cloud, Clock, Arrow, Key, Car, Book, Bed, Chair, Table, Door, Window, Lamp, Laptop, Shark, Hat, Smartphone, Television, Mango, Pineapple, Butterfly, or Rainbow. Kindly provide a clear and concise answer with the category name along with its accuracy. Here is an example:{"Category": "Apple", "Accuracy": 0.7}.Now a very important note: if the image appears completely white and does not contain any sketch, do not reply with anything""")

config = genai.GenerationConfig(response_mime_type="application/json", temperature=0)

st.set_page_config(
    page_title="Google QuickDraw Clone", page_icon="🎨"
)

st.title("QuickDraw Clone powered by Gemini")
st.markdown(
"""
Welcome to QuickDraw!
Unleash your inner artist and challenge our AI to guess your doodles. Draw, test, and see if our AI can keep up with your creativity. Let the fun begin! 
"""
)

if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = random.choice([
        "Fish", "Snake", "Elephant", "Sun", "Moon", "Star", "Tree", "Flower",
        "House", "Apple", "Banana", "Cake", "Pizza", "Ice Cream", "Cookie",
        "Donut", "Cloud", "Clock", "Arrow", "Key", "Car", "Book", "Bed",
        "Chair", "Table", "Door", "Window", "Lamp", "Laptop", "Shark", "Hat",
        "Smartphone", "Television", "Mango", "Pineapple", "Butterfly", "Rainbow"
    ])
if 'score' not in st.session_state:
    st.session_state.score = 0

col1, col2 = st.columns([0.7, 0.3])

with col1:
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == "point":
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#fff")

    # Canvas for drawing
    canvas_result = st_canvas(
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=False,
        width=480,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        key="full_app",
    )

with col2:
    with st.chat_message("assistant"):
        
        st.write(f"Sketch a picture of {st.session_state.current_prompt}")
        
        if canvas_result.image_data is not None:
            img = st.image(canvas_result.image_data)
            img_array = np.array(canvas_result.image_data)
            img = Image.fromarray(img_array)
            response = model.generate_content([img, "what is this image?"], generation_config=config)
            st.write(response.text)
            if response.text:
                dict_response = json.loads(response.text)
                if st.session_state.current_prompt == dict_response["Category"]:
                    st.session_state.score += 1
                else:
                    st.session_state.score -= 1
                st.write(f"Score: {st.session_state.score}")

                st.session_state.current_prompt = random.choice([
                    "Fish", "Snake", "Elephant", "Sun", "Moon", "Star", "Tree", "Flower",
                    "House", "Apple", "Banana", "Cake", "Pizza", "Ice Cream", "Cookie",
                    "Donut", "Cloud", "Clock", "Arrow", "Key", "Car", "Book", "Bed",
                    "Chair", "Table", "Door", "Window", "Lamp", "Laptop", "Shark", "Hat",
                    "Smartphone", "Television", "Mango", "Pineapple", "Butterfly", "Rainbow"
                ])
                