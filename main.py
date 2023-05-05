import sys
from main_modules.auth import AuthService
from main_modules.shortener import URLShortenerService


# Specify port for url_shortener_service
url_port = 3000

# Specify port for auth_service
auth_port = 3001

def main():
    service_name = sys.argv[1]

    if service_name == "url_shortener":
        auth_service = AuthService(None)
        url_shortener_service = URLShortenerService(auth_service)
        url_shortener_service.run(debug=True, port=url_port, use_reloader=False)
    elif service_name == "auth_service":
        url_shortener_service = URLShortenerService(None)
        auth_service = AuthService(url_shortener_service)
        auth_service.run(debug=True, port=auth_port, use_reloader=False)
    else:
        print("Invalid service name. Use 'url_shortener' or 'auth_service'.")

if __name__ == '__main__':
    main()