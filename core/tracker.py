import math


class Tracker:
    def __init__(self):
        self.target = None
        self.max_distance = 80
        self.max_lost_frames = 5
        self.lost_frames = 0

    def _select_best_bird(self, birds, center):
        best_bird = None
        best_distance = float("inf")
        best_confidence = -1.0

        for bird in birds:
            distance = math.dist(center, (bird["x"], bird["y"]))
            bird["distance"] = distance

            confidence = bird.get("confidence", 0.0)
            if distance < best_distance or (
                distance == best_distance and confidence > best_confidence
            ):
                best_distance = distance
                best_confidence = confidence
                best_bird = bird

        return best_bird

    def track(self, birds, frame_size):
        if not birds:
            if self.target is not None and self.lost_frames < self.max_lost_frames:
                self.lost_frames += 1
                return self.target

            self.target = None
            self.lost_frames = 0
            return None

        cx = frame_size["x"] // 2
        cy = frame_size["y"] // 2
        center = (cx, cy)
        self.lost_frames = 0

        if self.target is None:
            self.target = self._select_best_bird(birds, center)
            return self.target

        best_target = None
        best_distance = float("inf")
        best_confidence = -1.0

        for bird in birds:
            distance = math.dist((self.target["x"], self.target["y"]), (bird["x"], bird["y"]))
            bird["distance"] = distance

            confidence = bird.get("confidence", 0.0)
            if distance < best_distance or (
                distance == best_distance and confidence > best_confidence
            ):
                best_distance = distance
                best_confidence = confidence
                best_target = bird

        if best_target is not None and best_distance <= self.max_distance:
            self.target = best_target
            return self.target

        if self.target is not None and best_target is not None:
            self.target = best_target
            return self.target

        if self.target is not None and self.lost_frames < self.max_lost_frames:
            self.lost_frames += 1
            return self.target

        self.target = None
        self.lost_frames = 0
        return None