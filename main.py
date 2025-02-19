import cv2
import os

# Load the image
image = cv2.imread("pic.jpg")  # Provide the correct image path here

# Validate the image file
if image is None:
    print("Error: Could not locate the image file.")
    exit()

# Collect the hidden message and encryption key
secret_msg = input("Enter the message to embed: ")
key = input("Enter a passcode for encryption: ")

# Character-to-byte and byte-to-character mappings
char_to_byte = {chr(i): i for i in range(256)}
byte_to_char = {i: chr(i) for i in range(256)}

# Variables for tracking pixel locations
row = col = channel = 0

# Embed the message into the image
for char in secret_msg:
    if row >= image.shape[0] or col >= image.shape[1]:
        print("Error: The message exceeds the image's capacity.")
        break
    image[row, col, channel] = char_to_byte[char]
    col += 1
    row += col // image.shape[1]
    col %= image.shape[1]
    channel = (channel + 1) % 3

# Save the modified image
output_path = "stego_image.jpg"
cv2.imwrite(output_path, image)
print(f"Message embedded. Encrypted image saved as {output_path}.")
os.system(f"start {output_path}")  # Open the image (Windows-specific)

# Decryption process
decrypt_key = input("Enter passcode to decrypt the message: ")

if key == decrypt_key:
    extracted_msg = ""
    row = col = channel = 0

    for _ in secret_msg:
        if row >= image.shape[0] or col >= image.shape[1]:
            print("Error: Unable to decode the complete message.")
            break
        extracted_msg += byte_to_char[image[row, col, channel]]
        col += 1
        row += col // image.shape[1]
        col %= image.shape[1]
        channel = (channel + 1) % 3

    print("Decrypted message:", extracted_msg)
else:
    print("Decryption failed: Incorrect passcode.")
  
