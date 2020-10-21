import random
import vector

def random_points(n, x1, x2, y1, y2):
    return [Vec(random(x1, x2), random(y1, y2)) for _ in range(n)]

def random_points_on_curve(n, curve):
    # curve is assumed to be [Vec]
    cum_dists = [0]
    for i, j in zip(curve[:-1], curve[1:]):
        dist = (i - j).mag()
        cum_dists.append(cum_dists[-1] + dist)

    rands = [random.uniform(0, cum_dists[-1]) for _ in range(n)]
    points = []
    for rand in rands:
        # find points to interpolate between
        for i, dist in enumerate(cum_dists):
            if rand < dist:
                interpolation_dist = rand - cum_dists[i-1]
                point = vector.interpolate(curve[i-1], curve[i], interpolation_dist)
                points.append(point)
                break

    return points


# if __name__ == "__main__":
#     curve = [
#         vector.Vec(0,0),
#         vector.Vec(1,0),
#         vector.Vec(1,1),
#         vector.Vec(0,1),
#     ]

#     points = random_points_on_curve(100, curve)

#     print("bla")
