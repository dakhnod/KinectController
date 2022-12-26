class Joint:
    def __init__(self, x, y, z, orientation_x, orientation_y, orientation_z, x_projected, y_projected):
        self.x = x
        self.y = y
        self.z = z
        self.orientation_x = orientation_x
        self.orientation_y = orientation_y
        self.orientation_z = orientation_z
        self.x_projected = x_projected
        self.y_projected = y_projected

    def get_position_projected(self):
        return (self.x_projected, self.y_projected)

class Body:
    def __init__(self):
        self.joints = {}
    
    def add_joint(self, joint_index, position_real, orientation, position_projected):
        self.joints[joint_index] = Joint(
            position_real.x,
            position_real.y,
            position_real.z,
            orientation.x,
            orientation.y,
            orientation.z,
            position_projected.x,
            position_projected.y
        )

    def get_joint_SpineBase(self): return self.joints[0]
    def get_joint_SpineMid(self): return self.joints[1]
    def get_joint_Neck(self): return self.joints[2]
    def get_joint_Head(self): return self.joints[3]
    def get_joint_ShoulderLeft(self): return self.joints[4]
    def get_joint_ElbowLeft(self): return self.joints[5]
    def get_joint_WristLeft(self): return self.joints[6]
    def get_joint_HandLeft(self): return self.joints[7]
    def get_joint_ShoulderRight(self): return self.joints[8]
    def get_joint_ElbowRight(self): return self.joints[9]
    def get_joint_WristRight(self): return self.joints[10]
    def get_joint_HandRight(self): return self.joints[11]
    def get_joint_HipLeft(self): return self.joints[12]
    def get_joint_KneeLeft(self): return self.joints[13]
    def get_joint_AnkleLeft(self): return self.joints[14]
    def get_joint_FootLeft(self): return self.joints[15]
    def get_joint_HipRight(self): return self.joints[16]
    def get_joint_KneeRight(self): return self.joints[17]
    def get_joint_AnkleRight(self): return self.joints[18]
    def get_joint_FootRight(self): return self.joints[19]
    def get_joint_SpineShoulder(self): return self.joints[20]
    def get_joint_HandTipLeft(self): return self.joints[21]
    def get_joint_ThumbLeft(self): return self.joints[22]
    def get_joint_HandTipRight(self): return self.joints[23]
    def get_joint_ThumbRight(self): return self.joints[24]