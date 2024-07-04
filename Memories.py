import streamlit as st

def welcome_page():
    st.title('Welcome to Face Recognition App')
    st.write("""
        Upload your photos and videos with friends, and use facial recognition to identify each person.
        Search for a specific friend's name to see all the photos and videos they appear in.
    """)

if __name__ == '__main__':
    welcome_page()
