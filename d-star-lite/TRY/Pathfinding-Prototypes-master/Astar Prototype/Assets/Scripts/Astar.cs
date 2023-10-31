/*
Developed By: Muhammad Murtaza
Desc: Astar (algorithm) Script responsible for finding shortest path between two points.
*/

using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;

public class Astar : MonoBehaviour
{

	PathRequestManager requestManager;
	Grid grid;
    private int normalMoveCost = 10;
    private int diagonalMoveCost = 14;

    /// <summary>
    /// Initializing the grid and path request manager
    /// </summary>
	void Awake()
    {
		requestManager = GetComponent<PathRequestManager>();
		grid = GetComponent<Grid>();
	}

    /// <summary>
    /// Executes the coroutine function called FindPath
    /// to find path between passed two positions
    /// </summary>
    /// <param name="startPos"></param>
    /// <param name="targetPos"></param>
	public void StartFindPath(Vector3 startPos, Vector3 targetPos)
    {
		StartCoroutine(FindPath(startPos,targetPos));
	}

    /// <summary>
    /// Coroutine which finds the shortest path using A*
    /// </summary>
    /// <param name="startPos"></param>
    /// <param name="targetPos"></param>
    /// <returns></returns>
	IEnumerator FindPath(Vector3 startPos, Vector3 targetPos)
    {

		Vector3[] waypoints = new Vector3[0];
		bool pathFound = false;

		Node startNode = grid.NodeFromWorldPoint(startPos);
		Node targetNode = grid.NodeFromWorldPoint(targetPos);


		if (startNode.isWalkable && targetNode.isWalkable)  // start and target nodes are not blocked
        {
			Heap<Node> openNodes = new Heap<Node>(grid.MaxSize);    //  Contains unvisited nodes
            HashSet<Node> closedNodes = new HashSet<Node>();       //  Contains visited nodes
			openNodes.Add(startNode);

			while (openNodes.Count > 0)
            {
				Node currentNode = openNodes.RemoveFirst();
				closedNodes.Add(currentNode);

				if (currentNode == targetNode)
                {
					pathFound = true;
					break;
				}

                // Checking neigbours of the current node used from open list
				foreach (Node neighbour in grid.GetNeighbours(currentNode))
                {
					if (!neighbour.isWalkable || closedNodes.Contains(neighbour))
                    {
						continue;
					}

					int newMovementCostToNeighbour = currentNode.gCost + Cost(currentNode, neighbour);
					if (newMovementCostToNeighbour < neighbour.gCost || !openNodes.Contains(neighbour))
                    {
						neighbour.gCost = newMovementCostToNeighbour;
						neighbour.hCost = Cost(neighbour, targetNode);
						neighbour.parent = currentNode;

                        if (!openNodes.Contains(neighbour))
                        {
                            openNodes.Add(neighbour);
                        }
					}
				}
			}
		}
		yield return null;
		if (pathFound)
        {
			waypoints = RetracePath(startNode,targetNode);
		}
		requestManager.FinishedProcessingPath(waypoints,pathFound);

	}

    /// <summary>
    /// Returns path's waypoints
    /// </summary>
    /// <param name="startNode"></param>
    /// <param name="endNode"></param>
    /// <returns></returns>
	Vector3[] RetracePath(Node startNode, Node endNode)
    {
		List<Node> path = new List<Node>();
		Node currentNode = endNode;

		while (currentNode != startNode)
        {
			path.Add(currentNode);
			currentNode = currentNode.parent;
		}
		path.Add (startNode);
		Vector3[] waypoints = SimplifyPath(path);
		Array.Reverse(waypoints);
		return waypoints;

	}

    /// <summary>
    /// Returns the waypoints where direction changes hence reducing
    /// the no. of waypoints when going in the same direction
    /// </summary>
    /// <param name="path"></param>
    /// <returns></returns>
	Vector3[] SimplifyPath(List<Node> path)
    {
		List<Vector3> waypoints = new List<Vector3>();
		Vector2 directionOld = Vector2.zero;

		for (int i = 1; i < path.Count; i ++)
        {
			Vector2 directionNew = new Vector2(path[i - 1].gridX - path[i].gridX,path[i - 1].gridY - path[i].gridY);
			if (directionNew != directionOld)   // direction changes
            {
				waypoints.Add(path[i-1].worldPosition);
			}
			directionOld = directionNew;
		}
		return waypoints.ToArray();
	}


	/// <summary>
    /// Returns the cost to go from one node (NodeA) to another node (NodeB) 
    /// </summary>
    /// <param name="nodeA"></param>
    /// <param name="nodeB"></param>
    /// <returns></returns>
    int Cost(Node nodeA, Node nodeB)
    {
		int dstX = Mathf.Abs(nodeA.gridX - nodeB.gridX);
		int dstY = Mathf.Abs(nodeA.gridY - nodeB.gridY);

        if (dstX > dstY)
        {
            return diagonalMoveCost * dstY + normalMoveCost * (dstX - dstY);
        }

		return diagonalMoveCost * dstX + normalMoveCost * (dstY-dstX);
	}
}