###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import maya.cmds as py
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
###############################################################################
#"""# SEND EMAIL                                                              #
###############################################################################
def EMAIL(subjects,emailContent):
    subject = "["+py.optionMenu(subjects,v=1,q=1)+"]";
    message = py.scrollField(emailContent,text=1,q=1);
    fromAddress = "higgie@seasungames.com";
    if("STARMAN" not in subject):
        toAddress = "higgie@seasungames.com";
    else:
        toAddress = "linh@seasungames.com";
    msg = MIMEMultipart();
    msg["From"] = fromAddress;
    msg["To"] = toAddress;
    msg["Subject"] = subject;
    body = message;
    msg.attach(MIMEText(body,"plain"));
    server = smtplib.SMTP('smtp.gmail.com',587);
    server.starttls();
    server.login(fromAddress,"");#!
    text = msg.as_string();
    server.sendmail(fromAddress,toAddress,text);
    server.quit();
    py.headsUpMessage('"Your email was sent!" - HiGGiE',t=3);