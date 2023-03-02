def switch(key, options: dict):
        print("switch")
        item = options.get(key, options.get("default"))
        if hasattr(item, "__call__"):
            return item()
        else:
            return item