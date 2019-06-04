from app.models.model_mongo import ModelMongo


class RequestsDB(ModelMongo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, collection="requests")

    def save(self, data):

        pass

