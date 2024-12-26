from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Get the absolute path to the static folder (ensure this points to your existing static folder)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'downloads')  # Points to 'static/downloads'

# Ensure the download folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/', '.': '.-.-.-', ',': '--..--'
}

TEXT_FROM_MORSE = {value: key for key, value in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def morse_to_text(morse_code):
    return ''.join(TEXT_FROM_MORSE.get(char, '') for char in morse_code.split())

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    input_text = ""
    mode = "text_to_morse"

    if request.method == "POST":
        input_text = request.form["textInput"]
        mode = request.form["mode"]

        if mode == "text_to_morse":
            result = text_to_morse(input_text)
        elif mode == "morse_to_text":
            result = morse_to_text(input_text)

    return render_template("index.html", result=result, input_text=input_text, mode=mode)

@app.route("/download", methods=["POST"])
def download():
    content = request.form["result"]  # Get the result from the form
    filename = "conversion_result.txt"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the content to a file
    with open(filepath, "w") as file:
        file.write(content)

    # Use send_from_directory to return the file for download
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
