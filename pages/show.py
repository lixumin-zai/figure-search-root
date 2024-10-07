import pandas as pd
import streamlit as st
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

if 'search_wechat_id_text' not in st.session_state:
    st.session_state.search_wechat_id_text = ""
if 'search_code_text' not in st.session_state:
    st.session_state.search_code_text = ""

if 'data_df' not in st.session_state:
    st.session_state.data_df = pd.DataFrame(db.get_users(), columns=["user_id", "wechat_id", "verification_code", "times", "extra_column"])

    # 去掉不需要的列（根据你的需求，这里去掉"verification_code"和"extra_column"）
    st.session_state.data_df = st.session_state.data_df.drop(columns=["extra_column"])

def search_all_user():
    st.session_state.data_df = pd.DataFrame(db.get_users(), columns=["user_id", "wechat_id", "verification_code", "times", "extra_column"])

    # 去掉不需要的列（根据你的需求，这里去掉"verification_code"和"extra_column"）
    st.session_state.data_df = st.session_state.data_df.drop(columns=["extra_column"])


st.session_state.process_data = []  
def updata():
    for i in st.session_state.process_data:
        if i[0] == -1:
            db.delete_user(i[1].wechat_id)
        elif i[0] == 0:
            db.updata_by_user_id(i[1].user_id, i[1].wechat_id, i[1].verification_code, i[1].times)
        else:
            db.create_user(i[1].wechat_id, i[1].verification_code)
    st.session_state.process_data = []
    st.session_state.data_df = pd.DataFrame(db.get_users(), columns=["user_id", "wechat_id", "verification_code", "times", "extra_column"])
    st.session_state.data_df = st.session_state.data_df.drop(columns=["extra_column"])


def search_by_wechat_id():
    if st.session_state.search_wechat_id_text:
        data = db.get_user_info_by_wechat_id(st.session_state.search_wechat_id_text)
        if data:
            st.session_state.data_df = pd.DataFrame(
                [data], columns=["user_id", "wechat_id", "verification_code", "times", "extra_column"])
            st.session_state.data_df = st.session_state.data_df.drop(columns=["extra_column"])
        else:
            st.session_state.data_df = pd.DataFrame(columns=["user_id", "wechat_id", "verification_code", "times"])
    else:
        updata()

def search_by_verification_code():
    if st.session_state.search_code_text:
        data = db.get_user_info_by_verification_code(st.session_state.search_code_text)
        if data:
            st.session_state.data_df = pd.DataFrame(
                [data], columns=["user_id", "wechat_id", "verification_code", "times", "extra_column"])
            # 去掉不需要的列（根据你的需求，这里去掉"verification_code"和"extra_column"）
            st.session_state.data_df = st.session_state.data_df.drop(columns=["extra_column"])
        else:
            st.session_state.data_df = pd.DataFrame(columns=["user_id", "wechat_id", "verification_code", "times"])
    else:
        updata()


col1, col2, col3, col4 = st.columns(4)
with col1:
    search_wechat_id_text = st.text_input("根据wechat_id搜索", key="search_wechat_id_text", on_change=search_by_wechat_id)
    

with col2:
    search_code_text = st.text_input("根据code搜索", key="search_code_text", on_change=search_by_verification_code)
    

with col3:
    col_1, col_2  = st.columns(2)
    with col_1:
        st.button("搜索所有用户", on_click=search_all_user)
    with col_2:
        st.button("保存所有修改", on_click=updata)


data_col1, data_col2 = st.columns(2)
with data_col1:
    st.markdown("<h3 style='text-align: center; color: black;'>修改操作表</h3>", unsafe_allow_html=True)
    updated_data_df = st.data_editor(
        st.session_state.data_df,
        column_config={
            "user_id": st.column_config.NumberColumn(
                "用户ID",
                help="Streamlit **widget** commands 🎈",
                width="small",
                default=-1,
                disabled=True,
                format="%d"  # 确保 user_id 为整数
            ),
            "wechat_id": st.column_config.Column(
                "微信号",
                help="微信号",
                width="medium",
                required=True,
            ),
            "verification_code": st.column_config.Column(
                "执行码",
                help="执行码",
                width="medium",
                required=True,
            ),
            "times": st.column_config.NumberColumn(
                "剩余",
                help="剩余使用次数",
                width="medium",
                required=True,
                default=15,
                min_value=0,
                step=1,
                format="%d"  # 确保 user_id 为整数
            ),
        },
        hide_index=True,
        num_rows="dynamic",
        height=700
    )



def compare_row_changes(df_before, df_after, index):
    # 提取修改前后的行数据
    row_before = df_before.loc[index]
    row_after = df_after.loc[index]
    
    # 创建输出字典
    output = {}
    
    for column in df_before.columns:
        output[f"{column}_before"] = row_before[column]
        output[f"{column}_after"] = row_after[column]
    
    return output


with data_col2:
    st.markdown("<h3 style='text-align: center; color: black;'>变化表</h3>", unsafe_allow_html=True)
    if updated_data_df is not None:
        # 标记差异的部分，用红色突出显示源表的变化
        def highlight_diff(data, updated_data):
            # 创建一个布尔掩码，找出不同的地方
            diff = data != updated_data

            # 判断 data 的每一行是否全部为 NaN
            full_nan_mask = data.isna().all(axis=1)
                    

            # 创建一个空的样式表
            styles = pd.DataFrame('', index=data.index, columns=data.columns)
            
            # 标记不同的地方为红色
            styles = np.where(diff, 'color: red', styles)
            
            # 对于 data 全行 NaN 的情况，标记 updated_data 的值为绿色
            styles[full_nan_mask, :] = 'background-color: lightgreen'
            data[full_nan_mask] = updated_data[full_nan_mask]

            return pd.DataFrame(styles, index=data.index, columns=data.columns)
        
        # 找出有差异的行
        # 原来的值，修改的值
        aligned_data, aligned_updated_data = st.session_state.data_df.align(updated_data_df, fill_value=np.nan)
        diff_mask = (aligned_data != aligned_updated_data).any(axis=1)

        # 只保留有差异的行
        data_with_diff = aligned_data[diff_mask]
        updated_data_with_diff = aligned_updated_data[diff_mask]

        
        
        # 应用样式
        styled_diff_df = data_with_diff.style.apply(highlight_diff, 
                                                    updated_data=updated_data_with_diff, axis=None)
        
        st.dataframe(
            styled_diff_df,
            column_config={
                "user_id": st.column_config.NumberColumn(
                    "用户ID",
                    help="用户ID",
                    width="small",
                    default=0,
                    disabled=True
                ),
                "wechat_id": st.column_config.Column(
                    "微信号",
                    help="微信号",
                    width="medium",
                    required=True,
                ),
                "verification_code": st.column_config.Column(
                    "执行码",
                    help="执行码",
                    width="medium",
                    required=True,
                ),
                "times": st.column_config.NumberColumn(
                    "剩余",
                    help="剩余使用次数",
                    width="medium",
                    required=True,
                    default=15,
                    min_value=0,
                    step=1
                ),
            },
            hide_index=True,
            height=700
        )
        full_nan_mask = data_with_diff.isna().all(axis=1)
        # data_with_diff[full_nan_mask] = updated_data_with_diff[full_nan_mask]
        # is_in = data_with_diff['user_id'].isin(updated_data_df['user_id'])
        # data_with_diff[is_in] = updated_data_df[is_in]
        data_with_diff.loc[full_nan_mask] = updated_data_with_diff.loc[full_nan_mask]
        for row1, row2, isin in zip(updated_data_with_diff.itertuples(), data_with_diff.itertuples(), data_with_diff['user_id'].isin(updated_data_df['user_id'])):
            if isin:
                if row2.user_id==-1.0:
                    st.session_state.process_data.append([1, row2])
                else:
                    st.session_state.process_data.append([0, row1])
            else:
                st.session_state.process_data.append([-1, row2])
        styled_diff_df = []
                    
        
# streamlit run show.py

# docker run --network host --name nginx -v /root/software/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /root/software/nginx/conf/conf.d:/etc/nginx/conf.d -v /root/software/nginx/log:/var/log/nginx -v /root/software/nginx/html:/usr/share/nginx/html -d nginx:latest