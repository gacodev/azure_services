from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class Settings:
    def __init__(self, key_vault_name: str = "keyVaultName"):
        self.kv_uri = f"https://{key_vault_name}.vault.azure.net"
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.kv_uri, credential=self.credential)
        self.secret_map = self.build_secret_map()

    def build_secret_map(self):
        secret_map = {}
        for secret in self.client.list_properties_of_secrets():
            secret_name = secret.name
            pascal_case_name = ''.join(word.capitalize() for word in secret_name.replace('-', '_').split('_'))
            secret_map[pascal_case_name] = secret_name
            
            if secret_name != pascal_case_name:
                self.update_secret_name(secret_name, pascal_case_name)
        return secret_map

    def update_secret_name(self, original_name, new_name):
        secret_properties = self.client.get_secret(original_name)
        secret_value = self.client.get_secret(original_name).value
        self.client.set_secret(new_name, secret_value)
        self.client.begin_delete_secret(original_name)

# Instancia los ajustes 
settings = Settings()
