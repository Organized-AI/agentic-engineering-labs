GIB = 1024 ** 3

def weight_bytes(parameters: int, bytes_per_parameter: float) -> int:
    """TODO: validate positive inputs and estimate stored weight bytes."""
    raise NotImplementedError

def kv_cache_bytes(layers: int, kv_heads: int, head_dim: int, tokens: int, bytes_per_element: int, sequences=1) -> int:
    """TODO: calculate K and V storage for conventional full attention."""
    raise NotImplementedError

def fits(memory_bytes: int, required_bytes: int, headroom=.15) -> bool:
    """TODO: require free operational headroom."""
    raise NotImplementedError
