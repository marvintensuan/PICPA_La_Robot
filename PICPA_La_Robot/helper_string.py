def chain_replace(string, replace={}):
        for key, value in replace.items():
            string = string.replace(key, value)
        return string
