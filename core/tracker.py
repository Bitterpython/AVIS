import math

class Tracker:
    def __init__(self):
        pass
       
    def track(self, birds, frame_size):
        
        cx = frame_size["x"] // 2
        cy = frame_size["y"] // 2
        center = (cx, cy)
        best_bird = None
        
        for bird in birds:
            distance = math.dist(center, (bird["x"], bird["y"]))
            
            bird["distance"] = distance
            
            if best_bird == None:
                best_bird = bird
            elif bird["distance"] < best_bird["distance"]:
                best_bird = bird
                
        return best_bird