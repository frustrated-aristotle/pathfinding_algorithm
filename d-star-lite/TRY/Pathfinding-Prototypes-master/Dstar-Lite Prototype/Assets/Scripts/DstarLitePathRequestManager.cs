﻿using UnityEngine;
using System.Collections.Generic;
using System;

public class DstarLitePathRequestManager : MonoBehaviour
{

    Queue<PathRequest> pathRequestQueue = new Queue<PathRequest>();
    PathRequest currentPathRequest;

    static DstarLitePathRequestManager instance;
    DstarLite pathfinding;

    bool isProcessingPath;

    void Awake()
    {
        instance = this;
        pathfinding = GetComponent<DstarLite>();
    }


    /// <summary>
    /// Request for the path for the first element of the Request-Queue 
    /// </summary>
    /// <param name="pathStart"></param>
    /// <param name="pathEnd"></param>
    /// <param name="callback"></param>
    public static void RequestPath(Vector3 pathStart, Vector3 pathEnd, bool isFollowing, Action<Vector3, bool, bool> callback)
    {
        PathRequest newRequest = new PathRequest(pathStart, pathEnd, isFollowing, callback);
        instance.pathRequestQueue.Enqueue(newRequest);
        instance.TryProcessNext();
    }

    /// <summary>
    /// Processes the path from the pathRequestQueue (if any exists)
    /// </summary>
    void TryProcessNext()
    {
        if (!isProcessingPath && pathRequestQueue.Count > 0)
        {          
            currentPathRequest = pathRequestQueue.Dequeue();
            isProcessingPath = true;
            pathfinding.StartFindPath(currentPathRequest.pathStart, currentPathRequest.pathEnd, currentPathRequest.isFollowing);
        }
    }

    /// <summary>
    /// Stops processing current path-request
    /// </summary>
    /// <param name="path"></param>
    /// <param name="success"></param>
    public void FinishProcessingPath(Vector3 path, bool success, bool isFinish)
    {
        currentPathRequest.callback(path, success, isFinish);
        isProcessingPath = false;
        TryProcessNext();
    }

    /// <summary>
    /// Data structure to hold path's start, end and its waypoints 
    /// </summary>
    struct PathRequest
    {
        public Vector3 pathStart;
        public Vector3 pathEnd;
        public Action<Vector3, bool, bool> callback;
        public bool isFollowing;

        public PathRequest(Vector3 _start, Vector3 _end, bool _isFollowing, Action<Vector3, bool, bool> _callback)
        {
            pathStart = _start;
            pathEnd = _end;
            callback = _callback;
            isFollowing = _isFollowing;
        }
    }
}
