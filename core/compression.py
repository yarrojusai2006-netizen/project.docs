import msgpack


class StateCompressor:
    @staticmethod
    def compress(delta: dict) -> bytes:
        return msgpack.packb(delta, use_bin_type=True)

    @staticmethod
    def decompress(blob: bytes) -> dict:
        return msgpack.unpackb(blob, raw=False)