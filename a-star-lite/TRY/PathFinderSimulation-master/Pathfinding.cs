using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System;

public class Pathfinding : MonoBehaviour
{
 Grid grid;
 public Transform seeker,target;
 void Awake()
 {
    grid=GetComponent<Grid>(); // getting the Grid component from hierarchy
 }

 void Update()
 {
     if(Input.GetButtonDown("Jump"))
     {
         FindPath(seeker.position,target.position);
     }
 }
 
 void FindPath(Vector3 startPos,Vector3 targetPos) // method that finds the path from start to target
 {
    Stopwatch sw= new Stopwatch();
    sw.Start();
    Node startNode=grid.NodeFromWorldPoint(startPos); // creating start node from start position
    Node targetNode=grid.NodeFromWorldPoint(targetPos); // creating target node from target position

    Heap<Node> openSet=new Heap<Node>(grid.MaxSize); // creating openSet as a list
    HashSet<Node> closedSet=new HashSet<Node>(); // creating closeSet as a hashset

    openSet.Add(startNode); // adding start node to the open set
    while(openSet.Count > 0)  // initiating the main loop for A*
    {
      Node currentNode=openSet.RemoveFirst();   // initial node definition

      /* for(int i=1;i<openSet.Count;i++)  // traversing openset
      {
          if(openSet[i].fCost < currentNode.fCost || (openSet[i].fCost == currentNode.fCost && openSet[i].hCost < currentNode.hCost)) // finding the node with min cost
          {
              currentNode=openSet[i];  // basically linear search
          }
      } 
     openSet.Remove(currentNode);  // Now after finding the node with least cost remove it from openset */
     closedSet.Add(currentNode); // add it to closed set
     if(currentNode == targetNode) // target node reached by the pathfinder
     {
         sw.Stop();
         print("Path found"+sw.ElapsedMilliseconds+"ms");
         RetracePath(startNode,targetNode); // finally trace the path found by the algo END
         return;
     }   
     foreach (Node neighbour in grid.GetNeighbours(currentNode)) // checking weights of neighbours
     {
         if(!neighbour.walkable || closedSet.Contains(neighbour)) // enter only if neighbour is walkable and is not in closed set
         continue;
          int newMovementCostToNeighbour=currentNode.gCost+GetDistance(currentNode,neighbour); // var to hold temp recalc value of path
          if(newMovementCostToNeighbour < neighbour.gCost || !openSet.Contains(neighbour)) // check to cmp new value with previous best val
          {
             neighbour.gCost=newMovementCostToNeighbour; // Setting all req var to newe values
             neighbour.hCost=GetDistance(neighbour,targetNode);
             neighbour.parent=currentNode;

             if(!openSet.Contains(neighbour)) // if any neighbour was not in openSet add it
             {
                 openSet.Add(neighbour);
             }
          }

     }        
    }
 }
 void RetracePath(Node startNode,Node endNode) // method to find the path from the target node to initial node
 {
     List<Node> path=new List<Node>();
     Node currentNode=endNode;
     while(currentNode != startNode) //Retracing from target to start node
     {
         path.Add(currentNode);
         currentNode=currentNode.parent;
     }
     path.Reverse(); // to get the correct sequence of steps
     grid.path=path;
 }
 public int GetDistance(Node nodeA,Node nodeB) // method to obtain the req distance values
 {
     int dstX=Mathf.Abs(nodeA.gridX-nodeB.gridX);
     int dstY=Mathf.Abs(nodeA.gridY-nodeB.gridY);
    
    if(dstX > dstY)
        return 14*dstY+10*(dstX-dstY);
    return 14*dstX+10*(dstY-dstX);

 }
 
}

