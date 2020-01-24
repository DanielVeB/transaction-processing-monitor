from src.library.web_service import WebService


webservice = WebService("test", "root", "lukasz")

if __name__ == '__main__':
    webservice.run_web_service(8081)
