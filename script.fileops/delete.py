import os
import xbmc
import xbmcgui
import xbmcvfs
from pathlib import Path

from common import get_asset_path, get_target_path, localized_string


def delete_file(path: str) -> bool:
    """Delete a file if it exists and is not a directory."""
    if not xbmcvfs.exists(path):
        return False

    # Ensure it's a file, not a directory
    if not Path(path).is_file():
        return False

    try:
        return xbmcvfs.delete(path)
    except Exception as exc:
        xbmc.log(
            f"script.delete: xbmcvfs.delete failed for {path}: {exc}, trying os.remove", xbmc.LOGERROR)


def main() -> None:

    path = get_target_path()
    if not path:
        xbmcgui.Dialog().notification(
            localized_string(32025),
            localized_string(32026, ""),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        return

    filename = os.path.basename(path)
    if not filename:
        filename = path

    question = localized_string(32022, filename)
    confirmed = xbmcgui.Dialog().yesno(
        localized_string(32021),
        question,
        nolabel=localized_string(32027),
        yeslabel=localized_string(32028),
    )

    if not confirmed:
        return

    try:
        was_deleted = delete_file(path)
        if was_deleted:
            xbmcgui.Dialog().notification(
                localized_string(32023),
                localized_string(32024, filename),
                icon=get_asset_path("icon.png"),
                time=5000,
            )
            # Refresh the current container to update the file list
            xbmc.executebuiltin("Container.Refresh")
        else:
            raise OSError("Delete failed")

    except Exception as exc:
        xbmc.log(
            f"script.delete: error deleting file {path}: {exc}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            localized_string(32025),
            localized_string(32026, filename),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )


if __name__ == "__main__":
    main()
