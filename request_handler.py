from entries.request import update_entry
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from entries import get_all_entries, get_single_entry, delete_entry, find_entry_by_keyword, create_entry, update_entry
from moods import get_all_moods, get_single_mood


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/entrys/1", the resulting list will
        # have "" at index 0, "entrys" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        if "?" in resource:

            # /entries?q=${searchTerm}

            param = resource.split("?")[1]  # q=searchTerm
            resource = resource.split("?")[0]  # 'entries'
            pair = param.split("=")  # [ 'q', 'searchTerm' ]
            key = pair[0]  # 'q'
            value = pair[1]  # 'searchTerm'

            return ( resource, key, value )

        else:
            # Try to get the item at index 2
            try:
                # Convert the string "1" to the integer 1
                # This is the new parseInt()
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /entrys
            except ValueError:
                pass  # Request had trailing slash: /entrys/

            return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response
        parsed_url = self.parse_url(self.path)
        # Parse the URL and capture the tuple that is returned
        if len(parsed_url) == 2:
            (resource, id) = parsed_url
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                    pass
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                    pass
                else:
                    response = f"{get_all_moods()}"
        elif len(parsed_url) == 3:
            ( resource, key, value ) = parsed_url
            if key == "q" and resource == "entries":
                # pass in value to SQL database search
                response = f"{find_entry_by_keyword(value)}"

        self.wfile.write(response.encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        new_entry = None

        # Add a new entry to the list. Don't worry about
        # the orange squiggle, you'll define the create_entry
        # function next.
        if resource == "entries":
            new_entry = create_entry(post_body)
            # Encode the new entry and send in response
            self.wfile.write(f"{new_entry}".encode())


    # # Here's a method on the class that overrides the parent's method.
    # # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single entry from the list
        if resource == "entries":
            delete_entry(id)

        # Encode the new entry and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
