from os import listdir
from os.path import isfile, join
import subprocess

paths = ["./docs/users", "./docs/apis", "./docs/arch"]
for p in paths:
    files = [f for f in listdir(p) if isfile(join(p, f))]
    for i in files:
        subprocess.run(["md-to-html", "--input", p+"/"+i, "--output", p+"/"+i.split(".md")[0] + ".html"])
