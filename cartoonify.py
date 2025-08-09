import cv2
from tkinter import filedialog, Tk
import os

# Hide the main Tkinter window
root = Tk()
root.withdraw()

# Step 1: Choose an image
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
)

if file_path:
    # Step 2: Read the image
    img = cv2.imread(file_path)

    # Step 3: Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 4: Apply median blur
    gray_blur = cv2.medianBlur(gray, 5)

    # Step 5: Detect edges
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    # Step 6: Apply bilateral filter to smooth the image
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # Step 7: Combine color and edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Step 8: Save cartoonified image
    save_path = os.path.splitext(file_path)[0] + "_cartoon.jpg"
    cv2.imwrite(save_path, cartoon)

    # Step 9: Show output
    cv2.imshow("Cartoon", cartoon)
    print(f"Cartoonified image saved as: {save_path}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No image selected.")
