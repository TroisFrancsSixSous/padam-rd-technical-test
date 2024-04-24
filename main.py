from input import parse_cmd_line, parse_file
from graph import Graph


def main():
    in_file, plot_graph = parse_cmd_line()
    print(in_file)
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()

