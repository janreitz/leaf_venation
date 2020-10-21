import math
from vector import Vec
import polygon_helper
import vein
from quad_tree import QuadTree, BoundingBox
from random_helper import random_points_on_curve

# globals
sources = {}
root_vein = None
margin = []
origin = Vec(0,0)
_quad_tree = None
pause = False
growth_factor = 5
i = 0

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
  

def setup():
    global margin
    global _quad_tree
    global root_vein
    global origin
    size(1000,1000)
    background(255)
    frameRate(2)
    stroke(61, 103, 0)
    origin = Vec(width/2, height - 100)
    original_margin_radius = 100
    margin = [
        Vec(origin.x - original_margin_radius,origin.y), 
        Vec(origin.x - original_margin_radius,origin.y - 2 * original_margin_radius), 
        Vec(origin.x + original_margin_radius,origin.y - 2* original_margin_radius), 
        Vec(origin.x + original_margin_radius,origin.y)
    ]
    _quad_tree = QuadTree(BoundingBox(0, 0, width, height))
    root_vein = vein.Branch(origin, _quad_tree)
    
def draw():
    global margin
    global root_vein
    global sources
    global origin
    global _quad_tree
    global i
    global growth_factor
    
    if not pause:
        background(255)
        #growth_factor *= 0.95
        margin = uniform_linear_growth(margin, growth_factor, origin)
            
        # generate new sources
        new_sources = random_points_on_curve(5, margin + [margin[0]])
        for new_source in new_sources:
            # is the new source valid?
            if polygon_helper.is_within(new_source, margin):
                # Too close to existing sources
                x = round_to(new_source.x, gridsize)
                y = round_to(new_source.y, gridsize)
                if (x,y) not in sources:
                    sources[(x,y)] = new_source
        
        # render
        fill(0,255,0)
        strokeWeight(1)
        beginShape()
        for i in margin:
            vertex(i.x, i.y)
        endShape()
        
        for key, source in sources.items():
            # find closest segment
            closest = _quad_tree.lookup_closest(source.x, source.y)
            strokeWeight(1)
            stroke(0,0,255)
            line(source.x, source.y, closest.pos.x, closest.pos.y)
            closest.register_source(source)
            if (source - closest.pos).mag() < 20:
                del sources[key]
        
        root_vein.update()
                
        for p in sources.values():
            fill(255,0,0)
            circle(p.x, p.y, 5)
            
        root_vein.draw()
    
def mouseClicked():
    global pause
    pause = not pause
    
    
    
    
