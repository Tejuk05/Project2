def handle_request(path):
    """
    Handles requests based on the URL path and returns the content for the corresponding page.

    Args:
        path (str): The URL path requested by the user (e.g., "/", "/handicrafts").

    Returns:
        str: The content of the requested page.
    """
    if path == "/":
        return get_home_page()
    elif path == "/handicrafts":
        return get_handicrafts_page()
    elif path == "/culture_heritage":
        return get_culture_heritage_page()
    elif path == "/pure_natural":
        return get_pure_natural_page()
    elif path == "/regional_cuisine":
        return get_regional_cuisine_page()
    elif path == "/community":
        return get_community_page()
    else:
        return get_not_found_page()

def get_home_page():
    """Returns the content for the Home page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to Our Website!</h1>
        <p>Explore the wonders of our offerings.</p>
        <ul>
            <li><a href="/handicrafts">Handicrafts</a></li>
            <li><a href="/culture_heritage">Culture & Heritage</a></li>
            <li><a href="/pure_natural">Pure & Natural</a></li>
            <li><a href="/regional_cuisine">Regional Cuisine</a></li>
            <li><a href="/community">Community</a></li>
        </ul>
    </body>
    </html>
    """
    return html

def get_handicrafts_page():
    """Returns the content for the Handicrafts page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Handicrafts</title>
    </head>
    <body>
        <h1>Discover Exquisite Handicrafts</h1>
        <p>Browse our unique collection of handcrafted items.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

def get_culture_heritage_page():
    """Returns the content for the Culture & Heritage page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Culture & Heritage</title>
    </head>
    <body>
        <h1>Immerse Yourself in Culture & Heritage</h1>
        <p>Learn about our rich traditions and history.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

def get_pure_natural_page():
    """Returns the content for the Pure & Natural page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pure & Natural</title>
    </head>
    <body>
        <h1>Experience the Pureness of Nature</h1>
        <p>Explore our natural and organic products.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

def get_regional_cuisine_page():
    """Returns the content for the Regional Cuisine page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Regional Cuisine</title>
    </head>
    <body>
        <h1>Savor the Flavors of Regional Cuisine</h1>
        <p>Discover the authentic tastes of our region.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

def get_community_page():
    """Returns the content for the Community page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Community</title>
    </head>
    <body>
        <h1>Connect with Our Community</h1>
        <p>Join discussions and engage with fellow enthusiasts.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

def get_not_found_page():
    """Returns a 404 Not Found page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 Not Found</title>
    </head>
    <body>
        <h1>404 Not Found</h1>
        <p>The requested page was not found.</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # This is a very basic example and would require a web server
    # to actually serve these pages over HTTP.

    # For demonstration purposes, let's simulate a few requests:
    print("Requesting /:")
    print(handle_request("/"))
    print("\nRequesting /handicrafts:")
    print(handle_request("/handicrafts"))
    print("\nRequesting /culture_heritage:")
    print(handle_request("/culture_heritage"))
    print("\nRequesting /nonexistent_page:")
    print(handle_request("/nonexistent_page"))