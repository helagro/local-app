import _api as api
import json

res = api.color('light.lamp', '#ff0099')
# res = api.get_state('light.lamp')

print(json.dumps(res, indent=2))

# api.set_state('light.lamp', 'off')
