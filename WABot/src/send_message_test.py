from whatsapp_config import whatsapp
from messages.option_messages import send_welcome_message, enrollment_welcome_message, get_student_birth, get_student_gender, get_student_address, get_student_alternative_phone, get_olevel_results, confirm_upload_success, notify_upload_issue, get_science_combinations_list, request_custom_combination

phone = "263776681617"

username = "conel"
# send_welcome_message(whatsapp, phone, username)
# enrollment_welcome_message(whatsapp, phone)
# get_student_birth(whatsapp, phone)
# get_student_address(whatsapp, phone)
# get_student_alternative_phone(whatsapp, phone)
# get_olevel_results(whatsapp, phone)
# confirm_upload_success(whatsapp, phone)
# notify_upload_issue(whatsapp, phone)
# get_science_combinations_list(whatsapp, phone)
request_custom_combination(whatsapp, phone)