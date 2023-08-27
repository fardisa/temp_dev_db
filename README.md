# dev_db: Temporary Dummy Database REST API Server

**dev_db** is a project designed to provide developers with a functional dummy database REST API server. This server enables developers to perform various database-related actions through its API endpoints. It's particularly useful during the development phase when developers want to test and experiment with REST API calls before integrating their final chosen database platform.

## Features

- **User Account Management:** Developers can create user accounts and receive API keys for authorization.
- **Database Management:** Users with valid API keys can create databases that remain active for 5 hours. After this period, the database will be automatically deleted.
- **Data Interaction:** Developers can interact with databases by retrieving and modifying data.

## Getting Started

To use **dev_db** in your project, follow these steps:

1. **User Account Creation:**  Make GET request to the the API [/create_user](https://devdb-prmpsmart.b4a.run/create_user) to create a user account and obtain an API key.
2. **Database Operations:** Use the provided API endpoints to create, delete, and interact with databases.
3. **Data Interaction:** Fetch and modify data within the databases.

## API Endpoints

Here are the main API endpoints provided by **dev_db**:

- `GET /create_user?identifier={identifier}`: Create a user account and receive an API key for authorization.
- `POST /delete_user`: Delete a user account.
- `POST /get_user`: Get the details of a user account.
- `POST /create_database`: Create a new database using a valid API key.
- `POST /delete_database`: Delete a database by providing its ID and a valid API key.
- `POST /get_data`: Retrieve data from a specific database of the user using a valid API key.
- `POST /set_data`: Modify data within a specific database of the user using a valid API key.
- `POST /delete_data`: Delete data within a specific database of the user using a valid API key.

For detailed usage instructions and examples for each endpoint, refer to the [API Documentation](api-documentation.md) file.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow the guidelines outlined in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, feel free to contact me at [prmpsmart@gmail.com](mailto:prmpsmart@gmail.com).
