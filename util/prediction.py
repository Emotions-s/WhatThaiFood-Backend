import os
import numpy as np

from keras.models import load_model


curryModel = load_model(os.path.join(os.path.dirname(__file__), '..', 'AIModel', 'currySoupM.h5'))
dessertModel = load_model(os.path.join(os.path.dirname(__file__), '..', 'AIModel', 'dessertM.h5'))
otherModel = load_model(os.path.join(os.path.dirname(__file__), '..', 'AIModel', 'otherM.h5'))

def predict(type, image):
    if type == '1':
        result = curryModel.predict(image)
    elif type == '2':
        result = dessertModel.predict(image)
    elif type == '3':
        result = otherModel.predict(image)
    else:
        return None
    result = result[0]

    arr = np.array(result)

    ft_arr = np.where(arr > 0.15)[0]

    pair_arr = [(index + 1, value * 100) for index, value in enumerate(arr) if index in ft_arr]

    sorted_pairs = sorted(pair_arr, key=lambda pair: pair[1], reverse=True)

    result_pairs = [sorted_pairs[0:3]]

    return result_pairs[0]