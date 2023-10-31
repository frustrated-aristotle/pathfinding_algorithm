#include<bits/stdc++.h>
using namespace std;

map<int, list<int>> adj;
map<int,bool>visited;
//map<int,list<int>>unvisited;

// Add edge in undirected graph i.e, (a,b) (b,a)
void addEdge(int a, int b){
    adj[a].push_back(b);
    //adj[b].push_back(a);
}
void searchDFS(int u){
    visited[u] = true;
    cout << "node :" << u << endl;
    auto iter = adj[u].begin();
    //cout << "begin : " << *iter << endl;
    if(*iter !=0){
        //cout << "if true" <<endl;
        for(iter;iter!=adj[u].end();iter++){
            if (!visited[*iter])
                //unvisited[u].push_back(*iter)
                cout << "Next Node " << *iter << endl;
                searchDFS(*iter);
        }
    }
}
void nodeCheck(int N){
    auto iter = adj[N].begin();
    auto iter_end = adj[N].end();
    cout << "begin "<< *iter<<endl;
    cout << "end "<< *iter_end<<endl;
    int cnt = 1;
    for(iter;iter!=adj[N].end();iter++){
        cout << "child  " <<cnt <<" of Node "<< N << " is "<< *(iter) << endl;
        cnt++;
    }
}
int main(){

    
    addEdge(0,1);
    addEdge(0,2);
    addEdge(1,3);
    addEdge(1,4);
    addEdge(2,5);
    //nodeCheck(3);
    //child of " << *(iter) << endl;
    searchDFS(0);
    return 0;
}