from collections import deque
import random
import servo_control_pigpio as sc

POSES = [(90, 180, 0, 90), (45, 135, 90, 90), (180, 180, -1, -1), (180, 90, -1, -1), (-1, -1, 180, -1), (45, 45, 45, 45)]

class DanceQueue(object):
    def __init__(self, num_chunks):
        self.queue = deque()
        self.last_index = -1
        for i in range(num_chunks):
            self._add_move()

    def _add_move(self):
        move = random.randint(0, len(POSES)-1)
        while move == self.last_index:
            move = random.randint(0, len(POSES)-1)
        last_index = move
        self.queue.append(POSES[move])

    def execute_move(self, controller):
        if len(self.queue) == 0:
            return
        pose = self.queue.popleft()
        actions = [controller.move_arm_l, controller.move_arm_r, controller.move_body, controller.move_head]
        for i in len(pose):
            actions[i](pose[i])
