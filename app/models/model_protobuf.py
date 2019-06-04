from google.protobuf.json_format import MessageToJson, ParseDict, MessageToDict
from google.protobuf.message import Message


class ProtobuffModelBase:

    def __init__(self, *args, **kwargs):
        if not kwargs.get("message"):
            self.message = Message()

        self.message = kwargs.get("message")

    def to_json(self) -> str:
        """
        Returns JSON string representation of the Protobuf Message

        :return:
        """
        return MessageToJson(self.message)

    def to_dict(self) -> dict:
        """
        Returns dict representation of the Protobuf Message

        :return:
        """
        return MessageToDict(self.message)

    def _update_message(self, data) -> bool:
        if isinstance(data, dict):
            self.message = ParseDict(data, self.message)
            return True

        if isinstance(data, bytes):
            self.message.ParseFromString(data)
            return True

        return False

    def SerializeToString(self) -> bytes:
        """
        Returns byte representation of Protobuf Message.

        :return:
        """
        return self.message.SerializeToString()

    def update(self, data: object) -> bool:
        """
        updates the contents of the message body. Data can be in the form of bytes
        or dict.

        :param data: Can be of type bytes or dict.
        :return:
        """
        return self._update_message(data)

    @classmethod
    def new(cls, message):
        if isinstance(message, Message):
            return ProtobuffModelBase(message=message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: Message):
        if not isinstance(message, Message):
            raise TypeError(f'Must be of type {type(Message())}')
        self._message = message
