import re
import subprocess
import sys

viewers = [
    ("^https?://www\.youtube\.com/watch\?v=[0-z]+&.*$",["vlc", "-f"]),
    ("^https?://youtu.be/[0-z]+$", ["vlc", "-f"]),
]

def view(post, url=None):
    if url == None:
        url = post.url

    program = None

    for viewer in viewers:
        if re.match(viewer[0], url) is not None:
            program = viewer[1]
            program.append(url)
            break
    else:
        sys.stderr.write("INVALID URL\n")
        sys.stderr.write("{}\n\n".format(url))
        

    if program is not None:
        subprocess.run(program,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

