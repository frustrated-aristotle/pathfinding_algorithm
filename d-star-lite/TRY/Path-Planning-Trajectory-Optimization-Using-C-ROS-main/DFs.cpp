#include<bits/stdc++.h>
using namespace std;
int age;
string name;
map<int, list<int>> adj;
queue<int> q1;

void addEdge(int a, int b){
    adj[a].push_back(b);
    adj[b].push_back(a);
    //cout << "adj in addEdge Func: " << adj[1] << endl;
}
int main(){
    /*
    cout << "Enter Name" << endl;
    cin >> name;
    cout << "Enter Age" << endl;
    cin >> age;
    cout <<"Age of " << name << " is " << age<< endl;
    //cout << "DFS";*/
    int node = 6;
    map<int, list<int>> adj1;
    list<int> l1;
    vector<int> dummy;
    map<int, bool> visited;

    dummy.push_back(23);
    addEdge(0,1);
    for(int i =0; i<=5; i++){
        l1.push_back(i*2);
    }
    adj1[0].push_back(2);
    adj1[0].push_back(1);
    visited[0] = true;

    q1.push(1);
    q1.push(2);
    q1.push(3);
    auto fifo = q1.front();

    auto iter = l1.begin();
    auto iter_map = adj1[0].begin();
    //cout << "adj1 in main: " << adj1[0][*iter_map] << endl;
    cout << "iter_map: " << *(iter_map) << endl;
    cout << "list: " << *iter << endl;
    cout << "visited: " << visited[0] << endl;
    cout << "dummy: " << dummy[0]<<endl;
    cout << "FIFO: " << fifo << endl;
    return 0;
}
