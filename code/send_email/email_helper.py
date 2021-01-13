from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
import os
import smtplib
import codecs


class EmailNotifications:

    def __init__(self, mail_server, sender, logger):
        self.mail_server = mail_server
        self.sender = sender
        self.logger = logger

    def send_html_email(self, subject, recipients, html_template, **kwargs):

        self.logger.info('** compiling email message **')
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['to'] = recipients

        self.logger.info('** adding cc addresses **')
        if 'cc' in kwargs.keys():
            msg['cc'] = kwargs.get('cc')

        self.logger.info('** adding images **')
        if 'images' in kwargs.keys():
            for image_path in kwargs.get('images'):
                cid = os.path.basename(image_path)
                image_file = open(image_path, 'rb')
                image = MIMEImage(image_file.read())
                image_file.close()
                image.add_header('Content-ID', f'<{cid}>')
                msg.attach(image)

        self.logger.info('** adding attachments **')
        if 'attachments' in kwargs.keys():
            for attachment_path in kwargs.get('attachments'):
                attachment = MIMEApplication(open(attachment_path, 'rb').read())
                filename = os.path.basename(attachment_path)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)

        self.logger.info('** templating... **')
        template = codecs.open(html_template)
        body = template.read()

        # Common CEC Tags - Add your own find and replace tags here
        body = Template(body).safe_substitute(
            account_name=kwargs.get('account_name'),
            account_number=kwargs.get('account_number'),
            root_owner=kwargs.get('root_owner'),
            ad_groups=kwargs.get('ad_groups'),
            territory=kwargs.get('territory'),
            service=kwargs.get('service'),
            cost_centre=kwargs.get('cost_centre'),
            billing_team=kwargs.get('billing_team'),
            environment=kwargs.get('environment'),
            budget_owner=kwargs.get('budget_owner'),
            finance_analyst=kwargs.get('finance_analyst'),
            business_owner=kwargs.get('business_owner'),
            spark_service_ci=kwargs.get('spark_service_ci'),
            spark_support_group=kwargs.get('spark_support_group'),
            spark_request=kwargs.get('spark_request'),
            description=kwargs.get('description'),
            tenancy=kwargs.get('tenancy')
        )

        msg.attach(MIMEText(body, "html"))

        self.logger.info('** sending email message **')
        s = smtplib.SMTP(self.mail_server, '25')
        s.send_message(msg)
        s.quit()