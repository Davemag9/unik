import random
import cv2
import matplotlib.pyplot as plt
filename = '/Users/davemag9/VSCODE/Зайоба/tzi/tzi/lab4_test.png'
# filename = '/Users/davemag9/VSCODE/Зайоба/tzi/tzi/lab4_test2.png'
filename = '/Users/davemag9/VSCODE/Зайоба/tzi/tzi/lab4_test3.png'

def show_image(image, text=''):
    # plt.figure(figsize=(15, 15))
    plt.imshow(image)
    plt.title(text)
    plt.show()

def visualize_contour(contour):
    x_values = []
    y_values = []
    for x, y in contour:
        x_values.append(x)
        y_values.append(y)
    plt.plot(x_values, y_values, color='red', )
    plt.text(contour[0][0], contour[0][1], cv2.arcLength(contour,True), fontsize=5, color='blue')
    

def dfs(node ,_node, path):
        if _node == node:
            return path
        if not graph.get(_node):
            return
        for child in graph[_node]:
            if res := dfs(node, child, path + [child]):
                return res
            
def find_distance_from_root(node):
    return dfs(node, -1, [-1])

def find_distance_between_two_nodes(node1, node2):
    path1 = find_distance_from_root(node1)
    path2 = find_distance_from_root(node2)

    intersection = set(path1).intersection(path2)
    result = set(path1).difference(intersection) | set(path2).difference(intersection)
    return len(result)


img = cv2.imread(filename)
# show_image(img, "Default img")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# show_image(gray)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# show_image(blurred, "Blurred")

_, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
# show_image(threshold)

contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(contours)
# print(hierarchy[0])

# for contour in contours:
#     # perimeter = cv2.arcLength(contour,True)
#     visualize_contour(contour.reshape(-1, 2))
    
# plt.gca().invert_yaxis()
# plt.imshow(img)
# plt.show()

if(len(contours) <= 2):
    print("Not enought contours to find distance")
else:
    graph = {i: set() for i in range(0, len(contours), 2)}
    graph[-1] = set()
    for i, (_, _, _, parent) in list(enumerate(hierarchy[0]))[::2]:
        while parent not in graph:
            parent = hierarchy[0][parent][3]
        graph[parent].add(i)

    max = 0
    for _ in range(1000):
        figures = set(graph.keys())
        figures.discard(-1)

        pair = random.sample(list(figures), k=2)
        if cv2.arcLength(contours[pair[0]],True) < 10 or cv2.arcLength(contours[pair[1]],True) < 10:
            continue
        else:

            distance = find_distance_between_two_nodes(*pair)

            if distance > max:
                max = distance
                para = pair
              
    for i in para:
        contour = contours[i]
        visualize_contour(contour.reshape(-1, 2))

    plt.imshow(img)
    plt.title(f'Distance = {max}')
    plt.show()