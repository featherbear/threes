import instagram_web_api  # Metrics
import instagram_private_api  # Actions

import os

from dotenv import load_dotenv
load_dotenv()

from typing import List, Tuple, NewType

#region Types
SpacerAction = NewType('SpacerAction', str)
SpacerID = NewType('SpacerID', str)
#endregion


def getFeedCount() -> int:
    """Gets the number of items in the authenticated user's feed

    Returns:
        int: Feed count
    """
    # GET https://graph.instagram.com/{user-id}/?fields=media_count&access_token={access-token}

    return 0

def getSpacers() -> List[SpacerID]:
    """Gets the visible spacers

    Returns:
        List[str]: IDs of the visible spacers
    """
    # GET https://graph.instagram.com/{media-id}?fields=caption&access_token={access-token}
    return []

def calculateAction() -> List[Tuple[SpacerAction, SpacerID]]:
    posts = getFeedCount()
    postOffset = posts % 3

    spacers = getSpacers()
    spacerCount = len(spacers)
 
    if postOffset == 0:
        return []

    if spacerCount > 0:
        return [('hide', spacers[i]) for i in range(min(postOffset, spacerCount))]
    else: # postOffset > 0 and spacerCount == 0
        return [('show', spacers[i]) for i in range(3 - postOffset)]

def __main__():
    for (action, spacerID) in calculateAction():
        print(action, spacerID)

# web_api = Client(auto_patch=True, drop_incompat_keys=False)
# user_feed_info = web_api.user_feed('329452045', count=10)
# for post in user_feed_info:
#     print('%s from %s' % (post['link'], post['user']['username']))
# webClient = instagram_web_api.Client(
#     auto_patch=True, authenticate=True,
#     username=os.getenv('IG_USERNAME'), password=os.getenv('IG_PASSWORD'))
# print(webClient, dir(webClient))
# try:
#     api = instagram_private_api.Client(
#         os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'))
# except instagram_private_api.errors.ClientLoginError as e:
#     print("Bad username / password")
#     exit()

# print(api.authenticated_user_id)

# results = api.self_feed()
# print(results.keys())
# items = results.get('items', [])
# for item in items:
#     # Manually patch the entity to match the public api as closely as possible, optional
#     # To automatically patch entities, initialise the Client with auto_patch=True
#     ClientCompatPatch.media(item)
#     print(media['code'])
