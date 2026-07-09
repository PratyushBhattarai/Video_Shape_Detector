import math
import cv2


def classify_contour(contour):
    area = cv2.contourArea(contour)

    if area < 500:
        return None, "Too small; probably noise"

    perimeter = cv2.arcLength(contour, True)

    if perimeter == 0:
        return None, "Invalid contour"

    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    corners = len(approx)

    x, y, w, h = cv2.boundingRect(approx)

    if corners == 3:
        return "Triangle", "3 corners found"

    if corners == 4:
        aspect_ratio = w / float(h)

        if 0.90 <= aspect_ratio <= 1.10:
            return "Square", "4 corners and equal sides"

        return "Rectangle", "4 corners and unequal sides"

    circularity = 4 * math.pi * area / (perimeter * perimeter)

    if corners > 6 and circularity > 0.70:
        return "Circle", "Many corners and round boundary"

    return None, "Shape not recognized"


def detect_shapes_in_frame(frame_path):
    image = cv2.imread(str(frame_path))

    if image is None:
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    results = []

    for contour in contours:
        shape_name, note = classify_contour(contour)

        if not shape_name:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        crop = image[y:y+h, x:x+w]

        results.append({
            "shape_name": shape_name,
            "note": note,
            "crop": crop,
            "box": (x, y, w, h),
        })

    return results