import cv2
import matplotlib
import mediapipe as mp
import pyautogui
from gaze_tracking import GazeTracking
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from question import quiz_data

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
matplotlib.pyplot.switch_backend('Agg')
def answerSelected():
    a="center"
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()

        if gaze.is_right():
            a="right"
            break
            # text = "Looking right"
            # if landmark_points:
            #     landmarks = landmark_points[0].landmark
            #     left = [landmarks[145], landmarks[159]]
            #     if (left[0].y - left[1].y) < 0.004:
            #         text="clicked"
            #         # pyautogui.click()
            #         # pyautogui.sleep(1)
        elif gaze.is_left():
            a="left"
            break
            # text = "Looking left"
            # if landmark_points:
            #     landmarks = landmark_points[0].landmark
            #     left = [landmarks[145], landmarks[159]]
            #     if (left[0].y - left[1].y) < 0.004:
            #         pyautogui.click()
            #         pyautogui.sleep(1)  
        elif gaze.is_center():
            a="center"
        cv2.imshow("Demo", frame)
    return a
# Function to display the current question and choices
def show_question():
    question = quiz_data[current_question]
    qs_label.config(text=question["question"])
    # Display the choices on the buttons
    choices = question["choices"]
    for i in range(2):
        choice_btns[i].config(text=choices[i], state="normal")  # Reset button state

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled")
    
# Function to check the selected answer and provide feedback
def check_answer(choice):
    # Get the current question from the quiz_data list
    question = quiz_data[current_question]
    selected_choice = answerSelected()

    # Check if the selected choice matches the correct answer
    if selected_choice == question["answer"]:
        # Update the score and display it
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    # Disable all choice buttons and enable the next button
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

# Function to move to the next question
def next_question():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score and end the quiz
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
        root.destroy()


# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("600x500")
style = Style(theme="flatly")

# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Create the question label
qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

# Create the choice buttons
choice_btns = []
for i in range(2):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)
score = 0
score_label = ttk.Label(
    root,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)
next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)
current_question = 0
show_question()
root.mainloop()

