#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <bits/stdc++.h>
void add_edge(std::vector<int> adj[], int src, int dest)
{
    adj[src].push_back(dest);
    adj[dest].push_back(src);
}

bool BFS(std::vector<int> adj[], int src, int dest, int v, int pred[], int dist[])
{
    std::list<int> queue;
    bool visited[v];
    for (int i = 0; i < v; i++)
    {
        visited[i] = false;
        dist[i] = INT_MAX;
        pred[i] = -1;
    }
 
    visited[src] = true;
    dist[src] = 0;
    queue.push_back(src);
 
    while (!queue.empty()) 
	{
        int u = queue.front();
        queue.pop_front();
        for (int i = 0; i <adj[u].size(); i++) 
		{
            if (visited[adj[u][i]] == false) 
			{
                visited[adj[u][i]] = true;
                dist[adj[u][i]] = dist[u] + 1;
                pred[adj[u][i]] = u;
                queue.push_back(adj[u][i]);
 
                if (adj[u][i] == dest)
                    return true;
            }
        }
    }
    return false;
}
 

void printShortestDistance(std::vector<int> adj[], int s,int dest, int v)
{
    int pred[v], dist[v];
 
    if (BFS(adj, s, dest, v, pred, dist) == false) 
	{
        std::cout << "Error: Given source and destination are not connected"<<std::endl;
        return;
    }
 
    std::vector<int> path;
    int crawl = dest;
    path.push_back(crawl);
    while (pred[crawl] != -1) 
	{
        path.push_back(pred[crawl]);
        crawl = pred[crawl];
    }
    for (int i = path.size() - 1; i >=0; i--)
    {	
        std::cout << path[i];
	if(i!=0)
	 std::cout<<"-";
    }
    std::cout<<std::endl;
}

int main() 
{
 std::string CommandStr;
 int V, tempV;
 std::string InputStr;
 std::string VerticesStr;
 std::string EdgesStr; 
 int src;
 int dest;
 int e1,e2;
 char edges_index;
 std::vector<int> *adj;
 
 while (!std::cin.eof()) 
 {
    std::string line;
    std::getline(std::cin, line);
    std::istringstream input(line);
	
	if(std::cin.eof())
		break;
			
    while (!input.eof()) 
	{
        input>>CommandStr;
        if(CommandStr.compare("V")==0)
        {		
			input>>V;
			if(V<=1)
			{
				std::cout<<"Error: Invalid vertices specified"<<std::endl;
				break;
			}
			else
			{
				tempV=V+1;
				adj=new std::vector<int> [tempV];
			}
		}
		if(CommandStr.compare("E")==0)
        {
       		input>>InputStr;
        	std::istringstream EdgesString(InputStr);
  			EdgesString>>edges_index;
  			while(edges_index!='}')
  			{
  				EdgesString>>edges_index;
  				if(edges_index=='}')
  					break;
  				
				EdgesString>>e1;
				EdgesString>>edges_index;
				EdgesString>>e2;
				if(e1==e2 || e1>V || e2>V)
				{
					std::cout<<"Error: Invalid edge input"<<std::endl;
					break;
				}
  				else
  				{
  					add_edge(adj,e1,e2);
  					EdgesString>>edges_index;
  					EdgesString>>edges_index;
  				}
			}
		}
		if(CommandStr.compare("s")==0)
    	{
        		input>>src;
        		input>>dest;
				printShortestDistance(adj, src, dest, tempV);
		}
    	if (input.eof())
        break;
        else
        {
        	std::cerr<<"Error: Invalid input"<<std::endl;
			break;
		}
	}
}
 return 0;
}