## URL Shortener Application
This simple URL shortening application is built using Python and Flask. This application takes long URLs as input, and enables users to create, update, and delete shortened URLs. The shortened URLs contain a URI, which is generated using a combination of ASCII letters and digits. The length of this URI can be specified as a parameter and defaults to 8. The application also features additional functionality, such as viewing all stored URLs with their corresponding URI's and timestamps. For easy interaction, this application contains a simple User Interface (UI) that can be locally accessed from a web browser.

### Features
* Create a short URL given a long URL
* Update the original URL that is associated with the short URL
* Delete short URLs
* View all stored short URLs along with their corresponding unique identifiers and timestamps
* Redirect users to the original URL when accessing a shortened URL

### Requirements
* Python 3.8.8
* pip 22.3.1
* Flask 1.1.2
* List of other required libraries and their versions (see below)

### Installation and Usage
1. Clone the repository or download the provided Python and HTML files to your local machine.
2. Install the virtualenv package by running the following command in your terminal or command prompt:
```console
pip install virtualenv
```
3. Create and activate a virtual environment for your project:
```console
virtualenv env_name
source env_name/bin/activate # Mac or Linux
env_name\Scripts\activate.bat # Windows
```
4. Install the specified Flask version using pip (assuming pip is installed):
```console
pip install Flask==1.1.2
```
5. Install the other required libraries:
```console
pip install -r requirements.txt
```
6. Run the Flask app:
```console
python app.py
```
7. Open your browser and navigate to http://localhost:5000 to access the URL shortener. Now you can interact with the URL shortener application.

### Structure
The application consists of a single Python file (app.py) and an HTML file (index.html). The Python file contains the URLShortenerApp class that implements the URL shortening service, while the HTML file provides the user interface for interacting with the service.

The URLShortenerApp class contains methods for creating, updating, and deleting short URLs, as well as utility methods for validating URLs, generating unique identifiers, and checking for collisions between identifiers. The class also sets up the necessary Flask routes and provides a method for running the Flask application.

### Testing
The URL shortener application includes a test suite that covers most of the core functionalities. The tests are located in the test_url_shortener_app.py file. The tests cover validation and generation of short URLs, retrieval of short URLs, and redirection, updating, and deletion of short URLs. The tests also cover error handling for invalid input, unsupported requests, and nonexistent unique IDs.

### Running Tests
To run the tests, execute the following command from the terminal:
```console
python -m unittest test_app.py
```

### Limitations
The current implementation stores data into a dictionary and may not scale well when the number of entries grows. Dictionaries are in-memory data structures, which may cause performance issues or limitations in memory. A more efficient and scalable solution would be to use a database system to store the data. For example, a relational database management system or a NoSQL database.

Additionally, there is an trade-off between the length of the generated URI and the possibility of collisions. Collisions occurs when two different long URLs are assigned to the same shortened URI. Shorter URIs are more user-friendly and require less storage, but they also increase the likelihood of collisions. When the number of unique URIs increases, the probability of collisions also increases. This could lead to issues in the functionality of the application. To tackle this matter, the application could employ a more advanced URI generation algorithm, or increase the length of the generated URIs. However, increasing the length of the URIs may result into less convenient shortened URLs.