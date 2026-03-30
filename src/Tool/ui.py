"""
Schilda City — Disaster Management System
Graphical User Interface
Team E: Nazari, Rasos, Vo
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import heapq

import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# ─── Shared Constants ─────────────────────────────────────────────────────────

FILE_PATH = "src/Data/undirected_weighted_graph.txt"

NODE_ATTRS = {
    "A": "Hospital",
    "B": "Rescue Station",
    "C": "Government Building",
    "D": "Evacuation Point",
    "E": "Boat Rescue",
    "F": "Emergency Service",
    "G": "Supply Point",
    "H": "Staging Area",
    "I": "Staging Area",
}

# Catppuccin Mocha palette
BG       = "#1e1e2e"
SURFACE  = "#313244"
SURFACE0 = "#181825"
TEXT     = "#cdd6f4"
SUBTEXT  = "#a6adc8"
BLUE     = "#89b4fa"
GREEN    = "#a6e3a1"
YELLOW   = "#f9e2af"
RED      = "#f38ba8"
MAUVE    = "#cba6f7"
OVERLAY  = "#585b70"
TEAL     = "#94e2d5"


def load_graph():
    adj = pd.read_csv(FILE_PATH, sep=r"\s+", index_col=0)
    G = nx.Graph()
    for i, row in adj.iterrows():
        for j, w in row.items():
            if w > 0 and i != j:
                G.add_edge(i, j, weight=w)
    nx.set_node_attributes(G, NODE_ATTRS, "description")
    return G


def node_label(n):
    return f"{n}: {NODE_ATTRS[n]}"


def _style_fig(fig, ax):
    """Apply dark theme to a figure/axes."""
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(OVERLAY)
    ax.axis("off")


# ─── B1 / B2 — Data Structure Visualizer ─────────────────────────────────────

def run_b1b2(graph_type, mark_impassable, mark_waterway, add_points):
    """
    Build and visualise the city map based on user-selected options.
    Corresponds to B1 (load/display/print) and B2 (add features) functionality.
    """
    adj = pd.read_csv(FILE_PATH, sep=r"\s+", index_col=0)
    matrix = adj.values.tolist()
    labels = list(adj.columns)

    directed = "directed" in graph_type
    weighted = "weighted" in graph_type

    G = nx.DiGraph() if directed else nx.Graph()
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val != 0 and i != j:
                if weighted:
                    G.add_edge(labels[i], labels[j], weight=int(val))
                else:
                    G.add_edge(labels[i], labels[j])

    impassable_roads = []
    road_types = {}
    important_points = {}

    if mark_impassable:
        impassable_roads.append(("F", "E"))
        if G.has_edge("F", "E"):
            G.remove_edge("F", "E")
        if directed and G.has_edge("E", "F"):
            G.remove_edge("E", "F")

    if mark_waterway:
        road_types[("E", "I")] = "waterway"

    if add_points:
        important_points["Hospital"]            = ("A", 200)
        important_points["Government Building"] = ("C", 150)

    # ── text output ──────────────────────────────────────────────────────────
    lines = ["B1/B2 — City Map Data Structure Explorer", "=" * 42, ""]
    lines.append(f"Graph type : {graph_type.replace('_', ' ').title()}")
    lines.append(f"Directed   : {directed}")
    lines.append(f"Weighted   : {weighted}")
    lines.append(f"Nodes      : {G.number_of_nodes()}")
    lines.append(f"Edges      : {G.number_of_edges()}")
    lines.append("")

    if impassable_roads:
        lines.append("Impassable roads (removed from graph):")
        for s, e in impassable_roads:
            lines.append(f"  {s} ↔ {e}")
        lines.append("")

    if road_types:
        lines.append("Road types:")
        for (s, e), t in road_types.items():
            lines.append(f"  {s} — {e}  →  {t}")
        lines.append("")

    if important_points:
        lines.append("Important points:")
        for name, (loc, dist) in important_points.items():
            lines.append(f"  {name} @ {loc}  ({dist} m)")
        lines.append("")

    lines.append("Adjacency Matrix:")
    lines.append("     " + "  ".join(f"{l:>2}" for l in labels))
    for i, row in enumerate(matrix):
        vals = "  ".join(f"{int(v):>2}" for v in row)
        lines.append(f"  {labels[i]}  {vals}")

    # ── figure ───────────────────────────────────────────────────────────────
    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, seed=42, k=2.0)

    node_colors = []
    for n in G.nodes():
        if add_points and n in {v for v, _ in important_points.values()}:
            node_colors.append(YELLOW)
        else:
            node_colors.append(MAUVE)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color=node_colors)
    nx.draw_networkx_labels(G, pos,
                            labels={n: node_label(n) for n in G.nodes()},
                            ax=ax, font_size=7,
                            font_color=BG, font_weight="bold")

    edge_colors = []
    for u, v in G.edges():
        if (u, v) in impassable_roads or (v, u) in impassable_roads:
            edge_colors.append(RED)
        elif road_types.get((u, v)) == "waterway" or road_types.get((v, u)) == "waterway":
            edge_colors.append(BLUE)
        else:
            edge_colors.append(OVERLAY)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                           width=1.5, arrows=directed,
                           arrowstyle="-|>", arrowsize=15)

    if weighted:
        edge_lbl = {(u, v): str(d["weight"]) for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lbl, ax=ax,
                                     font_size=6, font_color=TEXT)

    if add_points:
        for name, (loc, dist) in important_points.items():
            x, y = pos[loc]
            ax.annotate(f"★ {name}\n({dist} m)", xy=(x, y),
                        xytext=(x + 0.06, y + 0.12),
                        fontsize=8, color=YELLOW, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=YELLOW, lw=0.8))

    legend_handles = [
        plt.Line2D([0],[0], marker="o", color="w",
                   markerfacecolor=YELLOW, markersize=9, label="Important point"),
        plt.Line2D([0],[0], color=BLUE,   linewidth=2, label="Waterway"),
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Impassable (removed)"),
    ]
    ax.legend(handles=legend_handles, loc="lower left",
              facecolor=SURFACE, labelcolor=TEXT, fontsize=8)

    ax.set_title(
        f"B1/B2: {graph_type.replace('_',' ').title()}  "
        f"({'Directed' if directed else 'Undirected'}, "
        f"{'Weighted' if weighted else 'Unweighted'})",
        fontsize=11, color=TEXT,
    )
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── F1 — Prim's MST ──────────────────────────────────────────────────────────

def run_f1():
    G = load_graph()
    for u, v in G.edges():
        if {"E", "I"} <= {u, v}:
            G.edges[u, v]["etype"] = "Waterway"
            G.edges[u, v]["color"] = BLUE
        elif {"F", "E"} <= {u, v}:
            G.edges[u, v]["etype"] = "Impassable"
            G.edges[u, v]["color"] = RED
        else:
            G.edges[u, v]["etype"] = ""
            G.edges[u, v]["color"] = OVERLAY

    start = "A"
    visited = {start}
    heap, mst_edges = [], []
    for nbr, data in G[start].items():
        heapq.heappush(heap, (data["weight"], start, nbr))
    while heap:
        w, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, w))
            for nbr, data in G[v].items():
                if nbr not in visited:
                    heapq.heappush(heap, (data["weight"], v, nbr))
    total_cost = sum(w for _, _, w in mst_edges)
    mst = nx.Graph()
    mst.add_weighted_edges_from(mst_edges)

    lines = ["F1 — Prim's Minimum Spanning Tree (Min-Heap)", "=" * 44, ""]
    lines.append(f"Start node        : {start} ({NODE_ATTRS[start]})")
    lines.append(f"Minimum total cost: {total_cost}")
    lines.append(f"Nodes in MST      : {len(mst_edges) + 1}")
    lines.append("")
    lines.append("MST edges (sorted by weight):")
    for u, v, w in sorted(mst_edges, key=lambda x: x[2]):
        lines.append(f"  {u} ({NODE_ATTRS[u]:<22}) — {v} ({NODE_ATTRS[v]:<22})  w={w}")
    lines.append("")
    lines.append("Time Complexity: O(E log V)")
    lines.append(f"  V={G.number_of_nodes()},  E={G.number_of_edges()}")
    lines.append(f"  ≈ O({G.number_of_edges()} · log {G.number_of_nodes()})")

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color=MAUVE)
    nx.draw_networkx_labels(G, pos,
                            labels={n: node_label(n) for n in G.nodes()},
                            ax=ax, font_size=7, font_color=BG, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color=[d["color"] for _,_,d in G.edges(data=True)],
                           width=1)
    nx.draw_networkx_edges(mst, pos, ax=ax, edge_color=GREEN, width=3)
    edge_lbl = {
        (u, v): (f"{d['etype']} ({d['weight']})" if d["etype"] else str(d["weight"]))
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lbl, ax=ax,
                                 font_size=6, font_color=TEXT)
    ax.legend(handles=[
        plt.Line2D([0],[0], color=GREEN,  linewidth=3, label="MST edges"),
        plt.Line2D([0],[0], color=BLUE,   linewidth=2, label="Waterway"),
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Impassable"),
        plt.Line2D([0],[0], color=OVERLAY,linewidth=1, label="Other edges"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    ax.set_title(f"F1: Prim's MST  —  Minimum Rebuild Cost: {total_cost}",
                 fontsize=11, color=TEXT)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── F2 — Edmonds-Karp Max Flow ───────────────────────────────────────────────

def run_f2():
    adj = pd.read_csv(FILE_PATH, sep=r"\s+", index_col=0)
    G = nx.from_pandas_adjacency(adj, create_using=nx.Graph)
    city_map = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        city_map.add_edge(u, v, capacity=data["weight"])
        city_map.add_edge(v, u, capacity=data["weight"])
    nx.set_node_attributes(city_map, NODE_ATTRS, "description")

    shelters       = {"A": 200, "B": 150, "C": 250, "H": 50, "I": 50}
    shelter_nodes  = ["A", "B", "C", "H", "I"]
    evac_needs     = 300
    routes         = {("D","A"):150, ("D","B"):130, ("D","C"):200,
                      ("D","H"):20,  ("D","I"):20}

    for (s, e), cap in routes.items():
        if city_map.has_edge(s, e):
            city_map[s][e]["capacity"] = cap
    nx.set_node_attributes(city_map, shelters, "capacity")

    for sh in shelters:
        city_map.remove_edges_from(
            [(sh, n) for n in list(city_map.successors(sh))]
        )

    shelter_flows, total_flow = {}, 0
    for sh, cap in sorted(shelters.items(), key=lambda x: x[1]):
        fv, cf = nx.maximum_flow(city_map, "D", sh,
                                 flow_func=nx.algorithms.flow.edmonds_karp)
        fv = min(fv, cap)
        total_flow += fv
        shelter_flows[sh] = fv
        for u, v, data in city_map.edges(data=True):
            if u in cf and v in cf[u]:
                data["capacity"] -= cf[u][v]

    ok = total_flow >= evac_needs
    lines = ["F2 — Edmonds-Karp Maximum Flow", "=" * 40, ""]
    lines.append(f"Source           : D ({NODE_ATTRS['D']})")
    lines.append(f"Evacuation needs : {evac_needs} people")
    lines.append(f"Maximum flow     : {total_flow} people")
    lines.append(f"Infrastructure   : {'✓ SUFFICIENT' if ok else '✗ INSUFFICIENT'}")
    lines.append("")
    lines.append("Flow per shelter:")
    for sh, fv in shelter_flows.items():
        cap = shelters[sh]
        filled = int(fv / cap * 20)
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"  {sh} ({NODE_ATTRS[sh]:<22})  {fv:>3}/{cap:<3}  [{bar}]")
    lines.append("")
    lines.append("Route capacities (D → shelter):")
    for (_, sh), cap in routes.items():
        lines.append(f"  D → {sh}  ({NODE_ATTRS[sh]:<22}) cap={cap}")
    lines.append("")
    lines.append("Time Complexity: O(V · E²)")

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(city_map, seed=42, k=5)
    nx.draw_networkx_nodes(city_map, pos, ax=ax, node_size=700, node_color=MAUVE)
    edge_colors = [
        RED if u == "D" and v in shelter_nodes else OVERLAY
        for u, v, _ in city_map.edges(data=True)
    ]
    nx.draw_networkx_edges(city_map, pos, ax=ax, width=2, alpha=0.8,
                           edge_color=edge_colors)
    nlabels = {
        n: f"{n}: {NODE_ATTRS[n]}" + (f"\ncap {shelters[n]}" if n in shelters else "")
        for n in city_map.nodes()
    }
    nx.draw_networkx_labels(city_map, pos, labels=nlabels, ax=ax,
                            font_size=7, font_color=BG)
    elabels = {
        ("D", sh): f"{shelter_flows.get(sh,0)}/{routes[('D',sh)]}"
        for sh in shelter_nodes if city_map.has_edge("D", sh)
    }
    nx.draw_networkx_edge_labels(city_map, pos, edge_labels=elabels, ax=ax,
                                 font_size=8, font_color=YELLOW)
    title_color = GREEN if ok else RED
    ax.set_title(
        f"F2: Max Flow = {total_flow}  |  Needs: {evac_needs}  "
        f"|  {'SUFFICIENT ✓' if ok else 'INSUFFICIENT ✗'}",
        fontsize=10, color=title_color,
    )
    ax.legend(handles=[
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Evacuation route (D→shelter)"),
        plt.Line2D([0],[0], color=OVERLAY,linewidth=1, label="Other edges"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── F3 — Dijkstra Hybrid Routes ─────────────────────────────────────────────

def run_f3():
    G = load_graph()
    for u, v in G.edges():
        if {"E", "I"} <= {u, v}:
            G.edges[u, v]["color"] = BLUE
            G.edges[u, v]["etype"] = "Waterway"
        else:
            G.edges[u, v]["color"] = OVERLAY
            G.edges[u, v]["etype"] = ""

    def dijkstra(graph, start, target):
        dist = {n: float("inf") for n in graph.nodes}
        prev = {n: None for n in graph.nodes}
        dist[start] = 0
        queue = [(0, start)]
        while queue:
            queue.sort()
            cd, cn = queue.pop(0)
            if cn == target:
                break
            for nbr in graph.neighbors(cn):
                d = cd + graph[cn][nbr]["weight"]
                if d < dist[nbr]:
                    dist[nbr] = d
                    prev[nbr] = cn
                    queue.append((d, nbr))
        path, cur = [], target
        while cur is not None:
            path.insert(0, cur)
            cur = prev[cur]
        return path, dist[target]

    e_node, i_node, target = "E", "I", "F"
    paths, distances = {}, {}
    for node in G.nodes:
        if node in {target, e_node, i_node}:
            continue
        p_e, d_e   = dijkstra(G, node, e_node)
        p_it, d_it = dijkstra(G, i_node, target)
        ei_w = G[e_node][i_node]["weight"]

        full_ei = p_e + [i_node] + p_it[1:]
        dist_ei = d_e + ei_w + d_it

        p_i, d_i   = dijkstra(G, node, i_node)
        p_et, d_et = dijkstra(G, e_node, target)
        full_ie = p_i + [e_node] + p_et[1:]
        dist_ie = d_i + ei_w + d_et

        if dist_ei <= dist_ie:
            paths[node], distances[node] = full_ei, dist_ei
        else:
            paths[node], distances[node] = full_ie, dist_ie

    lines = ["F3 — Dijkstra Hybrid Routes to F (Emergency Service)", "=" * 52, ""]
    lines.append("Rule: every route must traverse the E–I waterway.")
    lines.append(f"Target: F ({NODE_ATTRS['F']})")
    lines.append("")
    lines.append("Routes (sorted by distance):")
    for node, dist in sorted(distances.items(), key=lambda x: x[1]):
        pstr = " → ".join(paths[node])
        lines.append(f"  {node} ({NODE_ATTRS[node]:<22}):  dist={dist:>3}   {pstr}")
    lines.append("")
    lines.append("Time Complexity: O(V² log V + E)")

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color=MAUVE)
    nx.draw_networkx_labels(G, pos,
                            labels={n: node_label(n) for n in G.nodes()},
                            ax=ax, font_size=7, font_color=BG, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color=[d["color"] for _,_,d in G.edges(data=True)],
                           width=1)
    used = {(paths[n][i], paths[n][i+1])
            for n in paths for i in range(len(paths[n])-1)}
    path_edges = [(u, v) for u, v in used if G.has_edge(u, v)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax,
                           edge_color=GREEN, width=2.5)
    edge_lbl = {(u,v): str(d["weight"]) for u,v,d in G.edges(data=True)}
    for u, v in G.edges():
        if G.edges[u,v].get("etype") == "Waterway":
            edge_lbl[(u,v)] = "Waterway"
    if G.has_edge("F", "E"):
        edge_lbl[("F","E")] = "Impassable"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lbl, ax=ax,
                                 font_size=6, font_color=TEXT)
    ax.set_title("F3: Fastest Hybrid Routes to F via E–I Waterway",
                 fontsize=11, color=TEXT)
    ax.legend(handles=[
        plt.Line2D([0],[0], color=GREEN, linewidth=2.5, label="Hybrid paths"),
        plt.Line2D([0],[0], color=BLUE,  linewidth=2,   label="Waterway (E–I)"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── F4 — K-Medoids ───────────────────────────────────────────────────────────

def run_f4():
    G = load_graph()
    obstacles = [("F", "E")]
    waterways = [("E", "I")]

    def custom_dijkstra(graph, start, imp, ww):
        dist = {n: float("inf") for n in graph.nodes()}
        dist[start] = 0
        pq, visited = [(0, start)], set()
        while pq:
            cd, cn = heapq.heappop(pq)
            if cn in visited:
                continue
            visited.add(cn)
            for nbr in graph.neighbors(cn):
                if nbr in visited:
                    continue
                w = graph.edges[cn, nbr].get("weight", 1)
                if (cn,nbr) in imp or (nbr,cn) in imp:
                    w = float("inf")
                if (cn,nbr) in ww or (nbr,cn) in ww:
                    w += 10
                d = cd + w
                if d < dist[nbr]:
                    dist[nbr] = d
                    heapq.heappush(pq, (d, nbr))
        return dist

    def assign_clusters(graph, medoids, imp, ww):
        clusters  = {m: [] for m in medoids}
        md = {m: custom_dijkstra(graph, m, imp, ww) for m in medoids}
        for node in graph.nodes():
            if node not in medoids:
                dists   = [md[m][node] for m in medoids]
                closest = medoids[dists.index(min(dists))]
                clusters[closest].append(node)
        return clusters

    def calc_cost(graph, clusters, medoids, imp, ww):
        cost = 0
        for m, nodes in clusters.items():
            d = custom_dijkstra(graph, m, imp, ww)
            cost += sum(d[n] for n in nodes)
        return cost

    available = [n for n in G.nodes() if n != "G"]
    best_medoids, best_cost = None, float("inf")
    for i in range(len(available)):
        for j in range(i+1, len(available)):
            cands = ["G", available[i], available[j]]
            cls = assign_clusters(G, cands, obstacles, waterways)
            c = calc_cost(G, cls, cands, obstacles, waterways)
            if c < best_cost:
                best_cost, best_medoids = c, cands

    clusters = assign_clusters(G, best_medoids, obstacles, waterways)

    lines = ["F4 — K-Medoids Supply Point Optimization", "=" * 42, ""]
    lines.append("Constraints:")
    lines.append("  G (Supply Point) fixed as one medoid")
    lines.append("  F–E  impassable  (+∞ penalty)")
    lines.append("  E–I  waterway    (+10 penalty)")
    lines.append("")
    lines.append(f"k                 : 3 supply points")
    lines.append(f"Optimal medoids   : {best_medoids}")
    lines.append(f"Total cluster cost: {best_cost}")
    lines.append("")
    lines.append("Cluster assignments:")
    for m, cl_nodes in clusters.items():
        d = custom_dijkstra(G, m, obstacles, waterways)
        lines.append(f"\n  Medoid {m} ({NODE_ATTRS[m]}):")
        for node in cl_nodes:
            lines.append(f"    → {node} ({NODE_ATTRS[node]:<22})  dist={d[node]}")
    lines.append("")
    lines.append("Time Complexity: O(n² · (V + E log V))")

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, seed=42)
    node_colors = [YELLOW if n in best_medoids else MAUVE for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=800, node_color=node_colors)
    nx.draw_networkx_labels(G, pos,
                            labels={n: node_label(n) for n in G.nodes()},
                            ax=ax, font_size=7, font_color=BG, font_weight="bold")
    edge_colors = []
    for u, v in G.edges():
        if (u,v) in waterways or (v,u) in waterways:
            edge_colors.append(BLUE)
        elif (u,v) in obstacles or (v,u) in obstacles:
            edge_colors.append(RED)
        elif any((u==m and v in clusters[m]) or (v==m and u in clusters[m])
                 for m in best_medoids):
            edge_colors.append(GREEN)
        else:
            edge_colors.append(OVERLAY)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=1.5)
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels={(u,v): str(int(d["weight"]))
                                              for u,v,d in G.edges(data=True)},
                                 ax=ax, font_size=6, font_color=TEXT)
    ax.set_title(f"F4: K-Medoids — Supply Points: {best_medoids}  |  Cost: {best_cost}",
                 fontsize=10, color=TEXT)
    ax.legend(handles=[
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=YELLOW,
                   markersize=9, label="Medoid (supply point)"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=MAUVE,
                   markersize=9, label="Cluster node"),
        plt.Line2D([0],[0], color=GREEN,  linewidth=2, label="Cluster edge"),
        plt.Line2D([0],[0], color=BLUE,   linewidth=2, label="Waterway (+10)"),
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Impassable (+∞)"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── F5 — BFS Deployment ──────────────────────────────────────────────────────

def run_f5():
    adj = pd.read_csv(FILE_PATH, sep=r"\s+", index_col=0)
    G = nx.from_pandas_adjacency(adj, create_using=nx.Graph)
    dmap = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        dmap.add_edge(u, v, capacity=data["weight"])
        dmap.add_edge(v, u, capacity=data["weight"])
    nx.set_node_attributes(dmap, NODE_ATTRS, "description")

    deployment_needs = {
        "B": {"units": 30, "skills": ["medical"],      "equipment": ["first_aid_kit"]},
        "E": {"units": 20, "skills": ["rescue"],       "equipment": ["life_jacket"]},
        "F": {"units": 25, "skills": ["firefighting"], "equipment": ["hose"]},
    }
    staging_areas = {
        "H": {"capacity": 70,
              "skills": ["medical","rescue","firefighting"],
              "equipment": ["first_aid_kit","life_jacket","hose"]},
        "I": {"capacity": 50,
              "skills": ["medical","rescue"],
              "equipment": ["first_aid_kit","life_jacket"]},
    }
    routes = {
        ("H","B"):30, ("H","E"):20, ("H","F"):25,
        ("I","B"):30, ("I","E"):20, ("I","F"):25,
    }
    for (s, e), cap in routes.items():
        if dmap.has_edge(s, e):
            dmap[s][e]["capacity"] = cap

    details = {(u,v): 0 for u,v in dmap.edges()}
    if dmap.has_edge("F","E"):
        dmap["F"]["E"]["type"] = "Impassable"
        dmap["E"]["F"]["type"] = "Impassable"
    if dmap.has_edge("E","I"):
        dmap["E"]["I"]["type"] = "Waterway"
        dmap["I"]["E"]["type"] = "Waterway"

    def bfs(graph, start, target):
        visited = set()
        queue = [(start, [start])]
        while queue:
            vertex, path = queue.pop(0)
            for nxt in set(graph[vertex]) - visited:
                if graph[vertex][nxt].get("type") == "Impassable":
                    continue
                if nxt == target:
                    return path + [nxt]
                queue.append((nxt, path + [nxt]))
                visited.add(nxt)
        return None

    results = {}
    for site, needed in deployment_needs.items():
        nu = needed["units"]
        req_sk = set(needed["skills"])
        req_eq = set(needed["equipment"])
        deployed = 0
        results[site] = {"total_deployed": 0, "paths": []}
        qualifying = [s for s in staging_areas
                      if req_sk.issubset(staging_areas[s]["skills"])
                      and req_eq.issubset(staging_areas[s]["equipment"])]
        units_per = nu // (len(qualifying) if qualifying else 1)
        remaining = nu
        for staging in staging_areas:
            if deployed >= nu:
                break
            if not (req_sk.issubset(staging_areas[staging]["skills"])
                    and req_eq.issubset(staging_areas[staging]["equipment"])):
                continue
            utd = min(units_per, remaining)
            path = bfs(dmap, staging, site)
            if path:
                avail = min(
                    min(dmap[u][v]["capacity"] - details.get((u,v),0)
                        for u, v in zip(path[:-1], path[1:])),
                    staging_areas[staging]["capacity"],
                    utd,
                )
                if avail > 0:
                    for u, v in zip(path[:-1], path[1:]):
                        details[(u,v)] = details.get((u,v), 0) + avail
                    deployed += avail
                    results[site]["total_deployed"] += avail
                    results[site]["paths"].append({"path": path, "units": avail})
                    staging_areas[staging]["capacity"] -= avail
                    remaining -= avail

    all_ok = all(r["total_deployed"] >= deployment_needs[s]["units"]
                 for s, r in results.items())
    lines = ["F5 — BFS Resource Deployment", "=" * 40, ""]
    lines.append(f"Status: {'✓ ALL SITES FULLY DEPLOYED' if all_ok else '✗ SOME SITES UNDER-DEPLOYED'}")
    lines.append("")
    for site, res in results.items():
        nu   = deployment_needs[site]["units"]
        dep  = res["total_deployed"]
        ok   = dep >= nu
        bar  = "█" * dep + "░" * (nu - dep)
        lines.append(f"  {site} ({NODE_ATTRS[site]:<22}): {dep}/{nu}  "
                     f"{'✓' if ok else '✗'}")
        lines.append(f"    [{bar}]")
        for pi in res["paths"]:
            lines.append(f"    {' → '.join(pi['path'])}: {pi['units']} units")
    lines.append("")
    lines.append("Remaining staging area capacity:")
    for s, data in staging_areas.items():
        lines.append(f"  {s} ({NODE_ATTRS[s]}): {data['capacity']} units left")
    lines.append("")
    lines.append("Time Complexity: O(D · S · (V + E))")

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(dmap, seed=42, k=10)
    nx.draw_networkx_nodes(dmap, pos, ax=ax, node_size=700, node_color=MAUVE)
    edge_colors, edge_widths = [], []
    for u, v, data in dmap.edges(data=True):
        if data.get("type") == "Impassable":
            edge_colors.append(RED);    edge_widths.append(3)
        elif data.get("type") == "Waterway":
            edge_colors.append(BLUE);   edge_widths.append(2)
        elif (u,v) in routes:
            edge_colors.append(YELLOW); edge_widths.append(2)
        else:
            edge_colors.append(OVERLAY);edge_widths.append(1)
    nx.draw_networkx_edges(dmap, pos, ax=ax, width=edge_widths,
                           edge_color=edge_colors, alpha=0.8)
    nlabels = {}
    for node, data in dmap.nodes(data=True):
        lbl = f"{node}: {NODE_ATTRS[node]}"
        if node in deployment_needs:
            lbl += f"\nNeeds: {deployment_needs[node]['units']}"
        if node in staging_areas:
            lbl += f"\nCap: {staging_areas[node]['capacity']}"
        nlabels[node] = lbl
    nx.draw_networkx_labels(dmap, pos, labels=nlabels, ax=ax,
                            font_size=7, font_color=BG)
    nx.draw_networkx_edge_labels(dmap, pos,
        edge_labels={(u,v): f"{details.get((u,v),0)}/{data['capacity']}"
                     for u,v,data in dmap.edges(data=True) if (u,v) in routes},
        ax=ax, font_size=7, font_color=YELLOW)
    ax.set_title("F5: BFS Emergency Services Deployment", fontsize=11, color=TEXT)
    ax.legend(handles=[
        plt.Line2D([0],[0], color=YELLOW, linewidth=2, label="Deployment route"),
        plt.Line2D([0],[0], color=BLUE,   linewidth=2, label="Waterway"),
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Impassable"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── Overview ─────────────────────────────────────────────────────────────────

def run_overview():
    G = load_graph()
    for u, v in G.edges():
        if {"E","I"} <= {u,v}:
            G.edges[u,v]["color"] = BLUE;   G.edges[u,v]["label"] = "Waterway"
        elif {"F","E"} <= {u,v}:
            G.edges[u,v]["color"] = RED;    G.edges[u,v]["label"] = "Impassable"
        else:
            G.edges[u,v]["color"] = OVERLAY; G.edges[u,v]["label"] = ""

    adj = pd.read_csv(FILE_PATH, sep=r"\s+", index_col=0)
    lines = ["City of Schilda — Graph Overview", "=" * 40, ""]
    lines.append(f"Nodes : {G.number_of_nodes()}")
    lines.append(f"Edges : {G.number_of_edges()}")
    lines.append("")
    lines.append("Nodes:")
    for n, attr in sorted(NODE_ATTRS.items()):
        lines.append(f"  {n}  {attr}")
    lines.append("")
    lines.append("Special edges:")
    lines.append("  E — I  Waterway  (blue)")
    lines.append("  F — E  Impassable (red)")
    lines.append("")
    lines.append("Adjacency Matrix:")
    lines.append(adj.to_string())

    fig = Figure(figsize=(8, 7))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color=MAUVE)
    nx.draw_networkx_labels(G, pos,
                            labels={n: node_label(n) for n in G.nodes()},
                            ax=ax, font_size=7, font_color=BG, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color=[d["color"] for _,_,d in G.edges(data=True)],
                           width=1.5)
    edge_lbl = {
        (u,v): (f"{d['label']} ({d['weight']})" if d["label"] else str(d["weight"]))
        for u,v,d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lbl, ax=ax,
                                 font_size=6, font_color=TEXT)
    ax.set_title("Schilda City — Full Graph", fontsize=13, color=TEXT)
    ax.legend(handles=[
        plt.Line2D([0],[0], color=BLUE,   linewidth=2, label="Waterway (E–I)"),
        plt.Line2D([0],[0], color=RED,    linewidth=2, label="Impassable (F–E)"),
        plt.Line2D([0],[0], color=OVERLAY,linewidth=1, label="Road"),
    ], loc="lower left", facecolor=SURFACE, labelcolor=TEXT, fontsize=8)
    _style_fig(fig, ax)
    fig.tight_layout()
    return fig, "\n".join(lines)


# ─── UI helpers ───────────────────────────────────────────────────────────────

def _embed_figure(fig, right_frame, canvas_ref, toolbar_ref):
    """Destroy old canvas/toolbar, embed new figure with NavigationToolbar."""
    if canvas_ref["canvas"]:
        canvas_ref["canvas"].get_tk_widget().destroy()
        canvas_ref["canvas"] = None
    if toolbar_ref["toolbar"]:
        toolbar_ref["toolbar"].destroy()
        toolbar_ref["toolbar"] = None

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()

    toolbar_frame = tk.Frame(right_frame, bg=SURFACE)
    toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.config(background=SURFACE)
    for child in toolbar.winfo_children():
        try:
            child.config(background=SURFACE)
        except tk.TclError:
            pass
    toolbar.update()

    widget = canvas.get_tk_widget()
    widget.configure(bg=SURFACE0)
    widget.pack(fill=tk.BOTH, expand=True, padx=4, pady=(4, 0))

    canvas_ref["canvas"]   = canvas
    toolbar_ref["toolbar"] = toolbar_frame
    plt.close(fig)


# ─── App ──────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schilda Disaster Management System")
        self.geometry("1300x780")
        self.minsize(960, 640)
        self.configure(bg=BG)
        self._tab_buttons = []   # (run_btn, func) pairs for Run All
        self._build()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build(self):
        header = tk.Frame(self, bg=SURFACE, pady=10)
        header.pack(fill=tk.X)

        title_frame = tk.Frame(header, bg=SURFACE)
        title_frame.pack(side=tk.LEFT, padx=14, expand=True, fill=tk.X)
        tk.Label(title_frame,
                 text="Schilda City  —  Disaster Management System",
                 font=("Helvetica", 17, "bold"),
                 bg=SURFACE, fg=TEXT).pack(anchor=tk.W)
        tk.Label(title_frame,
                 text="Algorithms & Data Structures  ·  Team E: Nazari · Rasos · Vo",
                 font=("Helvetica", 10),
                 bg=SURFACE, fg=SUBTEXT).pack(anchor=tk.W)

        self._run_all_btn = tk.Button(
            header, text="▶▶  Run All",
            font=("Helvetica", 11, "bold"),
            bg=TEAL, fg=BG, relief=tk.FLAT,
            padx=14, pady=8, cursor="hand2",
            activebackground=GREEN, activeforeground=BG,
            command=self._run_all,
        )
        self._run_all_btn.pack(side=tk.RIGHT, padx=14)

        # ── Notebook ──────────────────────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=SURFACE, foreground=TEXT,
                        padding=[14, 6], font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", BLUE)],
                  foreground=[("selected", BG)])

        self._nb = ttk.Notebook(self)
        self._nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))

        # B1/B2 tab (special — has its own controls)
        b_frame = tk.Frame(self._nb, bg=BG)
        self._nb.add(b_frame, text="  B1/B2  Data  ")
        self._build_b1b2_tab(b_frame)

        # Overview + F1-F5 tabs
        algo_tabs = [
            ("Overview",           "City Graph — nodes, edges, adjacency matrix",
             run_overview),
            ("F1  MST",
             "Prim's Algorithm  ·  Minimum Spanning Tree\n"
             "Minimum cost to rebuild Schilda's infrastructure",
             run_f1),
            ("F2  Max Flow",
             "Edmonds-Karp Algorithm  ·  Maximum Flow\n"
             "Can the infrastructure evacuate 300 people?",
             run_f2),
            ("F3  Hybrid Routes",
             "Dijkstra's Algorithm  ·  Hybrid Shortest Paths\n"
             "Fastest route to Emergency Service via E–I waterway",
             run_f3),
            ("F4  Supply Points",
             "K-Medoids Clustering  ·  Supply Point Optimization\n"
             "Optimal placement of 3 supply points (G fixed)",
             run_f4),
            ("F5  Deployment",
             "BFS  ·  Resource Deployment\n"
             "Deploy emergency units from staging areas to sites",
             run_f5),
        ]
        for name, desc, func in algo_tabs:
            frame = tk.Frame(self._nb, bg=BG)
            self._nb.add(frame, text=f"  {name}  ")
            btn = self._build_tab(frame, desc, func)
            self._tab_buttons.append((btn, func))

    # ── B1/B2 special tab ─────────────────────────────────────────────────────
    def _build_b1b2_tab(self, parent):
        # Controls bar
        ctrl = tk.Frame(parent, bg=SURFACE, pady=8, padx=12)
        ctrl.pack(fill=tk.X)

        tk.Label(ctrl, text="B1/B2 — Data Structure Explorer",
                 font=("Helvetica", 11, "bold"),
                 bg=SURFACE, fg=TEAL).pack(side=tk.LEFT, padx=(0,16))

        # Graph type selector
        tk.Label(ctrl, text="Graph type:", bg=SURFACE, fg=SUBTEXT,
                 font=("Helvetica", 10)).pack(side=tk.LEFT)
        graph_var = tk.StringVar(value="undirected_weighted")
        graph_menu = ttk.Combobox(
            ctrl, textvariable=graph_var, width=22, state="readonly",
            values=["undirected_weighted", "undirected_unweighted",
                    "directed_weighted",   "directed_unweighted"],
        )
        graph_menu.pack(side=tk.LEFT, padx=(4, 16))

        # Toggle options
        imp_var  = tk.BooleanVar(value=True)
        wway_var = tk.BooleanVar(value=True)
        pts_var  = tk.BooleanVar(value=True)

        def _chk(text, var):
            cb = tk.Checkbutton(ctrl, text=text, variable=var,
                                bg=SURFACE, fg=TEXT, selectcolor=SURFACE0,
                                activebackground=SURFACE, activeforeground=TEXT,
                                font=("Helvetica", 10))
            cb.pack(side=tk.LEFT, padx=6)

        _chk("Mark F–E impassable", imp_var)
        _chk("Mark E–I waterway",   wway_var)
        _chk("Add important points", pts_var)

        run_btn = tk.Button(ctrl, text="▶  Run",
                            font=("Helvetica", 11, "bold"),
                            bg=BLUE, fg=BG, relief=tk.FLAT,
                            padx=14, pady=5, cursor="hand2",
                            activebackground=MAUVE, activeforeground=BG)
        run_btn.pack(side=tk.RIGHT, padx=6)

        # Paned content
        paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL,
                               bg=BG, sashwidth=5)
        paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        left = tk.Frame(paned, bg=SURFACE0)
        paned.add(left, minsize=280, width=340)
        tk.Label(left, text="Results", font=("Helvetica", 10, "bold"),
                 bg=SURFACE0, fg=SUBTEXT).pack(anchor=tk.W, padx=10, pady=(8,2))
        text_area = scrolledtext.ScrolledText(
            left, font=("Courier New", 10),
            bg=SURFACE0, fg=TEXT, insertbackground=TEXT,
            selectbackground=SURFACE, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED, wrap=tk.NONE,
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0,4))

        right = tk.Frame(paned, bg=SURFACE0)
        paned.add(right, minsize=500)
        placeholder = tk.Label(right, text="Click  ▶ Run  to visualize",
                                font=("Helvetica", 13), bg=SURFACE0, fg=OVERLAY)
        placeholder.pack(expand=True)

        status = tk.Label(parent, text="Ready", font=("Helvetica", 9),
                          bg=SURFACE, fg=SUBTEXT, anchor=tk.W, padx=12, pady=3)
        status.pack(fill=tk.X, side=tk.BOTTOM)

        canvas_ref  = {"canvas": None}
        toolbar_ref = {"toolbar": None}

        def _run():
            run_btn.configure(state=tk.DISABLED, text="Running…")
            status.configure(text="Building graph…", fg=YELLOW)
            self.update()

            gt   = graph_var.get()
            imp  = imp_var.get()
            wway = wway_var.get()
            pts  = pts_var.get()

            def worker():
                try:
                    fig, out = run_b1b2(gt, imp, wway, pts)
                    self.after(0, lambda: _done(fig, out))
                except Exception as exc:
                    self.after(0, lambda e=exc: _err(e))

            threading.Thread(target=worker, daemon=True).start()

        def _done(fig, out):
            text_area.configure(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, out)
            text_area.configure(state=tk.DISABLED)
            placeholder.pack_forget()
            _embed_figure(fig, right, canvas_ref, toolbar_ref)
            status.configure(text="Done", fg=GREEN)
            run_btn.configure(state=tk.NORMAL, text="▶  Run")

        def _err(exc):
            status.configure(text=f"Error: {exc}", fg=RED)
            run_btn.configure(state=tk.NORMAL, text="▶  Run")

        run_btn.configure(command=_run)

    # ── Generic algorithm tab ─────────────────────────────────────────────────
    def _build_tab(self, parent, description, func):
        # Top bar
        top = tk.Frame(parent, bg=SURFACE, pady=8, padx=12)
        top.pack(fill=tk.X)
        tk.Label(top, text=description, font=("Helvetica", 10),
                 bg=SURFACE, fg=GREEN, justify=tk.LEFT).pack(side=tk.LEFT)
        run_btn = tk.Button(top, text="▶  Run",
                            font=("Helvetica", 11, "bold"),
                            bg=BLUE, fg=BG, relief=tk.FLAT,
                            padx=14, pady=5, cursor="hand2",
                            activebackground=MAUVE, activeforeground=BG)
        run_btn.pack(side=tk.RIGHT, padx=6)

        # Paned content
        paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL,
                               bg=BG, sashwidth=5)
        paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        left = tk.Frame(paned, bg=SURFACE0)
        paned.add(left, minsize=280, width=320)
        tk.Label(left, text="Results", font=("Helvetica", 10, "bold"),
                 bg=SURFACE0, fg=SUBTEXT).pack(anchor=tk.W, padx=10, pady=(8,2))
        text_area = scrolledtext.ScrolledText(
            left, font=("Courier New", 10),
            bg=SURFACE0, fg=TEXT, insertbackground=TEXT,
            selectbackground=SURFACE, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED, wrap=tk.NONE,
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0,4))

        right = tk.Frame(paned, bg=SURFACE0)
        paned.add(right, minsize=500)
        placeholder = tk.Label(right, text="Click  ▶ Run  to visualize",
                                font=("Helvetica", 13), bg=SURFACE0, fg=OVERLAY)
        placeholder.pack(expand=True)

        status = tk.Label(parent, text="Ready", font=("Helvetica", 9),
                          bg=SURFACE, fg=SUBTEXT, anchor=tk.W, padx=12, pady=3)
        status.pack(fill=tk.X, side=tk.BOTTOM)

        canvas_ref  = {"canvas": None}
        toolbar_ref = {"toolbar": None}

        def _run():
            run_btn.configure(state=tk.DISABLED, text="Running…")
            status.configure(text="Running algorithm…", fg=YELLOW)
            self.update()

            def worker():
                try:
                    fig, out = func()
                    self.after(0, lambda: _done(fig, out))
                except Exception as exc:
                    self.after(0, lambda e=exc: _err(e))

            threading.Thread(target=worker, daemon=True).start()

        def _done(fig, out):
            text_area.configure(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, out)
            text_area.configure(state=tk.DISABLED)
            placeholder.pack_forget()
            _embed_figure(fig, right, canvas_ref, toolbar_ref)
            status.configure(text="Done", fg=GREEN)
            run_btn.configure(state=tk.NORMAL, text="▶  Run")

        def _err(exc):
            status.configure(text=f"Error: {exc}", fg=RED)
            run_btn.configure(state=tk.NORMAL, text="▶  Run")

        run_btn.configure(command=_run)
        return run_btn   # returned so Run All can trigger it

    # ── Run All ───────────────────────────────────────────────────────────────
    def _run_all(self):
        self._run_all_btn.configure(state=tk.DISABLED, text="Running…")

        def _chain(index):
            if index >= len(self._tab_buttons):
                self._run_all_btn.configure(state=tk.NORMAL, text="▶▶  Run All")
                return
            btn, _ = self._tab_buttons[index]
            # Switch to the tab so the user can see progress
            tab_index = index + 1          # +1 because B1/B2 is tab 0
            self._nb.select(tab_index)
            btn.invoke()
            # Wait for this tab to finish (poll its text), then continue
            self.after(200, lambda: _wait(index))

        def _wait(index):
            btn, _ = self._tab_buttons[index]
            if btn.cget("state") == "disabled":
                self.after(300, lambda: _wait(index))
            else:
                self.after(100, lambda: _chain(index + 1))

        _chain(0)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
