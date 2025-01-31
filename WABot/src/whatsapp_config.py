from dotenv import load_dotenv
import os
from wa_cloud_py import WhatsApp

# Load environment variables
load_dotenv()

# Retrieve sensitive data from environment variables
access_token = os.getenv("ACCESS_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")

# Configure WhatsApp client
whatsapp = WhatsApp(
    access_token=access_token,
    phone_number_id=phone_number_id
)