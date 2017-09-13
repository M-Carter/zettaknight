#!/usr/bin/python
#Matthew Carter 2017

import smtplib
import os
import mimetypes
import json

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer:

    def __init__(self, sender):
    
        self.sender = sender
        self.mail = MIMEMultipart()
    
    def send(self, recipients, subject, message, attachments = None):
    
        try:
            self.mail['Subject'] = str(subject)
            self.mail['From'] = str(self.sender)
            
            if isinstance(recipients, str):
                self.mail['To'] = recipients
            else:
                self.mail['To'] = ', '.join(recipients)
            
            m = MIMEText('{0}\n\n'.format(message))
            self.mail.attach(m)
            
            if attachments:
                for attachment in attachments:
                    if os.path.isfile(attachment):

                        mtype, encoding = mimetypes.guess_type(attachment)
                        
                        if mtype is None or encoding is not None:
                            mtype = 'application/octet-stream'
                            
                        type, subtype = mtype.split('/', 1)
                        
                        if type == 'text':
                            fp = open(attachment, 'rb')
                            m = MIMEText(fp.read(), _subtype=subtype)
                            fp.close()

                        elif type == 'image':
                            fp = open(attachment, 'rb')
                            m = MIMEImage(fp.read(), _subtype=subtype)
                            fp.close()
                                
                        elif type == 'audio':
                            fp = open(attachment, 'rb')
                            m = MIMEAudio(fp.read(), _subtype=subtype)
                            fp.close()
                        
                        else:
                            fp = open(attachment, 'rb')
                            m = MIMEBase(type, subtype)
                            m.set_payload(fp.read())
                            fp.close()
                            encoders.encode_base64(m)
                        
                        m.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                        self.mail.attach(m)

            s = smtplib.SMTP('localhost')
            s.sendmail(self.sender, recipients, self.mail.as_string())
            s.quit()
            
            return True
        
        except Exception, e:
            raise Exception(e)
    
    