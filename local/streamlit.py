import streamlit as st
import pandas as pd

 
session_key='data_source'
 
track_data = 'Track My Data'
if session_key not in st.session_state:
    data_source = pd.DataFrame({
        "Person": ["Bill","Sally","Bill","Sally","Bill","Sally","Bill","Sally","Bill"],
        track_data:  [15, 10, 30, 13, 8, 70, 17, 83, 70],
        "Date": ["2022-1-23", "2022-1-30", "2022-1-5", "2022-2-21", "2022-2-1", "2022-2-2", "2022-3-1", "2022-3-3", "2022-3-6"]
    })
    data_source['Date'] = pd.to_datetime(data_source['Date'])
    st.session_state[session_key] = data_source
 
 
def save_session():
   filtered_line_chart = st.session_state[session_key].query(
       "Date >= @start_date "
   )
   filtered_line_chart =  st.session_state[session_key]
 
def clear_data():
   st.session_state[session_key]  = pd.DataFrame()
 
 
with st.sidebar.form("my_form"):
    input_person = st.selectbox(
     'Who would you like to enter a ' + track_data + ' for?',
     ('Bill', 'Sally'))
 
    input_weight = st.text_input(track_data + " input")
    input_date = pd.to_datetime(st.date_input("Date input"))
   
 
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        data_source = st.session_state[session_key]
       
        data_source = data_source.append({track_data:int(input_weight),"Person":input_person,"Date":  pd.to_datetime(input_date)},ignore_index=True)
       
        st.session_state[session_key] = data_source
 
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
     # To read file as bytes:
      bytes_data = uploaded_file.getvalue()
      st.write(bytes_data)
 
     
      dataframe = pd.read_csv(uploaded_file)
      st.write(dataframe)
 
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')
 
csv = convert_df(st.session_state[session_key])      
   
 
col1, col2, col3= st.columns(3)
with col1:
   start_date = st.date_input(
     "Show " + track_data + " after this date",
     None)
 
   start_date = pd.to_datetime(start_date)
   filter_date_button = st.button('Filter',on_click=save_session)
 
 
with col2:
  st.write("")
 
 
with col3:
    if st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name=track_data + "_records.csv",
     mime='text/csv',
    ):
     st.write(' Data Downloaded')
    clear_data = st.button("Clear Data", on_click=clear_data)
 
 
if filter_date_button:
  filtered_line_chart =  st.session_state[session_key].query(
    "Date >= @start_date ")
else:
  filtered_line_chart = st.session_state[session_key]
 
if not st.session_state[session_key].empty:
    st.line_chart(filtered_line_chart)
else:
    st.write("All Data has been cleared")