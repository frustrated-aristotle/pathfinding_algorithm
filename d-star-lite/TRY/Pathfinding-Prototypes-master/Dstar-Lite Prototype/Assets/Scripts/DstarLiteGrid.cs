using UnityEngine;
using System.Collections.Generic;

public class DstarLiteGrid : MonoBehaviour
{

    public bool displayGridGizmos;      // Show grid or not
    public LayerMask unwalkableMask;    // Layer for the obstacles
    public Vector2 gridWorldSize;       // size of grid in the game
    public float nodeRadius;            // radius of each grid's node
    DstarLiteNode[,] grid;              // 2D array of Nodes (our grid)
    float nodeDiameter;                 // size of each node
    int gridSizeX, gridSizeY;           // Grid's x,y positions

    void Awake()
    {
        nodeDiameter = nodeRadius * 2;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
       
        CreateGrid();
    }

    /// <summary>
    /// Returns size of the grid
    /// </summary>
    public int MaxSize
    {
        get
        {
            return gridSizeX * gridSizeY;
        }
    }

    /// <summary>
    /// Initialized grid's nodes
    /// </summary>
    void CreateGrid()
    {
        grid = new DstarLiteNode[gridSizeX, gridSizeY];
        Vector3 worldBottomLeft = transform.position - Vector3.right * gridWorldSize.x / 2 - Vector3.forward * gridWorldSize.y / 2;

        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector3 worldPoint = worldBottomLeft + Vector3.right * (x * nodeDiameter + nodeRadius) + Vector3.forward * (y * nodeDiameter + nodeRadius);
                bool walkable = !(Physics.CheckSphere(worldPoint, nodeRadius, unwalkableMask));
                
                grid[x, y] = new DstarLiteNode(walkable, worldPoint, x, y, int.MaxValue);

                //initializing the rhs and g value to infinity 
                grid[x, y].SetNodeRhs_G_Values(double.PositiveInfinity, double.PositiveInfinity);
            }
        }
    }
    
    /// <summary>
    /// Gets the successors of the node
    /// </summary>
    /// <param name="node"></param>
    /// <returns></returns>
    public List<DstarLiteNode> GetSuccessors(DstarLiteNode node)
    {
        List<DstarLiteNode> neghbours = new List<DstarLiteNode>();

        if (!node.isWalkable || double.IsPositiveInfinity(node.cost))
        {
            return neghbours;
        }

        // Loop for checking node's neighbours in 8 directions
        /* x from left to right
         * y from bottom to top
         * ____________________
         * | -1,1 | 0,1  | 1,1 |
         * | -1,0 | 0,0  | 1,0 |
         * | -1,-1| 0,-1 | 1,-1|
         */
        for (int x = -1; x < 2; x++)
        {
            for (int y = -1; y < 2; y++)
            {
                if (x == 0 && y == 0)   // 0,0 is Node itself
                {
                    continue;
                }

                int neighbourXPos = node.gridX + x;
                int neighbourYPos = node.gridY + y;

                // Checking positions within the grid then add the neighbours
                if (neighbourXPos >= 0 && neighbourXPos < gridSizeX && neighbourYPos >= 0 && neighbourYPos < gridSizeY)
                {
                    if (grid[neighbourXPos, neighbourYPos].isWalkable && !double.IsPositiveInfinity(grid[neighbourXPos, neighbourYPos].cost))
                    {
                        neghbours.Add(grid[neighbourXPos, neighbourYPos]);
                    }
                }
            }
        }

        return neghbours;
    }

    /// <summary>
    /// Gets the predecessors of the node
    /// </summary>
    /// <param name="node"></param>
    /// <returns></returns>
    public List<DstarLiteNode> GetPredecessors(DstarLiteNode node)
    {
        List<DstarLiteNode> neghbours = new List<DstarLiteNode>();

        // Loop for checking node's neighbours in 8 directions
        /* x from left to right
         * y from bottom to top
         * ____________________
         * | -1,1 | 0,1  | 1,1 |
         * | -1,0 | 0,0  | 1,0 |
         * | -1,-1| 0,-1 | 1,-1|
         */
        for (int x = -1; x < 2; x++)
        {
            for (int y = -1; y < 2; y++)
            {
                if (x == 0 && y == 0)   // 0,0 is Node itself
                {
                    continue;
                }

                int neighbourXPos = node.gridX + x;
                int neighbourYPos = node.gridY + y;

                // Checking positions within the grid then add the neighbours
                if (neighbourXPos >= 0 && neighbourXPos < gridSizeX && neighbourYPos >= 0 && neighbourYPos < gridSizeY)
                {
                    if (grid[neighbourXPos, neighbourYPos].isWalkable && !double.IsPositiveInfinity(grid[neighbourXPos, neighbourYPos].cost))
                    {
                        neghbours.Add(grid[neighbourXPos, neighbourYPos]);
                    }
                }
            }
        }

        return neghbours;
    }

    /// <summary>
    /// Converts game environment position into grid coordinate
    /// </summary>
    /// <param name="worldPosition"></param>
    /// <returns> x,y coordinates of grid </returns>
    public DstarLiteNode NodeFromWorldPoint(Vector3 worldPosition)
    {
        float percentX = (worldPosition.x + gridWorldSize.x / 2) / gridWorldSize.x;
        float percentY = (worldPosition.z + gridWorldSize.y / 2) / gridWorldSize.y;      

        int x = Mathf.RoundToInt((gridSizeX - 1) * percentX);
        int y = Mathf.RoundToInt((gridSizeY - 1) * percentY);

        return grid[x, y];
    }

    /// <summary>
    /// Node's position in the Grid 
    /// </summary>
    /// <param name="x"></param>
    /// <param name="y"></param>
    /// <returns></returns>
    public DstarLiteNode NodeFromPos(int x, int y)
    {
        return grid[x, y];
    }

    /// <summary>
    /// Draws the grid on the Gizmos
    /// </summary>
    void OnDrawGizmos()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireCube(transform.position, new Vector3(gridWorldSize.x, 1, gridWorldSize.y));

        if (grid != null && displayGridGizmos)
        {
            
            foreach (DstarLiteNode n in grid)
            {
                Gizmos.color = (n.isWalkable) ? Color.gray : Color.red;                

                Gizmos.DrawCube(n.worldPosition, Vector3.one * (nodeDiameter - 0.1f));
            }
        }
    }
}