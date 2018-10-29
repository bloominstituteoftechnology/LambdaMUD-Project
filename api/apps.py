from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'


# i don't know if this is where it goes
import pusher

pusher_client = pusher.Pusher(
  app_id='634597',
  key='4830aec0ca635aa67084',
  secret='f6e93311137ccd4173c9',
  cluster='us2',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})