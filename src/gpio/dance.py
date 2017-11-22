from collections import deque
import random
import servo_control_pigpio as sc

POSES = [(90, 180, 0, 90), (45, 135, 90, 90), (180, 180, -1, -1),
         (180, 90, -1, -1), (-1, -1, 180, -1), (45, 45, 45, 45)]


class DanceQueue(object):
    def __init__(self, controller, num_chunks):
        self.queue = deque()
        self.last_index = -1
        self.controller = controller
        for i in range(num_chunks):
            self._add_move()

    def _add_move(self):
        move = random.randint(0, len(POSES) - 1)
        while move == self.last_index:
            move = random.randint(0, len(POSES) - 1)
        self.last_index = move
        self.queue.append(POSES[move])

    def execute_move(self):
        if len(self.queue) == 0:
            return
        pose = self.queue.popleft()
        actions = [
            self.controller.move_arm_l,
            self.controller.move_arm_r,
            self.controller.move_body,
            self.controller.move_head
        ]
        for i, position in enumerate(pose):
            if position != -1:
              actions[i](position)
