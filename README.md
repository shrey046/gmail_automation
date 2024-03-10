Gmail Automation Script Documentation

Introduction:

The Gmail Automation Script is a robust tool created to automate a variety of tasks in Gmail. It utilizes the Gmail API to programmatically interact with Gmail accounts, enabling users to perform tasks such as reading and filtering emails. This documentation will walk you through installing, setting up, and using the script.

1. Prerequisites:
   -  An active Gmail account
   - Python 3.x installed on your computer
   - Installed pip (Python package installer)
   - Stable internet connection

2. Installation:
    - Open a terminal or command prompt.
    - Clone this repository from GitHub by running the following command
        git clone https://github.com/shrey046/gmail_automation.git
    - Go to the project directory using the command line
        cd gmail_automation
    - Install the necessary Python dependencies by running the following command
        pip3 install -r requirements.txt

3. Google Authentication:
    - To enable the Gmail API for your Google account, follow the instructions in the Google API Console at 
    [ https://console.developers.google.com ]
    - Obtain the credentials (client_secret_data.json) for accessing the Gmail API and place them in the project directory.

4. Configuration:
    - Open the rules.json file in the project directory.
    - Modify the rules according to your requirements.
    - The rules.json file should contain a list of rules.

    A rule contains three main parts: conditions, actions, and predicate.
    "conditions" are filters to be applied to the available mails. Conditions have three parts: "field", "predicate", and "value".
        - "field" can have values: "from_email", "subject", "message", "email_date"
        - "predicate" can have values: "contains", "does not contain", "equals", "does not equal".
        - For string type fields ("from_email", "subject", "message"), use "contains", "does not contain", "equals", "does not equal".
        - For the date type field ("email_date"), use "less than" or "greater than" for date comparison. If you want to compare with days, add a new parameter days with an integer and if you want to compare with months, add a new parameter months with an integer.
        - "value" is the string to be used for comparison.
    "actions" is a dictionary of actions to be performed on the emails selected after applying the above conditions. Allowed keys are "move" and "mark".
        - "move": Mails can be moved to "INBOX", "IMPORTANT", "TRASH", "SPAM", "CATEGORY_FORUMS", "CATEGORY_UPDATES", "CATEGORY_PERSONAL", "CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "STARRED".
        - "mark": Mails can be marked as read or unread.

5. After creating the rules file run the script using python3 main.py

6. Problems with the implementation:
    - Unable to move the email to the draft folder due to an issue.

7. Future improvements:
    - Develop a validator to ensure the rules file is valid.
    - Implement a logging system that records the actions taken.
    - Integration with Other Services (Outlook, Yahoo)
