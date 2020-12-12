from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from cornice import Service

import model

route = Service(name='route',path='/',description='Get predictions')

@route.get()
def get_quote(request):

    model1 = model.Model()

    text = request.params['text']

    pred = model1.predict([text])

    return {
        'Text' : text,
        'Sentiment': pred
    }


if __name__ == '__main__':

    config = Configurator()

    config.include("cornice")
    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()