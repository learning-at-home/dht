""" A unified interface for several common serialization methods """
import pickle
import umsgpack


class SerializerBase:
    @staticmethod
    def dumps(obj: object) -> bytes:
        raise NotImplementedError()

    @staticmethod
    def loads(buf: bytes) -> object:
        raise NotImplementedError()


class PickleSerializer(SerializerBase):
    @staticmethod
    def dumps(obj: object) -> bytes:
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loads(buf: bytes) -> object:
        return pickle.loads(buf)


class MSGPackSerializer(SerializerBase):
    @staticmethod
    def dumps(obj: object) -> bytes:
        return umsgpack.dumps(obj, use_bin_type=False)  # TODO strict https://github.com/msgpack/msgpack-python/pull/158

    @staticmethod
    def loads(buf: bytes) -> object:
        return umsgpack.loads(buf, raw=False)
