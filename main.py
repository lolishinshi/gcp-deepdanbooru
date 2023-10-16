import functions_framework
import onnxruntime
import numpy as np
from PIL import Image
from werkzeug import Request

class DeepDanbooru:
    def __init__(self, model_path: str):
        self.model = onnxruntime.InferenceSession(model_path)
        self.tags = [t.strip() for t in open('./model/tags.txt').readlines()]

    def process_image(self, image: Image.Image) -> Image.Image:
        image = image.convert('RGB')
        image = image.resize((512, 512))
        image = np.asarray(image, dtype=np.float32) / 255
        return image

    def predict(self, image: Image.Image, threshold=0.7) -> dict[str, float]:
        image = self.process_image(image)
        preds = self.model.run(None, {'input_1': [image]})[0][0]

        result = {}
        for i, tag in enumerate(self.tags):
            if preds[i] > threshold:
                result[tag] = round(float(preds[i]), 4)

        return result


detector = DeepDanbooru('model/resnet_custom_v3.onnx')


@functions_framework.http
def detect(request: Request):
    if request.method != 'POST':
        return 'Method not allowed', 405

    files = request.files.getlist('images')
    if not files:
        return 'No images found', 400

    return [
        detector.predict(Image.open(f))
        for f in files
    ]
