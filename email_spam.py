from email.mime.text import MIMEText
import smtplib
import random, time


def spam(to_mail, spoofs):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()

    f = open("./email_spam_accounts.txt", "r")
    lines = f.readlines()
    f.close()
    
    account_1_username, account_1_password = lines[0].split(" ")[0], lines[0].split(" ")[1]
    account_2_username, account_2_password = lines[1].split(" ")[0], lines[1].split(" ")[1]
    
    from_mail = account_1_username
    s.login(from_mail, account_1_password)

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
                from_mail = account_2_username
                s.login(from_mail, account_2_password)
                switch = False
            else:
                from_mail = account_1_username
                s.login(from_mail, account_1_password)

    s.quit()


def main():
    to_mail = input("Enter To-mail: ")
    spoofs = int(input("Enter number of emails: "))

    spam(to_mail, spoofs)

    print("Done")


if __name__ == '__main__':
    main()
