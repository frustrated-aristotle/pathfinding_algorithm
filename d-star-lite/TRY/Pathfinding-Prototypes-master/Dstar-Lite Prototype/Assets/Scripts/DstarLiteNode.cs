using UnityEngine;

public class DstarLiteNode : IHeapItem<DstarLiteNode>
{
    // cell/node properties
    public bool isWalkable;
    public Vector3 worldPosition;
    public int gridX;
    public int gridY;    

    public double rhs;
    public double g;
    public double cost;

    public Pair<double, double> key = new Pair<double, double>(0, 0);
        
    int heapIndex;
    
    /// <summary>
    /// Setting Node's rhs and g values
    /// </summary>
    /// <param name="_rhs"></param>
    /// <param name="_g"></param>
    public void SetNodeRhs_G_Values(double _rhs, double _g)
    {
        rhs = _rhs;
        g = _g;
    }

    /// <summary>
    /// Constructor for setting Node's properties
    /// </summary>
    /// <param name="_walkable"></param>
    /// <param name="_worldPos"></param>
    /// <param name="_gridX"></param>
    /// <param name="_gridY"></param>
    /// <param name="_cost"></param>
    public DstarLiteNode(bool _isWalkable, Vector3 _worldPos, int _gridX, int _gridY, int _cost)
    {
        isWalkable = _isWalkable;
        worldPosition = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
        cost = _cost;
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
    /// Checks if two Nodes x,y positions are equal
    /// </summary>
    /// <param name="n2"></param>
    /// <returns></returns>
    public bool Equal(DstarLiteNode n2)
    {
        return ((this.gridX == n2.gridX) && (this.gridY == n2.gridY));
    }    

    
    /// <summary>
    /// Method for comparing two Nodes' primary & secondary keys
    /// </summary>
    /// <param name="nodeToCompare"></param>
    /// <returns></returns>
    public int CompareTo(DstarLiteNode nodeToCompare)
    {
        if (nodeToCompare != null)
        {
            if (this.key.First > nodeToCompare.key.First)
                return 1;
            else if (this.key.First < nodeToCompare.key.First)
                return -1;
            if (this.key.Second > nodeToCompare.key.Second)
                return 1;
            else if (this.key.Second < nodeToCompare.key.Second)
                return -1;
        }
        return 0;
    }
}