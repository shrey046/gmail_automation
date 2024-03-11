import sqlite3
from gmail_auth import fetch_emails

conn = sqlite3.connect("email.db")
cursor = conn.cursor()

def create_table():
    """
    Creates table if nor exists
    """
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS emails
        (
            id TEXT PRIMARY KEY,
            from_email TEXT,
            subject TEXT,
            message TEXT,
            email_date DATETIME,
            is_read INTEGER,
            mailbox TEXT default 'INBOX'
        )
        '''
    )
    conn.commit()

def store_email_data():
    """
    Inserting data into database
    """

    # fetching emails using OAuth
    emails_list = fetch_emails()

    for email in emails_list:
        cursor.execute(''' INSERT OR REPLACE INTO emails
                            (id, from_email, subject, message, email_date, is_read)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                        (email.get("id"), email.get("from_email"), email.get("subject"),
                        email.get("message"), email.get("email_date"), email.get("is_read"))
                    )
        conn.commit()

def fetch_query(where_condition):
    """
    Fetches query from the database
    """
    cursor.execute(f"SELECT id FROM emails WHERE {where_condition}")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def update_query(set_value,where_condition):
    """
    updates the query
    """
    cursor.execute(f"UPDATE emails SET {set_value} WHERE {where_condition};")
    conn.commit()
