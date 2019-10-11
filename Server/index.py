import tornado.web
import tornado.ioloop #thread keep listening to the port

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hi This is server")


class queryRequestHandler(tornado.web.RequestHandler):
    def get(self):
        print("Inside the even text")
        n=int(self.get_argument("n"))
        r="odd"  if n%2 else "even"
        self.write("The number is " + r)



class ocrTextRequestHandler(tornado.web.RequestHandler):
    def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))



if __name__=="__main__":
    app=tornado.web.Application([ #takes the array of handlers
            (r"/",basicRequestHandler),
            (r"/blog",queryRequestHandler)
    ])

    app.listen(8881)
    print("I'm listening to port 8881")
    tornado.ioloop.IOLoop.current().start()