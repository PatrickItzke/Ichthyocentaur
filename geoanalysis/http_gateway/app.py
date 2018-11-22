from connexion.resolver import RestyResolver
import connexion


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='swagger/')
    app.add_api('geoanalysis_service.yaml', resolver=RestyResolver('api'))
    app.run(port=8080)