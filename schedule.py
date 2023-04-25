import tkinter as tk
from tkinter import messagebox
import smtplib
import schedule
import time
from datetime import datetime

class EmailScheduler:
    def __init__(self, master):
        self.master = master
        master.title("Email Scheduler")

        self.time_label = tk.Label(master, text="Enter email send time (24-hour format):")
        self.time_label.pack()

        self.time_entry = tk.Entry(master)
        self.time_entry.pack()

        self.date_label = tk.Label(master, text="Enter email send date (YYYY-MM-DD format):")
        self.date_label.pack()

        self.date_entry = tk.Entry(master)
        self.date_entry.pack()

        self.schedule_button = tk.Button(master, text="Schedule Email", command=self.schedule_email)
        self.schedule_button.pack()

        self.cancel_button = tk.Button(master, text="Cancel", command=master.quit)
        self.cancel_button.pack()

    def send_email(self):
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Use 465 for SSL or 587 for TLS
        sender_email = "kvreddy4884@gmail.com"
        sender_password = "dpky xyir xxie wuey"
        receiver_email = "sunnysathwik369@gmail.com"

        # Create the email message
        #message = "Subject: Test Email\n\nThis is a test email sent using Python."
        message = "Subject"

        # Log in to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)

    def schedule_email(self):
        time_str = self.time_entry.get()
        date_str = self.date_entry.get()
        try:
            dt_str = date_str + ' ' + time_str
            scheduled_time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            schedule.every().day.at(scheduled_time.strftime('%H:%M')).do(self.send_email)
            messagebox.showinfo("Email Scheduled", "Email will be sent on {} at {}".format(date_str, time_str))
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY-MM-DD HH:MM")

root = tk.Tk()
email_scheduler = EmailScheduler(root)
root.mainloop()

# Keep running the script until the scheduled time has passed
while True:
    schedule.run_pending()
    time.sleep(1)
print("mail sent successfully")

