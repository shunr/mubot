import random
from collections import deque

# DanceQueue class generates, queues and executes dance moves

POSES = [(180, 0, -1, -1), (0, 180, -1, -1), (45, 45, -1, 180),
         (135, 135, -1, 0), (90, 180, 45, 135), (0, 90, 135, 45),
         (45, -1, 180, 75), (-1, 45, 0, 105), (-1, -1, -1, 90),
         (90, 90, 90, 90)]


class DanceQueue(object):
    def __init__(self, num_chunks, servo_controller, led_controller):
        self.queue = deque()
        self.color = 0
        self.last_index = -1
        self.servo_controller = servo_controller
        self.led_controller = led_controller
        for i in range(num_chunks):
            self._add_move()

    def _add_move(self):
        move = random.randint(0, len(POSES) - 1)
        while move == self.last_index:
            move = random.randint(0, len(POSES) - 1)
        self.last_index = move
        self.queue.append(POSES[move])

    def execute_move(self, intensity):
        if len(self.queue) == 0:
            return
        pose = self.queue.popleft()
        actions = [
            self.servo_controller.move_arm_l,
            self.servo_controller.move_arm_r,
            self.servo_controller.move_body,
            self.servo_controller.move_head
        ]
        for i, position in enumerate(pose):
            if position != -1:
                actions[i](position)

        brightness = min(intensity / 64000, 255)

        if self.color == 0:
            self.led_controller.set_r(brightness)
            self.led_controller.set_g(0)
            self.led_controller.set_b(0)
        elif self.color == 1:
            self.led_controller.set_r(0)
            self.led_controller.set_g(brightness)
            self.led_controller.set_b(0)
        elif self.color == 2:
            self.led_controller.set_r(0)
            self.led_controller.set_g(0)
            self.led_controller.set_b(brightness)
        self.color = (self.color + 1) % 3
