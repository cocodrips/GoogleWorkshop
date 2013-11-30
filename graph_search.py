#!/usr/bin/python
# Google Algorithm Workshop in 2013 Nov.

import sys

class Graph:
  class Node:
    def __init__(self):
      # The following members are the basic information of this node.
      self.name = "" # A node name.
      self.adjacents = [] # A list of adjacent nodes.

      # The following members are used for breadth first search.
      self.previous = None # The node that you visited before this node. This will be used in PrintPath().
      self.distance = 0 # A distance from a start node to this node.
      self.visited = False # A flag to indicate whether this node is already visited during search.

      # The following members are used for bidirectional breadth first search.
      # You can ignore these members if you don't work on BidirectionalBreadthFirstSearch().
      self.reverse_adjacents = []
      self.reverse_previous = None
      self.reverse_distance = 0
      self.reverse_visited = False

  # ==== Basic Exercise [A] ====
  # Reads a given 'file' and constructs a data strucuture for the graph.
  def __init__(self, file):
    self.nodes = []

    input_data = []
    try:
      for line in open(file, "r"):
        input_data += line.strip().split(' ')
    except:
      print "Cannot open file: %s" % file
      sys.exit(1)

    node_num = int(input_data.pop(0))
    name_to_nodes = {}
    for i in xrange(0, node_num):
      name = input_data.pop(0)
      node = Graph.Node()
      node.name = name
      name_to_nodes[name] = node
      self.nodes.append(node)

    edge_num = int(input_data.pop(0))
    for i in xrange(0, edge_num):
      src_name = input_data.pop(0)
      dst_name = input_data.pop(0)
      src_node = name_to_nodes[src_name]
      dst_node = name_to_nodes[dst_name]
      if src_node is None or dst_node is None:
        print "src_node or dst_node not found"
        sys.exit(1)

      src_node.adjacents.append(dst_node)
      dst_node.reverse_adjacents.append(src_node)
    self.reset()

  # A helper method to reset all members of the graph except for 'name', 'adjacents' and 'reverse_adjacents'.
  # You can call this method before starting something to ensure that the graph status is initialized.
  def reset(self):
    for node in self.nodes:
      node.visited = False
      node.distance = 0
      node.previous = None
      node.reverse_visited = False
      node.reverse_distance = 0
      node.reverse_previous = None

  # ==== Basic Exercise [B] ====
  # Calculates and prints a distance from 'src_name' to 'dst_name'.
  def calculate_distance(self, src_name, dst_name):
    self.reset()
    # Implement here.

  # ==== Advanced Exercise [A] ====
  # Calculates and prints the average distance and the max distance (i.e., diameter) of the graph.
  def calculate_average_and_max_distance(self):
    self.reset()
    # Implement here.

  # ==== Advanced Exercise [C] ====
  # Optimized version of calculate_average_and_max_distance().
  def calculate_average_and_max_distance_fast(self):
    self.reset()
    # Implement here.

  # ==== Advanced Exercise [D] ====
  # Optimized version of calculate_distance().
  def calculate_distance_fast(self, src_name, dst_name):
    self.reset()
    # Implement here.

  # ==== Advanced Exercise [E] ====
  # Suggests followers for 'name'.
  # Various algorithms are conceivable.
  # For example, you can print a list of nodes that have more common followers with 'name'.
  # Needless to say, the list should not contain the nodes that 'name' already follows.
  def suggest_followers(self, name):
    self.reset()
    # Implement here.
                                
  # ==== Advanced Exercise [F] ====
  # Calculates pageranks of all nodes in the graph and prints the top 10 nodes.
  def calculate_pagerank(self):
    self.reset()
    # Implement here.

  # The following methods are helper methods for the above methods.

  # Do breadth first search from 'srcNode' to 'dstNode'.
  # Returns a distance from 'srcNode' to 'dstNode'.
  # This method will be used by:
  #   - calculate_distance()
  #   - calculate_average_and_max_distance()
  #   - calculate_average_and_max_distance_fast()
  def breadth_first_search(self, src_node, dst_node):
    # Implement here.
    return -1

  # Do bidirectional breadth first search from 'srcNode' to 'dstNode'.
  # Returns a distance from 'srcNode' to 'dstNode'.
  # This method will be used by:
  #   - calculate_distance_fast()
  def bidirectional_breadth_first_search(self, src_node, dst_node):
    # Implement here.
    return -1

  # Prints a path from 'srcNode' to 'dstNode'.
  # This method traverses 'dstNode' => 'dstNode->previous' => 'dstNode->previous->previous' => ...
  # until the traversal reaches null. By printing the node names in the reverse order of the traversal,
  # you can print a path from 'srcNode' to 'dstNode'. This method will be also useful for debugging.
  # This method will be used by:
  #   - calculate_distance()
  #   - calculate_distance_fast()
  #   - calculate_average_and_max_distance()
  #   - calculate_average_and_max_distance_fast()
  def print_path(self, dst_node):
    path = []
    node = dst_node
    while node is not None:
      path.append(node.name)
      node = node.previous
    path.reverse()
    for i in xrange(0, len(path)):
      if i is not 0:
        print "=>",
      print path[i],
    print ""

  # Returns a Node that has a given 'name'.
  def get_node_from_name(self, name):
    for node in self.nodes:
      if node.name == name:
        return node
    return None


def main():
  if len(sys.argv) is not 3:
    print "usage %s: file [distance|average|average_fast|distance_fast|suggest_followers|pagerank" % sys.argv[0]
    sys.exit(1)

  file = sys.argv[1]
  option = sys.argv[2]
  graph = Graph(file)

  # ==== Basic Exercise [B] ====
  if option == "distance":
    graph.calculate_distance("A", "B")
    graph.calculate_distance("B", "A")

  # ==== Advanced Exercise [A] ====
  elif option == "average":
    graph.calculate_average_and_max_distance()

  # ==== Advanced Exercise [C] ====
  elif option == "average_fast":
    graph.calculate_average_and_max_distance_fast()

  # ==== Advanced Exercise [D] ====
  elif option == "distance_fast":
    graph.calculate_distance_fast("A", "B")
    graph.calculate_distance_fast("B", "A")

  # ==== Advanced Exercise [E] ====
  elif option == "suggest_followers":
    graph.suggest_followers("B")

  # ==== Advanced Exercise [F] ====
  elif option == "pagerank":
    graph.calculate_pagerank()

  else:
    print "Unknown option: %s" % option
    sys.exit(1)

if __name__ == '__main__':
  main()
