import streamlit as st
import IPython.display as ipd
import subprocess
import base64
import re
import os  # Add import for os module
from streamlit import cache

# Define a function to apply custom CSS
pathimage = r"C:\Users\50510\Downloads\blue-wavy-background-with-line-wave\yyuu14.jpg"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(pathimage)

st.title(':rainbow[Text to Speech Tamil] :notes:')

# Define custom CSS to style the text area and text color
# Define custom CSS to style the text area with a black background and white text color
custom_css = """
<style>
    /* Add a border to the text area */
    .custom-text-area {
        border: 1px solid #000; /* You can adjust the border properties as needed */
        border-radius: 5px;
        padding: 10px;
        background-color: black; /* Black background color */
        color: white; /* White text color */
    }
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

## Give Inputs
#  text = st.text_input("Enter your text:")

st.write("Enter your text Below:")
text = st.text_input("", key="text_input", help="Type your text here")



# Create a button for submitting
if st.button(':red[Enter]'):
    # Perform some action when the "Enter" button is clicked
    # st.write("You entered:", text)
    # Apply a CSS class to the text area div
    st.markdown('<div class="custom-text-area">' + text + '</div>', unsafe_allow_html=True)




## Preprocess the text

def remove_spaces_and_hyphens(texts):
    # Replace all hyphens (single or consecutive) with spaces
    t = texts.replace('-', ' ').replace('--', ' ')
    t = t.replace('"', ' ')
    t = t.replace('’', ' ')
    t = t.replace("'", ' ')
    t = t.replace("‘", ' ')
    t = re.sub('       +', " ", t)  ### For removing long spaces
    # Remove leading and trailing white spaces
    t = t.strip()

    # Remove extra spaces between words (if any)
    t = ' '.join(t.split())

    return t

hiphen_less = remove_spaces_and_hyphens(text)

cl_text = hiphen_less.strip()

# Change the numericals into word form
from num_to_words import num_to_word

def translate_numerals_to_words(text, lang='ta'):
    # Split the text into words
    words = text.split()

    # Initialize a list to store translated words
    translated_words = []

    for word in words:
        # Check if the word is a numeral (can be converted to a number)
        if word.isdigit():
            # Translate the numeral to words using your num_to_word function
            translated_word = num_to_word(int(word), lang=lang)
            translated_words.append(translated_word)
        else:
            # If it's not a numeral, leave it as it is
            translated_words.append(word)

    # Join the translated words into a single string
    translated_text = ' '.join(translated_words)
    
    return translated_text

cleaned_text = translate_numerals_to_words(cl_text, lang='ta')

# Path to the Models
model_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\best_model.pth"
config_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\config.json"
speakers_file_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\speakers.pth"
speaker_idx = "female"

# Define the output path
out_path = "output_audio.wav"

def run_tts_and_display_audio(text, model_path, config_path, out_path, speakers_file_path=None, speaker_idx=str):
    try:
        # Construct the command
        command = [
            "tts",  # Remove the "!" at the beginning
            f'--text "{text}"',
            f'--model_path "{model_path}"',
            f'--config_path "{config_path}"',
            f'--out_path "{out_path}"',
            f'--speakers_file_path "{speakers_file_path}"',
            f'--speaker_idx "{speaker_idx}"'
        ]

        # Join the command elements into a single string
        command_str = " ".join(command)

        # Run the TTS command using subprocess
        subprocess.run(command_str, shell=True, check=True)
        print("TTS completed successfully.")

        # Display the generated audio
        ipd.display(ipd.Audio(out_path))
    except subprocess.CalledProcessError as e:
        print("Error while running TTS:", e)

def Text_to_speech():
    st.header(':violet[The Audio File]', divider='rainbow')
    # Use the :color syntax within the header text to change the color
    # st.header(':violet[The Audio File]')

    run_tts_and_display_audio(cleaned_text, model_path, config_path, out_path, speakers_file_path, speaker_idx)

# Call the function to display the text-to-speech conversion
Text_to_speech()


# Display the generated audio using HTML audio tag
if os.path.exists(out_path):
    st.audio(open(out_path, 'rb').read(), format="audio/wav")