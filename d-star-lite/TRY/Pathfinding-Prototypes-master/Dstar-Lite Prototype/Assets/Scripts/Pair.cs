public class Pair<T, U>
{
    /// <summary>
    /// Used for storing key values (Primary, Secondary) of a Node
    /// Also used as Key,Value pair (For finding MinSuccessor)
    /// </summary>
    /// <param name="first"></param>
    /// <param name="second"></param>
    public Pair(T first, U second)
    {
        this.First = first;
        this.Second = second;
    }

    public T First { get; set; }
    public U Second { get; set; }
};
