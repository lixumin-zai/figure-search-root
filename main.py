import streamlit as st

# st.write("图推搜索管理系统❤️❤️")
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    .image-container {
        display: flex;
        justify-content: center;
    }
    </style>
    <h1 class="title">图推搜索应用管理系统</h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align: center;">
        图形推理搜索是针对图形推理题目通过题目中图形的相似度从题库中匹配相同的带有答案的题目图片
        <img src="https://public-1259491855.cos.ap-beijing.myqcloud.com/mini.png" width="200" height="auto">
    </div>
    """,
    unsafe_allow_html=True
)
st.divider() 
st.image("./pages/show.png")
st.markdown(
    """
    <div style="text-align: center;">
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
# with col2:
# if st.button("操作 用户数据 界面"):
# st.switch_page("pages/用户管理.py")

# # if st.button("题库 数据 查看界面"):
# st.switch_page("pages/题库数据.py")

# # if st.button("用户 图片 查看界面"):
# st.switch_page("pages/拍摄数据.py")

# # if st.button("用户 反馈 查看界面"):
# st.switch_page("pages/反馈数据.py")

# # if st.button("生成执行码"):
# st.switch_page("pages/生成执行码.py")

# nohup streamlit run main.py > main.log &