class Bcolors:
    # {bcolors.CYAN}{....}{bcolors.ENDC}
    END = '\033[0m'  # Обозначение места окончания примения форматирования
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BlUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    GRAY = '\033[47m'

# for i in range(120):
#     print(f'{i} - \033[{str(i)}m tets {Bcolors.ENDC}')
print(f'{Bcolors.CYAN}{1:^10}{Bcolors.END}')