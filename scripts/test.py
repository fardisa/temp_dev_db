from dev_db_client.user import User, Json

# user = User.create_user("prmpsmart")
user = Json()

api_key = "12e0155845388f1dd8d643ddd7485bce5c63155982508ed914c6393c6113d2c3"

if user.api_key:
    api_key = user.api_key

print(user.api_key)
user = User(
    identifier="prmpsmart",
    api_key=api_key,
)

# print(user.get_user())
# print(user.create_database("database_1"))
# print(user.delete_database("database_1"))

print(user.set_data("database_1/path", {"op": 90}))
# print(user.set_data("database_1/path", "op"))
print(user.get_data("database_1/path"))


# print(user.delete_data("database_1/path"))
# print(user.get_data("database_1/path"))


# print(User.get_users("Prmpsmart7625#"))
