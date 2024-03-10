from keras.preprocessing.image import img_to_array
from PIL import Image
import io

def prepare_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((224, 224))
    image = img_to_array(image)
    image = image.reshape(1, 224, 224, 3)
    return image