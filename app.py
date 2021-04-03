import instagram_web_api  # Metrics
import instagram_private_api  # Actions
from dotenv import load_dotenv
import os
load_dotenv()


# web_api = Client(auto_patch=True, drop_incompat_keys=False)
# user_feed_info = web_api.user_feed('329452045', count=10)
# for post in user_feed_info:
#     print('%s from %s' % (post['link'], post['user']['username']))
webClient = instagram_web_api.Client(
    auto_patch=True, authenticate=True,
    username=os.getenv('IG_USERNAME'), password=os.getenv('IG_PASSWORD'))
print(webClient, dir(webClient))
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
