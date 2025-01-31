from messages.option_messages import (
    send_academic_images_uploaded_message,
    send_upload_limit_message,
)
from db_operations import (
    update_academic_history,
    get_existing_academic_images,
    create_academic_history,
)


def handle_image_upload(db, whatsapp, phone, message, student_state):
    """
    Handles the image upload process and stores paths for up to 3 images.
    Sends a confirmation message only after successfully uploading 1, 2, or 3 images.
    Sends an error message only once if attempting to upload more than 3 images.
    """
    print("handling image iniated")
    if student_state == "upload_photo":
        print("student state matched")

        # Get the current list of saved academic images for this phone
        existing_images = get_existing_academic_images(phone)
        print(f"Existing images: {existing_images}")
        # Assume this function exists

        # Initialize image paths and flags
        if existing_images is None:
            create_academic_history(whatsapp_number=phone)
            existing_images = {
                "path1": None,
                "path2": None,
                "path3": None,
                "error_message_sent": False,
                "confirmation_sent": False,
            }

        path1 = existing_images.get("path1")
        path2 = existing_images.get("path2")
        path3 = existing_images.get("path3")
        error_message_sent = existing_images.get("error_message_sent", False)
        confirmation_sent = existing_images.get("confirmation_sent", False)

        # Count the number of uploaded images
        uploaded_count = sum(1 for path in [path1, path2, path3] if path is not None)

        # Check if the upload limit has been reached
        if uploaded_count >= 3:
            if not error_message_sent:
                send_upload_limit_message(whatsapp, phone)
                # Update the flag in the database
                update_academic_history(
                    db=db,
                    whatsapp_number=phone,
                    error_message_sent=True,
                )
            return

        # Assign the new image to the first available path
        full_file_path = f"/media/image_{message.id}"
        if not path1:
            path1 = full_file_path
        elif not path2:
            path2 = full_file_path
        elif not path3:
            path3 = full_file_path

        # Save the new image paths in the database
        saved_academic_images = update_academic_history(
            db=db,
            whatsapp_number=phone,
            path1=path1,
            path2=path2,
            path3=path3,
        )
        print(f"Saved academic images: {saved_academic_images}")

        # If the save operation succeeds, download the image and send a confirmation
        if saved_academic_images:
            whatsapp.download_media(
                message.media_id, filename=f"image_{message.id}", save_path="./media/"
            )
            print(f"Media downloaded successfully for message ID: {message.id}")

            # Send a confirmation message only once
            if not confirmation_sent:
                print(f"Sending confirmation message for phone: {phone}")
                send_academic_images_uploaded_message(whatsapp, phone)
                # Update the confirmation_sent flag in the database
                update_academic_history(
                    db=db,
                    whatsapp_number=phone,
                    confirmation_sent=True,
                )
            else:
                print(f"Confirmation already sent for phone: {phone}")
