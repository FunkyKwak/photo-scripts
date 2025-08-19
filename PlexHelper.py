
iter_photos = 0
iter_clips = 0



def iter_all_media(library):
    """Walk all albums in a library and yield all photos + clips"""
    for album in library.all():
        yield from walk_album(album)


def walk_album(album):
    """Recursively walk an album and yield photos & clips"""

    global iter_photos
    if iter_photos % 1000 == 0:
        print(f"...{iter_photos} photos walked...")
    global iter_clips
    if iter_clips % 1000 == 0:
        print(f"...{iter_clips} photos walked...")

    # Photos in this album
    for photo in album.photos():
        iter_photos = iter_photos + 1
        yield photo

    # Video clips in this album
    for clip in album.clips():
        iter_clips = iter_clips + 1
        yield clip

    # Recurse into sub-albums
    for sub in album.albums():
        yield from walk_album(sub)

def get_file_path(item):
    filePath = item.media[0].parts[0].file
    filePath = filePath.replace("/storage/[REDACTED]/photo/", "Z:\\")
    filePath = filePath.replace("/", "\\")
    return filePath