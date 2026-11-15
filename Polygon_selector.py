import cv2
import json


# =========================================================
# Global variables
# =========================================================

# Store the points selected by the user.
points = []


# Store the original frame.
original_frame = None


# Store the frame displayed on the screen.
display_frame = None


# =========================================================
# Mouse callback
# =========================================================

def mouse_callback(event, x, y, flags, param):

    # Check whether the left mouse button was pressed.
    if event == cv2.EVENT_LBUTTONDOWN:

        # Store the clicked point.
        points.append((x, y))

        print(f"Point added: ({x}, {y})")


# =========================================================
# Save polygon to JSON
# =========================================================

def save_polygon(points, filename):

    # Convert tuples to lists.
    polygon = [list(point) for point in points]

    # Create the JSON data.
    data = {
        "polygon": polygon
    }

    # Open the file for writing.
    with open(filename, "w") as file:

        # Write the data into the JSON file.
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"Polygon saved to: {filename}")


# =========================================================
# Open video
# =========================================================

video_path = "videos/Takhti_3.asf"

cap = cv2.VideoCapture(video_path)


if not cap.isOpened():

    print("Error: Could not open the video.")

    exit()


# =========================================================
# Read first frame
# =========================================================

ret, frame = cap.read()


if not ret:

    print("Could not read the video frame.")

    cap.release()

    exit()


original_frame = frame.copy()


# =========================================================
# Create window
# =========================================================

window_name = "Polygon Selector"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)


cv2.setMouseCallback(
    window_name,
    mouse_callback
)


# =========================================================
# Main loop
# =========================================================

while True:

    # Create a fresh copy of the original frame.
    display_frame = original_frame.copy()


    # -----------------------------------------------------
    # Draw selected points
    # -----------------------------------------------------

    for point in points:

        cv2.circle(
            display_frame,
            point,
            5,
            (0, 0, 255),
            -1
        )


    # -----------------------------------------------------
    # Draw lines between points
    # -----------------------------------------------------

    if len(points) >= 2:

        for i in range(1, len(points)):

            cv2.line(
                display_frame,
                points[i - 1],
                points[i],
                (255, 0, 0),
                2
            )


    # -----------------------------------------------------
    # Close the polygon
    # -----------------------------------------------------

    if len(points) >= 3:

        cv2.line(
            display_frame,
            points[-1],
            points[0],
            (255, 0, 0),
            2
        )


    # -----------------------------------------------------
    # Display instructions
    # -----------------------------------------------------

    cv2.putText(
        display_frame,
        "Left Click: Add Point | Enter: Finish | R: Reset | ESC: Exit",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    # -----------------------------------------------------
    # Show frame
    # -----------------------------------------------------

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    cv2.imshow(
        window_name,
        display_frame
    )


    # -----------------------------------------------------
    # Keyboard input
    # -----------------------------------------------------

    key = cv2.waitKey(20) & 0xFF


    # -----------------------------------------------------
    # ENTER → Finish polygon
    # -----------------------------------------------------

    if key == 13:

        if len(points) >= 3:

            print("\nPolygon selected.")

            print("Points:")

            for point in points:

                print(point)


            # Save polygon.
            save_polygon(
                points,
                "intersection_polygon.json"
            )

            break


        else:

            print("You need at least 3 points")
            print("to create a Polygon.")


    # -----------------------------------------------------
    # R → Reset
    # -----------------------------------------------------

    elif key == ord("r"):

        points.clear()

        print("Polygon reset.")


    # -----------------------------------------------------
    # ESC → Cancel
    # -----------------------------------------------------

    elif key == 27:

        print("Selection cancelled.")

        points.clear()

        break


# =========================================================
# Clean up
# =========================================================

cap.release()

cv2.destroyAllWindows()