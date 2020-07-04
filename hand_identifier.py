import cv2


def guessHand(img):
    # Converts the image into a binary image then resizes it to 512 x 512
    ret, binary = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.resize(binary, (512, 512))
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # This is to find the contour with the largest area because that will later be used for the moment function
    max_area = 0
    idx = -1
    for i in range(len(contours)):
        count = contours[i]
        area = cv2.contourArea(count)
        if(area > max_area):
            max_area = area
            idx = i
    count = contours[idx]
    moments = cv2.moments(count)

    # Calculate the x and y coordinates of the center of mass
    if moments["m00"] != 0:
        cX = int(moments["m10"] / moments["m00"])
        cY = int(moments["m01"] / moments["m00"])
    else:
        cX, cY = 0, 0

    # Find location based off the center of mass
    location = "unrecognizable"
    if 192 <= cX <= 320 and 192 <= cY <= 320:
        location = "center"
    elif 0 <= cX <= 192 and 0 <= cY <= 192:
        location = "upper left"
    elif 320 <= cX <= 512 and 0 <= cY <= 192:
        location = "upper right"
    elif 0 <= cX <= 192 and 320 <= cY <= 512:
        location = "lower left"
    elif 320 <= cX <= 512 and 320 <= cY <= 512:
        location = "lower right"

    print("Your hand is located at the " + location)

    # This method calculates the height and width of the object
    num, labels, stats, centroid = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
    w = 0
    h = 0

    # However, this information is stored in the "stats" list part of the return value
    # so I first have to loop through to figure out what the largest width and height are
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_WIDTH] > w:
            w = stats[i, cv2.CC_STAT_WIDTH]
        if stats[i, cv2.CC_STAT_HEIGHT] > h:
            h = stats[i, cv2.CC_STAT_HEIGHT]
    print("The height is " + str(h) + " and the width is " + str(w))

    # Determines the shape of the fist based on the ratio of the width and height
    ratio = w/h
    shape = "unrecognized"
    if .8 <= ratio < 1:
        shape = "fist"
    elif .8 > ratio >= .65:
        shape = "splayed five"
    elif .3 <= ratio <= .6:
        shape = "karate chop"
    print("Your hand is a " + shape)

    # cv2.drawContours(binary, [count], -1, (127, 127, 127), 2)
    cv2.circle(binary, (cX, cY), 5, (50, 127, 50), -1)
    cv2.putText(binary, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 50), 2)

    # Just displays the result
    cv2.imshow('Image', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    hand_img = input("Place the location to the image of your hand ")
    img = cv2.imread(hand_img, 0)
    guessHand(img)


if __name__ == "__main__":
    main()

