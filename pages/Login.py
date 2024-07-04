# import streamlit as st
# import cv2
# import numpy as np
# import os
# import mediapipe as mp
# # Function to authenticate user based on username and password
# def authenticate_user(username, password):
#     for face_id, data in face_encodings_db.items():
#         if data['username'] == username and data['password'] == password:
#             return data['name']
#     return None

# # Streamlit UI for login page
# def login_page():
#     st.title('Face Login')

#     username = st.text_input('Enter your username')
#     password = st.text_input('Enter your password', type='password')

#     uploaded_file = st.file_uploader("Upload an image for authentication", type=["jpg", "jpeg", "png"])
#     if uploaded_file is not None:
#         image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
#         image = cv2.imdecode(image, -1)

#         st.image(image, caption='Uploaded Image', use_column_width=True)

#         if st.button('Login'):
#             face_image = detect_face(image)
#             if face_image is not None:
#                 authenticated_name = authenticate_user(username, password)
#                 if authenticated_name is not None:
#                     st.success(f'Welcome, {authenticated_name}!')
#                 else:
#                     st.warning('Authentication failed. Please try again.')
#             else:
#                 st.warning('No face detected in the uploaded image.')

# # Main function to run the Streamlit app
# def main():
#     login_page()

# if __name__ == '__main__':
#     main()
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

# Streamlit UI for login page
def login_page():
    st.title('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if username and password:
            # Check if username and password match in the database
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()

            if user:
                st.success(f'Logged in as {user[1]}')
                main_app(user)
            else:
                st.error('Invalid username or password. Please try again.')

# Main application structure after login
def main_app(user):
    st.title('Face Recognition App')

    st.write(f'Welcome, {user[1]}!')

    uploaded_file = st.file_uploader("Upload a photo or video", type=["jpg", "jpeg", "png", "mp4"])

    if uploaded_file is not None:
        file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)

        # Convert uploaded file to image/video and process with facial recognition (to be implemented)
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        if uploaded_file.type == "image/jpeg" or uploaded_file.type == "image/png":
            image = cv2.imdecode(file_bytes, 1)
            st.image(image, caption='Uploaded Image', use_column_width=True)
        elif uploaded_file.type == "video/mp4":
            st.video(uploaded_file)
        else:
            st.error('Unsupported file format. Please upload an image or video.')

# Main function to run the Streamlit app
def main():
    login_page()

if __name__ == '__main__':
    main()
