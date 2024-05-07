import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

st.title("A first example")
st.write("Here we start to explore our first example in Streamlit")
st.header("Welcome here")

@st.cache_data
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/Stijnvhd/Streamlit_Course/main/First%20Example/diabetes.csv')
    return data

data = load_data()

# show data as table
st.subheader('Raw data')
st.dataframe(data)

# show basic data description
st.subheader('Data Description')
st.write(data.describe())

# different plots
st.subheader('Relation with outcome')

if st.sidebar.checkbox("Seaborn Pairplot", key="1"):
    fig = sns.pairplot(data = data, hue = 'Outcome')
    st.pyplot(fig)
if st.sidebar.checkbox("Histplot", key="2"):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    data.hist(alpha=0.5, figsize=(20, 10))
    plt.show()
    st.pyplot()

# elements in sidebar
agree = st.sidebar.button('Click to see nothing')

if agree:
    st.write("nothing")

st.subheader("An interesting table")
def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

selection = aggrid_interactive_table(df=data)

if selection:
    st.write("You selected:")
    st.write(selection["selected_rows"])