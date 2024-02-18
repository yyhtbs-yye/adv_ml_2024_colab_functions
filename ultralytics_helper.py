import cv2

def draw_boxes(image, result, names, color=(255, 0, 0), thickness=1):
  
    image = image.copy()
  
    if isinstance(result, list):
        print('''Error: Arg.0 "result" should not be a list!''')
        return image
    for box in result.boxes:
        xyxy = box.xyxy.to("cpu").view(-1)
        class_output = names[int(box.cls.cpu().numpy())]
    
        cv2.rectangle(image, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, thickness)
        cv2.putText(image, class_output, (int(xyxy[0]), int(xyxy[1]) - 2*thickness), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=color)
    return image
