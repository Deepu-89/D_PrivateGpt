import streamlit as st
import pandas as pd


st.title("Hello Stremlit World ! :100:")
# st write

st.write("hello stremlit")


l1 = [1, 2, 3]

l1

l2 = ["a", "b", "c"]

l2

l3 = dict(zip(l1, l2))
l3

d1 = pd.DataFrame({"first": [1, 2, 3, 4, 5], "second": list("abcde")})

d1


# widgets

name = st.text_input("your name")
if name:
    print(f"Hello {name}")


age = st.number_input("Yourage:", min_value=1, max_value=50, step=1)
print(f"age is : {age}")


st.divider()


click = st.button("clickme")
if click:
    st.write(f":goat:" * 3)

# check box

agree = st.checkbox("i agree")

if agree:
    st.write("We are in Agrement")


tumb = st.checkbox("continue", value=True)

if tumb:
    st.write(f":+1:" * 5)

showdata = st.checkbox("show Data")

if showdata:
    st.write(d1)
st.divider()
# radio

pf = ["marriage ", "head ache", "child", "happy"]

pf2 = st.radio("what is your favourate pet", pf, key="your pet", index=3)
st.write(f"your favourate pet: {pf2}")

st.divider()
# select widget( drop box)
cities = ["hyderabad", "delhi", "mumbai", "chennai"]

city = st.selectbox("your city", cities, index=0)

st.divider()

# slider

slide = st.slider("slider", value=10, min_value=0, max_value=50, step=2)
st.write(f"the value  if slide is {slide}")

# file upload

upload_file = st.file_uploader("upload your file", type=["txt", "csv", "xlxs"])
if upload_file:
    st.write(upload_file)
    if upload_file.type == "text/plain":
        from io import StringIO

        sting = StringIO(upload_file.getvalue().decode("utf-8"))
        st.write(sting.read())
    elif upload_file.type == "text/csv":
        import pandas as pd

        file = pd.read_csv(upload_file)
        st.write(file)
    else:
        import pandas as pd

        file = pd.read_excel(upload_file)
        st.write(file)

## layout
# sidebar
select_box = st.sidebar.selectbox("SELECT CONTRY", ["UK", "US", "CANADA", "AUSTRALIA"])
slider_side = st.sidebar.slider("Temp")

# columns
# same width columns
left, right = st.columns(2)

# creating random data
import random

data = [random.random() for _ in range(100)]

# now display data in right column you can do this by "with" or "."
# with right:
#     st.subheader("Line chart")
#     st.line_chart(data)
# with left:
#     st.subheader("barchart")
#     st.bar_chart(data)
right.subheader("linechart")
right.line_chart(data)
left.subheader("bar chart")
left.bar_chart(data)


# different width columns
col1, col2, col3 = st.columns([0.2, 0.5, 0.3])

col1.subheader("column 1")
col2.subheader("column2")
col3.write(data[:10])
# expander

with st.expander("click to expand"):
    st.bar_chart({"Data": [random.randint(2, 20) for _ in range(100)]})
    st.markdown("hello world ")
    st.image(
        "data:image/jpeg;base64,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"
    )
