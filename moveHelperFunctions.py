def intToCompOne(fen_segment):
    expanded_segment = ''
    for i, v in enumerate(fen_segment):
        if v.isdigit():
            for j in range(int(v)):
                expanded_segment += '1'
        else:
           expanded_segment += v
    return expanded_segment

def compOneToInt(fen_segment):
    condensed_segment = ''
    count = 0
    for i in range(0, len(fen_segment)):
        if (fen_segment[i] == '1'):
            count += 1
        else:
            if (count != 0):
                condensed_segment += str(count)
                count = 0
            condensed_segment += fen_segment[i]
    if (count != 0):
        condensed_segment += str(count)

    return condensed_segment

def fenBoardArrToString(fen_Board_Arr):
    fen_Board_str = ''
    for i in range(0, len(fen_Board_Arr) - 1):
        fen_Board_str += fen_Board_Arr[i] + '/'
    fen_Board_str += fen_Board_Arr[7]
    return fen_Board_str


def letterToInt(letter):
    switcher = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
    }
    return switcher.get(letter, "Invalid Letter")

def rankToIndex(rank):
    switcher = {
        8: 0,
        7: 1,
        6: 2,
        5: 3,
        4: 4,
        3: 5,
        2: 6,
        1: 7
    }
    return switcher.get(rank, "Invalid Rank")