# streamlit_client.py

import streamlit  as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000/api"

st.title("Notes App")

def create_notes():
    title = st.text_input("Enter Notes Title")
    content = st.text_input("Enter Notes Content")
    category = st.text_input("Enter Note Category")
    published = st.radio("Want to published?" , options=['Yes' , "No"] , key= [True , False] )
    if st.button("Save"):
        response = requests.post(f"{BASE_URL}/notes/", json={"title": title, "content": content , "category" : category , "published" : published})
        if response.status_code == 200:
            st.success("Notes added successfully")
            
    if st.button("Cancel"):
        main()

            
def delete_notes():
    notes_id = st.number_input("Enter notes ID to delete")
    if st.button("Delete notes"):
        response = requests.delete(f"{BASE_URL}/notes/{notes_id}")
        if response.status_code == 200:
            st.success("notes deleted successfully")

def update_notes_form_callback():
    print(st.session_state.notes_id)
    print(st.session_state.title)
    print(st.session_state.content)
    print(st.session_state.category)

    updated_data = {
        "title": st.session_state.title,
        "content": st.session_state.content,
        "category": st.session_state.category
    }

    response = requests.patch(f"{BASE_URL}/notes/{st.session_state.notes_id}" , json = updated_data)
    
    if response.status_code == 200:
        st.success("notes deleted successfully") 

def update_notes():

    notes_id = st.text_input("Enter notes ID to delete", key='notes_id')
    
    if st.button("Get"):
        response = requests.get(f"{BASE_URL}/notes/{notes_id}")
        
        if response.status_code == 200:
            
            with st.form(key='update_notes_form'):
                items = response.json()['note']
                
                st.text_input("Enter Notes Title" , key="title", value=items['title'])
                st.text_input("Enter Notes Content" , key="content", value=items['content'])
                st.text_input("Enter Note Category" , key="category", value=items['category'])
                
                st.form_submit_button(label='Update notes', on_click=update_notes_form_callback)

def main():
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     if st.button("Add Note"):
    #         create_notes()
    

    # with col2:
    #     if st.button("Edit Note"):
    #         update_notes()

    # with col3:
    #     if st.button("Delete Note"):
    #         delete_notes()

    create_notes()
    update_notes()
    delete_notes()
 
    response = requests.get(f"{BASE_URL}/notes/")
    if response.status_code == 200:
        st.table(response.json()['notes'])
        # st.data_editor("edit")

if __name__ == "__main__":
    main()