import cv2
import argparse
import os

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

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Resize images")
    parser.add_argument("-i", "--input-folder", type=str, help="Path to input folder containing images")
    parser.add_argument("-o", "--output-folder", type=str, help="Path to output folder for resized images")
    args = parser.parse_args()

    # Check if input folder exists
    if not os.path.exists(args.input_folder):
        print("Input folder does not exist:", args.input_folder)
        return

    # Resize images in the input folder and save to the output folder
    for filename in os.listdir(args.input_folder):
        input_path = os.path.join(args.input_folder, filename)
        if os.path.isfile(input_path):
            output_path = os.path.join(args.output_folder, filename)
            resize_image(input_path, output_path)

if __name__ == "__main__":
    main()

