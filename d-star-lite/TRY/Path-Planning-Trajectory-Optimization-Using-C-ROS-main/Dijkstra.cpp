#include<bits/stdc++.h>
using namespace std;

#define V 9
map<int,int>distFrmSrc;
map<int, list<int>> adj;
map<int,bool>visited;
map<int, list<map<int,int>>> dist;
int callVert = 0;
int backPropogation(int callNode, int vert){
        auto iter = adj[vert].begin();
        for(iter;iter!=adj[vert].end();iter++){
            // int dist = g_map[adjNode][*iter];
            if(vert !=0 && *iter !=0){
                // dist += totDist;
                int bnode = vert;
                if(visited[*iter] == true){
                    
                    if(visited[*iter] == true && callVert!=*iter){
                        cout << " Back vertices " << vert << " Back adj node " << *iter  << endl;
                        callVert = vert;
                        backPropogation(bnode, *iter);
                    }
                    
                }
                else{
                    cout << " Back vertices " << vert << " Node " << *iter << " is Unvisited" << endl;
                    //break;
                }
                
            }
            else if(vert == 0){
                cout << " Back Vertices is Src Node " << vert <<endl;
                //break;
            }
            else {
                 cout << " Back vertices "<< vert <<" Reached Src Node " << *iter << endl; 
                 //break;
            }
        
        }
    
    return 0;
}

int dijkstra(int g_map[V][V],int src){
    for(int i = 0; i<adj.size(); i++){
        auto iter = adj[i].begin();
        visited[i] = true;
        for(iter;iter!=adj[i].end();iter++){
            // int dist = g_map[i][*iter];
            cout << "vertices " << i << " adj nodes " <<  *iter <<endl;
            if(i!=0 && *iter !=0 && visited[*iter] == true){
                callVert = i;
                int back_dist = backPropogation(i,*iter);
            }
            else if(i == 0){
               cout << " Nodes " <<  i << " is Src Node" <<endl; 
               cout << " backDist " << 0 <<endl;
            }
            else if(*iter == 0){
                cout << " Adj node " << *iter <<" is Src node" <<endl;
            }
            else{
                cout << " Adj Node "<<*iter <<" is unvisited" << endl;
            }
            
        }
    }
    // distFrmSrc
    // cout << "adj size " << adj.size();

}

int main()
{
 
    /* Let us create the example graph discussed above */
    int graph[V][V] = { { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
                        { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
                        { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
                        { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
                        { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
                        { 0, 0, 4, 14, 10, 0, 2, 0, 0 },
                        { 0, 0, 0, 0, 0, 2, 0, 1, 6 },
                        { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
                        { 0, 0, 2, 0, 0, 0, 6, 7, 0 } };
    
    for(int i=0; i<V; i++){
        for(int j=0; j<V; j++)
        {
            if(graph[i][j] != 0){
                adj[i].push_back(j);
                //cout << "Vertices " << i <<endl;
            }
        }
    }
 
    // Function call
    dijkstra(graph, 0);
 
    return 0;
}