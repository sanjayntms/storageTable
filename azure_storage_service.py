from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
import os

account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")

if not account_name or not account_key:
    raise ValueError("Set AZURE_STORAGE_ACCOUNT_NAME and KEY")

credential = AzureNamedKeyCredential(account_name, account_key)

table_service_client = TableServiceClient(
    f"https://{account_name}.table.core.windows.net",
    credential=credential
)

TABLE_NAME = "UserProfiles"

# ✅ Ensure table exists
try:
    table_service_client.create_table(TABLE_NAME)
except Exception:
    pass

table_client = table_service_client.get_table_client(TABLE_NAME)


def create_user_profile(user_id, website=None, twitter=None, bio=None):
    entity = {
        'PartitionKey': 'Users',
        'RowKey': user_id,
    }

    if website:
        entity['Website'] = website
    if twitter:
        entity['TwitterHandle'] = twitter
    if bio:
        entity['Biography'] = bio

    table_client.upsert_entity(entity)


def get_all_profiles():
    return list(table_client.query_entities("PartitionKey eq 'Users'"))


def query_profiles_by_name(name):
    query = f"PartitionKey eq 'Users' and RowKey ge '{name.lower()}' and RowKey lt '{name.lower() + chr(0x10FFFF)}'"
    return list(table_client.query_entities(query))
