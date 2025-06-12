import cv2
import os
import json
import shutil
from PIL import Image

EMAILS_FILE = "emails.json"

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def is_valid_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(50, 50))
    return len(faces) > 0

def take_pictures_and_save_cli(folder_path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    poses = ["forward", "right", "left", "up", "down"]
    print("You will be asked to look in the following directions: forward, right, left, up, and down.")
    for pose in poses:
        print(f"Please look {pose}. Press SPACE to capture, or ESC to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read the frame.")
                break
            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1)
            if key == 27:  # ESC
                print("Capture cancelled.")
                cap.release()
                cv2.destroyAllWindows()
                return
            elif key == 32:  # SPACE
                if is_valid_face(frame):
                    file_name = os.path.join(folder_path, f"captured_image_{pose}.jpg")
                    cv2.imwrite(file_name, frame)
                    print(f"Image for pose '{pose}' saved to {file_name}")
                    break
                else:
                    print("No valid face detected. Please try again.")
        cv2.destroyAllWindows()
    cap.release()
    print("All pictures captured.")

def import_image_and_save_cli(folder_path):
    file_path = input("Enter the path to the image file to import: ").strip()
    if file_path and os.path.isfile(file_path):
        dest_path = os.path.join(folder_path, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)
        print(f"Image imported to {dest_path}")
    else:
        print("No valid file selected.")

def load_emails():
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_emails(emails):
    with open(EMAILS_FILE, "w") as f:
        json.dump(emails, f, indent=4)

def cli_main():
    print("SigmaBoys - Add People (CLI Version)")
    person_name = input("Enter the name of the person: ").strip()
    if not person_name:
        print("Error: Please enter a valid name.")
        return
    person_email = input("Enter the email of the person: ").strip()
    if not person_email:
        print("Error: Please enter a valid email.")
        return

    emails = load_emails()
    if person_email in emails.values():
        print(f"Error: The email '{person_email}' is already registered.")
        return
    if person_name in emails:
        print(f"Error: The person '{person_name}' is already registered.")
        return

    folder_path = os.path.join("personas_autorizadas", person_name)
    create_folder(folder_path)

    emails[person_name] = person_email
    save_emails(emails)

    print("Choose an option:")
    print("1. Take Pictures")
    print("2. Import Image")
    option = input("Enter 1 or 2: ").strip()
    if option == "1":
        take_pictures_and_save_cli(folder_path)
    elif option == "2":
        import_image_and_save_cli(folder_path)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    cli_main()
