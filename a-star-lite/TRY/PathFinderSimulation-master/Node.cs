using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Node : IHeapItem<Node>  // wasnt working as a seperate script
{
  public bool walkable;
  public int gridX;
  public int gridY;
  public Vector3 worldPosition;
  public int gCost;
  public int hCost;
  public Node parent;
  int heapIndex;
   public Node(bool _walkable,Vector3 _worldPos,int _gridX,int _gridY)
   {
      walkable=_walkable;
      worldPosition=_worldPos;
      gridX=_gridX;
      gridY=_gridY;
   }
   public int fCost{
       get{    // whenever fCost is called it gets the value from the current gCost and hCost values 
             return gCost+hCost;                  
       }
   }
   public int HeapIndex
   {
       get{
           return heapIndex;
           }
       set{
           heapIndex=value;
           }
   }
   public int CompareTo(Node nodeToCompare)
   {
       int compare=fCost.CompareTo(nodeToCompare.fCost);
       if(compare==0)
       {
           compare=hCost.CompareTo(nodeToCompare.hCost); // 1 if item has higher priority and -1 vice versa
       }
       return -compare;
   }
}