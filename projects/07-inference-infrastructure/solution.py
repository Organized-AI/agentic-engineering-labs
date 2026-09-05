GIB = 1024 ** 3

def _positive(*values):
    if any(type(v) not in {int,float} or v <= 0 for v in values): raise ValueError("all values must be positive numbers")

def weight_bytes(parameters: int, bytes_per_parameter: float) -> int:
    _positive(parameters,bytes_per_parameter); return int(parameters*bytes_per_parameter)

def kv_cache_bytes(layers: int, kv_heads: int, head_dim: int, tokens: int, bytes_per_element: int, sequences=1) -> int:
    _positive(layers,kv_heads,head_dim,tokens,bytes_per_element,sequences)
    return int(2*layers*kv_heads*head_dim*tokens*bytes_per_element*sequences)

def fits(memory_bytes: int, required_bytes: int, headroom=.15) -> bool:
    _positive(memory_bytes,required_bytes)
    if not 0 <= headroom < 1: raise ValueError("headroom must be in [0,1)")
    return required_bytes <= memory_bytes*(1-headroom)

if __name__ == "__main__":
    weights=weight_bytes(8_000_000_000,2)
    cache=kv_cache_bytes(32,8,128,8192,2,sequences=4)
    print({"weights_gib":round(weights/GIB,2),"cache_gib":round(cache/GIB,2),"fits_24_gib":fits(24*GIB,weights+cache)})
