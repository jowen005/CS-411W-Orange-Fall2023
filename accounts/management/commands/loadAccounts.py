from django.contrib.auth import get_user_model
from lcc_project.commands.load import LoadCommand, add_file_path

User = get_user_model()

@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/accountSetup.json'


    def load(self, data_list):
        restaurant_accounts = data_list["Restaurants"]
        patron_accounts = data_list["Patrons"]
        admin_accounts = data_list["Admin"]

        used_emails = list(User.objects.values_list('email', flat=True))
        skipped_emails = []
        added_emails = []
        
        for account in restaurant_accounts:
            if account["email"] in used_emails:
                skipped_emails.append(account["email"])
                continue
            email, username, password = account["email"], account["username"], account["password"]
            User.objects.create_user(email=email, username=username, password=password, user_type="restaurant")
            added_emails.append(email)

        for account in patron_accounts:
            if account["email"] in used_emails:
                skipped_emails.append(account["email"])
                continue
            email, username, password = account["email"], account["username"], account["password"]
            User.objects.create_user(email=email, username=username, password=password, user_type="patron")
            added_emails.append(email)

        for account in admin_accounts:
            if account["email"] in used_emails:
                skipped_emails.append(account["email"])
                continue
            User.objects.create_superuser(email=email, username=username, password=password, user_type="admin")
            added_emails.append(email)
        
        if skipped_emails:
            print("\nSKIPPED | These accounts had an email associated with an existing account")
            for email in skipped_emails:
                print(f" - {email}")
        
        if added_emails:
            print("\nCREATED | These accounts were successfully created:")
            for email in added_emails:
                print(f" - {email}")
