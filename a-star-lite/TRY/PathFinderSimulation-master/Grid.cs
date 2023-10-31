using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Grid : MonoBehaviour
{
 public bool onlyDisplayPathGizmos;
 public Transform player;
 public LayerMask unwalkableMask; // layer to mark as unwalkable areas 
 public Vector2 gridWorldSize; // world size parameters
 public float nodeRadius; // parameter for node radius 
 Node[,] grid; // declaration of the node grid


 float nodeDiameter; // extra parameter to map full length of the node
 int gridSizeX,gridSizeY; // extra parameter to specify the X and Y dimensions
 void Start()
 {
     nodeDiameter=nodeRadius*2; // diameter function decalaration 
     gridSizeX=Mathf.RoundToInt(gridWorldSize.x/nodeDiameter); // X dimension function 
     gridSizeY=Mathf.RoundToInt(gridWorldSize.y/nodeDiameter); // Y dimension function 
     CreateGrid(); // helper method to instantiate the world grid
 }
 void CreateGrid()
 {
     grid=new Node[gridSizeX,gridSizeY]; // instantiate the grid dimensions on the 
     Vector3 worldBottomLeft = transform.position - Vector3.right*gridWorldSize.x/2 - Vector3.forward*gridWorldSize.y/2; // defining the bottom left of the map
      for(int x=0;x<gridSizeX;x++)
      {
        for(int y=0;y<gridSizeY;y++)
          {
             Vector3 worldPoint=worldBottomLeft+Vector3.right*(x*nodeDiameter+nodeRadius)+Vector3.forward*(y*nodeDiameter+nodeRadius); // defining the points starting from the bottom left
             bool walkable=!(Physics.CheckSphere(worldPoint,nodeRadius,unwalkableMask)); // checks against the layer masks for the given node obj and radius
             grid[x,y]=new Node(walkable,worldPoint,x,y); // creating a grid with the given bool conditions for each node and position
          }
      }
 }
 public List<Node> GetNeighbours(Node node)
 {
   List<Node> neighbours=new List<Node>();
   for(int x=-1;x<=1;x++)
   {
       for(int y=-1;y<=1;y++)
       {
           if(x==0 && y==0)
           continue;
           int checkX=node.gridX+x;
           int checkY=node.gridY+y;

           if(checkX >= 0 && checkX< gridSizeX && checkY >=0 && checkY < gridSizeY)
           {
               neighbours.Add(grid[checkX,checkY]);
           }
       } 
   } 
   return neighbours;
 } 
 public int MaxSize
 {
     get{
         return gridSizeX*gridSizeY;
     }
 }
 public Node NodeFromWorldPoint(Vector3 worldPosition)
 {
     float percentX=(worldPosition.x+gridWorldSize.x/2)/gridWorldSize.x;
     float percentY=(worldPosition.z+gridWorldSize.y/2)/gridWorldSize.y;
	 percentX = Mathf.Clamp01(percentX);
	 percentY = Mathf.Clamp01(percentY);
 
	 int x = Mathf.RoundToInt((gridSizeX-1) * percentX);
	 int y = Mathf.RoundToInt((gridSizeY-1) * percentY);
	 return grid[x,y];
 }
 public List<Node> path;
 void OnDrawGizmos()
 {
     Gizmos.DrawWireCube(transform.position,new Vector3(gridWorldSize.x,1,gridWorldSize.y)); // creation parameters for Wire Cube
     if(onlyDisplayPathGizmos)
     {
         if(path!=null){
             foreach (Node n in path){
                 Gizmos.color=Color.black;
                  Gizmos.DrawCube(n.worldPosition,Vector3.one*(nodeDiameter-.1f));
             }
         }
         else
         {
            if(grid != null)
              {
                 Node playerNode=NodeFromWorldPoint(player.position); // assign the player node
                 foreach(Node n in grid)
                     {
                       Gizmos.color=(n.walkable)?Color.white:Color.red; // assigns the color of the gizmos used for the given node 
                       if(playerNode==n)
                         {

                           Gizmos.color=Color.cyan;
                         }
                       if(path!=null)
                         {
                            if(path.Contains(n))
                              Gizmos.color=Color.black;
                         }
                      Gizmos.DrawCube(n.worldPosition,Vector3.one*(nodeDiameter-.1f)); // creates cubical gizmo for a given position and diameter
                     } 
               } 
         }
     }
     
 }
}

