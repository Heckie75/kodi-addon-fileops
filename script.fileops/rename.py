import os
import xbmc
import xbmcgui
import xbmcvfs

from common import get_asset_path, get_target_path, localized_string


def rename_file(path: str, new_name: str) -> bool:
    """Rename a file if it exists and is not a directory."""
    if not xbmcvfs.exists(path):
        return False

    dir_path = os.path.dirname(path.rstrip(os.sep))
    new_path = os.path.join(dir_path, new_name)

    xbmc.log(
        f"script.delete: renaming file {path} to {new_path} using xbmcvfs.rename", xbmc.LOGINFO)

    try:
        return xbmcvfs.rename(path, new_path)
    except Exception as exc:
        xbmc.log(
            f"script.delete: xbmcvfs.rename failed for {path}: {exc}, trying os.rename", xbmc.LOGERROR)


def main() -> None:

    path = get_target_path()
    if not path:
        xbmcgui.Dialog().notification(
            localized_string(32033),
            localized_string(32034, ""),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        return

    filename = os.path.basename(path.rstrip(os.sep))
    if not filename:
        filename = path

    new_name = xbmcgui.Dialog().input(
        localized_string(32030),
        filename,
        type=xbmcgui.INPUT_ALPHANUM
    )
    if not new_name or new_name == filename:
        return

    try:
        was_renamed = rename_file(path, new_name)
        if was_renamed:
            xbmcgui.Dialog().notification(
                localized_string(32031),
                localized_string(32032, filename),
                icon=get_asset_path("icon.png"),
                time=5000,
            )
            # Refresh the current container to update the file list
            xbmc.executebuiltin("Container.Refresh")
        else:
            raise OSError("Rename failed")

    except Exception as exc:
        xbmc.log(
            f"script.delete: error renaming file {path}: {exc}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            localized_string(32033),
            localized_string(32034, filename),
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )


if __name__ == "__main__":
    main()
