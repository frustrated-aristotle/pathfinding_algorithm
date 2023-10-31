using System;

// T in this case will be Node
// T : IHeapItem<T> means that the Node has to implement the interface
public class Heap<T> where T : IHeapItem<T>
{

    T[] items;  // The array that will hold the heap
    int currentItemCount;    // Number of nodes we have stored in the heap

    /// <summary>
    /// Constructor, when instantiate heap, you must specify the maxheapsize
    /// </summary>
    /// <param name="maxHeapSize"></param>
    public Heap(int maxHeapSize)
    {
        items = new T[maxHeapSize];     //  instantiate the array with the maxheapsize specified by the user
    }

    /// <summary>
    /// CLears the Heap items
    /// </summary>
    public void Clear()
    {
        Array.Clear(items, 0, items.Length);

        currentItemCount = 0;
    }

    /// <summary>
    /// Adds the new item (Node) to the heap
    /// </summary>
    /// <param name="item"></param>
    public void Add(T item)
    {
        if (currentItemCount + 1 > items.Length)
        {
            //Debug.Log("Heap is full cannot add new item");

            return;
        }

        item.HeapIndex = currentItemCount;

        items[currentItemCount] = item; // Adding item to the end of the array
        SortUp(item);   // Sorting the item's position in the heap
        currentItemCount++;
    }

    /// <summary>
    /// Remove the first item from the heap, which is the node with the lowest fcost
    /// </summary>
    /// <returns></returns>
    public T RemoveFirst()
    {
        if (Count > 1)
        {
            T firstItem = items[0];
            currentItemCount--;
            items[0] = items[currentItemCount];
            items[0].HeapIndex = 0;
            SortDown(items[0]);

            return firstItem;
        }
        else if (Count == 1){
            T firstItem = items[0];
            currentItemCount--;
            items[0] = default(T);

            return firstItem;
        }

        return default(T);
    }

    /// <summary>
    /// Removes the specified item(Node) from Heap
    /// </summary>
    /// <param name="item"></param>
    public void Remove(T item)
    {
        if (Count > 1)
        {
            int pos = item.HeapIndex;

            currentItemCount--;
            T lastItem = items[currentItemCount];
            lastItem.HeapIndex = pos;

            items[currentItemCount] = default(T);

            items[pos] = lastItem;
            SortUp(lastItem);
            SortDown(lastItem);
        }
        else if (Count == 1)
        {
            RemoveFirst();
        }
    }

    /// <summary>
    /// Gets the first element from the Heap set
    /// </summary>
    /// <returns> First item from items array </returns>
    public T First()
    {
        T firstItem = items[0];

        return firstItem;
    }

    /// <summary>
    /// Check the heap contains this item
    /// </summary>
    /// <param name="item"></param>
    /// <returns></returns>
    public bool Contains(T item)
    {
        return Equals(items[item.HeapIndex], item);
    }


    /// <summary>
    /// Updates an item already exists in the Heap
    /// </summary>
    /// <param name="item"></param>
    public void UpdateItem(T item)
    {
        SortUp(item);
        SortDown(item);
    }

    public int Count
    {
        get
        {
            return currentItemCount;
        }
    }

    /// <summary>
    /// Sorts an item down in the array to the position where it should be
    /// </summary>
    /// <param name="item"></param>
    void SortDown(T item)
    {
        while (true)
        {
            // Formula for finding childs
            // left child = (2n + 1)
            // right child = (2n + 2)
            // n is position of item in array ( T[])

            int leftChild = 2 * item.HeapIndex + 1;
            int rightChild = 2 * item.HeapIndex + 2;
            int swapIndex = 0;

            if (leftChild < currentItemCount)  // Check if left child is last item
            {
                swapIndex = leftChild;

                if (rightChild < currentItemCount) // Check if right child is last item
                {
                    //  Compare the left and the right node, to find if we should swap with the left or the right node
                    if (items[leftChild].CompareTo(items[rightChild]) > 0)
                    {
                        swapIndex = rightChild;
                    }
                }

                if (item.CompareTo(items[swapIndex]) > 0)
                {
                    Swap(item, items[swapIndex]);
                }
                else
                {
                    return;
                }
            }
            else
            {
                return;
            }
        }
    }


    /// <summary>
    /// Sorts an item up in the array to the position where it should be
    /// </summary>
    /// <param name="item"></param>
    void SortUp(T item)
    {
        // Formula for finding parent
        // parentIndex = (n - 1) / 2
        // n is position of item in array ( T[])
        int parentIndex = (item.HeapIndex - 1) / 2; //From heap index to array index

        while (true)
        {
            T parentItem = items[parentIndex];
            if (item.CompareTo(parentItem) < 0) //If item has a lower f cost than the parent
            {
                Swap(item, parentItem);
            }
            else
            {
                break;
            }

            parentIndex = (item.HeapIndex - 1) / 2;
        }
    }

    /// <summary>
    /// Swap 2 items in the heap, which is the same as moving one item up (or down)
    /// and the other item down (or up)
    /// </summary>
    /// <param name="itemA"></param>
    /// <param name="itemB"></param>
    void Swap(T itemA, T itemB)
    {
        items[itemA.HeapIndex] = itemB;
        items[itemB.HeapIndex] = itemA;
        //  Swapping the heap indexes
        int itemAIndex = itemA.HeapIndex;
        itemA.HeapIndex = itemB.HeapIndex;
        itemB.HeapIndex = itemAIndex;
    }
}

/// <summary>
/// Each node has to implement this, HeapIndex and CompareTo
/// </summary>
/// <typeparam name="T"></typeparam>
public interface IHeapItem<T> : IComparable<T>
{
    int HeapIndex
    {
        get;
        set;
    }
}