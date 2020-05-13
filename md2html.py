from os import listdir
from os.path import isfile, join, exists
import subprocess
import markdown
# markdown-3.2.2
paths = ["./docs/users", "./docs/apis", "./docs/arch"]
for p in paths:
    files = [f for f in listdir(p) if isfile(join(p, f))]
    for i in files:
        with open(p+"/"+i) as f:
            html = markdown.markdown(f.read())
            f.close()
            subprocess.run(["rm", p+"/"+i.split(".md")[0].split(".html")[0]+".html"])
            # with open(p+"/"+i.split(".md")[0].split(".html")[0]+".html", "w+") as c:
            #     c.write(html)

