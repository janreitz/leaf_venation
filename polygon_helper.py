def bounds(polygon):
    x_low = 999999
    y_low = 999999
    x_high = -999999
    y_high = -999999
    for p in polygon:
        if p.x < x_low: x_low = p.x
        if p.x > x_high: x_high = p.x
        if p.y < y_low: y_low = p.y
        if p.y > y_high: y_high = p.y
    return (x_low, x_high, y_low, y_high)
    
def line_coefficients(x1,y1,x2,y2):
    # infinite lines of the form a*x + b*y + c
    a = y2 - y1
    b = x2 - x1
    c = (x2*y1) - (x1*y2)
    return [a, b, c]
    
def areIntersecting( v1x1, v1y1, v1x2, v1y2, v2x1, v2y1, v2x2, v2y2):
    # Convert vector 1 to a line (line 1) of infinite length.
    # We want the line in linear equation standard form: A*x + B*y + C = 0
    # See: http://en.wikipedia.org/wiki/Linear_equation
    a1 = v1y2 - v1y1
    b1 = v1x1 - v1x2
    c1 = (v1x2 * v1y1) - (v1x1 * v1y2)

    # Every point (x,y), that solves the equation above, is on the line,
    # every point that does not solve it, is not. The equation will have a
    # positive result if it is on one side of the line and a negative one 
    # if is on the other side of it. We insert (x1,y1) and (x2,y2) of vector
    # 2 into the equation above.
    d1 = (a1 * v2x1) + (b1 * v2y1) + c1
    d2 = (a1 * v2x2) + (b1 * v2y2) + c1

    # If d1 and d2 both have the same sign, they are both on the same side
    # of our line 1 and in that case no intersection is possible. Careful, 
    # 0 is a special case, that's why we don't test ">=" and "<=", 
    # but "<" and ">".
    if d1 > 0 and d2 > 0:
        return False
    if d1 < 0 and d2 < 0:
        return False

    # The fact that vector 2 intersected the infinite line 1 above doesn't 
    # mean it also intersects the vector 1. Vector 1 is only a subset of that
    # infinite line 1, so it may have intersected that line before the vector
    # started or after it ended. To know for sure, we have to repeat the
    # the same test the other way round. We start by calculating the 
    # infinite line 2 in linear equation standard form.
    a2 = v2y2 - v2y1
    b2 = v2x1 - v2x2
    c2 = (v2x2 * v2y1) - (v2x1 * v2y2)

    # Calculate d1 and d2 again, this time using points of vector 1.
    d1 = (a2 * v1x1) + (b2 * v1y1) + c2
    d2 = (a2 * v1x2) + (b2 * v1y2) + c2

    # Again, if both have the same sign (and neither one is 0),
    # no intersection is possible.
    if d1 > 0 and d2 > 0: 
        return False
    if d1 < 0 and d2 < 0: 
        return False

    # If we get here, only two possibilities are left. Either the two
    # vectors intersect in exactly one point or they are collinear, which
    # means they intersect in any number of points from zero to infinite.
    if (a1 * b2) - (a2 * b1) == 0.0:
        return 3

    # If they are not collinear, they must intersect in exactly one point.
    return True



def is_within(p, polygon):
    # bounding box check
    x_low, x_high, y_low, y_high = bounds(polygon)
    if p.x < x_low or p.x > x_high: 
        return False
    if p.y < x_low or p.y > y_high:
        return False
    
    # ray casting
    start = (x_low - 10, y_low - 9)
    intersections = 0
    for p1, p2 in zip(polygon, polygon[1:] + [polygon[0]]):
        if areIntersecting(start[0], start[1], p.x, p.y, p1.x, p1.y, p2.x, p2.y) == 1:
            intersections += 1
        
    if intersections%2 == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    print("lets go")

    class Point():
        def __init__(self, x, y):
            self.x = x
            self.y = y

    a = Point(1,0)
    b = Point(1,1)
    c = Point(0,1)
    d = Point(0,0)

    poly = [a,b,c,d]

    test = Point(0.5, 0.5)

    a, b, c = line_coefficients(0,0,1,1)
    a, b, c = line_coefficients(0,1,1,0)

    if is_within(test, poly):
        print("works")
    else:
        print("doesn't work")
