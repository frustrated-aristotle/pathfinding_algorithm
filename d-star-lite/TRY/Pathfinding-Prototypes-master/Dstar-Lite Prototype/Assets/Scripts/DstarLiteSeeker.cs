/*
Developed By: Muhammad Murtaza
Desc: Used by D* Lite seekers to chase the target (player)
*/

using UnityEngine;
using System.Collections;

public class DstarLiteSeeker : MonoBehaviour
{

    public Transform target;
    GameObject dstarLite;
    DstarLite ds;
    public float speed = 6;
    public float rotationSpeed = 6;
    Vector3 nextMove;
    Vector3 currentWaypoint;
    Vector3[] path = new Vector3[0];    
    bool isFinished = false;
    bool isFollowing = false;
    bool showPath = false;  

    void Awake()
    {
        dstarLite = GameObject.Find("D*Lite");
        ds = dstarLite.GetComponent<DstarLite>();              

    }    

    void Start()
    {
        isFinished = false;
        isFollowing = false;
        DstarLitePathRequestManager.RequestPath(transform.position, target.position, isFollowing, OnPathFound);
    }

    /// <summary>
    /// Calls the 'FollowPath' coroutine if path is found
    /// </summary>
    /// <param name="newPath"></param>
    /// <param name="pathSuccessful"></param>
    public void OnPathFound(Vector3 _nextMove, bool pathSuccessful, bool isFinish)
    {
        isFinished = isFinish;

        if (pathSuccessful)
        {
            nextMove = _nextMove;            
            StopCoroutine("FollowPath");
            StartCoroutine("FollowPath");
        }
    }

    IEnumerator FollowPath()
    {
        currentWaypoint = nextMove;
               
        while (true)
        {
            if (transform.position == currentWaypoint)
            {
                if (!isFinished)
                {                    
                    isFollowing = true;

                    DstarLitePathRequestManager.RequestPath(transform.position, target.position, isFollowing, OnPathFound);
                }

                
                yield break;
            }
            
            showPath = true;
            transform.position = Vector3.MoveTowards(transform.position, currentWaypoint, speed * Time.deltaTime);

            Vector3 targetWaypointDirection = currentWaypoint - transform.position;
            if (targetWaypointDirection != Vector3.zero)    // not looking in the direction of the path
            {
                // Seeker rotates/looks in the direction of the path
                transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.LookRotation(targetWaypointDirection, Vector3.up), rotationSpeed * Time.fixedDeltaTime);
            }
            yield return null;
        }
    }

    /// <summary>
    /// Drawing path on the Gizmos
    /// </summary>
    public void OnDrawGizmos()
    {
        
        if(showPath)
        {

            path = ds.PathWaypoints();
        }
        
        //UnityEngine.Debug.Log("Path length: " + path.Length);        

        if (path != null)
        {
            for (int i = 0; i < path.Length; i++)
            {
                Gizmos.color = Color.black;
                Gizmos.DrawCube(path[i], Vector3.one);

                if (i == 0)
                {
                    Gizmos.DrawLine(transform.position, path[i]);
                }
                else
                {
                    Gizmos.DrawLine(path[i - 1], path[i]);
                }
            }
            showPath = false;
        }
    }
}