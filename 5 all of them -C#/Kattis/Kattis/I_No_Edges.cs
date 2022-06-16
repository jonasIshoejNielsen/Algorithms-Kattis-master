using Kattis.IO;
using Microsoft.Win32.SafeHandles;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Threading;

namespace Kattis
{
    class Node
    {
        public Boolean isWalkable;
        public Tuple<int, int> pos;
        public Node(bool isWalkable, Tuple<int, int> pos)
        {
            this.isWalkable = isWalkable;
            this.pos = pos;
        }
        public override string ToString()
        {
            return isWalkable ? "." : "#";
        }
        public void PrintSelf()
        {
            Console.WriteLine(this.ToString() + "  -  " +pos);
        }
    }
    class Case{
        public Node[][] nodes;
        public Node s;
        public Node t;
        public int n;

        public Case(int numberOfRowsCols)
        {
            n = numberOfRowsCols;
            this.nodes =  new Node[numberOfRowsCols][];
        }
        public void addLine(char[] line, int lineIndex)
        {
            var currNodes = new Node[line.Length];
            for(int i=0; i<line.Length; i++)
                currNodes[i] = new Node(line[i] == '.', Tuple.Create(lineIndex, i));
            nodes[lineIndex] = currNodes;
        }
        public void finish()
        {
            s = nodes[0][0];
            t = nodes[n - 1][n - 1];
        }
        public void printCase()
        {
            s.PrintSelf();
            foreach (Node[] nodeRow in nodes){
                foreach (Node node in nodeRow)
                    Console.Write(node);
                Console.WriteLine("");
            }
        }
    }

    class I_No_Edges
    {
        static void Main(string[] args)
        {
            var currCase = parse_start();
            currCase.finish();
            //currCase.printCase();

            var dijk = dijkstraFindNumberOfPaths(currCase.s, currCase.nodes, currCase.n);
            if (dijk[currCase.n - 1][currCase.n - 1] > 0) { 
                BigInteger mod = BigInteger.Pow(2, 31) - 1;
                Console.WriteLine(dijk[currCase.n - 1][currCase.n - 1] % mod);
            }
            else
            {
                var foundPath = bfs(currCase.nodes);
                if(foundPath) Console.WriteLine("THE GAME IS A LIE");
                else Console.WriteLine("INCONCEIVABLE");
            }
        }

        static Case parse_start()
        {
            Scanner s = new Scanner();
            Case currCase = new Case(s.NextInt());

            int line_number = 0;        //first is numBlocks above
            //while (s.HasNext())
            while(line_number < currCase.n)
            {
                line_number++;
                string line = s.Next();

                var split = line.ToCharArray();
                currCase.addLine(split, line_number - 1);
            }
            return currCase;
        }

        static BigInteger[][] dijkstraFindNumberOfPaths(Node s, Node[][] nodes, int n)
        {
            var visited = new BigInteger[n][];
            for (int i = 0; i < n; i++)
                visited[i] = new BigInteger[n];
            visited[0][0] = 1;
            for (int row = 0; row < n; row++)
            {
                for (int col = 0; col < n; col++)
                {
                    var curr = nodes[row][col];
                    if (!curr.isWalkable) continue;
                    BigInteger pathsToN = 0;
                    if (row > 0)        pathsToN += visited[row - 1][col];
                    else if (col == 0)  continue;
                    if (col > 0)        pathsToN += visited[row][col - 1];
                    visited[row][col] = pathsToN;
                }
            }


            return visited;
        }
        static List<Tuple<int, int>> edges(int row, int col, int n) {
            var res = new List<Tuple<int, int>>();
            if (row > 0) res.Add(Tuple.Create(row - 1, col));
            if (row < n - 1) res.Add(Tuple.Create(row + 1, col));
            if (col > 0) res.Add(Tuple.Create(row, col-1));
            if (col < n - 1) res.Add(Tuple.Create(row, col+1));
            return res;
        }

        static bool bfs(Node[][] nodes)
        {
            int n = nodes.Length;
            var visited = new bool[n][];
            for (int i = 0; i < n; i++)
                visited[i] = new bool[n];
            visited[0][0] = true;
            var frontier = new Stack<Tuple<int,int>>();
            foreach (var e in edges(0, 0, n)) 
                frontier.Push(e);
            while (frontier.Count > 0)
            {
                var e = frontier.Pop();
                if (visited[e.Item1][e.Item2]) continue;
                if (!nodes[e.Item1][e.Item2].isWalkable) continue;
                if (e.Item1 == n - 1 && e.Item2 == n - 1)
                    return true;

                visited[e.Item1][e.Item2] = true;
                foreach (var eNew in edges(e.Item1, e.Item2, n))
                    frontier.Push(eNew);
                
            }

            return false;
        }

    }
}