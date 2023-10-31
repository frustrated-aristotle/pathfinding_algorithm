using UnityEngine;

public class Node : IHeapItem<Node>
{

	public bool isWalkable;
	public Vector3 worldPosition;
	public int gridX;
	public int gridY;
	public int gCost;   // path cost from start to target
	public int hCost;   // estimated cost to the target
	public Node parent; // The node we took to get here so we can get the final path
    int heapIndex;      //  The index this node has in the heap, to make sorting nodes faster

    /// <summary>
    /// Constructor of this class
    /// </summary>
    /// <param name="_isWalkable"></param>
    /// <param name="_worldPos"></param>
    /// <param name="_gridX"></param>
    /// <param name="_gridY"></param>
    public Node(bool _isWalkable, Vector3 _worldPos, int _gridX, int _gridY)
    {
		isWalkable = _isWalkable;
		worldPosition = _worldPos;
		gridX = _gridX;
		gridY = _gridY;
	}

    
    /// <summary>
    /// Returns total cost of the path 
    /// </summary>
	public int fCost
    {
		get
        {
			return gCost + hCost;
		}
	}

    //  The IHeapItem interface requires that we implement this
    public int HeapIndex
    {
		get
        {
			return heapIndex;
		}
		set
        {
			heapIndex = value;
		}
	}
    
    /// <summary>
    /// To compare nodes when sorting the heap  
    /// </summary>
    /// <param name="nodeToCompare"></param>
    /// <returns></returns>
    public int CompareTo(Node nodeToCompare)
    {
		int compare = fCost.CompareTo(nodeToCompare.fCost);

		if (compare == 0)   // 0 means f costs of two nodes are same
        {
			compare = hCost.CompareTo(nodeToCompare.hCost); // Comparing nodes' h costs
		}
		return compare;
	}
}