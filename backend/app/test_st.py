import streamlit as st



def change():
    print(st.session_state.checker)

state = st.checkbox(label="Say Hi!", value=False, on_change=change, key="checker")

radio_btn = st.radio("radio btn label: ", options=("a", "b", "c"))


def clicked():
    print("btn click")

btn = st.button("click here", on_click=clicked)

select = st.selectbox("your option: ", options=("a", "b", "c"))
print(select)

mulselect = st.multiselect("selecr", options=("a", "b", "c"))
st.write(mulselect)

image = st.file_uploader("upload here:", type=["png", "jpg"])
if image is not None:
    st.image(image)






