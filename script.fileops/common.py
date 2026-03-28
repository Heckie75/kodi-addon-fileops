import os
import xbmc
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon()


def get_target_path() -> str | None:
    """Get target path from context menu invocation."""
    return xbmc.getInfoLabel("ListItem.FileNameAndPath")


def localized_string(index: int, *args) -> str:
    text = addon.getLocalizedString(index)
    if args:
        try:
            text = text % args
        except Exception:
            pass
    return text


def get_asset_path(asset: str) -> str:

    return os.path.join(xbmcvfs.translatePath(addon.getAddonInfo('path')),
                        "resources",
                        "assets", asset)
