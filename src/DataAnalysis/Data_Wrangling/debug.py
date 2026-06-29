def p_info(title=None, sep="*" * 50, **kwargs):
    print(sep)

    if title:
        print(f"[{title}]")
        print(sep)

    for name, value in kwargs.items():
        print(f"{name}:")
        print(f"type: {type(value).__name__}")

        if hasattr(value, "shape"):
            print(f"shape: {value.shape}")

        print(value)
        print("-" * 50)

    print(sep)
