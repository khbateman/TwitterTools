import imaplib
import email
# import pprint

# def get_mail(host, username, password):
#     # connect to host using SSL
#     imap = imaplib.IMAP4_SSL(host)

#     # login to server
#     imap.login(username, password)

#     imap.select('Inbox', readonly = True)

#     tmp, data = imap.search(None, 'ALL')

#     for num in data[-1].split():
#         tmp, data = imap.fetch(num, '(RFC822)')
#         print('Message: {0}\n'.format(num))
#         break

#     imap.close()

# from imap_tools import MailBox, A
from datetime import datetime, date, timedelta

def get_recent_emails(host, username, password, num_emails = 3):

    # Get emails within the last week 
    one_week_ago = datetime.today() - timedelta(days = 3)

    imap = imaplib.IMAP4_SSL(host)
    imap.login(username, password)
    imap.select('Inbox', readonly = True)

    response, msg_numbers = imap.search(None, 'ALL')
    msg_numbers_string = msg_numbers[0]

    for num in msg_numbers_string.split()[-num_emails:]:
        _, data = imap.fetch(num, '(RFC822)')

        message_data = email.message_from_bytes(data[0][1])

        print(message_data.get('From'))
        print(message_data.get('Date'))

        for part in message_data.walk():
            if part.get_content_type() == "text/html":
                print(part.get_payload())
    
    imap.close()


    # # get list of email bodies from INBOX folder
    # with MailBox(host).login(username, password, 'INBOX') as mailbox:
    #     responses = mailbox.idle.wait(timeout=5)
    #     if responses:
    #         for message in mailbox.fetch(A(date_gte = one_week_ago.date()), limit = num_emails):
    #         # for message in mailbox.fetch(A(from_='rw@inspiredhygiene.com')):
    #             print(message.html)

