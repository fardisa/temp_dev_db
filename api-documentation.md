# Dev DB

Data can only be saved for 5 hours. This is where all the rough work was done.

> Access the Swagger UI on [Swagger UI](https://devdb-prmpsmart.b4a.run/docs) for full API documentation.

## Endpoints and HTTP Methods

- If error in the response is true, then the message and code is found in the error_response.
- All timestamps are in seconds.

- /create_user?identifier={identifier}
    - GET
        - response {
            message: User created successfully,
            identifier: new desired user identifier,
            api_key: server generated key, keep safe,
            code: created_user,
            error: bool,
        }
        - error_response
            - identifier_exists {
                message: given identifier already exists,
                code: identifier_exists,
            }
            - identifier_too_long {
                message: given identifier is too long, valid length for an identifier is 20,
                code: identifier_too_long,
            }

- /get_user
    - POST
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
        }
        - response {
            identifier: new desired user identifier,
            api_key: server generated key, keep safe,
            database_details: {
                database_name: {
                    name: name of the database,
                    description: description of the database,
                    created_timestamp: int,
                    expiration_timestamp: int,
                    remaining_timestamp: int,
                },
            }
        }
        - error_response {
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }
        }

- /create_database
    - POST
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
            name: name of the new database,
            description: description of database,
            created_timestamp: int,
            expiration_timestamp: int,
            remaining_timestamp: int,
        }
        - response {
            message: database created successfully,
            error: bool,
            code: created_database,
            name: new database name,
        }
        - error_response
            - database_already_exists {
                message: given name for database already exists,
                code: database_already_exists,
            }
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }

- /delete_database
    - POST
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
            database_name: name of the new database,
        }
        - response {
            message: database deleted successfully,
            code: deleted_database,
            error: bool,
            name: database name,
        }
        - error_response
            - database_non_exist {
                message: given identifier non exists,
                code: database_non_exist,
            }
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }

- /get_data
    - POST
        - to get a data
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
            path: database_name/child/another_child,
        }
        - response {
            message: path foun and data returned,
            code: get_made,
            error: bool,
            path: path to data,
            data: {},
            remaining_timestamp: int,
        }
        - error_response {
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }
            - invalid_path {
                message: provided path does not exist in database,
                code: invalid_path,
            }
        }

- /set_data
    - POST
        - to get a data
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
            path: database_name/child/another_child,
            data: data,
        }
        - response {
            path: path to data,
            remaining_timestamp: int,
            message: data set successfully,
            code: set_made,
            error:bool,
        }
        - error_response {
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }
            - invalid_path {
                message: provided path does not exist in database,
                code: invalid_path,
            }
        }

- /delete_data
    - POST
        - to delete a data
        - request {
            api_key: user's api_key,
            identifier: user's identifier,
            path: database_name/child/another_child,
        }
        - response {
            path: path to data,
            message: data deleted successfully,
            code: delete_made,
            error:bool,

        }
        - error_response {
            - invalid_identifier_or_api_key {
                message: provided identifier or api_key in path is invalid,
                code: invalid_identifier_or_api_key,
            }
            - invalid_path {
                message: provided path does not exist in database,
                code: invalid_path,
            }
        }