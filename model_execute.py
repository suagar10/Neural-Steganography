from tensorflow.keras.models import load_model, Model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt

def ascii_encode(message, sentence_len):
    sen = np.zeros((1, sentence_len))
    for i, a in enumerate(message.encode("ascii")):
        sen[0, i] = a
    return sen


def ascii_decode(message):
    return ''.join(chr(int(a)) for a in message[0].argmax(-1))

def main():
    model = load_model('best_model.h5')
    encoder = Model(model.input, model.get_layer('image_reconstruction').output)
    decoder = model.get_layer('sentence_reconstruction')

    img = np.expand_dims(img_to_array(load_img("monalisa.jpeg", target_size=(100, 100))) / 255.0, axis=0)
    str1=input("Enter text to encode:")
    sen = ascii_encode(str1, 100)
    y = encoder.predict([img, sen])
    y_hat = decoder.predict(y)

    img_to_show=[load_img("monalisa.jpeg", target_size=(100, 100)), y[0]]
    titles=["Input image", "Image after encoding"]

    plt.figure(num=1, figsize=(4, 2))
    for i in range(2):
        plt.subplot(1, 2, i+1), plt.imshow(img_to_show[i])
        plt.xticks([])
        plt.yticks([])
        plt.title(titles[i])
    plt.show()

    print("\n\n\nDecode message: "+ascii_decode(y_hat))

if __name__ == "__main__":
    main()