import numpy
import numpy as np
import cv2
import os
import pandas as pd

def load_images_from_folder(folder):
    train_data = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            ctrs, ret = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
            w = int(28)
            h = int(28)
            maxi = 0
            for c in cnt:
                x, y, w, h = cv2.boundingRect(c)
                maxi = max(w * h, maxi)
                if maxi == w * h:
                    x_max = x
                    y_max = y
                    w_max = w
                    h_max = h
            im_crop = thresh[y_max:y_max + h_max + 10, x_max:x_max + w_max + 10]
            im_resize = cv2.resize(im_crop, (28, 28))
            im_resize = np.reshape(im_resize, (784, 1))
            train_data.append(im_resize)
    return train_data


root_dir = 'dataset_images'
j = 0
data = [[]]
for root, dirs, files in os.walk(root_dir):
    for directory in dirs:
        print(j)
        path = root_dir + '/' + directory
        tmp = load_images_from_folder(path)

        for i in range(0, len(tmp)):
            tmp[i] = np.append(tmp[i], [directory])

        if j == 0:
            data = tmp
        else:
            data = np.concatenate((data, tmp))
        j += 1

df = pd.DataFrame(data, index=None)
df.to_csv('train_data.csv', index=False)
