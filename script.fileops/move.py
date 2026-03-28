import os
import shutil
import xbmc
import xbmcgui
import xbmcvfs

from common import get_asset_path, get_target_path, localized_string


def move_file(path: str, dest_dir: str) -> bool:
    """Move a file to a destination directory."""
    if not xbmcvfs.exists(path):
        return False

    filename = os.path.basename(path)
    dest_path = os.path.join(dest_dir, filename)

    try:
        shutil.move(path, dest_path)
        return True
    except Exception as exc:
        xbmc.log(
            f"script.delete: error moving file {path}: {exc}", xbmc.LOGERROR)
        return False


def main() -> None:
    path = get_target_path()
    if not path:
        xbmcgui.Dialog().notification(
            localized_string(32041),
            localized_string(32042, ""),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        return

    filename = os.path.basename(path)
    if not filename:
        filename = path

    # Browse for destination directory
    dest_dir = xbmcgui.Dialog().browseSingle(
        type=0,  # Directory
        heading=localized_string(32038),
        shares="files",
        mask="",
        useThumbs=False,
        treatAsFolder=True,
        defaultt=""
    )

    if not dest_dir:
        return

    try:
        was_moved = move_file(path, dest_dir)
        if was_moved:
            xbmcgui.Dialog().notification(
                localized_string(32039),
                localized_string(32040, filename),
                icon=get_asset_path("icon.png"),
                time=5000,
            )
            # Refresh the current container to update the file list
            xbmc.executebuiltin("Container.Refresh")
        else:
            raise OSError("Move failed")

    except Exception as exc:
        xbmc.log(
            f"script.delete: error moving file {path}: {exc}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            localized_string(32041),
            localized_string(32042, filename),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )


if __name__ == "__main__":
    main()