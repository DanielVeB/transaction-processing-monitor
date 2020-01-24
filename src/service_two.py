from src.library.web_service import WebService

webservice2 = WebService("test2", "root", "lukasz", db_type='postgres')

if __name__ == '__main__':
    webservice2.run_web_service(8082)
