# import tkinter as tk
# from tkinter import ttk
# from pyttsx3 import init
# import threading

# # Initialize the TTS engine (once)
# engine = init()
# engine.setProperty('rate', 180)  # Default speed

# class TextToSpeechApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Text-to-Speech Reader")
#         self.root.geometry("700x550")
#         self.root.configure(bg="#f0f0f0")

#         # Title Label
#         title = tk.Label(root, text="Text-to-Speech Reader", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
#         title.pack(pady=15)

#         # Text Input Area
#         tk.Label(root, text="Enter or paste your text below:", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=20)

#         self.text_area = tk.Text(root, height=15, width=80, font=("Arial", 11), wrap="word", relief="solid", bd=1)
#         self.text_area.pack(padx=20, pady=10)

#         # Frame for controls
#         control_frame = tk.Frame(root, bg="#f0f0f0")
#         control_frame.pack(pady=10)

#         # Speed Label and Slider
#         tk.Label(control_frame, text="Speech Speed:", bg="#f0f0f0", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        
#         self.speed_var = tk.IntVar(value=180)
#         speed_scale = ttk.Scale(control_frame, from_=50, to=300, orient="horizontal", variable=self.speed_var, length=250)
#         speed_scale.pack(side=tk.LEFT, padx=10)

#         self.speed_label = tk.Label(control_frame, text="180", bg="#f0f0f0", font=("Arial", 11))
#         self.speed_label.pack(side=tk.LEFT, padx=5)

#         # Update speed label when slider moves
#         speed_scale.config(command=self.update_speed_label)

#         # Buttons Frame
#         button_frame = tk.Frame(root, bg="#f0f0f0")
#         button_frame.pack(pady=15)

#         self.read_button = tk.Button(button_frame, text="🔊 Read Aloud", font=("Arial", 14, "bold"),
#                                      bg="#4CAF50", fg="white", width=15, height=2, command=self.start_reading)
#         self.read_button.pack(side=tk.LEFT, padx=10)

#         self.stop_button = tk.Button(button_frame, text="⏹ Stop", font=("Arial", 14, "bold"),
#                                      bg="#f44336", fg="white", width=10, height=2, command=self.stop_reading, state=tk.DISABLED)
#         self.stop_button.pack(side=tk.LEFT, padx=10)

#         self.is_speaking = False

#     def update_speed_label(self, val):
#         speed = int(float(val))
#         self.speed_label.config(text=str(speed))
#         engine.setProperty('rate', speed)

#     def start_reading(self):
#         text = self.text_area.get("1.0", tk.END).strip()
#         if not text:
#             tk.messagebox.showwarning("Empty Text", "Please enter some text to read!")
#             return

#         if not self.is_speaking:
#             self.is_speaking = True
#             self.read_button.config(state=tk.DISABLED)
#             self.stop_button.config(state=tk.NORMAL)

#             # Run speech in a separate thread to avoid freezing GUI
#             thread = threading.Thread(target=self.speak_text, args=(text,), daemon=True)
#             thread.start()

#     def speak_text(self, text):
#         engine.say(text)
#         engine.runAndWait()

#         # After speaking is done
#         self.is_speaking = False
#         self.root.after(0, self.speaking_finished)

#     def speaking_finished(self):
#         self.read_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)

#     def stop_reading(self):
#         engine.stop()
#         self.is_speaking = False
#         self.read_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)


# # Run the app
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TextToSpeechApp(root)
#     root.mainloop()






import streamlit as st
import pyttsx3
import tempfile
import os

# Initialize TTS engine
engine = pyttsx3.init()

st.set_page_config(page_title="Text-to-Speech Reader", layout="centered")

# Title
st.title("🔊 Text-to-Speech Reader (Streamlit Version)")
st.write("Type or paste text below, adjust the speed, and click **Read Aloud**.")

# Text Input
text = st.text_area("Enter your text:", height=250)

# Speed Slider
speed = st.slider("Speech Speed", 50, 300, 180)
engine.setProperty("rate", speed)

# Button to Speak
if st.button("🔊 Read Aloud"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        # Generate temporary audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
        
        engine.save_to_file(text, temp_filename)
        engine.runAndWait()

        audio_file = open(temp_filename, "rb")

        st.audio(audio_file.read(), format="audio/mp3")

        audio_file.close()
        os.remove(temp_filename)

        st.success("Speech generated successfully!")

