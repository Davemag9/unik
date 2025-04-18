import numpy as np
from PIL import Image

def load_image(path):
    """ Завантажує зображення в grayscale"""
    image = Image.open(path).convert("L")
    return np.array(image, dtype=np.float32)


def roberts_operator(image):
    """ Оператор Робертса """
    Gx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    Gy = np.array([[0, -1], [1, 0]], dtype=np.float32)

    edges = np.zeros_like(image)

    for i in range(image.shape[0] - 1):
        for j in range(image.shape[1] - 1):
            gx = np.sum(Gx * image[i:i + 2, j:j + 2])
            gy = np.sum(Gy * image[i:i + 2, j:j + 2])
            edges[i, j] = np.sqrt(gx ** 2 + gy ** 2)

    return edges


def sobel_operator(image):
    """ Оператор Собеля """
    Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    Gy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32)

    edges = np.zeros_like(image)

    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            gx = np.sum(Gx * image[i - 1:i + 2, j - 1:j + 2])
            gy = np.sum(Gy * image[i - 1:i + 2, j - 1:j + 2])
            edges[i, j] = np.sqrt(gx ** 2 + gy ** 2)

    return edges


def dilate(image, kernel_size=4):
    """ Дилатація """
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    pad = kernel_size // 2
    padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(image.shape[2]):
                region = padded_image[i:i + kernel_size, j:j + kernel_size, c]
                output[i, j, c] = np.max(region * kernel)

    return output


def load_color_image(path):
    """ Завантажує зображення в кольорі """
    image = Image.open(path).convert("RGB")
    return np.array(image, dtype=np.uint8)


def save_image(array, filename):
    image = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))
    image.save(filename)


def save_color_image(array, filename):
    image = Image.fromarray(array)
    image.save(filename)


image_path = "k.jpg"
image = load_image("original_photos/" + image_path)

# roberts_edges = roberts_operator(image)
sobel_edges = sobel_operator(image)

# save_image(roberts_edges, image_path + "roberts_edges.jpg")
save_image(sobel_edges, image_path + "sobel_edges.jpg")

# img = load_color_image("original_photos/" + image_path)
#
# dilate_edges = dilate(img)
#
# save_color_image(dilate_edges, "test_img/" + image_path + "dilate_edges.jpg")



# import numpy as np
# from PIL import Image
#
# def load_color_image(path):
#     """ Load an RGB image and convert it to a NumPy array """
#     image = Image.open(path).convert("RGB")
#     return np.array(image, dtype=np.float32)
#
# def save_image(array, filename):
#     """ Save an image from a NumPy array (convert to uint8) """
#     image = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))
#     image.save(filename)
#
# def apply_filter(image, kernel_x, kernel_y):
#     """ Apply a convolution filter to each color channel separately """
#     output = np.zeros_like(image)
#     pad = kernel_x.shape[0] // 2
#     padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)
#
#     for i in range(image.shape[0]):
#         for j in range(image.shape[1]):
#             for c in range(image.shape[2]):  # Process each color channel separately
#                 region = padded_image[i:i+kernel_x.shape[0], j:j+kernel_x.shape[1], c]
#                 gx = np.sum(kernel_x * region)
#                 gy = np.sum(kernel_y * region)
#                 output[i, j, c] = np.sqrt(gx**2 + gy**2)
#
#     return output
#
# def roberts_operator(image):
#     """ Apply the Roberts operator to a color image """
#     Gx = np.array([[1, 0], [0, -1]], dtype=np.float32)
#     Gy = np.array([[0, 1], [-1, 0]], dtype=np.float32)
#     return apply_filter(image, Gx, Gy)
#
# def sobel_operator(image):
#     """ Apply the Sobel operator to a color image """
#     Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
#     Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
#     return apply_filter(image, Gx, Gy)
#
# def convert_to_grayscale(image):
#     """ Convert an RGB image to grayscale using max-gradient method """
#     return np.max(image, axis=2)
#
# # Load image
# image_path = "original_photos/tokio.jpeg"  # Replace with your image path
# color_image = load_color_image(image_path)
#
# # Apply Roberts and Sobel operators
# roberts_edges = roberts_operator(color_image)
# print(1)
# sobel_edges = sobel_operator(color_image)
#
# # Convert to grayscale (optional)
# # roberts_gray = convert_to_grayscale(roberts_edges)
# # sobel_gray = convert_to_grayscale(sobel_edges)
#
# # Save results
# save_image(roberts_edges, "roberts_color_edges.jpg")
# save_image(sobel_edges, "sobel_color_edges.jpg")