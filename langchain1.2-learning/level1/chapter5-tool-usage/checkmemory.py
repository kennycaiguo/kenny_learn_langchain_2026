import psutil

def check_memory():
    mem = psutil.virtual_memory()
    print(f"总内存: {mem.total / (1024**3):.2f} GB")
    print(f"可用内存: {mem.available / (1024**3):.2f} GB")
    print(f"使用率: {mem.percent}%")

if __name__ == "__main__":
    check_memory()