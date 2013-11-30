#!/usr/bin/python
# Google Algorithm Workshop in 2013 Nov.

import sys
import Queue
import time

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
  def calculate_distance(self, src_name, dst_name, memo = {}):
    self.reset()
    src = self.get_node_from_name(src_name)
    dst = self.get_node_from_name(dst_name)

    node_list = Queue.Queue()

    src.visited = True
    src.distance = 0
    node_list.put(src)

    while node_list.qsize != 0:
      node = node_list.get()
      if node == dst:
        # self.print_path(node)
        return dst.distance
      if not memo.has_key(node.name):
        memo[node.name] = {}

      for adjacent in node.adjacents:
        if adjacent.visited:
          continue
        else:
          adjacent.visited = True
          adjacent.distance = node.distance + 1
          adjacent.previous = node
          if not memo[src.name].has_key(adjacent.name):
            memo[src.name][adjacent.name] = adjacent.distance
          node_list.put(adjacent)

    return -1


  # ==== Advanced Exercise [A] ====
  # Calculates and prints the average distance and the max distance (i.e., diameter) of the graph.
  def calculate_average_and_max_distance(self):
    self.reset()
    dist_max = 0
    dist_sum = 0

    for src in self.nodes:
      for dst in self.nodes:
        if src == dst:
          continue
        else:
          dist = self.calculate_distance(src.name, dst.name)
          if dist > dist_max:
            dist_max = dist
          dist_sum = dist_sum + dist

    print dist_sum
    average = float(dist_sum) / float((len(self.nodes) * (len(self.nodes) - 1)))

    return (average, dist_max)


  # ==== Advanced Exercise [C] ====
  # Optimized version of calculate_average_and_max_distance().
  def calculate_average_and_max_distance_fast(self):
    self.reset()
    # Implement here.
    memo = {}
    max_dist = 0
    sum_dist = 0

    for src in self.nodes:
      for dst in self.nodes:
        # print "src: " + src.name + " dst: " + dst.name + str(memo)
        if src == dst:
          continue
        if not memo.has_key(src.name):
          memo[src.name] = {}
        if not memo[src.name].has_key(dst.name):
          dist = self.calculate_distance(src.name, dst.name, memo)
        else:
          dist = memo[src.name][dst.name]
          # print "src.name" + src.name + " dst.name" + dst.name
        if max_dist < dist:
          max_dist = dist
        sum_dist = sum_dist + dist

    print sum_dist
    average = float(sum_dist) / float((len(self.nodes) * (len(self.nodes) - 1)))

    return (average, max_dist)

  # ==== Advanced Exercise [D] ====
  # Optimized version of calculate_distance().
  def calculate_distance_fast(self, src_name, dst_name, memo={}):
    self.reset()
    src = self.get_node_from_name(src_name)
    dst = self.get_node_from_name(dst_name)
    src.visited = True
    queue1 = Queue.Queue()
    queue1.put(src)
    queue2 = Queue.Queue()
    queue2.put(dst)
 
    q1 = queue1.get()
    q2 = queue2.get()
 
    while True:
      while q1.distance <= q2.distance:
        for adjacent in q1.adjacents:
          if not adjacent.visited:
            adjacent.previous = q1
            adjacent.distance = q1.distance + 1
            adjacent.visited = True
            if not memo.has_key(q1.name):
              memo[q1.name] = {}
            if not memo[q1.name].has_key(adjacent.name):
              memo[q1.name][adjacent.name] = adjacent.distance
            if adjacent.reverse_visited:
              return adjacent.distance + adjacent.reverse_distance
            queue1.put(adjacent)
        q1 = queue1.get()
 
      while q2.distance < q1.distance:
        for adjacent in q2.adjacents:
          if not adjacent.reverse_visited:
            adjacent.reverse_previous = q2
            adjacent.reverse_distance = q2.reverse_distance + 1
            adjacent.reverse_visited = True
            if not memo.has_key(q2.name):
              memo[q2.name] = {}
            if not memo[q2.name].has_key(adjacent.name):
              memo[q2.name][adjacent.name] = adjacent.distance
            if adjacent.visited:
              return adjacent.distance + adjacent.reverse_distance
            queue2.put(adjacent)
        q2 = queue2.get()

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
    ans1 = graph.calculate_distance("A", "B")
    ans2 = graph.calculate_distance("B", "A")
    print "distance1: " + str(ans1)
    print "distance2: " + str(ans2)

  # ==== Advanced Exercise [A] ====
  elif option == "average":
    start = time.clock()
    (average, dist_max) = graph.calculate_average_and_max_distance()
    goal = time.clock()
    print "average: " + str(average)
    print "max: " + str(dist_max)
    print "time: " + str(goal - start)

  # ==== Advanced Exercise [C] ====
  elif option == "average_fast":
    start = time.clock()
    (average, dist_max) = graph.calculate_average_and_max_distance_fast()
    goal = time.clock()
    print "average: "  + str(average)
    print "max: " + str(dist_max)
    print "time: " + str(goal - start)

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
