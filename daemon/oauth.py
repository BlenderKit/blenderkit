"""OAuth for login."""

import typing
import uuid

import globals
import tasks
from aiohttp import client_exceptions, web


async def get_tokens(request: web.Request, auth_code=None, refresh_token=None, grant_type="authorization_code") -> typing.Tuple[dict, int, str|Exception]:
  server_url = "https://www.blenderkit.com"
  data = {
    "grant_type": grant_type,
    "state": "random_state_string",
    "client_id": globals.OAUTH_CLIENT_ID,
    "scopes": "read write",
    "redirect_uri" : f"http://localhost:{globals.PORT}/consumer/exchange/",
  }

  if auth_code:
    data['code'] = auth_code
  if refresh_token:
    data['refresh_token'] = refresh_token

  session = request.app['SESSION_API_REQUESTS']
  try:
    async with session.post(f"{server_url}/o/token/", data = data) as response:
      await response.text()

      if response.status != 200:
        return None, response.status, response.text

      response_json = await response.json()
      print("Token retrieval OK.")

      return response_json, 200, None

  except client_exceptions.ClientConnectorError as err:
    return None, -1, err


async def refresh_tokens(request: web.Request):
  data = await request.json()
  refresh_token = data["refresh_token"]
  response_json, status, error = await get_tokens(request, refresh_token=refresh_token, grant_type="refresh_token")
  
  for app_id in globals.active_apps:
    task = tasks.Task(None, str(uuid.uuid4()), app_id, 'login', message='Refreshing tokens')
    globals.tasks.append(task)
    task.result = response_json
    if status == 200:
      return task.finished("Refreshed tokens obtained")
    if status == -1:
      return task.error(f"Couldn't refresh API tokens, server is not reachable: {error}. Please login again.")
    
    return task.error(f"Couldn't refresh API tokens ({status}). Please login again.")
