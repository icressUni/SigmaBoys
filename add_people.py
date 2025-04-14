from tkinter import Tk, filedialog, Label, Button, Entry, StringVar, Toplevel, Radiobutton, Canvas
from PIL import Image, ImageTk
import cv2
import os
import json

EMAILS_FILE = "emails.json"

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def is_valid_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Increase the strictness of face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(50, 50))
    return len(faces) > 0

def take_pictures_and_save_with_gui(folder_path, canvas, video_label):
    if not folder_path or not os.path.exists(folder_path):
        video_label.config(text="Error: Please create a folder by entering your name first.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        video_label.config(text="Error: Could not open the camera.")
        return

    poses = ["forward", "right", "left", "up", "down"]
    video_label.config(text="You will be asked to look in the following directions: forward, right, left, up, and down.")
    picture_count = 0

    def update_frame():
        nonlocal picture_count
        ret, frame = cap.read()
        if not ret:
            video_label.config(text="Error: Could not read the frame.")
            return

        # Convert the frame to an image for tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor="nw", image=imgtk)

        if picture_count < len(poses):
            video_label.config(text=f"Currently capturing: Look {poses[picture_count]}.")
        canvas.after(10, update_frame)

    def capture_image():
        nonlocal picture_count
        ret, frame = cap.read()
        if ret and is_valid_face(frame):
            file_name = os.path.join(folder_path, f"captured_image_{poses[picture_count]}.jpg")
            cv2.imwrite(file_name, frame)
            video_label.config(text=f"Image for pose '{poses[picture_count]}' saved to {file_name}")
            picture_count += 1
            if picture_count >= len(poses):
                video_label.config(text="All pictures captured.")
                cap.release()
                return
        else:
            video_label.config(text="No valid face detected. Please try again.")

    def quit_capture():
        cap.release()
        video_label.config(text="Exiting capture.")
        canvas.after_cancel(update_frame)

    # Start updating the frame immediately
    update_frame()

    # Add buttons for capture and quit
    Button(canvas.master, text="Capture", command=capture_image).grid(row=3, column=0, padx=10, pady=5)
    Button(canvas.master, text="Quit", command=quit_capture).grid(row=3, column=2, padx=10, pady=5)

def import_image_and_save(folder_path):
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        file_name = os.path.join(folder_path, os.path.basename(file_path))
        os.rename(file_path, file_name)
        print(f"Image imported to {file_name}")
    else:
        print("No file selected.")

def load_emails():
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_emails(emails):
    with open(EMAILS_FILE, "w") as f:
        json.dump(emails, f, indent=4)

def gui_main():
    def start_capture():
        person_name = name_var.get().strip()
        person_email = email_var.get().strip()
        
        if not person_name:
            status_label.config(text="Error: Please enter a valid name.")
            return
        if not person_email:
            status_label.config(text="Error: Please enter a valid email.")
            return

        # Load existing emails
        emails = load_emails()

        # Check if the email is already registered
        if person_email in emails.values():
            status_label.config(text=f"Error: The email '{person_email}' is already registered.")
            return

        # Check if the name is already registered
        if person_name in emails:
            status_label.config(text=f"Error: The person '{person_name}' is already registered.")
            return

        folder_path = os.path.join("personas_autorizadas", person_name)
        create_folder(folder_path)

        # Save the email to the JSON file
        emails[person_name] = person_email
        save_emails(emails)

        # Replace the "Start" button with a "Capture" button and start capturing images
        start_button.grid_forget()
        take_pictures_and_save_with_gui(folder_path, video_canvas, status_label)

    root = Tk()
    root.title("SigmaBoys - Add People")

    Label(root, text="Enter the name of the person:").grid(row=0, column=0, padx=10, pady=5)
    name_var = StringVar()
    Entry(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Enter the email of the person:").grid(row=1, column=0, padx=10, pady=5)
    email_var = StringVar()
    Entry(root, textvariable=email_var).grid(row=1, column=1, padx=10, pady=5)

    Label(root, text="Choose an option:").grid(row=2, column=0, padx=10, pady=5)
    option_var = StringVar(value="1")
    Radiobutton(root, text="Take Pictures", variable=option_var, value="1").grid(row=2, column=1, padx=10, pady=5)
    Radiobutton(root, text="Import Image", variable=option_var, value="2").grid(row=2, column=2, padx=10, pady=5)

    start_button = Button(root, text="Start", command=start_capture)
    start_button.grid(row=3, column=1, padx=10, pady=10)

    status_label = Label(root, text="Please enter your name and email to create a folder before taking pictures.")
    status_label.grid(row=4, column=0, columnspan=3, pady=10)

    # Add a canvas for video feed
    video_canvas = Canvas(root, width=640, height=480)
    video_canvas.grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
