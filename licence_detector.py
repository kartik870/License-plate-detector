from ultralytics import YOLO
import cv2
import cvzone
import math
from collections import OrderedDict


class Detector:

    def __init__(self):
        # Initialize YOLO model
        self.model = YOLO("./yolo_models/yolov8n.pt")

        # Initialize video capture
        self.video = cv2.VideoCapture("./upload/output.mp4")

        # Object classifier array
        self.classify = ["", "bicycle", "car", "motorcycle",
                         "", "bus", "train", "truck", ""]

        # Helps to skip frames
        self.frameTime = 0
        self.skipTime = 3

        # Line dimensions
        self.lineY1 = 380
        self.lineX1 = 0
        self.lineY2 = 380
        self.lineX2 = 1072

        # offset [height around line under which car count]
        self.offset_top = 0
        self.offset_bottom = 25
        # limit under which it detects same vehical
        self.ecd_dist = 0

        # Initialize object tracking
        # stores object_id as key and object_info as dictionary
        self.object_dict = OrderedDict()
        self.object_id_counter = 0

        # Variables for counting unique objects
        self.unique_object_count = 0
        self.tracked_objects = set()

        # capturing clean Frames
        self.frameArr = []

    def process(self):
        # Iterating frames of the video
        while True:
            # Fetching frame with status
            success, frame = self.video.read()

            # Stopping video after completion
            if not success:
                break

            # Incrementing skip
            self.frameTime = self.frameTime + 1

            # Only process frames at the specified skip time
            if self.frameTime % self.skipTime != 0:
                continue

            # Passing frame to model and fetching objects
            objects = self.model(frame, stream=True)

            # Iterating detected objects
            for obj in objects:
                boxes = obj.boxes

                # Iterating all boxes in the frame
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    # fetching accuracy
                    accuracy = math.ceil(box.conf[0]*100) / 100
                    # class names
                    idx = int(box.cls[0])

                    if idx == 2 or idx == 3 or idx == 5 or idx == 7:
                        class_name = self.classify[idx]
                        # # creating box in frame
                        # cvzone.cornerRect(frame, (x1, y1, w, h))
                        # # putting text above box
                        # cvzone.putTextRect(
                        #     frame, f'{class_name} {accuracy}', (x1, y1-20),
                        #     scale=2, thickness=2, offset=3)

                        # Calculate the center of the object
                        cx, cy = x1 + w // 2, y1 + h // 2

                        # # marking center point in objects
                        # cv2.circle(frame, (cx, cy), radius=5, color=(
                        #     255, 0, 255), thickness=cv2.FILLED)
                        # # making line
                        # cv2.line(frame, (lineX1, lineY1),
                        #          (lineX2, lineY2), (0, 0, 255),
                        #          thickness=3)

                        # Check if the object is already being tracked
                        matched_object = None
                        for object_id, object_info in self.object_dict.items():
                            # calculating eucledian distance b/w 2 points
                            dist = math.hypot(
                                object_info['cx'] - cx, object_info['cy'] - cy)
                            if dist < self.ecd_dist:
                                matched_object = object_info
                                break

                        if matched_object:
                            # Update the tracked object's position
                            object_id = matched_object['object_id']
                            self.object_dict[object_id]['cx'] = cx
                            self.object_dict[object_id]['cy'] = cy
                        else:
                            # Create a new entry for a unique object
                            self.object_id_counter += 1
                            object_id = self.object_id_counter
                            # Initialize 'object_id'
                            self.object_dict[object_id] = {
                                'cx': cx, 'cy': cy, 'object_id': object_id}

                        # # offset lines
                        # # top offset line
                        # cv2.line(frame, (lineX1, lineY1-offset_top),
                        #          (lineX2, lineY2-offset_top), (0, 200, 255),
                        #          thickness=2)
                        # # bottom offset line
                        # cv2.line(frame, (lineX1, lineY1+offset_bottom),
                        #          (lineX2, lineY2+offset_bottom), (100, 0, 200),
                        #          thickness=2)

                        # Tracking logic: Check if the object has crossed the line
                        if self.lineX1 <= cx <= self.lineX2 and self.lineY1 - self.offset_top <= cy <= self.lineY2 + self.offset_bottom:
                            if idx == 2 or idx == 3 or idx == 5 or idx == 7:
                                if object_id not in self.tracked_objects:
                                    self.tracked_objects.add(object_id)
                                    self.unique_object_count += 1
                                    copy_frame = frame.copy()
                                    # fetching only car
                                    copy_frame = copy_frame[y1:y2, x1:x2]
                                    # resizing only car
                                    copy_frame = cv2.resize(
                                        copy_frame, (600, 400))
                                    # cv2.imshow("car", copy_frame)
                                    self.frameArr.append(copy_frame)

            print("Unique Object Count:", self.unique_object_count)

            # Showing the frame
            # cv2.imshow("Image", frame)

            # Display screen waits for a key press
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # storing frames
        self.store_frames()

        # Release the video capture and close the OpenCV window
        self.video.release()
        # cv2.destroyAllWindows()

    def store_frames(self):
        # display frames
        for idx in range(len(self.frameArr)):
            # showing frame
            # cv2.imshow("Image", self.frameArr[idx])
            status = cv2.imwrite("datasets/cars/car" +
                                 str(idx)+".png", self.frameArr[idx])
            print("Image sending for extraction : "+str(status))
            # cv2.waitKey(0)

            # display screen wait for key to press
            # if cv2.waitKey(10) & 0xFF == ord('z'):
            #     break
