from __future__ import annotations

import argparse
import math
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


DEFAULT_OUTPUT_NAME = "mermaid_diagram.pdf"
TOKEN_RE = re.compile(r"\s*(?:(-\.->|-->)|(\|[^|]+\|)|([A-Za-z0-9_]+(?:\[[^\]]*\])?))")
NODE_RE = re.compile(r"^([A-Za-z0-9_]+)(?:\[(.*)\])?$")
BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
PALETTE = ["#DBEAFE", "#E0F2FE", "#DCFCE7", "#FDE68A", "#FBCFE8", "#E9D5FF", "#CFFAFE"]


@dataclass
class Node:
    node_id: str
    label: str
    order: int


@dataclass
class Edge:
    source: str
    target: str
    dashed: bool = False
    label: str = ""


@dataclass
class Diagram:
    direction: str
    nodes: dict[str, Node]
    edges: list[Edge]


@dataclass
class RenderNode:
    node_id: str
    x: float
    y: float
    width: float
    height: float
    title_lines: list[str]
    subtitle_lines: list[str]
    fill: str


def normalize_label(raw: str | None) -> str:
    if not raw:
        return ""
    text = BREAK_RE.sub("\n", raw)
    text = text.replace("&nbsp;", " ")
    text = text.replace("\\n", "\n")
    return "\n".join(part.strip() for part in text.splitlines() if part.strip())


def parse_node_token(token: str) -> tuple[str, str]:
    match = NODE_RE.fullmatch(token.strip())
    if not match:
        raise ValueError(f"Unsupported Mermaid node token: {token}")
    node_id = match.group(1)
    label = normalize_label(match.group(2)) or node_id
    return node_id, label


def tokenize_line(line: str) -> list[tuple[str, str]]:
    clean_line = line.strip().rstrip(";")
    tokens: list[tuple[str, str]] = []
    pos = 0
    while pos < len(clean_line):
        match = TOKEN_RE.match(clean_line, pos)
        if not match:
            raise ValueError(f"Could not parse Mermaid line: {line}")
        edge_token, label_token, node_token = match.groups()
        if edge_token:
            tokens.append(("edge", edge_token))
        elif label_token:
            tokens.append(("label", label_token[1:-1].strip()))
        elif node_token:
            tokens.append(("node", node_token))
        pos = match.end()
    return tokens


def upsert_node(nodes: dict[str, Node], node_id: str, label: str, order_counter: list[int]) -> None:
    if node_id in nodes:
        if label and nodes[node_id].label == node_id:
            nodes[node_id].label = label
        return
    nodes[node_id] = Node(node_id=node_id, label=label or node_id, order=order_counter[0])
    order_counter[0] += 1


def parse_mermaid(text: str) -> Diagram:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("No Mermaid text provided")

    header = lines[0].strip()
    if not header.lower().startswith("graph "):
        raise ValueError("Mermaid text must start with 'graph TD' or similar")

    parts = header.split()
    direction = parts[1].upper() if len(parts) > 1 else "TD"
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    order_counter = [0]

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("%%"):
            continue

        tokens = tokenize_line(stripped)
        if not tokens or tokens[0][0] != "node":
            continue

        current_id, current_label = parse_node_token(tokens[0][1])
        upsert_node(nodes, current_id, current_label, order_counter)

        idx = 1
        while idx < len(tokens):
            token_type, token_value = tokens[idx]
            if token_type != "edge":
                raise ValueError(f"Expected edge token in line: {line}")
            dashed = token_value == "-.->"
            idx += 1

            edge_label = ""
            if idx < len(tokens) and tokens[idx][0] == "label":
                edge_label = tokens[idx][1]
                idx += 1

            if idx >= len(tokens) or tokens[idx][0] != "node":
                raise ValueError(f"Expected destination node in line: {line}")

            target_id, target_label = parse_node_token(tokens[idx][1])
            existing = nodes.get(target_id)
            if existing and existing.label and existing.label != target_label and not edge_label:
                edge_label = target_label
            else:
                upsert_node(nodes, target_id, target_label, order_counter)

            edges.append(Edge(source=current_id, target=target_id, dashed=dashed, label=edge_label))
            current_id = target_id
            idx += 1

    if not nodes:
        raise ValueError("No nodes could be parsed from the Mermaid text")

    return Diagram(direction=direction, nodes=nodes, edges=edges)


def split_label(label: str) -> tuple[str, str]:
    lines = [line.strip() for line in label.splitlines() if line.strip()]
    if not lines:
        return "", ""
    return lines[0], "\n".join(lines[1:])


def estimate_node_size(node: Node) -> tuple[float, float, list[str], list[str]]:
    title, subtitle = split_label(node.label)
    title_lines = title.splitlines() if title else [node.node_id]
    subtitle_lines = subtitle.splitlines() if subtitle else []
    all_lines = title_lines + subtitle_lines or [node.node_id]
    max_chars = max(len(line) for line in all_lines)
    width = min(max(36 * mm, 8 * mm + max_chars * 2.2), 72 * mm)
    height = 12 * mm + len(title_lines) * 4 * mm + len(subtitle_lines) * 3.6 * mm
    height = max(18 * mm, min(height, 32 * mm))
    return width, height, title_lines, subtitle_lines


def compute_levels(diagram: Diagram) -> dict[str, int]:
    solid_edges = [edge for edge in diagram.edges if not edge.dashed]
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {node_id: 0 for node_id in diagram.nodes}

    for edge in solid_edges:
        adjacency[edge.source].append(edge.target)
        indegree[edge.target] = indegree.get(edge.target, 0) + 1

    roots = sorted([node_id for node_id, value in indegree.items() if value == 0], key=lambda item: diagram.nodes[item].order)
    if not roots:
        roots = [min(diagram.nodes, key=lambda item: diagram.nodes[item].order)]

    queue = deque(roots)
    incoming_left = dict(indegree)
    depth = {node_id: 0 for node_id in roots}

    while queue:
        current = queue.popleft()
        for target in adjacency.get(current, []):
            candidate = depth[current] + 1
            depth[target] = max(depth.get(target, 0), candidate)
            incoming_left[target] -= 1
            if incoming_left[target] == 0:
                queue.append(target)

    for node_id in sorted(diagram.nodes, key=lambda item: diagram.nodes[item].order):
        depth.setdefault(node_id, 0)

    return depth


def layout_nodes(diagram: Diagram, page_width: float, page_height: float) -> dict[str, RenderNode]:
    levels = compute_levels(diagram)
    grouped: dict[int, list[str]] = defaultdict(list)
    for node_id, level in levels.items():
        grouped[level].append(node_id)

    for node_ids in grouped.values():
        node_ids.sort(key=lambda item: diagram.nodes[item].order)

    margins = {"left": 18 * mm, "right": 18 * mm, "top": 28 * mm, "bottom": 18 * mm}
    render_nodes: dict[str, RenderNode] = {}
    max_level = max(grouped)
    palette_len = len(PALETTE)
    sizes = {node_id: estimate_node_size(node) for node_id, node in diagram.nodes.items()}

    if diagram.direction == "LR":
        level_widths = {level: max(sizes[node_id][0] for node_id in node_ids) for level, node_ids in grouped.items()}
        available_width = page_width - margins["left"] - margins["right"]
        gap_x = 14 * mm if max_level == 0 else max(10 * mm, (available_width - sum(level_widths.values())) / max(max_level, 1))
        current_x = margins["left"]
        for level in range(max_level + 1):
            node_ids = grouped.get(level, [])
            if not node_ids:
                current_x += gap_x
                continue
            total_height = sum(sizes[node_id][1] for node_id in node_ids) + (len(node_ids) - 1) * 10 * mm
            current_y = page_height - margins["top"] - total_height
            for node_id in node_ids:
                width, height, title_lines, subtitle_lines = sizes[node_id]
                render_nodes[node_id] = RenderNode(
                    node_id=node_id,
                    x=current_x + (level_widths[level] - width) / 2,
                    y=current_y,
                    width=width,
                    height=height,
                    title_lines=title_lines,
                    subtitle_lines=subtitle_lines,
                    fill=PALETTE[level % palette_len],
                )
                current_y += height + 10 * mm
            current_x += level_widths[level] + gap_x
    else:
        level_heights = {level: max(sizes[node_id][1] for node_id in node_ids) for level, node_ids in grouped.items()}
        available_height = page_height - margins["top"] - margins["bottom"]
        gap_y = 14 * mm if max_level == 0 else max(8 * mm, (available_height - sum(level_heights.values())) / max(max_level, 1))
        current_top = page_height - margins["top"]
        for level in range(max_level + 1):
            node_ids = grouped.get(level, [])
            if not node_ids:
                current_top -= gap_y
                continue
            total_width = sum(sizes[node_id][0] for node_id in node_ids) + (len(node_ids) - 1) * 10 * mm
            current_x = max(margins["left"], (page_width - total_width) / 2)
            row_y = current_top - level_heights[level]
            for node_id in node_ids:
                width, height, title_lines, subtitle_lines = sizes[node_id]
                render_nodes[node_id] = RenderNode(
                    node_id=node_id,
                    x=current_x,
                    y=row_y + (level_heights[level] - height) / 2,
                    width=width,
                    height=height,
                    title_lines=title_lines,
                    subtitle_lines=subtitle_lines,
                    fill=PALETTE[level % palette_len],
                )
                current_x += width + 10 * mm
            current_top = row_y - gap_y

    return render_nodes


def draw_box(pdf: canvas.Canvas, node: RenderNode) -> None:
    pdf.setFillColor(colors.HexColor(node.fill))
    pdf.setStrokeColor(colors.HexColor("#334155"))
    pdf.roundRect(node.x, node.y, node.width, node.height, 4 * mm, fill=1, stroke=1)

    text_y = node.y + node.height - 5 * mm
    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.setFont("Helvetica-Bold", 9)
    for line in node.title_lines[:2]:
        wrapped = simpleSplit(line, "Helvetica-Bold", 9, node.width - 6 * mm)
        for item in wrapped[:2]:
            pdf.drawCentredString(node.x + node.width / 2, text_y, item)
            text_y -= 4 * mm

    if node.subtitle_lines:
        pdf.setFillColor(colors.HexColor("#334155"))
        pdf.setFont("Helvetica", 8)
        for line in node.subtitle_lines[:3]:
            wrapped = simpleSplit(line, "Helvetica", 8, node.width - 6 * mm)
            for item in wrapped[:2]:
                pdf.drawCentredString(node.x + node.width / 2, text_y, item)
                text_y -= 3.6 * mm


def anchor_points(source: RenderNode, target: RenderNode) -> tuple[tuple[float, float], tuple[float, float]]:
    source_center_x = source.x + source.width / 2
    source_center_y = source.y + source.height / 2
    target_center_x = target.x + target.width / 2
    target_center_y = target.y + target.height / 2
    dx = target_center_x - source_center_x
    dy = target_center_y - source_center_y

    if abs(dx) > abs(dy):
        if dx >= 0:
            start = (source.x + source.width, source_center_y)
            end = (target.x, target_center_y)
        else:
            start = (source.x, source_center_y)
            end = (target.x + target.width, target_center_y)
    else:
        if dy >= 0:
            start = (source_center_x, source.y)
            end = (target_center_x, target.y + target.height)
        else:
            start = (source_center_x, source.y + source.height)
            end = (target_center_x, target.y)
    return start, end


def draw_arrow(pdf: canvas.Canvas, start: tuple[float, float], end: tuple[float, float], dashed: bool = False) -> None:
    x1, y1 = start
    x2, y2 = end

    pdf.saveState()
    pdf.setStrokeColor(colors.HexColor("#475569"))
    pdf.setLineWidth(1.6)
    if dashed:
        pdf.setDash(5, 3)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()

    angle = math.atan2(y2 - y1, x2 - x1)
    head_length = 4 * mm
    head_angle = math.pi / 7
    x3 = x2 - head_length * math.cos(angle - head_angle)
    y3 = y2 - head_length * math.sin(angle - head_angle)
    x4 = x2 - head_length * math.cos(angle + head_angle)
    y4 = y2 - head_length * math.sin(angle + head_angle)

    pdf.setStrokeColor(colors.HexColor("#475569"))
    pdf.line(x2, y2, x3, y3)
    pdf.line(x2, y2, x4, y4)


def draw_edge_label(pdf: canvas.Canvas, label: str, start: tuple[float, float], end: tuple[float, float]) -> None:
    if not label:
        return
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    width = max(18 * mm, min(44 * mm, len(label) * 2.4))
    height = 7 * mm

    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(colors.HexColor("#CBD5E1"))
    pdf.roundRect(mid_x - width / 2, mid_y - height / 2, width, height, 2 * mm, fill=1, stroke=1)
    pdf.setFillColor(colors.HexColor("#334155"))
    pdf.setFont("Helvetica", 7)
    pdf.drawCentredString(mid_x, mid_y - 1.2, label)


def build_pdf(diagram: Diagram, output_path: Path, title: str) -> Path:
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(str(output_path), pagesize=(page_width, page_height))
    pdf.setTitle(title)

    pdf.setFillColor(colors.HexColor("#F7FAFC"))
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(18 * mm, page_height - 16 * mm, title)
    pdf.setFillColor(colors.HexColor("#475569"))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(18 * mm, page_height - 23 * mm, "VINOL Enterprices")

    render_nodes = layout_nodes(diagram, page_width, page_height)

    for edge in diagram.edges:
        source = render_nodes[edge.source]
        target = render_nodes[edge.target]
        start, end = anchor_points(source, target)
        draw_arrow(pdf, start, end, dashed=edge.dashed)
        draw_edge_label(pdf, edge.label, start, end)

    for node in render_nodes.values():
        draw_box(pdf, node)

    legend_x = 18 * mm
    legend_y = 14 * mm
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.drawString(legend_x, legend_y + 10 * mm, "Legend")
    pdf.setLineWidth(1.6)
    pdf.setStrokeColor(colors.HexColor("#475569"))
    pdf.line(legend_x, legend_y + 5 * mm, legend_x + 18 * mm, legend_y + 5 * mm)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(legend_x + 22 * mm, legend_y + 3.5 * mm, "Primary flow")
    pdf.saveState()
    pdf.setDash(5, 3)
    pdf.line(legend_x, legend_y, legend_x + 18 * mm, legend_y)
    pdf.restoreState()
    pdf.drawString(legend_x + 22 * mm, legend_y - 1.5 * mm, "Dashed flow / backup path")

    pdf.showPage()
    pdf.save()
    return output_path


def read_mermaid_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.input:
        return Path(args.input).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    if args.clipboard:
        return read_mermaid_from_clipboard()
    raise ValueError("Provide Mermaid text with --text, an input file path, stdin, or --clipboard")


def read_mermaid_from_clipboard() -> str:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    try:
        text = root.clipboard_get()
    finally:
        root.destroy()

    text = str(text or "").strip()
    if not text:
        raise ValueError("Clipboard is empty")
    return text


def derive_output_path(project_root: Path, args: argparse.Namespace) -> Path:
    if args.output:
        output_path = Path(args.output)
        return output_path if output_path.is_absolute() else project_root / output_path
    if args.input:
        return project_root / f"{Path(args.input).stem}.pdf"
    return project_root / DEFAULT_OUTPUT_NAME


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Mermaid graph text into a readable PDF layout")
    parser.add_argument("input", nargs="?", help="Path to a Mermaid text file")
    parser.add_argument("-o", "--output", help="Output PDF path")
    parser.add_argument("--text", help="Raw Mermaid text passed directly on the command line")
    parser.add_argument("--clipboard", action="store_true", help="Read Mermaid text from the system clipboard")
    parser.add_argument("--title", default="Mermaid Diagram", help="Title to show in the PDF")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    mermaid_text = read_mermaid_text(args)
    diagram = parse_mermaid(mermaid_text)

    project_root = Path(__file__).resolve().parents[1]
    output_path = derive_output_path(project_root, args)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        created_path = build_pdf(diagram, output_path, args.title)
    except PermissionError:
        fallback_name = f"{output_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{output_path.suffix}"
        created_path = build_pdf(diagram, output_path.with_name(fallback_name), args.title)

    print(f"Created: {created_path}")


if __name__ == "__main__":
    main()