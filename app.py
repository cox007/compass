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
                'administrative block': {'main gate': 100, 'mba college': 60, 'Jn. F': 17, 'Jn. G': 7, 'Jn. A': 8, 'bio block': 39},
                'mba college': {'administrative block': 60},
                'bio block': {'service gate': 33, 'Jn. B': 27},
                'Jn. A': {'administrative block': 8, 'church': 10, 'knowledge centre': 22},
                'Jn. G': {'Jn. F': 15, 'auditorium': 10, 'Jn. E': 27, 'church': 10, 'administrative block': 7},
                'Jn. F': {'administrative block': 17, 'Jn. G': 15, 'ground': 22},
                'service gate': {'bio block': 33},
                'Jn. B': {'bio block': 27, 'boys hostel': 13, 'knowledge centre': 9},
                'knowledge centre': {'Jn. A': 22, 'church': 10, 'Jn. B': 9},
                'church': {'Jn. G': 10, 'Jn. D': 15, 'knowledge centre': 10, 'Jn. A': 10},
                'auditorium': {'Jn. G': 6},
                'ground': {'Jn. F': 22, 'decinial block': 14},
                'decinial block': {'Jn. E': 5, 'ground': 14},
                'Jn. E': {'Jn. G': 27, 'decinial block': 5, 'Jn. D': 8},
                'Jn. D': {'church': 15, 'Jn. C': 19, 'Jn. E': 8},
                'Jn. C': {'girls hostel': 11, 'Jn. D': 19, 'canteen': 9, 'boys hostel': 12},
                'boys hostel': {'Jn. B': 13, 'Jn. C': 12},
                'canteen': {'Jn. C': 9},
                'girls hostel': {'Jn. C': 11},
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
                    return path, str(shortest_distance[goal])
            path, distance = dijkstra(graph, origin, destination)
            word = ""

            for items in path:
                word = word + " " + "→" + " " + items


    return render_template("result.html", path = word, distance= distance, len = len(path))

@app.route("/result")
def result():
    return render_template("result.html",)

if __name__ == '__main__':
    app.run(debug=True)