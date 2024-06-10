import pytesseract  # read text from images
import cv2          # read images
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter


# path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\pukhrajsingh\\Desktop\\LicenceModel\\tesseract-ocr\\tesseract.exe'

cascade = cv2.CascadeClassifier(
    "./haarcascade_russian_plate_number.xml")
states = {"AN": "Andaman and Nicobar", "AP": "Andhra Pradesh", "AR": "	Arunachal Pradesh", "AS": "Assam", "BR": "Bihar", "CH": "Chandigarh", "DN": "Dadra and Nagar Haveli", "DD": "Daman and Diu", "DL": "Delhi", "GA": "Goa", "GJ": "Gujarat", "HR": "Haryana", "HP": "Himachal Pradesh", "JK": "Jammu and Kashmir", "KA": "Karnataka",
          "KL": "Kerala", "LD": "Lakshadweep", "MP": "Madhya Pradesh", "MH": "Maharashtra", "MN": "Manipur", "ML": "Meghalaya", "MZ": "Mizoram", "NL": "Nagaland", "OR": "Orissa", "PY": "Pondicherry", "PB": "Punjab", "RJ": "Rajasthan", "SK": "Sikkim", "TN": "TamilNadu", "TR": "Tripura", "UP": "Uttar Pradesh", "WB": "West Bengal"}

# list contains number plate info
plate_details = []


def extract_num(img_name):
    global read
    frame = cv2.imread(img_name)
    img = upscale_image(img_name, 1.0, 1.05)  # reading img

    # cropping image to remove recording number
    # img = img[300:500, 400:800]  # height, width

    # Get image dimensions
    height, width = img.shape[:2]

    # Define the source points (corners of the region to be corrected)
    src_points = np.float32([(330, 300), (560, 247), (565, 330), (345, 390)])

    width = 400
    height = 200
    # Define the destination points (corners of the desired rectangle)
    dst_points = np.float32([(0, 0), (width, 0), (width, height), (0, height)])

    # Calculate the perspective transformation matrix
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective correction
    img = cv2.warpPerspective(
        img, perspective_matrix, (width, height))

    upscaled_width, upscaled_height = 800, 400
    img = cv2.resize(img, (upscaled_width, upscaled_height))

    # # Set the rotation angle (in degrees)
    # angle = -20

    # # Calculate the rotation matrix
    # rotation_matrix = cv2.getRotationMatrix2D(
    #     (width / 2, height / 2), angle, 1)

    # # Perform the rotation
    # img = cv2.warpAffine(img, rotation_matrix, (width, height))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert img to bg
    nplate = cascade.detectMultiScale(gray, 1.1, 4)  # detect numberplate
    for (x, y, w, h) in nplate:
        a, b = (int(0.04*img.shape[0]), int(0.027*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]

        # image processing
        kernal = np.ones((1, 1), np.uint8)
        plate = cv2.dilate(plate, kernal, iterations=1)
        plate = cv2.erode(plate, kernal, iterations=1)
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)  # gray krna
        (_, plate) = cv2.threshold(plate_gray,
                                   100, 225, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # pdf jaisi krna

        read = pytesseract.image_to_string(plate)

        # string processing: remove spaces
        read = ''.join(e for e in read if e.isalnum())
        stat = read[0:2]

        state = "NONE"
        try:
            state = states[stat]
            print('\nCar belongs to ', state)
        except:
            print('State not recognised!')

        print(read)

        # showing none for non detected number plate
        if not read:
            read = "None"
        # Adding number plate detail pair in dictionary
        plate_details.append({"plate": read,
                              "state": state, "img": frame})

        # 2 rectangles 1 having the number other around the number plate
        # cv2.rectangle(img, (x, y), (x+w, y+h), (51, 51, 255), 2)
        # cv2.rectangle(img, (x, y-40), (x+w, y), (51, 51, 255), -1)
        # cv2.putText(img, read, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
        #             1, (255, 0, 0), 2, cv2.LINE_8)

        # Showing number plate
        # cv2.imshow('plate', plate)

    # Showing detection of number plate
    # cv2.imshow("result", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()


def upscale_image(input_image_path, resize_factor, sharpen_factor):
    # Open the image
    with Image.open(input_image_path) as img:
        # Resize the image to improve quality
        width, height = img.size
        # upscaling
        new_width = int(width * resize_factor)
        new_height = int(height * resize_factor)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        # Sharpen the image
        enhanced_img = resized_img.filter(ImageFilter.SHARPEN)

        # Enhance the sharpness
        enhancer = ImageEnhance.Sharpness(enhanced_img)
        enhanced_img = enhancer.enhance(sharpen_factor)

        # Convert the Pillow Image to a NumPy array
        upscaled_img = np.array(enhanced_img)

        # Convert the NumPy array to a Mat-like object (compatible with OpenCV)
        upscaled_img = cv2.cvtColor(upscaled_img, cv2.COLOR_RGB2BGR)

        return upscaled_img


def extract_number_plate():
    # extracting from all images
    noOfFiles = os.listdir("./datasets/cars")
    for idx in range(len(noOfFiles)):
        extract_num("./datasets/cars/car"+str(idx)+".png")
    # showing stored frames
    # for item in plate_details:
    #     print(item['state'], item['plate'])
    #     cv2.imshow("image", item['img'])
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return plate_details
