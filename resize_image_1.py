import cv2
import os
import argparse

def resize_image(input_path, output_path):
    # Load an image from file
    image = cv2.imread(input_path)

    # Check if the image was loaded successfully
    if image is not None:
        print("Image loaded successfully")
    else:
        print("Failed to load image")
        return

    # Resize the image to shape 128 x 128
    resized_image = cv2.resize(image, (128, 128))

    # Find the shape of the resized image
    height, width, channels = resized_image.shape
    print("Resized image shape:", height, "x", width, "x", channels)

    # Save the resized image
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cv2.imwrite(output_path, resized_image)
    print("Resized image saved to:", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize an image.")
    parser.add_argument("-i", "--input_path", type=str, help="Path to the input image")
    parser.add_argument("-o", "--output_path", type=str, help="Path to save the resized image")
    args = parser.parse_args()

    # Resize the image
    resize_image(args.input_path, args.output_path)

#python resize_image.py -i /home/sysadm/Downloads/emotalkingface/profile_pic.jpg -o /home/sysadm/Downloads/emotalkingface/resize_profile_pic.jpg

