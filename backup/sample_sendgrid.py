# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

# Unix
"""
echo "export SENDGRID_API_KEY='<sendgrid-api-key>'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
"""

# windows cmd/powershell, python3 terminal
"""
>>> import os
>>> os.environ["SENDGRID_API_KEY"] = "<sendgrid-api-key>"
>>> print(os.environ["SENDGRID_API_KEY"])
"""

"""
pip install sendgrid
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


message = Mail(
    from_email='indranil.pal.test@gmail.com',
    to_emails='indra.tutun@gmail.com',
    subject='Sending with Twilio SendGrid for testing',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')

try:
    os.environ['SENDGRID_API_KEY'] = "<sendgrid-api-key>"
    print("SENDGRID_API_KEY", os.environ.get('SENDGRID_API_KEY'))
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(f"{response.status_code = }")
    print(f"{response.body = }")
    print(f"{response.headers = }")
except Exception as e:
    print(f"{e = }")


# import sendgrid
#
# sg = sendgrid.SendGridClient("YOUR_SENDGRID_API_KEY")
# message = sendgrid.Mail()
#
# message.add_to("test@sendgrid.com")
# message.set_from("you@youremail.com")
# message.set_subject("Sending with SendGrid is Fun")
# message.set_html("and easy to do anywhere, even with Python")
# sg.send(message)

