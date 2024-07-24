"""
This code is used to detect names of metal bands in a video stream or image using YOLOv8.

Currently only recognizes 3 bands that are cannibal corpse, burzum and bathory

"""
import cv2
import imutils
from ultralytics import YOLO


class MetalBandLogoDetector:
    def __init__(self, model_path="best.pt", resize_width=0):
        """
        Initialize the MetalBandLogoDetector with a YOLO model.

        :param model_path: Path to the trained YOLO model.
        :param resize_width: Width to resize images and video frames. If 0, no resizing.
        """
        self.model = YOLO(model_path)
        self.resize_width = resize_width

    def __detect_and_annotate(self, frame):
        """
        Detect logos in a frame and annotate the results.

        :param frame: Frame to be processed.
        :return: Annotated frame.
        """
        if self.resize_width > 0:
            frame = imutils.resize(frame, width=self.resize_width)

        results = self.model(frame)  # run model
        annotated_frame = results[0].plot()  # plot results
        return annotated_frame

    def video_detection(self, video_path):
        """
        Perform logo detection on a video file.

        :param video_path: Path to the video file or camera index.
        """
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            annotated_frame = self.__detect_and_annotate(frame)
            # show video
            cv2.imshow("Detection of metal bands", annotated_frame)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def image_detection(self, image_path):
        """
        Perform logo detection on an image file.

        :param image_path: Path to the image file.
        """
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to open image file: {image_path}")
            return

        annotated_frame = self.__detect_and_annotate(image)
        # show video
        cv2.imshow("Detection of metal bands", annotated_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = MetalBandLogoDetector("best.pt", 600)
    # detector.image_detection("./resources/1.jpeg")
    detector.image_detection("./resources/2.jpeg")
    # detector.video_detection(1)