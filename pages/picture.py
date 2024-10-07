import streamlit as st

from PIL import Image
import time
import io
import base64
import os


import pandas as pd
import numpy as np
from db_process import Database

st.set_page_config(
    page_title="图推搜索后台管理",  # 设置页面标题
    page_icon="🔍",  # 设置页面图标
    layout="wide",  # 可以选择"centered" 或 "wide"
    menu_items={
        'About': "[请添加飞书联系托马斯羊](https://www.feishu.cn/invitation/page/add_contact/?token=910q4204-4b5f-43a0-acd6-66cce399e2a3&amp;unique_id=wMk5MKmubTeopGkKkxsglg==)"
    }
)
db = Database("/root/project/figure_search/db/test_0928.db")

image_path_root = "/root/project/figure_search/public/upload/"

if 'search_wechat_id_text' not in st.session_state:
    st.session_state.search_wechat_id_text = ""
if 'search_code_text' not in st.session_state:
    st.session_state.search_code_text = ""


col1, col2, col3, col4 = st.columns(4)



def search_by_wechat_id():
    data = db.get_user_info_by_wechat_id(st.session_state.search_wechat_id_text)
    if data:
        st.session_state.search_code_text = data[2]
    else:
        st.session_state.search_code_text = ""

def search_by_verification_code():
    data = db.get_user_info_by_verification_code(st.session_state.search_code_text)
    if data:
        st.session_state.search_code_text = data[2]
    else:
        st.session_state.search_code_text = ""


with col1:
    search_wechat_id_text = st.text_input("根据wechat_id搜索", key="search_wechat_id_text", on_change=search_by_wechat_id)

with col2:
    search_code_text = st.text_input("根据code搜索", key="search_code_text", on_change=search_by_verification_code)


if st.session_state.search_code_text:
    image_name = os.listdir(image_path_root)
    search_images_name = [i for i in image_name if i.startswith(st.session_state.search_code_text)]
    for idx, image_name in enumerate(search_images_name):
        st.markdown(f":red[{image_name}]")
        st.image(f"{image_path_root}/{image_name}")
        st.markdown("---")


# ../show.png

# https://lismin.online:30000