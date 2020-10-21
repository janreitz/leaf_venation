import math
import vector

class Branch():
    i = 0
    def __init__(self, pos, quad_tree):
        self.pos = pos
        self.children = []
        self.sources = []
        self.thickness = 1
        self.quad_tree = quad_tree
        quad_tree.insert(pos.x, pos.y, self)
        self.i = Branch.i
        Branch.i += 1

    def branch(self):
        #print("Branch")
        if len(self.sources) == 0:
            return
        
        pull = vector.Vec(0,0)
        for source in self.sources:
            dist = (source - self.pos)
            pull += dist

        angle = pull.angle()
                    
        # New Branch
        new_shape = vector.vec_from_angle(angle).mult_scalar(10)
        branch = Branch(self.pos + new_shape, self.quad_tree)

        self.children.append(branch)
        
    def register_source(self, source):
        #print("Registering source")
        self.sources.append(source)

    def update_thickness(self):
        sum_squared_thicknesses = 1
        for child in self.children:
            sum_squared_thicknesses += child.thickness#**2
        new_thickness = math.sqrt(sum_squared_thicknesses)
        print("Updating thickness from " + str(self.thickness) + " to " + str(new_thickness) )
        self.thickness = new_thickness

    def update(self):
        for child in self.children:
            child.update()
            
        if not len(self.sources) == 0:
            self.branch()
            # reset sources
            self.sources = []
            
        self.update_thickness()
        
    def draw(self):
        #print("My drawing thickness is " + str(self.thickness))
        for child in self.children:
            child.draw()
            strokeWeight(self.thickness)
            stroke(0)
            line(self.pos.x, self.pos.y, child.pos.x, child.pos.y)
            
if __name__ == "__main__":
    from vector import Vec
    from quad_tree import QuadTree, BoundingBox

    q_tree = QuadTree(BoundingBox(-1,-1,1,1))
    root = Branch(Vec(0,0), q_tree)

    q_tree.insert(0,0,root)

    hopefully_root = q_tree.lookup_closest(0,0)

    print(root is hopefully_root)

    root.register_source(Vec(0.5,0.5))
    root.update()

    print("something")
