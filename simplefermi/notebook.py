import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import re
import sys
import functools
import parser

app = Flask(__name__)
socketio = SocketIO(app)

eprint = functools.partial(print, file=sys.stderr)

environments = (
    "align",
    "align*",
    "alignat",
    "alignat*",
    "aligned",
    "alignedat",
    "array",
    "bmatrix",
    "Bmatrix",
    "bmatrix*",
    "Bmatrix*",
    "bsmallmatrix",
    "Bsmallmatrix",
    "bsmallmatrix*",
    "Bsmallmatrix*",
    "cases",
    "cases*",
    "CD",
    "crampedsubarray",
    "dcases",
    "dcases*",
    "drcases",
    "drcases*",
    "empheq",
    "eqnarray",
    "eqnarray*",
    "equation",
    "equation*",
    "flalign",
    "flalign*",
    "gather",
    "gather*",
    "gathered",
    "lgathered",
    "matrix",
    "matrix*",
    "multline",
    "multline*",
    "multlined",
    "numcases",
    "pmatrix",
    "pmatrix*",
    "prooftree",
    "psmallmatrix",
    "psmallmatrix*",
    "rcases",
    "rcases*",
    "rgathered",
    "smallmatrix",
    "smallmatrix*",
    "split",
    "spreadlines",
    "subarray",
    "subnumcases",
    "vmatrix",
    "Vmatrix",
    "vmatrix*",
    "Vmatrix*",
    "vsmallmatrix",
    "Vsmallmatrix",
    "vsmallmatrix*",
    "Vsmallmatrix*",
    "xalignat",
    "xalignat*",
    "xxalignat",
)

block_math_patterns = [
    re.compile(r"(\$\$.*?\$\$)", re.DOTALL),
    re.compile(r"(\\\[.*?\\\])", re.DOTALL),
] + [
    re.compile(r"(\\begin\{" + word + r"\}.*?\\end\{" + word + r"\})", re.DOTALL)
    for word in environments
]


def preprocess_math(s):
    for patt in block_math_patterns:
        s = patt.sub(r"<p class='math'>\1</p>", s)
    return s


class FermiExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # TODO: Implement Fermi language parsing and execution
        pass


FERMI_BLOCK = re.compile(r"(```fermi\n(.*?)(?<=\n)```($|\n))", re.DOTALL)


def preprocess_fermi(s):
    def subfn(match):
        full = match.group(0)
        fermi_code = match.group(1)
        out = str(parser.parse(fermi_code))
        return f"{full}\n<div class='fermiout'>{out}</div>"

    return FERMI_BLOCK.sub(subfn, s)


class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            eprint(f"Updating {event.src_path}...")
            with open(event.src_path, "r") as f:
                content = f.read()
                content = preprocess_math(content)
                content = preprocess_fermi(content)
            html = markdown.markdown(
                content, extensions=[FermiExtension(), "codehilite", "fenced_code"]
            )
            socketio.emit("update", {"html": html})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    path = "."  # Path to watch
    event_handler = MarkdownHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        socketio.run(app)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
