import _api as api
import json

res = api.color('light.roof', '#ff0000')
# res = api.get_state('light.roof')

print(json.dumps(res, indent=2))

# api.set_state('light.lamp', 'off')
