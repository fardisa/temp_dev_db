from dev_db_client.user import User


# user = User.create_user("prmpsmart")
# print(user)


user = User(
    identifier="prmpsmart",
    api_key="53f33499c33657d277f82939b790ed44d1d1c928a1e83e07cc46da1c424332fc",
)

# print(user.get_user())
print(user.create_database("database_1"))
# print(user.delete_database("database_1"))

# print(user.set_data("database_1/path", {"op": 90}))
# print(user.get_data("database_1"))

print(user.set_data("database_1/path", ' 90'))

print(user.delete_data("database_1/path"))
print(user.get_data("database_1/path"))
