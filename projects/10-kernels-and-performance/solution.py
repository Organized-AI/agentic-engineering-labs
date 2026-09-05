def vector_add(x: list[float], y: list[float], block_size=8) -> list[float]:
    if len(x) != len(y): raise ValueError("vectors must have equal length")
    if block_size < 1: raise ValueError("block size must be positive")
    out=[0.0]*len(x)
    for start in range(0,len(x),block_size):
        for offset in range(block_size):
            index=start+offset
            if index < len(x): out[index]=x[index]+y[index]
    return out

def overall_speedup(fraction_improved: float, local_speedup: float) -> float:
    if not 0 <= fraction_improved <= 1 or local_speedup <= 0: raise ValueError("invalid inputs")
    return 1/((1-fraction_improved)+fraction_improved/local_speedup)

if __name__ == "__main__":
    print(vector_add(list(range(11)),[1]*11,block_size=4))
    print("whole-system speedup:",round(overall_speedup(.2,4),3))
