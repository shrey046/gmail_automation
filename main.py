import json

from gmail_auth import (
    mark_as_read_or_unread, move_to_folder, get_valid_mailbox
)

from sql_queries import (
    create_table, store_email_data, fetch_query, update_query
)

valid_mailbox = get_valid_mailbox()

def implement_rules(rules):
    """
    This function will implement rules and perform actions on them
    """

    rules = rules.get("rules")
    for rule in rules:

        conditions = rule.get("conditions")
        action = rule.get("action")
        rule_predicate = rule.get("predicate")

        condition_query = []

        for condition in conditions:

            field_name = condition.get("field")
            predicate = condition.get("predicate")
            value = condition.get("value")
            days = condition.get("days")
            months = condition.get("months")
            
            if predicate == "contains":
                condition_query.append(f"{field_name} LIKE '%{value}%'")
            if predicate == "does not contain":
                condition_query.append(f"{field_name} NOT LIKE '%{value}%'")
            if predicate == "equals":
                condition_query.append(f"{field_name} = '%{value}%'")
            if predicate == "does not equal":
                condition_query.append(f"{field_name} != '%{value}%'")
            
            if field_name == "date received":
                if predicate == "less than":
                    days_or_months = f"{days} days" if days else f"{months} months"
                    condition_query.append(f"email_date < DATE('now', '{days_or_months}')")
                if predicate == "greater than":
                    days_or_months = f"{days} days" if days else f"{months} months"
                    condition_query.append(f"email_date > DATE('now', '{days_or_months}')")
            
        join_operator = " AND " if rule_predicate == "All" else " OR "

        email_ids = fetch_query(where_condition=join_operator.join(condition_query))

        for email_id in email_ids:
            if action.get("mark"):
                mark_as_read_or_unread(email_id,action.get("mark"))
                set_value = "is_read = 1" if action.get("mark") == "read" else "is_read = 0"
                where_condition = f"id = '{email_id}'"
                update_email = update_query(set_value,where_condition)
            if action.get("move") in valid_mailbox:
                mailbox = action.get("move")
                move_to_folder(email_id,mailbox)
                set_value = f"mailbox = '{mailbox}'"
                where_condition = f"id = '{email_id}'"
                update_email = update_query(set_value,where_condition)
                

def main():

    create_table()
    update_email = input('Update database (Y,N)?')

    if update_email =='Y':
        store_email_data()

    try:
        # Load rules from JSON file
        RULES_FILE = 'rules.json'
        with open(RULES_FILE) as file:
            rules = json.load(file)
            
            if len(rules)>=1:
                implement_rules(rules)
            
    except FileNotFoundError as f:
        print("Could not find rules file")
       
if __name__ == '__main__':
    main()
