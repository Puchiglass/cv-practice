import cv2 as cv
import numpy as np
import argparse

<<<<<<< HEAD
class YOLODetector:
    def __init__(self, weights, config, names):
        self.net = cv.dnn.readNet(weights, config)
        with open(names, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.output_layers = [self.net.getLayerNames()[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_objects(self, frame, conf_threshold=0.5, nms_threshold=0.4, input_size=(416, 416)):
        h, w = frame.shape[:2]
        blob = cv.dnn.blobFromImage(frame, 0.00392, input_size, (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        boxes, confidences, class_ids = [], [], []
        detected_objects = {}

        for out in outputs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x, center_y = int(detection[0] * w), int(detection[1] * h)
                    width, height = int(detection[2] * w), int(detection[3] * h)
                    x, y = int(center_x - width / 2), int(center_y - height / 2)
                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    detected_objects[self.classes[class_id]] = detected_objects.get(self.classes[class_id], 0) + 1

        indices = cv.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices.flatten():
            x, y, width, height = boxes[i]
            color = self.colors[class_ids[i]]
            label = f"{self.classes[class_ids[i]]}: {confidences[i]:.3f}"
            cv.rectangle(frame, (x, y), (x + width, y + height), color, 2)
            cv.putText(frame, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame, detected_objects

    def process_frame(self, frame, conf_threshold, nms_threshold, input_size):
        output_frame, detected_objects = self.detect_objects(frame, conf_threshold, nms_threshold, input_size)
        for obj, count in detected_objects.items():
            print(f"{obj}: {count}")
        return output_frame

    def display_frame(self, frame, window_name="Object Detection", wait_for_key=False):
        cv.imshow(window_name, frame)
        if wait_for_key:
            key = cv.waitKey(0)
        else:
            key = cv.waitKey(1)
        return key != ord("q")
    def cleanup(self):
        cv.destroyAllWindows()


def process_input(input_path, yolo, conf_threshold, nms_threshold, input_size):
    if input_path.endswith((".mp4", ".avi")):
        cap = cv.VideoCapture(input_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            output_frame = yolo.process_frame(frame, conf_threshold, nms_threshold, input_size)
            if not yolo.display_frame(output_frame):
                break
        cap.release()
    else:
        image = cv.imread(input_path)
        if image is None:
            print("Error: Could not load the image.")
            return
        output_image = yolo.process_frame(image, conf_threshold, nms_threshold, input_size)
        yolo.display_frame(output_image, wait_for_key=True)
    yolo.cleanup()



=======
# Загрузка модели YOLO
def load_model(weights_path, config_path, names_path):
    net = cv.dnn.readNet(weights_path, config_path)
    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors

def preprocess_frame(frame, input_size):
    (h, w) = frame.shape[:2]
    blob = cv.dnn.blobFromImage(frame, 0.00392, input_size, (0, 0, 0), True, crop=False)
    return blob, h, w

def process_with_model(net, blob):
    net.setInput(blob)
    outputs = net.forward([net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers()])
    return outputs

def postprocess_frame(frame, outputs, classes, colors, h, w, conf_threshold, nms_threshold):
    boxes, confidences, class_ids = [], [], []
    detected_objects = {}

    for out in outputs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x, center_y = int(detection[0] * w), int(detection[1] * h)
                width, height = int(detection[2] * w), int(detection[3] * h)
                x, y = int(center_x - width / 2), int(center_y - height / 2)
                boxes.append([x, y, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices.flatten():
        x, y, width, height = boxes[i]
        label = f"{classes[class_ids[i]]}: {confidences[i]:.3f}"
        color = colors[class_ids[i]]
        cv.rectangle(frame, (x, y), (x + width, y + height), color, 2)
        cv.putText(frame, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        detected_objects[classes[class_ids[i]]] = detected_objects.get(classes[class_ids[i]], 0) + 1

    return frame, detected_objects

# Обработка кадра
def process_frame(frame, net, classes, colors, conf_threshold, nms_threshold, input_size):
    blob, h, w = preprocess_frame(frame, input_size)
    outputs = process_with_model(net, blob)
    return postprocess_frame(frame, outputs, classes, colors, h, w, conf_threshold, nms_threshold)

# Обработка видео
def process_video(video_path, net, classes, colors, conf_threshold, nms_threshold, input_size):
    cap = cv.VideoCapture(video_path)
    print("Нажмите 'q', чтобы завершить просмотр.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output_frame, detected_objects = process_frame(frame, net, classes, colors, conf_threshold, nms_threshold, input_size)
        for obj, count in detected_objects.items():
            print(f"{obj}: {count}")
        if not display_frame("Object Detection", output_frame):
            break
    cap.release()
    cv.destroyAllWindows()

# Функция для отображения изображения
def display_frame(window_name, frame, wait_time=1):
    cv.imshow(window_name, frame)
    key = cv.waitKey(wait_time) & 0xFF
    if key == ord('q'):
        return False
    return True


# Обработка изображения
def process_image(image_path, net, classes, colors, conf_threshold, nms_threshold, input_size):
    image = cv.imread(image_path)
    if image is None:
        print("Не удалось загрузить изображение")
        return
    output_image, detected_objects = process_frame(image, net, classes, colors, conf_threshold, nms_threshold, input_size)
    for obj, count in detected_objects.items():
        print(f"{obj}: {count}")
    display_frame("Object Detection", output_image, wait_time=0)

# Главная функция
>>>>>>> a34ae6ece904841494beb8419907205cb45ec9bb
def main():
    parser = argparse.ArgumentParser(description="Object Detection with YOLO")
    parser.add_argument('-i', '--input', required=True, help="Path to the input image or video")
    parser.add_argument('-c', '--confidence_threshold', type=float, default=0.5, help="Confidence threshold (default: 0.5)")
    parser.add_argument('-n', '--nms_threshold', type=float, default=0.4, help="NMS threshold (default: 0.4)")
<<<<<<< HEAD
    parser.add_argument('-s', '--input_size', type=int, nargs=2, default=[416, 416], help="YOLO input size (default: 416 416)")
    parser.add_argument('-w', '--weights', required=True, help="Path to YOLO weights file")
    parser.add_argument('-cfg', '--config', required=True, help="Path to YOLO config file")
    parser.add_argument('-names', '--names', required=True, help="Path to class names file")

    args = parser.parse_args()
    yolo = YOLODetector(args.weights, args.config, args.names)
    process_input(args.input, yolo, args.confidence_threshold, args.nms_threshold, tuple(args.input_size))
=======
    parser.add_argument('-s', '--input_size', type=int, nargs=2, default=[416, 416], help="YOLO input size (width height, default: 416 416)")
    parser.add_argument('-w', '--weights', required=True, help="Path to YOLO weights file")
    parser.add_argument('-cf', '--config', required=True, help="Path to YOLO config file")
    parser.add_argument('-nms', '--names', required=True, help="Path to class names file")
    args = parser.parse_args()
>>>>>>> a34ae6ece904841494beb8419907205cb45ec9bb

    net, classes, colors = load_model(args.weights, args.config, args.names)

    if args.input.endswith((".mp4", ".avi", ".gif")):
        process_video(args.input, net, classes, colors, args.confidence_threshold, args.nms_threshold, tuple(args.input_size))
    else:
        process_image(args.input, net, classes, colors, args.confidence_threshold, args.nms_threshold, tuple(args.input_size))

if __name__ == '__main__':
    main()
