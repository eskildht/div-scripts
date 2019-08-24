from email.mime.text import MIMEText
import smtplib
import random, time


def spam(to_mail, spoofs):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()

    from_mail = "yurtyurtyurt67@gmail.com"
    s.login(from_mail, "yurtyurtyurtyurt")

    switch = True

    for x in range(spoofs):
        content = ""
        for y in range(random.randint(10, 30)):
            c = random.randint(97, 126)
            content += chr(c)

        me = from_mail
        you = to_mail
        msg = MIMEText(content)
        msg['Subject'] = "Cnt " + str(x + 1)
        msg['From'] = from_mail
        msg['To'] = "AnythingWillDoForTo"

        s.sendmail(me, [you], msg.as_string())
        print("\temail nr " + str(x + 1) + " sent msg -> " + content)

        if (x + 1) % 50 == 0:
            s.quit()
            print("Sleeping for 60 seconds, and switching sender to not overflow.")
            time.sleep(60)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()

            if switch:
                from_mail = "yurtyurtyurt68@gmail.com"
                s.login(from_mail, "yurtyurtyurtyurtyurt")
                switch = False
            else:
                from_mail = "yurtyurtyurt67@gmail.com"
                s.login(from_mail, "yurtyurtyurtyurt")

    s.quit()


def main():
    to_mail = input("Enter To-mail: ")
    spoofs = int(input("Enter number of emails: "))

    spam(to_mail, spoofs)

    print("Done")


if __name__ == '__main__':
    main()