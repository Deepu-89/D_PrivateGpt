import streamlit as st


st.title("Session State")
st.write(st.session_state)

if "Counter" not in st.session_state:
    st.session_state["Counter"] = 0
else:
    st.session_state.Counter += 1


f"counter:{st.session_state.Counter}"


button = st.button("update State")

if "clicks" not in st.session_state:
    st.session_state["clicks"] = 0
else:
    st.session_state.clicks += 1
    f"After Pressing Button :{st.session_state}"


number = st.slider(label="myslider", min_value=1, max_value=10, key="myslider")
st.session_state
