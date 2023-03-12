import argparse
import pathlib
import graphviz
import os


parser = argparse.ArgumentParser(description='Create images of dot diagrams. Need installed graphviz.')
parser.add_argument('-s', '--src', dest="src", type=pathlib.Path, help='Directory with .gv files to render', required=True)
parser.add_argument('-d', '--dst', dest="dst", type=pathlib.Path, help='Directory to render images', required=True)
parser.add_argument('-f', '--format', dest="format", type=str, help='Image format for dot', default="png")

args = parser.parse_args()

if not args.dst.exists():
    os.mkdir(args.dst)

files = pathlib.Path(args.src).glob('**/*.gv')
for file in files:
    print(f"Process {file.name}")
    source = graphviz.Source.from_file(file.name, directory=file.parent)
    source.render(directory=args.dst, format=args.format, cleanup=True)
