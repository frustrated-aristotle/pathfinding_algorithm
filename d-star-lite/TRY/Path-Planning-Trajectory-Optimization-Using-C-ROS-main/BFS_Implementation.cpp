#include<bits/stdc++.h>
using namespace std;

map<int, list<int>> adj;
map<int,bool>visited;
//vector<int>unvisited;
queue<int> unvisited; 

// Add edge in undirected graph i.e, (a,b) (b,a)
void addEdge(int a, int b){
    adj[a].push_back(b);
    //adj[b].push_back(a);
}
void searchBFS(int u){
    int uv=0;
    visited[u] = true;
    cout << "node :" << u << endl;
    auto iter = adj[u].begin();
    //cout << "begin : " << *iter << endl;
    if(*iter !=0){
        //cout << "if true" <<endl;
        for(iter;iter!=adj[u].end();iter++){
            if (!visited[*iter])
            {
                unvisited.push(*iter);
                cout << "Node " << u <<" child " <<*iter<< endl;
            }
        }
    }

    char size = unvisited.size();
    //cout << "unvisited size " << unvisited.size()<<endl;
    int new_node = unvisited.front();
    if(!visited[new_node]){
        unvisited.pop();
        cout << "Next node "<<new_node<<endl;
        searchBFS(new_node);
    }
    
    /*
    for(int i =0; i<size;i++){
        int new_node = unvisited.front();
        auto iter_n = adj[new_node].begin();
        cout << "New Node " << new_node<<endl;
        //cout << "Unvisited " << i+1 << " is " << unvisited.front()<<endl;
        for(iter_n;iter_n!=adj[new_node].end();iter_n++){
        if (!visited[*iter_n])
            unvisited.push(*iter_n);
            cout << "Next Node " << *iter_n << endl;
        }    
        unvisited.pop();
    }*/
    /*
    if (!visited[*iter]){
        //unvisited.pop();
        auto iter_n = adj[new_node].begin();
        cout << "Recursive" <<endl;
        cout << "Unvisited " <<*iter_n<<endl;
        unvisited.pop();
        searchBFS(*iter);
    }*/

    /*
    for(int uv = 0;uv<visited.size();uv++){
        auto iter_b = adj[uv].begin();
        for(iter_b;iter_b!=adj[uv].end();iter_b++){
            //adj[uv][*iter_b]
            if (!visited[*iter])
                searchBFS(*iter_b);
        }
    
    }*/
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
    addEdge(5,6);
    addEdge(5,7);
    addEdge(5,8);
    addEdge(7,9);
    //nodeCheck(3);
    //child of " << *(iter) << endl;
    searchBFS(0);
    return 0;
}