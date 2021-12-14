from typing import List, Tuple, Dict, NewType

from lib.patched_instagram_web_api import PatchedClient as WebClient  # Metrics
from instagram_private_api import Client as AppClient, MediaTypes  # Actions

import os

from dotenv import load_dotenv
load_dotenv()

#region Types
SpacerAction = NewType('SpacerAction', str)
MediaID = NewType('MediaID', str)
#endregion

def rateUsage(*, weight: int):
    if not hasattr(rateUsage, 'weightCount'):
        rateUsage.weightCount = 0

    def decorator(func):
        def wrapper(*args, **kwargs):
            rateUsage.weightCount += weight
            return func(*args, **kwargs)
        return wrapper
    return decorator


@rateUsage(weight=1)
def getFeedCount() -> int:
    """Gets the number of items in the authenticated user's feed

    # GET https://graph.instagram.com/{user-id}/?fields=media_count&access_token={access-token}

    Returns:
        int: Feed count
    """

    global web_api

    username = os.getenv('IG_USERNAME')
    # if authenticated ------ web_api.timeline_feed()['data']['user']['username']
    return web_api.user_info2(username)['counts']['media']


def getSpacers() -> Dict[MediaID, bool]:
    """Gets the visibility of the spacers

    # GET https://graph.instagram.com/{media-id}?fields=caption&access_token={access-token}

    Returns:
        List[str]: IDs of the visible spacers
    """

    global web_api

    result = dict()

    @rateUsage(weight=1)
    def getMediaInfo(shortCode):
        obj = app_api.media_info(mediaID)
        if obj["items"][0].get("visibility", None) == "only_me":
            raise Exception("Hidden")
        return obj

        # No longer works
        # return web_api.media_info2(shortCode)

    for shortCode, mediaID in map(lambda s: s.strip().split(":"), os.getenv("SPACERS").strip().split(",")):
        try:
            getMediaInfo(shortCode)
            result[mediaID] = True  # result[r['id']] = True
        except:
            result[mediaID] = False

    return result


def calculateAction() -> List[Tuple[SpacerAction, MediaID]]:
    spacers = getSpacers()

    def getSpacersByVisibility(visibility: bool):
        return dict(filter(lambda o: o[1] == visibility, spacers.items()))

    visibleSpacers = getSpacersByVisibility(True)
    invisibleSpacers = getSpacersByVisibility(False)

    posts = getFeedCount()
    realPosts = posts - len(visibleSpacers)

    print(
        f"Currently has {realPosts} posts, and {len(visibleSpacers)} visible spacers")

    posts = getFeedCount()
    if posts % 3 == 0:
        return []

    reqSpacers = (3 - (realPosts % 3)) % 3

    if reqSpacers == len(visibleSpacers):
        return []

    if reqSpacers > len(visibleSpacers):
        return [('show', [*invisibleSpacers.keys()][i]) for i in range(reqSpacers - len(visibleSpacers))]
    else:
        return [('hide', [*visibleSpacers.keys()][i]) for i in range(len(visibleSpacers) - reqSpacers)]


if __name__ == "__main__":

    commonSettings = dict(
        drop_incompat_keys=False,
        auto_patch=True,
    )
    import pickle

    #region Web API
    web_api_session = None
    try:
        with open(".webAPI.session", "rb") as f:
            web_api_session = pickle.load(f)
        print("Found existing web api session")
    except:
        pass

    web_api = None

    if web_api_session is not None:
        try:
            web_api = WebClient(
                **commonSettings, cookie=web_api_session["cookie"], settings=web_api_session)
            print("Using existing web api session")
        except:
            print("Web API session likely expired, renewing")

    if web_api is None:
        web_api = WebClient(**commonSettings, authenticate=True,
                            username=os.getenv('IG_USERNAME'), password=os.getenv('IG_PASSWORD'))
        # The onLoad parameter from Client only is called after a login, not a session resumption
        with open(".webAPI.session", "wb") as f:
            pickle.dump(web_api.settings, f)
        print("Successfully authenticated to the web api")

    #endregion

    #region App API

    app_api_session = None
    try:
        with open(".appAPI.session", "rb") as f:
            app_api_session = pickle.load(f)
        print("Found existing app api session")

    except:
        pass

    app_api = None

    if app_api_session is not None:
        try:
            app_api = AppClient(os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'), **commonSettings, cookie=app_api_session["cookie"], settings=app_api_session)
            print("Using existing app api session")
        except:
            print("App API session likely expired, renewing")

    if app_api is None:
        app_api = AppClient(os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'), **commonSettings)
        with open(".appAPI.session", "wb") as f:
            pickle.dump(app_api.settings, f)
        print("Successfully authenticated to the app api")
    #endregion

    actions = calculateAction()
    if len(actions) == 0:
        exit()

    @rateUsage(weight=1)
    def setArchived(mediaID, status):
        return app_api.media_only_me(mediaID, MediaTypes.PHOTO, not status)

    for (action, spacerID) in actions:
        print(action, spacerID)
        setArchived(spacerID, action == 'hide')
        
    if hasattr(rateUsage, 'weightCount'):
        print("API Call Usage:", rateUsage.weightCount)
