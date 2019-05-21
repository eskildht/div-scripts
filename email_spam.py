from email.mime.text import MIMEText
import smtplib
import random

spoofs = int(input("Enter number of emails: "))
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("yurtyurtyurt67@gmail.com", "yurtyurtyurtyurt")

print("Sending emails...")
for x in range(spoofs):
    content = ""
    for y in range(random.randint(10, 30)):
        c = random.randint(97,126)
        content += chr(c)
    me = "yurtyurtyurt67@gmail.com"
    you = "test@gmail.com"
    msg = MIMEText(content)
    msg['Subject'] = "Cnt " + str(x)
    msg['From'] = "yurtyurtyurt67@gmail.com"
    msg['To'] = "hei@gmail.com"

    s.sendmail(me, [you], msg.as_string())
    print("\temail nr " + str(x+1) + " sent msg -> " + content) 

s.close()

print("Done")
