import math

class BoundingBox():
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
    
    def __str__(self):
        return "(" + str(self.min_x) + "|" + str(self.min_y) + ") - ("+ str(self.max_x) + "|" + str(self.max_y) + ")"

    def intersects(self, other):
        min_x = max(self.min_x, other.min_x)
        max_x = min(self.max_x, other.max_x)
        if min_x < max_x: 
            return True
        min_y = max(self.min_y, other.min_y)
        max_y = min(self.max_y, other.max_y)
        return min_y < max_y

    def contains(self, x, y):
        if x < self.min_x or x > self.max_x:
            return False
        if y < self.min_y or y > self.max_y:
            return False
        return True

class PositionalData():
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data

class Node():
    i = 0
    def __init__(self, bounding_box):
        self.bounding_box = bounding_box
        self.children = []
        self.data = []
        self.id = Node.i
        Node.i += 1

    def __str__(self):
        return str(self.bounding_box) + "; " + str(self.data)

    def is_leaf(self):
        return len(self.children) == 0

    def is_empty(self):
        return len(self.data) == 0

    def center(self):
        x = (self.bounding_box.max_x + self.bounding_box.min_x)/2
        y = (self.bounding_box.max_y + self.bounding_box.min_y)/2
        return x, y

    # 0 1
    # 2 3
    def identify(self, x, y):
        center_x, center_y = self.center() 
        sum = 0
        if x >= center_x:
            sum += 1
        if y >= center_y:
            sum += 2
        #print("identify (" + str(x) + "|" + str(y) + ") as " + str(sum))
        return sum

    def subdivide(self):
        center_x, center_y = self.center()
        #print("Center: (" + str(center_x) + "|" + str(center_y) + ")")

        # print(
        #     str(BoundingBox(self.bounding_box.min_x, self.bounding_box.min_y, center_x, center_y)) + "; " +
        #     str(BoundingBox(center_x, self.bounding_box.min_y, self.bounding_box.max_x, center_y)) + "; " +
        #     str(BoundingBox(self.bounding_box.min_x, center_y, center_x, self.bounding_box.max_y)) + "; " +
        #     str(BoundingBox(center_x, center_y, self.bounding_box.max_x, self.bounding_box.max_y)) 
        # )

        self.children.append(Node(BoundingBox(self.bounding_box.min_x, self.bounding_box.min_y, center_x, center_y)))
        self.children.append(Node(BoundingBox(center_x, self.bounding_box.min_y, self.bounding_box.max_x, center_y)))
        self.children.append(Node(BoundingBox(self.bounding_box.min_x, center_y, center_x, self.bounding_box.max_y)))
        self.children.append(Node(BoundingBox(center_x, center_y, self.bounding_box.max_x, self.bounding_box.max_y)))

        for d in self.data:
            # assign positional data to children
            # print("Data goes to child: " + str(self.identify(d.x, d.y)))
            self.children[self.identify(d.x, d.y)].data.append(d)

        self.data = []

    def bounding_box_lookup(self, bounding_box):
        if not self.bounding_box.intersects(bounding_box):
            return []

        data = list(self.data)
        for child in self.children:
            data += child.bounding_box_lookup(bounding_box)
        #print(f"bounding_box_lookup -> len(self.data) {len(self.data)} len(data) {len(data)}")
        return data

    def lookup(self, x, y):
        if not self.bounding_box.contains(x, y):
            return None

        if self.is_leaf:
            return self.data
        else:
            return self.children[self.identify(x, y)].lookup(x, y)
            
class QuadTree():
    def __init__(self, bounding_box):
        self.root = Node(bounding_box)
        self.depth = 1
        self.max_depth = 20

    def bounding_box_lookup(self, bounding_box):
        return self.root.bounding_box_lookup(bounding_box)

    def lookup(self, x, y):
        return self.root.lookup(x, y)

    def lookup_closest(self, x, y):
        candidates = []
        
        max_width = self.root.bounding_box.max_x - self.root.bounding_box.min_x
        max_height = self.root.bounding_box.max_y - self.root.bounding_box.min_y

        current_width = max_width * 0.5**self.depth
        current_height = max_height * 0.5**self.depth
        while len(candidates) == 0 and current_width <= max_width:
            search_window = BoundingBox(x - current_width, y - current_height, x + current_width, y + current_height)
            candidates += self.root.bounding_box_lookup(search_window)
            current_width *= 2
            current_height *= 2

        min_dist = (self.root.bounding_box.max_x - self.root.bounding_box.min_x)**2 + (self.root.bounding_box.max_y - self.root.bounding_box.min_y)**2
        min_index = None
        #print(f"lookup_closest -> len(candidates) {len(candidates)}")
        for i, d in enumerate(candidates):
            dist = (d.x - x)**2 + (d.y - y)**2
            if dist < min_dist:
                min_dist = dist
                min_index = i
        if min_index == None: 
            return None
        return candidates[min_index].data

    def insert(self, x, y, data):
        if not self.root.bounding_box.contains(x, y):
            return False

        node = self.root
        depth = 1
        # find the right leaf
        while not node.is_leaf():
            node = node.children[node.identify(x, y)]
            depth += 1
        # subdivide until the relevant leaf is free
        while not node.is_empty() and depth < self.max_depth:
            node.subdivide()
            #print("Assigning " + str(node.identify(x, y)) + " as new node")
            node = node.children[node.identify(x, y)]
            depth += 1
        
        self.depth = max(self.depth, depth)
        #print(f"insert -> appending data, current length: {len(node.data)}")
        node.data.append(PositionalData(x, y, data))
        
if __name__ == "__main__":

    tree = QuadTree(BoundingBox(0,0,7,7))
    tree.insert(6, 6, "hi")
    tree.insert(5, 5, "hi again")

    #lookup_data = tree.bounding_box_lookup(b)
    #print(lookup_data)
    
    print(tree.lookup_closest(5, 6))
