import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
    AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-only-not-secure")

    @property
    def airtable_configured(self) -> bool:
        return bool(self.AIRTABLE_TOKEN and self.AIRTABLE_BASE_ID)

    @property
    def stripe_configured(self) -> bool:
        return bool(self.STRIPE_SECRET_KEY)


config = Config()
