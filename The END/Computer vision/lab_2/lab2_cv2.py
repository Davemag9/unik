import cv2
import os


def compute_sift(image):
    if isinstance(image, str):
        image = cv2.imread(image)

    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors


def transform_image(image_path, angle):
    image = cv2.imread(image_path)

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, matrix, (w, h))
    return cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)


def match_descriptors(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches


def draw_matches(img1, kp1, img2, kp2, matches, output_path):
    match_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite(output_path, cv2.cvtColor(match_img, cv2.COLOR_RGB2BGR))
    print(f"Результат матчмейкінгу збережено в {output_path}")


img1_path = "original_photos/metr.jpg"
output_path = f"./clrdcv2_matches_{os.path.basename(img1_path)}.jpg"

img1 = cv2.imread(img1_path)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = transform_image(img1_path, 30)
print('images read')

kp1, des1 = compute_sift(img1)
print('sift1 ready')
kp2, des2 = compute_sift(img2)
print('sift2 ready')

matches = match_descriptors(des1, des2)
print('matches ready')
draw_matches(img1, kp1, img2, kp2, matches, output_path)