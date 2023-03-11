import os
import shutil
from threading import Thread

def create_session_dir():
    # Create session directory with current timestamp
    session_dir = os.path.join('/', 'shared', f"rec-{int(time.time())}")
    os.makedirs(session_dir)

    # Create GIF subdirectory
    gif_dir = os.path.join(session_dir, 'gif')
    os.makedirs(gif_dir)

    return session_dir, gif_dir

def delete_files(files_to_delete):
    # Delete JPEG files used to create each GIF in a separate thread
    def _delete_files(files):
        for file in files:
            os.remove(file)

    t = Thread(target=_delete_files, args=(files_to_delete,))
    t.start()

def delete_session_dir(session_dir):
    # Delete session directory and all its contents
    shutil.rmtree(session_dir)
