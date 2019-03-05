import cv2
import numpy as np
from .block_class import Block
from .processing_functions import decompose_matrix
from .camera_async_class import VideoCaptureAsync


class Camera():
    # Create boolean matrix to eliminate edges
    X = 640;
    Y = 480  # Dimensions of camera feed
    x, y = np.meshgrid(np.arange(0, X), np.arange(0, Y))
    condition = (x < 10) | (x > X - 20) | ((x > 586) & (y > 160) & (y < 274)) | ((x > 430) & (y < 50))  # | (y < 10) | (y > Y-10)      and | ((x > 313) & (x < 322)) for vertical line

    robot_query = cv2.imread('robot_query_5.png', 0)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    surf = cv2.xfeatures2d.SURF_create(400)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    def __init__(self):
        """Sets up a camera object and gives some pre-determined functions"""
        self.open = True
        #self.cap = cv2.VideoCapture(1)
        self.cap = VideoCaptureAsync(2)
        self.cap.start()

        frame = self.cap.read()


    def take_shot(self):
        """Takes a single shot and returns the hsv image"""
        #print("Taking shot")

        frame = self.cap.read()

        #cv2.imshow("Image with locations", frame)
        #cv2.waitKey(5)

        # Convert BGR to HSV
        frame[self.condition] = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("frame_saving_inside.png", frame)

        return frame

    def apply_mask(self, hsv, colour):
        """Returns the blurred mask"""

        # Colour required to identify features in format (H in degrees, S decimal, V decimal)
        blue = (210, 0.52, 0.87)
        red = (1, 0.44, 0.93)
        green = (165, 0.79, 0.64)
        purple = (345, 0.26, 0.49)  # Change! RGB 234, 12, 208
        orange = (31, 0.60, 0.73)  # RGB 226, 183, 0
        dark_green = (178, 0.21, 0.60)

        # Create dictionary of "colour": (lower_colour, upper_colour) where each are tuple len=3
        colour_dict = {"dark_green": (((dark_green[0] - 10) * 0.5, 255 * max(dark_green[1] - 0.1, 0), 255 * max(dark_green[2] - 0.1, 0)), ((dark_green[0] + 10) * 0.5, 255 * min(dark_green[1] + 0.1, 1), 255 * min(dark_green[2] + 0.1, 1))), "orange": (((orange[0] - 10) * 0.5, 255 * max(orange[1] - 0.2, 0), 255 * max(orange[2] - 0.2, 0)), ((orange[0] + 10) * 0.5, 255 * min(orange[1] + 0.2, 1), 255 * min(orange[2] + 0.2, 1))), "purple": (((purple[0] - 10) * 0.5, 255 * max(purple[1] - 0.1, 0), 255 * max(purple[2] - 0.1, 0)), ((purple[0] + 10) * 0.5, 255 * min(purple[1] + 0.1, 1), 255 * min(purple[2] + 0.1, 1))), "blue": (((blue[0] - 15) * 0.5, 255 * max(blue[1] - 0.3, 0), 255 * max(blue[2] - 0.2, 0)), ((blue[0] + 15) * 0.5, 255 * min(blue[1] + 0.3, 1), 255 * min(blue[2] + 0.2, 1))), "green": (((green[0] - 10) * 0.5, 255 * max(green[1] - 0.2, 0), 255 * max(green[2] - 0.2, 0)), ((green[0] + 10) * 0.5, 255 * min(green[1] + 0.2, 1), 255 * min(green[2] + 0.2, 1))), "red": (((red[0] - 10) * 0.5, 255 * max(red[1] - 0.2, 0), 255 * max(red[2] - 0.2, 0)), ((red[0] + 10) * 0.5, 255 * min(red[1] + 0.2, 1), 255 * min(red[2] + 0.2, 1)))}

        mask = cv2.inRange(hsv, np.array(colour_dict[colour][0]), np.array(colour_dict[colour][1]))

        blurred = cv2.GaussianBlur(mask, (5, 5), 0)

        cv2.imwrite("blurred.png", blurred)

        return blurred

    def calculate_moment(self, contour):
        M = cv2.moments(contour)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return (cX,cY)

    def find_contours(self, blurred):
        some_image, cnts, hierarchy = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL,
                                                       cv2.CHAIN_APPROX_SIMPLE)  # might have to do blurred.copy()

        return cnts

    def get_position_orientation_robot(self):
        """Updates the position of the robot

        Returns (x,y) and angle in °

        """
        frame = self.take_shot()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.sift.detectAndCompute(self.robot_query, None)
        kp2, des2 = self.sift.detectAndCompute(gray, None)

        if des2 is None:
            print("Connection lost, no descriptors found")
            while (des2 is None):
                print("Retrying")
                frame = self.cap.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # find the keypoints and descriptors with SIFT
                kp1, des1 = self.sift.detectAndCompute(self.robot_query, None)
                kp2, des2 = self.sift.detectAndCompute(gray, None)

        matches = self.flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        print("Good matches", len(good))

        MIN_MATCH_COUNT = 10

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            scale, shear, angles, translate, perspective = decompose_matrix(M)
            orientation = angles[2]

            h, w = self.robot_query.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            position = self.calculate_moment(dst)

            gray = cv2.polylines(gray, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            #cv2.circle(gray, position, 10, (255, 0, 255), -1)

        else:
            print("Not enough matches are found - {} {}".format(len(good), MIN_MATCH_COUNT))
            matchesMask = None
            position, orientation = self.get_position_orientation_robot()
            return position, orientation

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor = None,
                           matchesMask = matchesMask,  # draw only inliers
                           flags=2)

        print("Position robot:", position)
        print("Orientation robot:", orientation)

        img3 = cv2.drawMatches(self.robot_query, kp1, gray, kp2, good, None, **draw_params)

        cv2.imshow("Image with matches", img3)
        cv2.waitKey(5)

        return np.array(position), orientation

    def init_blocks(self):
        """Initialises the blocks"""
        blocks = []

        frame = self.take_shot()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blurred_blue = self.apply_mask(hsv, "blue")
        cnts = self.find_contours(blurred_blue)

        good_c = list(filter(lambda x: cv2.contourArea(x) < 200 and cv2.contourArea(x) > 100, cnts))

        if len(good_c) > 10:
            print("ValueError(You fucked it, more than 10 blue contours found)")

        i = 0
        for c in good_c:
            centroid = self.calculate_moment(c)
            blocks.append(Block(np.array(centroid), i))
            i += 1

            # draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)
            cv2.circle(frame, centroid, 3, (255, 0, 255), -1)

            # show the image
            cv2.imshow("Image with locations", frame)
            # cv2.imwrite("frame_drawn_on.png", frame)
            cv2.waitKey(5)

            print("Blocks made")

        return blocks

    def update_blocks(self):    #use some kind of conditional parametr so the hsv image from previous can be re-used
        """Updates the positions of the blocks"""
        hsv = take_shot()
        blurred_blue = apply_mask(hsv, "blue")
        centroids = find_centroid(blurred_blue)
        if len(centroids) > 10:
            raise ValueError("You fucked it, more than 10 blue contours found")
        else:
            for centroid in centroids:
                pass
                #have to somehow only update their position using the approximate positions of the previous
                #distance matrix?? each element to the other one

    def close(self):
        #self.cap.release()
        self.cap.stop()
        cv2.destroyAllWindows()
        self.open = False

    def __repr__(self):
        return "Camera :\n open: {}".format(self.open)