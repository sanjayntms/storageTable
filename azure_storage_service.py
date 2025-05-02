from azure.data.tables import TableServiceClient, TableClient
from azure.core.credentials import AzureNamedKeyCredential
import os

account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")

if not account_name or not account_key:
    raise ValueError("Azure Storage Account Name and Key must be set as environment variables.")

credential = AzureNamedKeyCredential(account_name, account_key)
table_service_client = TableServiceClient(f"https://{account_name}.table.core.windows.net", credential=credential)
table_client = table_service_client.get_table_client(table_name="UserProfiles")

def create_user_profile(user_id, website=None, twitter=None, bio=None):
    """Creates or updates a user profile in Azure Table Storage."""
    user_entity = {
        'PartitionKey': 'Users',
        'RowKey': user_id,
    }
    if website:
        user_entity['Website'] = website
    if twitter:
        user_entity['TwitterHandle'] = twitter
    if bio:
        user_entity['Biography'] = bio

    try:
        table_client.upsert_entity(entity=user_entity)
        print(f"Profile for user {user_id} created successfully.")
    except Exception as e:
        print(f"Error creating profile for user {user_id}: {e}")

def get_user_profile(user_id):
    """Retrieves a user profile from Azure Table Storage by RowKey."""
    try:
        entity = table_client.get_entity(partition_key='Users', row_key=user_id)
        return entity
    except Exception as e:
        print(f"Error retrieving profile for user {user_id}: {e}")
        return None

def query_profiles_by_name(name):
    """Queries profiles where the RowKey (which is based on the name) starts with the search term."""
    try:
        query_filter = f"PartitionKey eq 'Users' and RowKey ge '{name.lower()}' and RowKey lt '{name.lower() + chr(0x10FFFF)}'"
        profiles = table_client.query_entities(query_filter=query_filter)
        return list(profiles)
    except Exception as e:
        print(f"Error querying profiles by name '{name}': {e}")
        return []

def get_all_profiles():
    """Retrieves all user profiles."""
    try:
        query_filter = "PartitionKey eq 'Users'"
        profiles = table_client.query_entities(query_filter=query_filter)
        return list(profiles)
    except Exception as e:
        print(f"Error retrieving all profiles: {e}")
        return []
