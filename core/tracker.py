import math

class Tracker:
    def __init__(self):
        self.target = None
        self.max_distance = 80
        
       
    def track(self, birds, frame_size):
        
        if not birds:
            self.target = None
            return None
        
        cx = frame_size["x"] // 2
        cy = frame_size["y"] // 2
        center = (cx, cy)
        best_bird = None
        best_target = None
        
        if self.target == None:
            for bird in birds:
                distance = math.dist(center, (bird["x"], bird["y"]))
                bird["distance"] = distance
                
                if best_bird == None:
                    best_bird = bird
                elif bird["distance"] < best_bird["distance"]:
                    best_bird = bird
            
            self.target = best_bird
        
        else:
            for bird in birds:
                distance = math.dist((self.target["x"], self.target["y"]), (bird["x"], bird["y"]))
                bird["distance"] = distance
                
                if best_target == None:
                    best_target = bird
                elif bird["distance"] < best_target["distance"] and bird["distance"] <= self.max_distance:
                    best_target = bird
            
            self.target = best_target
                
        return self.target