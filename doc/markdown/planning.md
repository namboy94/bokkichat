# Planning

Basic Idea:

```python
settings = TelegramSetting(username="username", password="password")
connection = TelegramConnection(settings)

msg = TextMessage(to="address", body="Hello World")

connection.send(msg)
```

Support looping:

```python
connection.loop(lambda conn, msg: do_stuff(conn, msg))
```