import streamlit as st
import streamlit.components.v1 as components
from db_process import Database
import uuid

db = Database("/root/project/figure_search/db/test_0928.db")


code_10 = ""
if st.button("生成10次用户"):
    new_code = str(uuid.uuid4())
    db.create_user_and_usage_count(new_code, new_code, 10)
    code_10 = f"小程序中使用: {new_code}\n网页链接使用: https://lismin.online:10003/?code={new_code}"
col1, col2 = st.columns([4, 2])
with col1:
    st.code(f"{code_10}")


code_100 = ""
if st.button("生成100次用户"):
    new_code = str(uuid.uuid4())
    db.create_user_and_usage_count(new_code, new_code, 100)
    code_100 = f"小程序中使用: {new_code}\n网页链接使用: https://lismin.online:10003/?code={new_code}"
col3, col4 = st.columns([4, 2])
with col3:
    st.code(f"{code_100}")


# 要复制的文本
# text_to_copy = "sdffsadfdasf"

# 使用 HTML 组件和 JS 实现复制功能
# components.html(f"""
#     <button onclick="copyToClipboard()">点击复制文本</button>
#     <script>
#         function copyToClipboard() {{
#             var text = "{text_to_copy}";
#             navigator.clipboard.writeText(text).then(function() {{
#                 alert('文本已成功复制到剪贴板！');
#             }}).catch(function(err) {{
#                 console.error('复制失败：', err);
#             }});
#         }}
#     </script>
#     """, height=100)



