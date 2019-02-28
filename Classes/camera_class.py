import cv2
import numpy as np
import matplotlib.pyplot as plt


class Camera():
    # Create boolean matrix to eliminate edges
    X = 640;
    Y = 480  # Dimensions of camera feed
    x, y = np.meshgrid(np.arange(0, X), np.arange(0, Y))
    condition = (x < 10) | (x > X - 20) | ((x > 586) & (y > 160) & (y < 274)) | ((x > 313) & (x < 322))  # | (y < 10) | (y > Y-10)


    def __init__(self):
        """Sets up a camera object and gives some pre-determined functions"""
        self.open = True
        self.cap = cv2.VideoCapture(2)


    def take_shot(self):
        """Takes a single shot and returns the hsv image"""
        print("okay")
        i = 0
        while(i < 2):
            _, frame = self.cap.read()

            #cv2.imshow("Image with locations", frame)
            #cv2.waitKey(5)

            # Convert BGR to HSV
            frame[self.condition] = 0
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            i += 1

        cv2.imwrite("frame_saving_inside.png", frame)

        return hsv, frame

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
        colour_dict = {"dark_green": (((dark_green[0] - 10) * 0.5, 255 * max(dark_green[1] - 0.1, 0), 255 * max(dark_green[2] - 0.1, 0)), ((dark_green[0] + 10) * 0.5, 255 * min(dark_green[1] + 0.1, 1), 255 * min(dark_green[2] + 0.1, 1))), "orange": (((orange[0] - 10) * 0.5, 255 * max(orange[1] - 0.2, 0), 255 * max(orange[2] - 0.2, 0)), ((orange[0] + 10) * 0.5, 255 * min(orange[1] + 0.2, 1), 255 * min(orange[2] + 0.2, 1))), "purple": (((purple[0] - 10) * 0.5, 255 * max(purple[1] - 0.1, 0), 255 * max(purple[2] - 0.1, 0)), ((purple[0] + 10) * 0.5, 255 * min(purple[1] + 0.1, 1), 255 * min(purple[2] + 0.1, 1))), "blue": (((blue[0] - 10) * 0.5, 255 * max(blue[1] - 0.2, 0), 255 * max(blue[2] - 0.2, 0)), ((blue[0] + 10) * 0.5, 255 * min(blue[1] + 0.2, 1), 255 * min(blue[2] + 0.2, 1))), "green": (((green[0] - 10) * 0.5, 255 * max(green[1] - 0.2, 0), 255 * max(green[2] - 0.2, 0)), ((green[0] + 10) * 0.5, 255 * min(green[1] + 0.2, 1), 255 * min(green[2] + 0.2, 1))), "red": (((red[0] - 10) * 0.5, 255 * max(red[1] - 0.2, 0), 255 * max(red[2] - 0.2, 0)), ((red[0] + 10) * 0.5, 255 * min(red[1] + 0.2, 1), 255 * min(red[2] + 0.2, 1)))}

        mask = cv2.inRange(hsv, np.array(colour_dict[colour][0]), np.array(colour_dict[colour][1]))

        blurred = cv2.GaussianBlur(mask, (5, 5), 0)

        cv2.imwrite("blurred.png", blurred)

        return blurred

    def calculate_moment(self, contour):
        M = cv2.moments(contour)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return (cX,cY)

    def find_centroid(self, blurred):
        some_image, cnts, hierarchy = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL,
                                                       cv2.CHAIN_APPROX_SIMPLE)  # might have to do blurred.copy()

        return cnts
        """
        locations = []

        #Loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Update locations list
            locations.append((cX, cY))

            #For VISUAL TESTING, drawing on to the frame
            
            # draw the contour and center of the shape on the image
            cv2.drawContours(blurred, [c], -1, (0, 255, 0), 1)
            cv2.circle(blurred, (cX, cY), 3, (255, 0, 255), -1)

            # show the image
            cv2.imshow("Image with locations", blurred)
            cv2.waitKey(5)
            

        return locations
        """

    def update_robot(self, robot):
        """Updates the position of the robot"""
        hsv, frame = self.take_shot()

        blurred_purple = self.apply_mask(hsv, "purple")
        blurred_darkgreen = self.apply_mask(hsv, "dark_green")

        cnts_purple = self.find_centroid(blurred_purple)
        cnts_darkgreen = self.find_centroid(blurred_darkgreen)

        print("Length purple", len(cnts_purple))
        good_c_purple = list(filter(lambda x: cv2.contourArea(x) > 600, cnts_purple))
        good_c_darkgreen = list(filter(lambda x: cv2.contourArea(x) > 400, cnts_darkgreen))
        print("Length good purple", len(good_c_purple))
        print("Length good darkgreen", len(good_c_darkgreen))
        #FOR TESTING MAINLY SAVING IMAGE AND DISPLAYING IT
        for c in good_c_purple:
            # draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)
            cv2.circle(frame, self.calculate_moment(c), 3, (255, 0, 255), -1)

            # show the image
            cv2.imshow("Image with locations", frame)
            #cv2.imwrite("frame_drawn_on.png", frame)
            cv2.waitKey(5)

        for c in good_c_darkgreen:
            # draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)
            cv2.circle(frame, self.calculate_moment(c), 3, (255, 0, 255), -1)

            # show the image
            cv2.imshow("Image with locations", frame)
            cv2.imwrite("frame_drawn_on.png", frame)
            cv2.waitKey(5)

        if len(good_c_purple) == 1 and len(good_c_darkgreen) == 1:
            robot.back = self.calculate_moment(good_c_purple[0])
            robot.front = self.calculate_moment(good_c_darkgreen[0])
            print("Robot position updated", robot.front, robot.back)
            return True

        else:
            return False

    def init_blocks(self):
        """Initialises the blocks"""
        hsv = take_shot()
        blurred_blue = apply_mask(hsv, "blue")
        centroids = find_centroid(blurred_blue)
        if len(centroids) > 10:
            raise ValueError("You fucked it, more than 10 blue contours found")
        else:
            i = 0
            blocks = []
            for centroid in centroids:
                blocks.append(Block(centroid, i))
                i += 1
        print("Blocks made")
        for block in blocks:
            block.print()

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
        self.cap.release()
        cv2.destroyAllWindows()
        self.open = False

    def __repr__(self):
        return "Camera :\n open: {}".format(self.open)