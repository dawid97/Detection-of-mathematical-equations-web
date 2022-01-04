import cv2
import numpy as np
import os
import json
import base64

from tensorflow.keras import backend
from tensorflow.keras.models import model_from_json

class ImageChecker:

    def __init__(self):
        backend.set_image_data_format('channels_first')
        path = os.path.dirname(__file__)
        json_file = open(f'{path}\\model_final.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        self.loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        self.loaded_model.load_weights(f'{path}\\model_final.h5')

    def serialise_image(self, image_location):
        data = {}
        with open(image_location, mode='rb') as file:
            img = file.read()

        # Encode do b64
        data_encoded = base64.b64encode(img)
        # convert bytes to string
        data['img'] = data_encoded.decode('utf-8')
        return json.dumps(data)

    def deserialise_image(self, image_data):
        # Decode b64
        data_decoded = base64.b64decode(image_data)
        return data_decoded
    
    
    def check_image(self, data):
        found_characters = ''

        #img = cv2.imread(image_location, cv2.IMREAD_GRAYSCALE)
        nparr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if img is not None:
            img = ~img
            ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            ctrs, ret = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
            w = int(28)
            h = int(28)
            predict_data = []

            rects = []
            for c in cnt:
                x, y, w, h = cv2.boundingRect(c)
                rect = [x, y, w, h]
                rects.append(rect)

            bool_rect = []
            for r in rects:
                l = []
                for rec in rects:
                    flag = 0
                    if rec != r:
                        if r[0] < (rec[0] + rec[2] + 10) and rec[0] < (r[0] + r[2] + 10) and r[1] < (rec[1] + rec[3] + 10) and \
                                rec[1] < (r[1] + r[3] + 10):
                            flag = 1
                        l.append(flag)
                    if rec == r:
                        l.append(0)
                bool_rect.append(l)

            dump_rect = []
            for i in range(0, len(cnt)):
                for j in range(0, len(cnt)):
                    if bool_rect[i][j] == 1:
                        area1 = rects[i][2] * rects[i][3]
                        area2 = rects[j][2] * rects[j][3]
                        if (area1 == min(area1, area2)):
                            dump_rect.append(rects[i])

            final_rect = [i for i in rects if i not in dump_rect]

            for r in final_rect:
                x = r[0]
                y = r[1]
                w = r[2]
                h = r[3]
                im_crop = thresh[y:y + h + 10, x:x + w + 10]

                im_resize = cv2.resize(im_crop, (28, 28))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                im_resize = np.reshape(im_resize, (1, 28, 28))
                predict_data.append(im_resize)

                found_characters = ''
                for i in range(len(predict_data)):
                    predict_data[i] = np.array(predict_data[i])
                    predict_data[i] = predict_data[i].reshape(1, 1, 28, 28)
                    result = self.loaded_model.predict_classes(predict_data[i])

                    switch={
                        0:'0',
                        1:'1',
                        2:'2',
                        3:'3',
                        4:'4',
                        5:'5',
                        6:'6',
                        7:'7',
                        8:'8',
                        9:'9',
                        10:'+',
                        11:'-',
                        12:'*',
                        13:'/',
                        14:'(',
                        15:')',
                        16:'-'
                    }

                    found_characters += switch.get(result[0])
            print(f'\n***********************\nEquation: {found_characters}\n')
        return found_characters


# check = ImageChecker()
# des = check.deserialise_image(im)
# check.check_image(des)