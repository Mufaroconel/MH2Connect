from wa_cloud_py.components.messages import ListSection, SectionRow
from wa_cloud_py.messages.types import (
    TextMessage,
    ImageMessage,
    DocumentMessage,
    AudioMessage,
    VideoMessage,
    LocationMessage,
    InteractiveListMessage,
)


def send_welcome_message(whatsapp, phone, username):
    whatsapp.send_interactive_list(
        to=phone,
        body=f"👋Hello {username} \n Welcome to the *Mufakose 2 Secondary School WhatsApp Chatbot*! 🎒\n\nHow may we assist you today? 😊\nPlease select an option from the menu below:",
        button="📋 Select",
        sections=[
            ListSection(
                title="📚 Main Menu",
                rows=[
                    SectionRow(
                        id="class_enrollment",
                        title="📖 Class Enrollment",
                        description="Get help with student enrollment. 📝",
                    ),
                    SectionRow(
                        id="tuition_fees",
                        title="💰 Tuition Fees",
                        description="Learn about tuition fees and payment options. 🏦",
                    ),
                    SectionRow(
                        id="school_schedule",
                        title="🗓️ School Schedule",
                        description="View the school calendar and timetable. 📆",
                    ),
                    SectionRow(
                        id="other_options",
                        title="🔍 Other Options",
                        description="Explore additional services. 🛠️",
                    ),
                ],
            ),
        ],
    )


def send_upload_limit_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body="🚫 Upload Limit Reached\n\nYou can only upload a maximum of 3 images. What would you like to do next?",
        button="Choose an option",
        sections=[
            ListSection(
                title="Options",
                rows=[
                    SectionRow(
                        id="review_images",
                        title="✅ Review Uploaded Images",
                        description="Review the images you just uploaded.",
                    ),
                    SectionRow(
                        id="reupload_images",
                        title="🔄 Re-upload Images",
                        description="Remove existing images and upload new ones.",
                    ),
                    SectionRow(
                        id="continue_application",
                        title="➡️ Continue Application",
                        description="Proceed with your application using the current images.",
                    ),
                ],
            ),
        ],
    )


def send_academic_images_uploaded_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body="📚 Academic Images Uploaded\n\nYour academic images have been successfully uploaded. What would you like to do next?",
        button="Choose an option",
        sections=[
            ListSection(
                title="Options",
                rows=[
                    SectionRow(
                        id="review_images",
                        title="✅ Review Uploaded Images",
                        description="Review the images you just uploaded.",
                    ),
                    SectionRow(
                        id="reupload_images",
                        title="🔄 Re-upload Images",
                        description="Start over and upload your academic images again.",
                    ),
                    SectionRow(
                        id="continue_application",
                        title="➡️ Continue Application",
                        description="Proceed with your application using the uploaded images.",
                    ),
                ],
            ),
        ],
    )


def enrollment_welcome_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body="Welcome to Mufakose 2 High's Enrollment System! 🎓\n\nHi there! 👋 We're thrilled to have you here. Are you enrolling for:\n\n- 🏫 *Form 1 (O-Level)*\n- 🎓 *Lower Six (A-Level)*\n\nSelect your level below to get started on this exciting journey! ✨",
        button="Choose Level",
        sections=[
            ListSection(
                title="Enrollment Levels",
                rows=[
                    SectionRow(
                        id="form_1",
                        title="🏫 Form 1 (O-Level)",
                    ),
                    SectionRow(
                        id="lower_six",
                        title="🎓 Lower Six (A-Level)",
                    ),
                ],
            ),
        ],
    )


def get_student_fullname(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body="😊 Great choice! Let's get to know you better.\n\nPlease reply with your **Full Name** (e.g., *Mufaro Conel Nyakudya*). 🌟\n\nThis will help us personalize your enrollment process. 📝",
    )


def get_student_birth(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body="🎉 Almost there! Now, let's confirm your **Date of Birth*.\n\nPlease reply with your **Date of Birth* in this format: *DD/MM/YYYY* (e.g., *25/12/2005*). 🗓️\n\nThis will help us ensure you're enrolled in the right level! 🌟",
    )


def get_student_gender(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body="🌟 Let's move forward! Please tell us your *Gender*.\n\nReply with **M for Male** or **F for Female**. 🙋‍♂️🙋‍♀️\n\nThis helps us customize your enrollment process! 😊",
    )


def get_student_address(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body="🏠 Finally, could you please provide your *Address*?\n\nReply with your full address (e.g., *123 Street, City, Country*). 📍\n\nThis is needed for the registration process! 🌍",
    )


def get_student_alternative_phone(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body="📞 We also need an **Alternate Contact Number**.\n\nPlease provide a phone number that is different from the one you're using to contact us (e.g., *+263 77 123 4567*). This will help us reach you if needed! 📱 \n Click skip if you do not have an alternative phone✨",
        button="Next",
        sections=[
            ListSection(
                title="Alternate Contact Number",
                rows=[
                    SectionRow(
                        id="no_alternate_number",
                        title="No Alternate Number",
                        description="Skip this step and continue",
                    ),
                ],
            ),
        ],
    )


def get_olevel_results(whatsapp, phone):
    """
    Sends a message prompting the user to upload their O-Level results slip,
    with a maximum of 3 images allowed.
    """
    whatsapp.send_text(
        to=phone,
        body=(
            "📄 Now let's extract your academic results! \n\n"
            "Please upload a **clear photo** of your **original O-Level result slip**. 📝\n\n"
            "Ensure the image is *clear and readable*. If it's not, your application may be considered invalid. ❌\n\n"
            "You are allowed to upload **a maximum of 3 images**. Please attach your file here or use the upload button below. 📤"
        ),
    )

def get_olevel_results_by_subject(whatsapp, phone):
    """
    Sends a message prompting the user to enter their academic results in the specified format.
    """
    whatsapp.send_text(
        to=phone,
        body=(
            "📄 Now let's extract your academic results! \n\n"
            "Please provide your **O-Level results** in the following format:\n\n"
            "*Subject1, A; Subject2, B; Subject3, A; etc.*\n\n"
            "For example:\n"
            "Maths, A; English, B; Physics, C; Chemistry, A\n\n"
            "Once done, send the message with your results. 📝\n\n"
            "Ensure that the subjects and grades are correct. If the format is incorrect, your application may be considered invalid. ❌"
        ),
    )


def reupload_olevel_results(whatsapp, phone):
    """
    Sends a message prompting the user to reupload their O-Level results slip
    if the previous upload was not clear or invalid.
    """
    whatsapp.send_text(
        to=phone,
        body=(
            "🔄 Re-upload your O-Level results slip! \n\n"
            "It seems that the previous photo was either unclear or invalid. Please upload a **clear and readable** "
            "photo of your **original O-Level result slip**. 📝\n\n"
            "Your image must be legible for your application to be processed. ❌\n\n"
            "You are allowed to upload **up to 3 images**. Kindly use the upload button below to attach the new file. 📤"
        ),
    )


def confirm_upload_success(whatsapp, phone):
    """
    Sends a confirmation message to the user after successful file upload.
    """
    whatsapp.send_text(
        to=phone,
        body=(
            "✅ Thank you! We've received your **O-Level results slip** successfully. 🎉\n\n"
            "Your application is moving forward, and we’ll be in touch if we need anything else. 😊"
        ),
    )


def notify_upload_issue(whatsapp, phone):
    """
    Sends a message to the user if there’s an issue with the uploaded file.
    """
    whatsapp.send_text(
        to=phone,
        body=(
            "⚠️ Oops! It seems there was an issue with the file you uploaded. 😞\n\n"
            "Please ensure the file is clear and in one of these formats: JPG, PNG, or PDF. 📂\n"
            "Try uploading your **O-Level results slip** again. 📤"
        ),
    )


def get_science_combinations_list(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            "🔬 **Choose Your Science Combinations for A-Level**\n\n"
            "Please select one of the predefined combinations or define your own custom combination. "
            "These options are designed to align with popular science-oriented career paths. 🚀\n"
            "Click 'Custom Combination' if you'd like to specify your own subjects. ✨"
        ),
        button="Select Combination",
        sections=[
            ListSection(
                title="Science Combinations",
                rows=[
                    SectionRow(
                        id="core_sciences",
                        title="Core Sciences",
                        description="Physics, Chemistry, Pure Maths",
                    ),
                    SectionRow(
                        id="biological_sciences",
                        title="Biological Sciences",
                        description="Biology, Chemistry, Statistics",
                    ),
                    SectionRow(
                        id="applied_sciences",
                        title="Applied Sciences",
                        description="Physics, Computer Science, Pure Maths",
                    ),
                    SectionRow(
                        id="science_and_geo",
                        title="Science & Geography",
                        description="Biology, Chemistry, Geography",
                    ),
                ],
            ),
            ListSection(
                title="Custom Combination",
                rows=[
                    SectionRow(
                        id="custom_combination",
                        title="Own Combination",
                        description="Select your own subjects manually",
                    ),
                ],
            ),
        ],
    )


def request_custom_combination(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body=(
            "📝 **Define Your Own A-Level Combination**\n\n"
            "Please type your desired combination of **three subjects** in the following format:\n"
            "\n📌 *Subject1, Subject2, Subject3*\n"
            "\nExamples:\n"
            "- Physics, Chemistry, Pure Maths\n"
            "- Biology, Geography, Statistics\n\n"
            "**Important:** Ensure you only include three subjects, separated by commas."
        ),
    )


def enrollment_continue_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            "It seems you didn't complete your enrollment application. Would you like to continue? 🤔\n\n"
            "Choose an option below to proceed:"
        ),
        button="Choose Option",
        sections=[
            ListSection(
                title="Enrollment Options",
                rows=[
                    SectionRow(
                        id="yes_continue",
                        title="✅ Yes, Continue",
                    ),
                    SectionRow(
                        id="no_exit",
                        title="❌ No, Exit",
                    ),
                ],
            ),
        ],
    )


def send_academic_images_reviewed_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body="📚 Academic Images Reviewed\n\nYou have successfully reviewed your academic images. What would you like to do next?",
        button="Choose an option",
        sections=[
            ListSection(
                title="Next Steps",
                rows=[
                    SectionRow(
                        id="reupload_images",
                        title="🔄 Re-upload Images",
                        description="Start over and upload your academic images again.",
                    ),
                    SectionRow(
                        id="continue_application",
                        title="➡️ Continue Application",
                        description="Proceed with your application using the uploaded images.",
                    ),
                ],
            ),
        ],
    )


def request_preferred_combination(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body=(
            "📚 **Choose Your Preferred A-Level Combination**\n\n"
            "Kindly send your preferred combination of **three subjects** in the exact format below:\n"
            "\n📌 *Subject1, Subject2, Subject3*\n"
            "\nExamples:\n"
            "- Physics, Chemistry, Pure Maths\n"
            "- History, Literature, Divinity\n\n"
            "**Note:** Double-check your selection to ensure you include only three subjects, separated by commas with no extra spaces between the subjects."
        ),
    )


def request_second_combination(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body=(
            "📚 **Second A-Level Combination Option**\n\n"
            "Now, kindly provide your **second choice** of combination, in the format:\n"
            "\n📌 *Subject1, Subject2, Subject3*\n"
            "\nExamples:\n"
            "- Biology, Chemistry, Geography\n"
            "- Economics, Business, Accounting\n\n"
            "**Note:** Make sure your second combination follows the same format as the first one, with no extra spaces between the subjects."
        ),
    )


def request_third_combination(whatsapp, phone):
    whatsapp.send_text(
        to=phone,
        body=(
            "📚 **Third A-Level Combination Option**\n\n"
            "Finally, please provide your **third choice** of combination, in the format:\n"
            "\n📌 *Subject1, Subject2, Subject3*\n"
            "\nExamples:\n"
            "- Art, Design, Photography\n"
            "- Computer Science, Mathematics, Further Maths\n\n"
            "**Note:** Please ensure that your third combination is formatted just like the previous ones."
        ),
    )


def information_confirmation_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            "Please confirm that the information you've provided is accurate. 📝\n\n"
            "Take note that any information found to be a mismatch with the actual details will result in the application being considered invalid. ⚠️\n\n"
            "Choose an option below to proceed:"
        ),
        button="Choose Option",
        sections=[
            ListSection(
                title="Confirmation Options",
                rows=[
                    SectionRow(
                        id="confirm_accuracy",
                        title="✅ Agree",
                    ),
                ],
            ),
        ],
    )


def confirm_combination(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            "Please review and confirm the subject combination you selected. 🎓\n\n"
            "If the combination is correct, confirm to proceed. If you'd like to make changes, select the edit option. ⚙️\n\n"
            "Choose an option below to continue:"
        ),
        button="Choose Option",
        sections=[
            ListSection(
                title="Verification",
                rows=[
                    SectionRow(
                        id="confirm_combination",
                        title="✅ Confirm Combination",
                    ),
                    SectionRow(
                        id="edit_combination",
                        title="✏️ Edit Combination",
                    ),
                ],
            ),
        ],
    )


def edit_combination_message(whatsapp, phone):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            "Please select the combination option you'd like to edit. 📝\n\n"
            "Choose an option below to proceed. If you're satisfied with the current combination, you can confirm it as well. ⚙️\n\n"
            "Choose an option below to continue:"
        ),
        button="Choose Option",
        sections=[
            ListSection(
                title="Combination",
                rows=[
                    SectionRow(
                        id="edit_option_A",
                        title="✏️ Edit Option A",
                    ),
                    SectionRow(
                        id="edit_option_B",
                        title="✏️ Edit Option B",
                    ),
                    SectionRow(
                        id="edit_option_C",
                        title="✏️ Edit Option C",
                    ),
                    SectionRow(
                        id="confirm_combination",
                        title="✅ Confirm",
                    ),
                ],
            ),
        ],
    )


def lower_six_application_success_message(whatsapp, phone, username):
    whatsapp.send_interactive_list(
        to=phone,
        body=(
            f"👋 Hello {username},\n\n"
            "We are pleased to inform you that your application for the Lower Six program has been successfully submitted! 🎉\n\n"
            "We are currently verifying your details, and our team will contact you shortly to finalize the next steps. 📲\n\n"
            "In the meantime, feel free to explore the options below for additional assistance. 😊"
        ),
        button="📋 Select",
        sections=[
            ListSection(
                title="📚 Main Menu",
                rows=[
                    SectionRow(
                        id="class_enrollment",
                        title="📖 Class Enrollment",
                        description="Get help with student enrollment. 📝",
                    ),
                    SectionRow(
                        id="tuition_fees",
                        title="💰 Tuition Fees",
                        description="Learn about tuition fees and payment options. 🏦",
                    ),
                    SectionRow(
                        id="school_schedule",
                        title="🗓️ School Schedule",
                        description="View the school calendar and timetable. 📆",
                    ),
                    SectionRow(
                        id="other_options",
                        title="🔍 Other Options",
                        description="Explore additional services. 🛠️",
                    ),
                ],
            ),
        ],
    )
