import streamlit as st
import cv2
import numpy as np
import sqlite3

# Initialize SQLite database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Function to convert image to binary
def image_to_binary(image):
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

# Streamlit UI for registration page
def registration_page():
    st.title('Face Registration')

    name = st.text_input('Enter your name')
    username = st.text_input('Enter a username')
    password = st.text_input('Enter a password', type='password')
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button('Register'):
        if name and username and password and uploaded_file:
            # Check if username already exists
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()

            if existing_user:
                st.error('Username already exists. Please choose a different username.')
            else:
                # Convert uploaded file to image and detect face
                image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(image, -1)

                # Process image to extract face encoding (use your face recognition code here)
                face_encoding = np.random.rand(128)  # Replace with actual face encoding

                # Add user to database
                add_user(name, username, password, face_encoding)

                st.success('Registration successful!')
                st.info('You can now proceed to login.')

# Function to add a user to the database
def add_user(name, username, password, face_encoding):
    c.execute("INSERT INTO users (name, username, password, face_encoding) VALUES (?, ?, ?, ?)",
              (name, username, password, image_to_binary(face_encoding)))
    conn.commit()

# Main function to run the Streamlit app
def main():
    registration_page()

if __name__ == '__main__':
    main()
