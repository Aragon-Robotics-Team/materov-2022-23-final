
class Numbers:
    def __init__(self):
        self.yaw_x = None
        self.shift_x = None
        self.shift_y = None
        self.heave_a = None
        self.heave_b = None

        self.middle_pwm = 1500
        self.max_pwm = 1725
        self.min_pwm = 1275
        self.pwm_k = self.max_pwm-self.middle_pwm

    def set_controller_vals(self, ls):
        self.shift_x = ls[0]
        self.shift_y = ls[1]
        self.yaw_x = ls[2]
        self.heave_a = ls[3]
        self.heave_b = ls[4]
