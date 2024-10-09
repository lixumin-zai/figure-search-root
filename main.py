import streamlit as st

st.write("🐑老板好❤️❤️")

if st.button("操作用户数据界面"):
    st.switch_page("pages/show.py")

if st.button("题库数据查看界面"):
    st.switch_page("pages/answer_db.py")

if st.button("用户数据查看界面"):
    st.switch_page("pages/picture.py")

if st.button("淘宝生成执行码"):
    st.switch_page("pages/create_user.py")
    
# streamlit run main.py