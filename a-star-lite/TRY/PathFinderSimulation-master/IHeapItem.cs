using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public interface IHeapItem<T> :IComparable<T>  //interface for the generic class wtf even is this shit docs ftw
{
int HeapIndex
    {
    get;
    set;
    }
}
