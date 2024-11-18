import customtkinter as ctk
import pyttsx3
import google.generativeai as genai
import speech_recognition as s
import winsound
import threading

identity_questions = [
    "who are you", "what is your name", "what do you call yourself", "who made you",
    "who created you", "who developed you", "who is your creator", "what are you",
    "what is your purpose", "what is your job", "what do you do", "what's your name",
    "tell me about yourself", "tell me who you are", "describe yourself", "what is Byte",
    "what is this chatbot", "who's behind this", "who is behind you", "who's the developer",
    "who developed Byte", "who made Byte", "who created Byte", "what is your function",
    "what is your role", "what's your function", "what's your role", "are you an assistant",
    "are you a chatbot", "are you virtual", "what can you do", "what is a chatbot",
    "what do you want to do", "what's your goal", "what's your mission", "who made",
    "your name", "name"
]

engine = pyttsx3.init()

root = ctk.CTk()
root.title("Byte Assistant")
root.geometry('300x400')
root.iconbitmap('byte.ico')
root.resizable(False, False)

canvas = ctk.CTkCanvas(
    root, highlightthickness=0, bg='#242424', border=0, width=300, height=300
)
canvas.pack(side='bottom')

canvas_width = 300
canvas_height = 300

radius = 50
center_x = canvas_width / 2
center_y = canvas_height / 2

x0 = center_x - radius
y0 = center_y - radius
x1 = center_x + radius
y1 = center_y + radius

circle_id = canvas.create_oval(x0, y0, x1, y1, fill='#39E3FF')

speech_label = ctk.CTkLabel(root, text_color='#39E3FF', font=('Helvetica', 14, 'bold'))


def speak_async(answer):
    def speak_thread():
        engine.say(answer)
        engine.runAndWait()

    threading.Thread(target=speak_thread, daemon=True).start()


def ask():
    global circle_id

    canvas.delete(circle_id)

    canvas_width = 300
    canvas_height = 300

    radius = 100
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    x0 = center_x - radius
    y0 = center_y - radius
    x1 = center_x + radius
    y1 = center_y + radius

    circle_id = canvas.create_oval(x0, y0, x1, y1, fill='#39E3FF')

    root.update_idletasks()

    genai.configure(api_key="AIzaSyAlKf03HL60NkYNnyFWiH0dFI3flSZl95w")

    recognize = s.Recognizer()

    with s.Microphone() as mic:
        text = recognize.listen(mic)

    try:
        canvas.delete(circle_id)

        root.update_idletasks()

        canvas_width = 300
        canvas_height = 300

        radius = 50
        center_x = canvas_width / 2
        center_y = canvas_height / 2

        x0 = center_x - radius
        y0 = center_y - radius
        x1 = center_x + radius
        y1 = center_y + radius

        circle_id = canvas.create_oval(x0, y0, x1, y1, fill='#39E3FF')

        root.update_idletasks()

        winsound.PlaySound("Speech_sound.wav", winsound.SND_FILENAME)
        speech = "{}".format(recognize.recognize_google(text))

        # Truncate speech to 27 characters and add "..." if it's 28 characters or longer
        if len(speech) >= 28:
            speech = speech[:27] + "..."

        # Display speech in the label and pack it
        speech_label.configure(text=speech)
        speech_label.pack()
        root.update_idletasks()

        # Set a 2-second delay to forget the label
        root.after(2000, lambda: speech_label.pack_forget())

        print(speech)

        # Ensure case-insensitive matching
        question = speech.lower()

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        response = None
        for iq in identity_questions:
            if iq.lower() in question:
                response = "I am Byte, a virtual chatbot developed by Backspace Studios. My purpose is to assist with various tasks and engage in conversation."
                break

        # If not an identity question, process the question as usual
        if response is None:
            response = chat_session.send_message(speech).text

        # Remove any asterisks if present in the response
        response = response.replace("*", "")

        speak_async(response)

        print(response)

    except s.UnknownValueError:
        print("Sorry, I didn't catch that.")
        engine.say("Sorry, I didn't catch that.")
        engine.runAndWait()


# Function to trigger ask() using spacebar
def check_spacebar(event):
    ask()


root.bind("<space>", check_spacebar)

heading = ctk.CTkLabel(
    root, text="Byte Assistant", text_color='#39E3FF', font=('Helvetica', 35, 'bold')
)
heading.pack(pady=15)

submit_button = ctk.CTkButton(
    root,
    fg_color='#39E3FF',
    corner_radius=10,
    text="Speak",
    text_color='black',
    font=('Helvetica', 16, 'bold'),
    command=ask
)
submit_button.pack()

hint_label = ctk.CTkLabel(
    root,
    text="<Press spacebar or speak button to speak>",
    text_color='grey',
    font=('Helvetica', 13, 'bold')
)
hint_label.pack(pady=5)


# Handle close button (x)
def on_close():
    print("Closing Byte Assistant...")
    root.quit()


root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
