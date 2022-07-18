# Importing the required Modules
import cv2 as cv
import pandas as pd

# selecting the image
img_path = r'geometry-colorful-triangles-and-squares-wallpaper.jpg'
img = cv.imread(img_path)

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0


# Reading csv file with pandas and giving names to each column
# There are 6 columns in that CSV file
index = ["color", "color_name", "hex", "R", "G", "B"]
color_csv = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(color_csv)):
        d = abs(R - int(color_csv.loc[i, "R"])) + abs(G - int(color_csv.loc[i, "G"])) + abs(B - int(color_csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = color_csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv.namedWindow('Find The Color')
cv.setMouseCallback('Find The Color', draw_function)

while True:

    cv.imshow("Find The Color", img)
    if clicked:

        # cv.rectangle(Find The Color, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv.LINE_AA)

        clicked = False

    # Break the loop when user hits 'enter' key
    if (cv.waitKey(20) & 0xFF == 13) or (cv.getWindowProperty('Find The Color', cv.WND_PROP_VISIBLE) < 1) :
        break

cv.destroyAllWindows()