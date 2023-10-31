# D* Lite Algorithm
#### This Program implements the DStar lite algorithm based on the D* Lite Psuedo code presented in the following path planning paper [1]

"Anytime Dynamic A\*: An Anytime, Replanning Algorithm" 


## How to use the program
#### Example graph for this demo is as shown below

![Alt text](./images/1.png?raw=true "Initial graph")

##### Step 1: Initalie graph in the Graph.py as shown below

```python 
    #define and start and goal node names
        #the same needs to be used in the graph creation
        self.start_node_name = "xs"
        self.goal_node_name = "xg"

        #Create the graph using the node objects
        #Ex node creation: 
        #   node(node_name, {parent:action_cost, ...}, G, rhs, heuristc_cost_to_come)

        #Add created nodes into the node dictionary
        self.nodes["xs"] = node("xs", [], math.inf, math.inf, 0)
        self.nodes["xg"] = node("xg", {"x4":1, "x7": 1, "x8": 1}, math.inf, 0, 5)

        self.nodes["x8"] = node("x8", {"xs":7}, math.inf, math.inf, 1)
        self.nodes["x7"] = node("x7", {"x6":6}, math.inf, math.inf, 3)
        self.nodes["x6"] = node("x6", {"x5":1}, math.inf, math.inf, 2)
        self.nodes["x5"] = node("x5", {"x1":1, "xs":13}, math.inf, math.inf, 1)
        self.nodes["x4"] = node("x4", {"x3":1}, math.inf, math.inf, 8)
        self.nodes["x3"] = node("x3", {"x2":1}, math.inf, math.inf, 6)
        self.nodes["x2"] = node("x2", {"x1":1}, math.inf, math.inf, 5)
        self.nodes["x1"] = node("x1", {"xs":1}, math.inf, math.inf, 1)

```


##### Step 2: Run D* Lite algorithm and press enter
``` sh
 python3 DStartLite.py
```

##### The algorithm shall find the optimal path and same has been illustrated for the example graph as below

#####  Program output:

![Alt text](./images/7.png?raw=true "Discovered optimal path")

#####  Illustration:
![Alt text](./images/5.png?raw=true "Discovered optimal path")

##### Step 3: To introduce dynamic obstacle, the program requests to user for new link cost when the program displays the below prompt

![Alt text](./images/3.png?raw=true "Introducing Dynamic obstacle in the graph")

##### Step 4: The user can modify the graph with updated cost for each link seperated by semi-colon as shown below 

##### ex: parent_node,cost,child_node;parent_node,cost,child_node

``` sh
 Please enter edge updates (ex-format : x1,100,x2;x2,100,x3 ): x1,100,x2
```
##### For the above cost update the modified graph would look like this

![Alt text](./images/4.png?raw=true "Initial graph")

##### Step 5: For the above updated graph, a new path will be discovered as shown below.

![Alt text](./images/6.png?raw=true "Initial graph")

###### <br />
##### References
###### <a id="1">[1]</a>  Maxim Likhachev and David Ferguson and Geoffrey Gordon and Anthony (Tony) Stentz and Sebastian Thrun. (2005). 
###### The D* Lite Algorithm (basic version).
###### Anytime Dynamic A\*: An Anytime, Replanning Algorithm, Figure 2.