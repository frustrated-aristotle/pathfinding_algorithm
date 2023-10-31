/*
Developed By: Muhammad Murtaza
Desc: D* Lite (algorithm) Script responsible for finding shortest path in a dynamic environment.
*/


using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;

public class DstarLite : MonoBehaviour
{
    public Camera mainCamera;
    public GameObject dynamicObstacle;

    DstarLitePathRequestManager requestManager;
    DstarLiteGrid grid;

    Vector3 nextMove;    
    private double kmFactor;    

    private DstarLiteNode startNode;
    private DstarLiteNode targetNode;
    private DstarLiteNode lastNode;
    private int numOfObstacles = 7;
    bool replanReturn = false;
    Vector3[] waypoints = new Vector3[0];

    private Heap<DstarLiteNode> openSet;
    Hashtable cellHash = new Hashtable();        
    List<DstarLiteNode> updatedNodes = new List<DstarLiteNode>();    
    List<DstarLiteNode> path = new List<DstarLiteNode>();

    void Awake()
    {
        requestManager = GetComponent<DstarLitePathRequestManager>();
        grid = GetComponent<DstarLiteGrid>();
        
    }

    public void StartFindPath(Vector3 startPos, Vector3 targetPos, bool isFollowing)
    {        
        StartCoroutine(FindPath(startPos, targetPos, isFollowing));
    }
    

    /// <summary>
    /// This Update function handles the mouse input and instantiate the dynamic obstacles
    /// </summary>
    void Update()
    {        

        if (Input.GetMouseButtonUp(0))  // Mouse's left button is clicked
        {
            RaycastHit hit;
            Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit, 10000))
            {
                DstarLiteNode nodeHit = grid.NodeFromWorldPoint(hit.point);
                if (nodeHit != null && (!nodeHit.Equal(startNode)) && (!nodeHit.Equal(targetNode)))
                {
                    if (!double.IsPositiveInfinity(nodeHit.cost))
                    {
                        updatedNodes.Add(nodeHit);

                        Instantiate(dynamicObstacle, nodeHit.worldPosition, Quaternion.identity);
                    }

                    int tempX = nodeHit.gridX;
                    int tempY;
                    for (int y = 1; y < numOfObstacles; y++)
                    {                        
                        tempY = nodeHit.gridY + y;

                        if (tempY >= 0 && tempY < grid.gridWorldSize.y) // Checking it is within grid's y-axis boundary 
                        {
                            DstarLiteNode node = grid.NodeFromPos(tempX, tempY);
                            updatedNodes.Add(node);

                            Instantiate(dynamicObstacle, node.worldPosition, Quaternion.identity);  // Spawning obstacles vertically
                        }
                    }
                }
            }
        }

        if (Input.GetMouseButtonUp(1))  // Mouse's right button is clicked
        {
            RaycastHit hit;
            Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit, 100000))
            {
                DstarLiteNode nodeHit = grid.NodeFromWorldPoint(hit.point);
                if (nodeHit != null && (!nodeHit.Equal(startNode)) && (!nodeHit.Equal(targetNode)))
                {
                    if (!double.IsPositiveInfinity(nodeHit.cost))
                    {
                        updatedNodes.Add(nodeHit);

                        Instantiate(dynamicObstacle, nodeHit.worldPosition, Quaternion.identity);
                    }

                    int tempX;
                    int tempY = nodeHit.gridY;

                    // Spawning obstacles on the mouse position
                    for (int x = 1; x < numOfObstacles; x++)
                    {                        
                        tempX = nodeHit.gridX + x;

                        if (tempX >= 0 && tempX < grid.gridWorldSize.x)  // Checking it is within grid's x-axis boundary 
                        {                        
                            DstarLiteNode node = grid.NodeFromPos(tempX, tempY);
                            updatedNodes.Add(node);

                            Instantiate(dynamicObstacle, node.worldPosition, Quaternion.identity);  // Spawning obstacles Horizontally
                        }
                    }
                }
            }
        }
    }

    /// <summary>
    /// Compares primary/secondary key values
    /// </summary>
    /// <param name="key1"></param>
    /// <param name="key2"></param>
    /// <returns></returns>
    public bool CompareKey(Pair<double, double> key1, Pair<double, double> key2)
    {
        if (key1.First < key2.First)
            return true;
        else if (key1.First > key2.First)
            return false;
        else if (key1.Second < key2.Second)
            return true;
        else if (key1.Second > key2.Second)
            return false;

        return false;
    }    

    private Pair<double, double> CalculateKey(DstarLiteNode u)
    {
        double val = Math.Min(RHS(u), G(u));

        Pair<double, double> key = new Pair<double, double>(0,0);
        key.First = val + Heuristic(startNode, u) + kmFactor;
        key.Second = val;

        return key;
    }

    private double RHS(DstarLiteNode node, double value = double.MinValue)
    {
        if (node.Equal(targetNode))
            return 0.0;

        MakeNewCell(node);

        Pair<double, double> g_rhs = (Pair<double, double>)cellHash[node];

        if (value != double.MinValue)
        {
            g_rhs.Second = value;            
            cellHash[node] = g_rhs;
        }

        return g_rhs.Second;
    }

    private double G(DstarLiteNode node, double value = double.MinValue)
    {
        MakeNewCell(node);

        Pair<double, double> g_rhs = (Pair<double, double>)cellHash[node];

        if (value != double.MinValue)
        {
            g_rhs.First = value;
            cellHash[node] = g_rhs;            
        }

        return g_rhs.First;
    }

    private void MakeNewCell(DstarLiteNode u)
    {
        if (cellHash.Contains(u))
            return;        

        double h = double.PositiveInfinity;        
        cellHash.Add(u, new Pair<double, double>(h, h));
    }

    private void AddToOpenList(DstarLiteNode node)
    {
        openSet.Add(node);
    }

    private void UpdateOpenList(DstarLiteNode node)
    {
        openSet.UpdateItem(node);
    }

    private void RemoveFromOpenList(DstarLiteNode node)
    {
        openSet.Remove(node);
    }

    /// <summary>
    /// Initializes the value of necessary components related to the algorithm
    /// </summary>
    /// <param name="startPos"></param>
    /// <param name="targetPos"></param>
    /// <returns></returns>
    private bool Init(Vector3 startPos, Vector3 targetPos)
    {
        startNode = grid.NodeFromWorldPoint(startPos);
        targetNode = grid.NodeFromWorldPoint(targetPos);

        if (startNode.isWalkable && targetNode.isWalkable)
        {
            openSet = new Heap<DstarLiteNode>(grid.MaxSize);

            kmFactor = 0;            

            Pair<double, double> key = CalculateKey(targetNode);
            targetNode.key = key;

            AddToOpenList(targetNode);

            lastNode = startNode;

            return true;
        }
        else
        {
            return false;
        }
    }

    /// <summary>
    /// Add/Remove Node to/from the required list
    /// </summary>
    /// <param name="u"></param>
    private void UpdateVertex(DstarLiteNode u)
    {
        bool diff = G(u) != RHS(u);
        bool exists = openSet.Contains(u);

        if (diff && exists)
        {
            u.key = CalculateKey(u);
            UpdateOpenList(u);
        }
        else if (diff && !exists)
        {
            u.key = CalculateKey(u);
            AddToOpenList(u);
        }
        else if (!diff && exists)
        {
            RemoveFromOpenList(u);
        }
    }

    private int ComputeShortestPath()
    {
        if (openSet.Count == 0)
            return 1;        

        DstarLiteNode u;
        Pair<double, double> kOld;
        Pair<double, double> kNew;
        List<DstarLiteNode> predecessorNodes = new List<DstarLiteNode>();
        double gOld;
        double tempG;
        double tempRHS;

        while (openSet.Count > 0 && ((CompareKey(openSet.First().key, CalculateKey(startNode))) ||
               (!Math.Equals(RHS(startNode), G(startNode)))))
        {            

            u = openSet.First();
            kOld = u.key;
            kNew = CalculateKey(u);

            tempRHS = RHS(u);
            tempG = G(u);            

            if (CompareKey(kOld, kNew))
            {
                u.key = kNew;
                UpdateOpenList(u);
            }
            else if (tempG > tempRHS)
            {
                G(u, tempRHS);
                tempG = tempRHS;

                RemoveFromOpenList(u);

                predecessorNodes = grid.GetPredecessors(u);
                for (int i = 0; i < predecessorNodes.Count; i++)
                {
                    DstarLiteNode temp = predecessorNodes[i];

                    if (!temp.Equal(targetNode))
                        RHS(temp, Math.Min(RHS(temp), Cost(temp, u) + tempG));

                    UpdateVertex(temp);
                }
            }
            else //g <= rhs
            {
                gOld = tempG;
                G(u, double.PositiveInfinity);

                if (!u.Equal(targetNode))
                {
                    RHS(u, MinSuccessor(u).Second);
                }

                UpdateVertex(u);

                predecessorNodes = grid.GetPredecessors(u);

                for (int i = 0; i < predecessorNodes.Count; i++)
                {
                    DstarLiteNode temp = predecessorNodes[i];

                    if (Math.Equals(RHS(temp), (Cost(temp, u) + gOld)))
                    {
                        if (!temp.Equal(targetNode))
                        {
                            RHS(temp, MinSuccessor(temp).Second);
                        }
                    }

                    UpdateVertex(temp);
                }
            }
        }

        return 0;
    }

    /// <summary>
    /// Returns the minimun successor of the specified node
    /// </summary>
    /// <param name="node"></param>
    /// <returns> Returns node's successor node which has least cost out of all successors </returns>
    private Pair<DstarLiteNode, double> MinSuccessor(DstarLiteNode node)
    {
        List<DstarLiteNode> successorNodes = new List<DstarLiteNode>();
        successorNodes = grid.GetSuccessors(node);        

        double tempCost;
        double tempG;

        DstarLiteNode nodeMin = null;
        double costMin = double.PositiveInfinity;

        for (int i = 0; i < successorNodes.Count; i++)
        {
            DstarLiteNode successorNode = successorNodes[i];

            if (path.Contains(successorNode))
                continue;

            tempCost = Cost(node, successorNode);
            tempG = G(successorNode);

            if (double.IsPositiveInfinity(tempCost) || double.IsPositiveInfinity(tempG))
                continue;

            tempCost += tempG;

            
            if (tempCost < costMin)
            {                
                costMin = tempCost;
                nodeMin = successorNode;
            }
        }
        successorNodes.Clear();

        return new Pair<DstarLiteNode, double>(nodeMin, costMin);
    }

    /// <summary>
    /// Checks if their is need to replan the path
    /// </summary>
    /// <returns> boolean value to indicate replanning required or not </returns>
    public bool replan()
    {
        path.Clear();

        int result = ComputeShortestPath();
        if (result != 0)
            return false;

        DstarLiteNode currentNode = startNode;
        path.Add(currentNode);

        while (currentNode != null && !currentNode.Equal(targetNode))
        {
            if (double.IsPositiveInfinity(G(currentNode)))
            {
                return false;
            }

            currentNode = MinSuccessor(currentNode).First;

            path.Add(currentNode);
        }

        return true;
    }

    /// <summary>
    /// Updates the km factor value
    /// </summary>
    public void UpdateKM()
    {
        kmFactor += Heuristic(lastNode, startNode);
        lastNode = startNode;
    }

    public void UpdateNodeCost(DstarLiteNode u, double cost)
    {
        if (u.Equal(targetNode))
        {
            return;
        }

        MakeNewCell(u);

        double costOld = u.cost;
        double costNew = cost;        

        List<DstarLiteNode> predecessorNodes = grid.GetPredecessors(u);

        double tempCostOld, tempCostNew;
        double tempRHS, tempG;        

        // Update U
        for (int i = 0; i < predecessorNodes.Count; i++)
        {           
            DstarLiteNode temp = predecessorNodes[i];

            u.cost = costOld;
            tempCostOld = Cost(u, temp);
            u.cost = costNew;
            tempCostNew = Cost(u, temp);

            tempRHS = RHS(u);
            tempG = G(temp);

            if (tempCostOld > tempCostNew)
            {
                if (!u.Equal(targetNode))
                {
                    RHS(u, Math.Min(tempRHS, (tempCostNew + tempG)));
                }
            }
            else if (Math.Equals(tempRHS, (tempCostOld + tempG)))
            {
                if (!u.Equal(targetNode))
                {
                    RHS(u, MinSuccessor(u).Second);
                }
            }
        }

        UpdateVertex(u);

        // Update neighbors
        for (int i = 0; i < predecessorNodes.Count; i++)
        {
            DstarLiteNode temp = predecessorNodes[i];

            u.cost = costOld;
            tempCostOld = Cost(u, temp);
            u.cost = costNew;
            tempCostNew = Cost(u, temp);

            tempRHS = RHS(temp);
            tempG = G(u);

            if (tempCostOld > tempCostNew)
            {
                if (!temp.Equal(targetNode))
                {
                    RHS(temp, Math.Min(tempRHS, (tempCostNew + tempG)));
                }
            }
            else if (Math.Equals(tempRHS, (tempCostOld + tempG)))
            {
                if (!temp.Equal(targetNode))
                {
                    RHS(temp, MinSuccessor(temp).Second);
                }
            }

            UpdateVertex(temp);
        }
    }
    

    IEnumerator FindPath(Vector3 startPos, Vector3 targetPos, bool isFollowing)
    {               
        if (!isFollowing)
        {
            if (Init(startPos, targetPos))
            {
                replanReturn = replan();
            }
        }
        else
        {
            if (updatedNodes.Count > 0)
            {
                UpdateKM();               

                for (int i = 0; i < updatedNodes.Count; i++)
                {
                    DstarLiteNode nodeHit = updatedNodes[i];
                    UpdateNodeCost(nodeHit, double.PositiveInfinity);
                }

                updatedNodes.Clear();               

                replanReturn = replan();
            }
            else
            {
                replanReturn = true;
            }
        }

        yield return null;

        if (replanReturn)
        {
            if (path.Count > 0)
            {                

                waypoints.Initialize();

                waypoints = SimplifyPath(path);
                
                path.RemoveAt(0);

                nextMove = path[0].worldPosition;
                startNode = path[0];                
            }

            requestManager.FinishProcessingPath(nextMove, replanReturn, (startNode.Equal(targetNode)));
        }
    }

    /// <summary>
    /// Returns the waypoints (for drawing on gizmos)
    /// </summary>
    /// <returns></returns>
    public Vector3[] PathWaypoints()
    {
        return waypoints;
    }

    /// <summary>
    /// Returns the waypoints where direction changes hence reducing
    /// the no. of waypoints when going in the same direction
    /// </summary>
    /// <param name="path"></param>
    /// <returns></returns>
    Vector3[] SimplifyPath(List<DstarLiteNode> path)
    {
        List<Vector3> waypoints = new List<Vector3>();
        Vector2 directionOld = Vector2.zero;

        for (int i = 0; i < path.Count; i++)
        {
            Vector2 directionNew = new Vector2(path[1 - 1].gridX - path[i].gridX, path[1 - 1].gridY - path[i].gridY);
            if (directionNew != directionOld)
            {
                waypoints.Add(path[i].worldPosition);
            }

            directionOld = directionNew;
        }

        return waypoints.ToArray();
    }
    

    //Returns the 8-way distance between state a and state b
    double Heuristic(DstarLiteNode a, DstarLiteNode b)
    {
        // For approximation of distance between two nodes
        // Maximum of absolute differences of their x and y coordinates are used         
        double xd = Math.Abs(a.gridX - b.gridX);
        double yd = Math.Abs(a.gridY - b.gridY);        

        return  xd + yd;
    }
    
    /// <summary>
    /// Calculates the cost from Node A to Node B
    /// </summary>
    /// <param name="nodeA"></param>
    /// <param name="nodeB"></param>
    /// <returns> cost from one node to another </returns>
    double Cost(DstarLiteNode nodeA, DstarLiteNode nodeB)
    {
        if ((!nodeA.isWalkable || double.IsPositiveInfinity(nodeA.cost)) ||
             (!nodeB.isWalkable || double.IsPositiveInfinity(nodeB.cost)))
        {
            return double.PositiveInfinity;
        }        

        return (nodeA.cost + nodeB.cost) / 2;
    }
}