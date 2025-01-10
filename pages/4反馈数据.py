import streamlit as st

from PIL import Image
import time
import io
import base64
import os
import datetime


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

image_path_root = "/root/project/figure_search/feedback"

if 'search_wechat_id_text' not in st.session_state:
    st.session_state.search_wechat_id_text = ""
if 'search_code_text' not in st.session_state:
    st.session_state.search_code_text = ""

if 'start_datetime' not in st.session_state:
    st.session_state.start_datetime = datetime.datetime.now()
if 'end_datetime' not in st.session_state:
    st.session_state.end_datetime = datetime.datetime.now()

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

with col3:
    start_date = st.date_input("开始日期", datetime.datetime.now())
    end_date = st.date_input("结束日期", datetime.datetime.now())
with col4:
    start_time = st.time_input("Set an alarm for", datetime.time(0, 0))
    end_time = st.time_input("Set an alarm for", datetime.time(23, 59))

st.session_state.start_datetime = datetime.datetime.combine(start_date, start_time)
st.session_state.end_datetime = datetime.datetime.combine(end_date, end_time)

# with st.sidebar:
#     st.session_state.choose_page  = st.select_slider(
#         "选择页数",
#         options=[i for i in range(1, len(st.session_state.images_data)//10+1)],
#     )   
#     print(st.session_state.choose_page)


def get_image_by_time(image_name_list):
    # 将字符串转换为 datetime 对象
    date_time_objects = [
        (image_name, datetime.datetime.strptime(image_name.split("|")[1].split(".")[0], '%Y-%m-%d-%H-%M-%S')) for image_name in image_name_list if not ("bini" in image_name or "lixumin" in image_name or "9f2734c4-4d35-4bb5-9a83-2097d230830d" in image_name)
    ]

    # 筛选出在 2023 年 10 月 9 日之后的日期
    filtered_dates = [dt for dt in date_time_objects if st.session_state.start_datetime < dt[1] < st.session_state.end_datetime]

    sorted_dates = sorted(filtered_dates, key=lambda x:x[1])
    return [i[0] for i in sorted_dates]


if st.session_state.search_code_text:
    image_name = os.listdir(image_path_root)
    search_images_name = [i for i in image_name if i.startswith(st.session_state.search_code_text)]
    search_images_name = sorted(search_images_name)
    for idx, image_name in enumerate(search_images_name[::-1]):
        st.markdown(f":red[{image_name}]")
        st.image(f"{image_path_root}/{image_name}", width=300)
        st.markdown("---")
else:
    image_name_list = os.listdir(image_path_root)
    image_name_list = get_image_by_time(image_name_list)
    for idx, image_name in enumerate(image_name_list[::-1]):
        st.markdown(f":red[{image_name}]")
        st.image(f"{image_path_root}/{image_name}", width=300)
        st.markdown("---")

# ../show.png

# https://lismin.online:30000