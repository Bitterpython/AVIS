import cv2
import time

class Compare:
    def __init__(self):
        # Percentage threshold for overall change (e.g., 0.1%)
        self.treshold = 0.1
    
    def compare(self, img1, img2):
        # 1. Safety check: Ensure frames have identical dimensions
        if img1.shape != img2.shape:
            return True # Treat structural changes as different
            
        # 2. Convert both frames to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # 3. Apply blur to eliminate live camera sensor noise
        blur1 = cv2.GaussianBlur(gray1, (21, 21), 0)
        blur2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        
        # 4. Compute absolute difference between the blurred frames
        diff = cv2.absdiff(blur1, blur2)
        
        # 5. Threshold to isolate distinct motion/changes
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        
        # 6. Calculate percentage of altered pixels
        total_pixels = thresh.size
        changed_pixels = cv2.countNonZero(thresh)
        percentage_changed = (changed_pixels / total_pixels) * 100
        
        # 7. Evaluate against threshold
        if percentage_changed >= self.treshold:
            return True
            
        return False

