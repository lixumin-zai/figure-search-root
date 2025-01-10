import streamlit as st
from answer_db_process import AnswerImageDB
import pandas as pd

import base64
from io import BytesIO
from streamlit_paste_clipboard import paste_clipboard

st.set_page_config(
    page_title="图推搜索后台管理",  # 设置页面标题
    page_icon="🔍",  # 设置页面图标
    layout="wide",  # 可以选择"centered" 或 "wide"
    menu_items={
        'About': "[请添加飞书联系托马斯羊](https://www.feishu.cn/invitation/page/add_contact/?token=910q4204-4b5f-43a0-acd6-66cce399e2a3&amp;unique_id=wMk5MKmubTeopGkKkxsglg==)"
    }
)

def image_to_base64(img):
    if img:
        raw_base64 = base64.b64encode(img).decode()
        return f"data:image/png;base64,{raw_base64}"


db = AnswerImageDB("answer.db")


col1_main, col2_main = st.columns([7,1])
st.session_state.images_data = db.search_all_image()

def delete_image(idx):
    db.delete_image(idx)
    st.session_state.images_data = db.search_all_image()


if "choose_page" not in st.session_state:
    st.session_state.choose_page = 1

with st.sidebar:
    st.session_state.choose_page  = st.select_slider(
        "选择页数",
        options=[i for i in range(1, len(st.session_state.images_data)//10+2)],
    )   
    print(st.session_state.choose_page)

with col1_main:
    print(st.session_state.choose_page)
    for idx, image_data in enumerate(st.session_state.images_data[(st.session_state.choose_page-1)*10:(st.session_state.choose_page)*10]):
        st.markdown(f"ID\: :red[{image_data[0]}]")
        col1, col2 = st.columns([4,1])
        with col1:
            st.image(image_data[1], width=300)
        with col2:
            st.button("删除",key=image_data[0], on_click=delete_image, args=(image_data[0],))
        st.markdown("---")



st.session_state.upload_image = None
st.session_state.paste_clipboard_image = None
@st.dialog("添加图片")
def insert_image():
    st.session_state.paste_clipboard_image = paste_clipboard()
    st.session_state.upload_image = st.file_uploader("", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    
    if st.button("Submit"):
        if st.session_state.paste_clipboard_image:
            with BytesIO() as image:
                st.session_state.paste_clipboard_image.save(image, "PNG")
                db.insert_image(image.getvalue())
        if st.session_state.upload_image:
            db.insert_image(st.session_state.upload_image.getvalue())
            st.session_state.upload_image = None
        st.session_state.images_data = db.search_all_image()
        st.rerun()
        
with st.sidebar:
    st.button("添加图片", key=-1, on_click=insert_image)
        
