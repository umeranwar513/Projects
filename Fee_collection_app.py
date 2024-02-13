import json
import smtplib
from getpass import getpass
from tinydb import TinyDB, Query

class Student:
    def __init__(self, username, password, email, pending_fee):
        self.username = username
        self.password = password
        self.email = email
        self.pending_fee = pending_fee

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'pending_fee': self.pending_fee
        }

class FeeCollectionApp:
    def __init__(self):
        self.db = TinyDB('students_db.json')
        self.current_student = None

    def load_students(self):
        students_data = self.db.all()
        for student_data in students_data:
            student = Student(**student_data)
            if student.username not in self.db:
                self.db.insert(student.to_dict())

    def save_student(self, student):
        self.db.upsert(student.to_dict(), Query().username == student.username)

    def login(self):
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        student_data = self.db.get(Query().username == username)

        if student_data and student_data['password'] == password:
            self.current_student = Student(**student_data)
            print(f"Welcome, {username}!")
        else:
            print("Invalid credentials. Please try again.")

    def signup(self):
        username = input("Enter a new username: ")
        if self.db.get(Query().username == username):
            print("Username already exists. Please choose another one.")
            return

        password = getpass("Enter a password: ")
        email = input("Enter your email address: ")

        try:
            initial_pending_fee = float(input("Enter your initial pending fee: "))
        except ValueError:
            print("Invalid pending fee. Please enter a valid number.")
            return

        if initial_pending_fee < 0:
            print("Pending fee cannot be negative. Please enter a valid amount.")
            return

        student = Student(username, password, email, initial_pending_fee)
        self.save_student(student)
        self.current_student = student
        print("Account created successfully!")

    def display_fee_status(self):
        if self.current_student:
            print(f"Pending Fee: Rs{self.current_student.pending_fee}")
        else:
            print("Please log in first.")

    def pay_fee(self):
        if not self.current_student:
            print("Please log in first.")
            return

        try:
            amount = float(input("Enter the amount to be paid: "))
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        if amount <= 0:
            print("Amount should be greater than zero. Please enter a valid amount.")
            return

        if amount > self.current_student.pending_fee:
            print("Amount cannot exceed the pending fee. Please enter a valid amount.")
            return

        account_number = input("Enter your account number: ")
        bank_name = input("Enter your bank name: ")
        ifsc_code = input("Enter your IFSC code: ")

        # Process payment logic (not implemented here)
        # You can update the pending_fee, send email, etc.

        self.current_student.pending_fee -= amount
        self.save_student(self.current_student)

        print("Payment successful!")

        # Send email
        self.send_email()

    def send_email(self):
        if not self.current_student:
            print("Cannot send email. Please log in first.")
            return

        subject = "Payment Successful"
        body = f"Dear {self.current_student.username},\n\nYour payment of ${self.current_student.pending_fee} was successful."

        try:
            # Replace these values with your email credentials and settings
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "202101738@vupune.ac.in"
            sender_password = "Umeranwar@369"
            receiver_email = self.current_student.email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                message = f"Subject: {subject}\n\n{body}"
                server.sendmail(sender_email, receiver_email, message)

            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

    def run(self):
        self.load_students()

        while True:
            print("\nFee Collection App")
            print("1. Login")
            print("2. Signup")
            print("3. Display Fee Status")
            print("4. Pay Fee")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.signup()
            elif choice == '3':
                self.display_fee_status()
            elif choice == '4':
                self.pay_fee()
            elif choice == '5':
                print("Exiting Fee Collection App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = FeeCollectionApp()
    app.run()
