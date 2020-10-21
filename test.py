import math
import random
from vector import Vec
import polygon_helper
import vein
from quad_tree import QuadTree, BoundingBox

# globals
sources = {}
root_vein = None
margin = []
origin = Vec(0,0)
_quad_tree = None


width = 1000
height = 1000

gridsize = 20

def round_to(num, multiple_of):
    return round(num/multiple_of) * multiple_of

def uniform_exponential_growth(iterable, factor, reference = Vec(0,0)):
    temp = []
    for i in iterable:
        temp +=  [reference + (i - reference).mult_scalar(factor)]
    return temp

def uniform_linear_growth(iterable, factor, reference = Vec(0,0)):
    temp = []
    for i in iterable:
        temp.append(i + (i - reference).set_mag(factor))
    return temp

def random_points(n, x1, x2, y1, y2):
    return [Vec(random.uniform(x1, x2), random.uniform(y1, y2)) for _ in range(n)]

def setup():
    global margin
    global _quad_tree
    global root_vein
    global origin
    origin = Vec(width/2, height - 100)
    margin = [Vec(origin.x - 100,origin.y), Vec(origin.x - 100,origin.y - 200), Vec(origin.x + 100,origin.y - 200), Vec(origin.x + 100,origin.y)]
    _quad_tree = QuadTree(BoundingBox(0, 0, width, height))
    root_vein = vein.Branch(origin, _quad_tree)
    
def draw():
    global margin
    global root_vein
    global sources
    global origin
    global _quad_tree
    margin = uniform_linear_growth(margin, 1.05, origin)
        
    # generate new sources
    new_sources = random_points(5, *polygon_helper.bounds(margin))
    for new_source in new_sources:
        # is the new source valid?
        if polygon_helper.is_within(new_source, margin):
            # Spatial Hashing to avoid sources too close to each other
            x = round_to(new_source.x, gridsize)
            y = round_to(new_source.y, gridsize)
            if (x,y) not in sources:
                sources[(x,y)] = new_source

    # register source with closest vein segment    
    for source in sources.values():
        closest = _quad_tree.lookup_closest(source.x, source.y)
        closest.register_source(source)
        
        if (source - closest.pos).mag() < 20:
            print("deleting source")
            del sources[(source.x, source.y)]
        
    root_vein.update()
    print("Current Depth: " + str(_quad_tree.depth))
    
if __name__ == "__main__":

    setup()

    for i in range(30):
        draw()
