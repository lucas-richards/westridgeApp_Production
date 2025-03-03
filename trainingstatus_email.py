import sys
import requests
import time
import logging
import os
import django
# Set up Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

sys.path.append('/home/bc/BigCommerceBackOrder')  
 
import Group47_100 as Group47
import config_TrainingStatus as config
from users.models import Profile
from django.contrib.auth.models import User

VERSION = '101'

def main():
    TrainingStatus('Training Status')

def TrainingStatus(entity):
   
    # 2023.03.16 Version 100
    #   Email Training Status to all supervisors including the team status.


    # Setup logging
    #
    logging.basicConfig(
        filename=config.LOG_FILE,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        encoding='utf-8',
        level=logging.INFO,
    )

    # logging.info(f'*** Training Status v{VERSION} for {entity} ***')
    print       (f'*** Training Status v{VERSION} for {entity} ***')

    emails_sent = []
    emails_failed = []
    #  get users and filter by supervisors
    #
    supervisors = User.objects.filter(supervisor_profiles__isnull=False, profile__active=True).distinct()
    print(f'Found {len(supervisors)} supervisors')
    for supervisor in supervisors:
        print(f'{supervisor.username} is a supervisor {supervisor.email}')
        modules = supervisor.profile.get_supervised_training_modules()
        # create a dictonary with people supervised and roles assigned
        #
        supervised_profiles = {}
        for profile in supervisor.profile.user.supervisor_profiles.filter(active=True):
            supervised_profiles[profile.user.username] = profile.roles.all()

        required_modules = []
        recommended_modules = []

        for status in ['missing', 'expired', 'toexpire']:
            for module in modules[status]:
                if module.name.startswith('TM5'):
                    if module.name not in recommended_modules:
                        recommended_modules.append(module.name)
                else:
                    if module.name not in required_modules:
                        required_modules.append(module.name)

        print("Missing or expired Required Modules:")
        for item in required_modules:
            if required_modules:
                print(item)
            else:
                print("No modules found")
        
        print("Missing or required Recommended Modules:")
        for item in recommended_modules:
            if recommended_modules:
                print(item)
            else:
                print("No modules found")

        # create a nice text to show all the people and their roles. 
        #

        # email the supervisor
        try:
            required_modules_text = "No modules found" if not required_modules else ', '.join(required_modules)
            recommended_modules_text = "No modules found" if not recommended_modules else ', '.join(recommended_modules)
            if required_modules or recommended_modules:

                supervised_profiles_text = "<ol>" + "".join(
                    [f'<li><strong>{user}</strong>: {", ".join([role.description for role in roles])}</li>' for user, roles in supervised_profiles.items()]
                ) + "</ol>"
                email_body = f"""
                <html>
                <body>
                    <p>Dear {supervisor.first_name},</p>
                    <p>This is your monthly automated training compliance update from IDTraining.</p>
                    <p>Below are the required training modules that one or more of your team members are <strong>missing</strong>, <strong>have expired</strong>, or are <strong>nearing expiration</strong>:</p>
                    <p><strong>Quality-Related Modules:</strong><br>
                    {required_modules_text}</p>
                    <p><strong>Safety & HR-Related Modules:</strong><br>
                    {recommended_modules_text}</p>
                    <p>Please ensure the necessary training is completed and submit the training records to the Quality Department upon completion.</p>
                    <p><strong>Your team members and their roles:</strong><br>
                    {supervised_profiles_text}</p>
                    <p>For more details, please visit <a href="{config.APP_URL}">IDTraining</a> app.</p>
                    <p>Best regards,<br>
                    IDTraining Team</p>
                    <p><em>*** (/home/bc/westridgeApp/trainingstatus_email.py) ***</em></p>
                </body>
                </html>
                """
            else:
                email_body = f"""
                <html>
                <body>
                    <p>Dear {supervisor.first_name},</p>
                    <p>This is your monthly automated training compliance update from IDTraining.</p>
                    <p>Good job! All the people you supervise are up to date with their training modules.</p>
                    <p><strong>Your team members and their roles:</strong><br>
                    {supervised_profiles_text}</p>
                    <p>For more details, please visit <a href="{config.APP_URL}">IDTraining</a> app.</p>
                    <p>Best regards,<br>
                    IDTraining Team</p>
                    <p><em>*** (/home/bc/westridgeApp/trainingstatus_email.py) ***</em></p>
                </body>
                </html>
                """
            
            Group47.send_email(
                to_address={supervisor.email}, 
                # to_address={config.ADMIN_EMAIL},
                subject="Training Status", 
                body_text='This is the email content', 
                body_html=email_body,
                send=True
            )
            print(f'email sent to {supervisor.email}')
            # print(f'email sent to {config.ADMIN_EMAIL}')
            print(f'for {supervisor.username}')
            # logging.info(f'email sent to {supervisor.email} for {supervisor.username}')
            emails_sent.append(supervisor.username)
            #  if supervisor gregg then send email to him  with greggs training modules
            #
            
        except Exception as e:
            print(f'Error sending email to {supervisor.email} for {supervisor.username}: {e}')
            logging.error(f'Error sending email to {supervisor.email} for {supervisor.username}')
            emails_failed.append(supervisor.username)

    Group47.send_email(
        to_address=config.ADMIN_EMAIL, 
        subject="Training Status", 
        body_text=f"Emails sent: {', '.join(emails_sent)}\nEmails failed: {', '.join(emails_failed)}", 
        send=True
    )



if __name__=='__main__':main()


        




