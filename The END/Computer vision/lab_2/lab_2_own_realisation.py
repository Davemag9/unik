import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import sobel
from scipy.spatial import KDTree

def convert_to_grayscale(image):
    """Convert image to grayscale."""
    return image.convert("L")

def gaussian_blur(image, sigma=1.6):
    """Apply Gaussian blur."""
    return image.filter(ImageFilter.GaussianBlur(radius=sigma))

def compute_gradients(image):
    """Compute gradients (magnitude and orientation)."""
    img_array = np.array(image, dtype=np.float32)

    grad_x = sobel(img_array, axis=1)
    grad_y = sobel(img_array, axis=0)

    magnitude = np.hypot(grad_x, grad_y)
    orientation = np.arctan2(grad_y, grad_x) * (180 / np.pi)

    return magnitude, orientation

def detect_keypoints(magnitude, threshold=15, max_keypoints=1000):
    """Detect and return top N keypoints based on gradient magnitude."""
    keypoints = np.argwhere(magnitude > threshold)

    # Sort and pick top max_keypoints strongest keypoints
    keypoints = sorted(keypoints, key=lambda pt: magnitude[pt[0], pt[1]], reverse=True)[:max_keypoints]

    return [tuple(pt) for pt in keypoints]

def compute_descriptors(keypoints, magnitude, orientation, size=4):
    """Create descriptors for keypoints."""
    descriptors = []

    for y, x in keypoints:
        patch_mag = magnitude[max(y - size, 0):y + size, max(x - size, 0):x + size]
        patch_orient = orientation[max(y - size, 0):y + size, max(x - size, 0):x + size]

        if patch_mag.shape != (2 * size, 2 * size):
            continue

        # Histogram of gradients in the region of keypoint
        hist, _ = np.histogram(patch_orient, bins=8, range=(-180, 180), weights=patch_mag)
        hist = hist / (np.linalg.norm(hist) + 1e-7)  # Normalize histogram
        descriptors.append(hist)

    return np.array(descriptors)

def match_features(des1, des2, threshold=0.8):
    """Match features between two sets of descriptors."""
    tree = KDTree(des2)
    matches = []

    for i, d in enumerate(des1):
        distances, indices = tree.query(d, k=2)
        # Implement Lowe's ratio test to filter matches
        if distances[0] < threshold * distances[1]:
            matches.append((i, indices[0]))

    return matches

def draw_keypoints(image, keypoints, output_path="keypoints.jpg"):
    """Draw keypoints on the image."""
    draw = ImageDraw.Draw(image)
    for y, x in keypoints:
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="red", outline="red")

    image.save(output_path)
    print(f"Keypoints saved to {output_path}")

def draw_matches(image1, image2, keypoints1, keypoints2, matches, output_path="matches.jpg"):
    """Draw matches between two images."""
    w1, h1 = image1.size
    w2, h2 = image2.size

    combined_image = Image.new("RGB", (w1 + w2, max(h1, h2)))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (w1, 0))

    draw = ImageDraw.Draw(combined_image)

    for i1, i2 in matches:
        y1, x1 = keypoints1[i1]
        y2, x2 = keypoints2[i2]

        x2 += w1  # Adjust coordinates for second image
        draw.line([(x1, y1), (x2, y2)], fill="yellow", width=1)

    combined_image.save(output_path)
    print(f"Matches saved to {output_path}")

# Load images
image_path = "original_photos/cars.jpg"
image = Image.open(image_path)
distorted_image = image.rotate(15).transpose(Image.FLIP_LEFT_RIGHT)  # Example distorted image

# Preprocessing
gray1 = convert_to_grayscale(image)
gray2 = convert_to_grayscale(distorted_image)

blurred1 = gaussian_blur(gray1)
blurred2 = gaussian_blur(gray2)

magnitude1, orientation1 = compute_gradients(blurred1)
magnitude2, orientation2 = compute_gradients(blurred2)

# Detect keypoints and compute descriptors
keypoints1 = detect_keypoints(magnitude1)
keypoints2 = detect_keypoints(magnitude2)

descriptors1 = compute_descriptors(keypoints1, magnitude1, orientation1)
descriptors2 = compute_descriptors(keypoints2, magnitude2, orientation2)

# Match features
matches = match_features(descriptors1, descriptors2)

# Visualization
draw_keypoints(image.copy(), keypoints1, "trash/keypoints1.jpg")
draw_keypoints(distorted_image.copy(), keypoints2, "trash/keypoints2.jpg")
draw_matches(image, distorted_image, keypoints1, keypoints2, matches, "trash/matches.jpg")
