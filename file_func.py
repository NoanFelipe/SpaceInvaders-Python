def create_file(name):
    try:
        a = open(name, 'wt+')
        a.close()
    except:
        print('Houve um ERRO na criação do arquivo')
    
    else:
        print(f"Arquivo \033[1;35m{name}\033[m criado com sucesso")


def file_exists(name):
    try:
        a = open(name, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True

def write_on_file(obj, file):
    file = open(file, "w")
    file.write(str(obj))
    file.close()

def read_file(file):
    f = open(file, "r")
    string = f.read()
    f.close()
    return string