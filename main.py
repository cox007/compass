from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods = ['POST','GET'])
def home():
    return render_template("page.html")

@app.route("/form_data", methods = ['POST','GET'])
def data():
    if request.method == 'POST':
        if 'origin' in request.form and 'destination' in request.form:
            origin = request.form['origin']
            origin = origin.lower()
            destination = request.form['destination']
            destination = destination.lower()

            graph = {
                'main gate': {'administrative block': 100},
                'administrative block': {'main gate': 100, 'mba college': 60, 'F': 17, 'G': 7, 'A': 8, 'bio block': 39},
                'mba college': {'administrative block': 60},
                'bio block': {'service gate': 33, 'B': 27},
                'A': {'administrative block': 8, 'church': 10, 'knowledge centre': 22},
                'G': {'F': 15, 'auditorium': 10, 'E': 27, 'church': 10, 'administrative block': 7},
                'F': {'administrative block': 17, 'G': 15, 'ground': 22},
                'service gate': {'bio block': 33},
                'B': {'bio block': 27, 'boys hostel': 13, 'knowledge centre': 9},
                'knowledge centre': {'A': 22, 'church': 10, 'B': 9},
                'church': {'G': 10, 'D': 15, 'knowledge centre': 10, 'A': 10},
                'auditorium': {'G': 6},
                'ground': {'F': 22, 'decinial block': 14},
                'decinial block': {'E': 5, 'ground': 14},
                'E': {'G': 27, 'decinial block': 5, 'D': 8},
                'D': {'church': 15, 'C': 19, 'E': 8},
                'C': {'girls hostel': 11, 'D': 19, 'canteen': 9, 'boys hostel': 12},
                'boys hostel': {'B': 13, 'C': 12},
                'canteen': {'C': 9},
                'girls hostel': {'C': 11},
            }

            def dijkstra(graph, start, goal):
                shortest_distance = {}
                predecessor = {}
                unseenNodes = graph
                infinity = 9999999
                path = []
                for node in unseenNodes:
                    shortest_distance[node] = infinity
                shortest_distance[start] = 0

                while unseenNodes:
                    minNode = None
                    for node in unseenNodes:
                        if minNode is None:
                            minNode = node
                        elif shortest_distance[node] < shortest_distance[minNode]:
                            minNode = node

                    for childNode, weight in graph[minNode].items():
                        if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                            shortest_distance[childNode] = weight + shortest_distance[minNode]
                            predecessor[childNode] = minNode
                    unseenNodes.pop(minNode)

                currentNode = goal
                while currentNode != start:
                    try:
                        path.insert(0, currentNode)
                        currentNode = predecessor[currentNode]
                    except KeyError:
                        print('Path not reachable')
                        break
                path.insert(0, start)
                if shortest_distance[goal] != infinity:
                    # print('Shortest distance is ' + str(shortest_distance[goal]))
                    return str(path), str(shortest_distance[goal])

            path, distance = dijkstra(graph, origin, destination)
    return render_template("result.html", a = path)

@app.route("/result")
def result():
    return render_template("result.html",)

if __name__ == '__main__':
    app.run(debug=True)