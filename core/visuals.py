import cv2

class Visuals:
    def __init__(self):
        pass
    
    def draw_birds(self, frame, birds):
        for bird in birds:
            x1 = int(bird["x"] - bird["width"] / 2)
            y1 = int(bird["y"] - bird["height"] / 2)
            x2 = int(bird["x"] + bird["width"] / 2)
            y2 = int(bird["y"] + bird["height"] / 2)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    def draw_target(self, frame, bird):
        if bird != None:
            x1 = int(bird["x"] - bird["width"] / 2)
            y1 = int(bird["y"] - bird["height"] / 2)
            x2 = int(bird["x"] + bird["width"] / 2)
            y2 = int(bird["y"] + bird["height"] / 2)
    
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    def draw_center(self, frame, frame_size):
        cx = frame_size["x"] // 2
        cy = frame_size["y"] // 2
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        return