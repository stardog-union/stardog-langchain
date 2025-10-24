# Default Stardog Cloud API endpoint
DEFAULT_STARDOG_CLOUD_ENDPOINT = "https://cloud.stardog.com/api"

# Default client ID for Voicebox applications
DEFAULT_CLIENT_ID = "VBX-LANGCHAIN"


class Headers:
    """HTTP header names for Stardog Cloud API."""

    STARDOG_CLOUD_API_KEY = "x-sdc-api-key"
    STARDOG_CLOUD_CLIENT_ID = "x-sdc-client-id"
    STARDOG_AUTH_TOKEN_OVERRIDE = "x-sd-auth-token"
