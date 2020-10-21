import math

def deg2rad(deg):
    return math.pi/180*deg

def rad2deg(rad):
    return 180/math.pi*rad

def vec_from_angle(rad):
        x = math.cos(rad)
        y = math.sin(rad)
        return Vec(x, y)

def interpolate(vec1, vec2, dist):
    delta = vec2 - vec1
    if delta.mag() == 0:
        print("This should not happen")
        return vec1
    delta.set_mag(dist)
    return vec1 + delta

class Vec():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self):
        return math.atan2(self.y, self.x)
    
    def mult_scalar(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)
        
    def normalize(self):
        mag = self.mag()
        if mag == 0:
            return None
        self.x /= mag
        self.y /= mag
        return self

    def set_mag(self, mag):
        self.normalize()
        self.x *= mag
        self.y *= mag
        return self

if __name__ == "__main__":
    # initial_1 = Vec(1,1)
    # initial_2 = Vec(-1,-1)
    # initial_3 = Vec(-1,1)
    # initial_4 = Vec(1,-1)
    # from_angle_1 = vec_from_angle(initial_1.angle())
    # from_angle_2 = vec_from_angle(initial_2.angle())
    # from_angle_3 = vec_from_angle(initial_3.angle())
    # from_angle_4 = vec_from_angle(initial_4.angle())
    # print(f"Test 1: {initial_1.angle() == from_angle_1.angle()}")
    # print(f"Test 2: {initial_2.angle() == from_angle_2.angle()}")
    # print(f"Test 3: {initial_3.angle() == from_angle_3.angle()}")
    # print(f"Test 4: {initial_4.angle() == from_angle_4.angle()}")
    # print(f"Test 5: {from_angle_1.mag() == 1}")
    v = Vec(5,5)
    v.normalize()

    print("Test1: " + str(v.mag() == 1))

    v.set_mag(10)
    print("Test2: " + str(v.mag() == 10))