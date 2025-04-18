import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance

def adjust_contrast(image, factor):
    """Змінює контрастність зображення."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def roll_and_shift_image(image, angle_range=(10, 110), shift_range=(0, 100)):
    """Обертає та зміщує зображення на випадкові значення."""
    h, w = image.shape[:2]  # Використовуємо NumPy-формат (cv2)

    # Випадковий кут повороту
    angle = random.uniform(*angle_range)

    # Випадкове зміщення
    shift_x = random.randint(-shift_range[1], shift_range[1])
    shift_y = random.randint(-shift_range[1], shift_range[1])

    # Обчислення матриці обертання
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Обертання зображення
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    # Обчислення матриці зміщення
    translation_matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])

    # Зміщення зображення
    transformed_image = cv2.warpAffine(rotated_image, translation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    return transformed_image

def convert_to_grayscale(image):
    """Перетворює зображення PIL у відтінки сірого для OpenCV."""
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

def compute_sift_features(image):
    """Обчислює ключові точки та дескриптори SIFT."""
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def draw_keypoints(image, keypoints, output_path):
    """Малює та зберігає зображення з ключовими точками."""
    keypoints_image = cv2.drawKeypoints(image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite(output_path, keypoints_image)

def match_features(des1, des2):
    """Використовує FLANN для знаходження відповідностей між дескрипторами."""
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]
    return good_matches

def find_transformation(kp1, kp2, matches):
    """Знаходить параметри геометрічного перетворення."""
    if len(matches) > 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        matrix, mask = cv2.estimateAffinePartial2D(src_pts, dst_pts)

        if matrix is not None:
            angle = np.arctan2(matrix[1, 0], matrix[0, 0]) * 180 / np.pi
            shift_x, shift_y = matrix[0, 2], matrix[1, 2]
            return angle, shift_x, shift_y
    return None


if __name__ == '__main__':
    # Завантаження зображення
    image_path = "original_photos/cars.jpg"  # Замініть на ваш шлях
    image = Image.open(image_path)

    # Створення спотвореного зображення (зміна контрасту)
    distorted_pil = adjust_contrast(image, 1.5)

    # Конвертуємо в NumPy для OpenCV
    distorted_np = np.array(distorted_pil)

    # Обробляємо зображення (обертаємо та зміщуємо)
    distorted_np = roll_and_shift_image(distorted_np)

    # Зберігаємо спотворене зображення
    transformed_pil = Image.fromarray(distorted_np)
    transformed_pil.save("transformed_image.jpg")

    # Конвертація у відтінки сірого
    gray1 = convert_to_grayscale(image)
    gray2 = convert_to_grayscale(transformed_pil)

    # Знаходження SIFT-дескрипторів
    kp1, des1 = compute_sift_features(gray1)
    kp2, des2 = compute_sift_features(gray2)

    # Зберігаємо зображення з ключовими точками
    draw_keypoints(gray1, kp1, "trash/keypoints_original.jpg")
    draw_keypoints(gray2, kp2, "trash/keypoints_transformed.jpg")

    # Порівняння ключових точок
    matches = match_features(des1, des2)

    # Знаходження параметрів геометрічного перетворення
    transformation = find_transformation(kp1, kp2, matches)

    # Вивід результату
    if transformation:
        angle, shift_x, shift_y = transformation
        print(f"Кут повороту: {angle:.2f} градусів")
        print(f"Зміщення X: {shift_x:.2f} пікселів")
        print(f"Зміщення Y: {shift_y:.2f} пікселів")
    else:
        print("Не вдалося знайти відповідність між зображеннями")

    print("Спотворене зображення збережено як transformed_image.jpg")
    print("Ключові точки збережено у keypoints_original.jpg та keypoints_transformed.jpg")
