from datetime import date
def add_time(amount, unit, date=date.today()):
    """takes in an amount, either (d,w,m) and an option start date and returns an altered date"""
    if unit == 'd':
        today = str(date)
        lyst = today.split('-')
        lyst2 = []
        word = ''
        counter = 0
        for item in lyst:
            lyst2.append(int(item))
        if lyst2[1] == 2 and lyst2[1]%4 == 0 and lyst2[2] + amount > 29: # leap year
            lyst2[2] = (lyst2[2] + amount) - 29
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] == 2 and lyst2[1]%4 != 0 and lyst2[2] + amount > 28:
            lyst2[2] = (lyst2[2] + amount) - 28
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] == 2 and lyst[2] + amount <= 28:
            lyst2[2] += amount
        if lyst2[1] in [1,3,5,7,8,10,12] and lyst2[2] + amount > 31:
            lyst2[2] = (lyst2[2] + amount) - 31
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] in [1,3,5,7,8,10,12] and lyst2[2] + amount <= 31:
            lyst2[2] += amount
        if lyst2[1] in [4,6,9,11] and lyst2[2] + amount > 30:
            lyst2[2] = (lyst2[2] + amount) - 30
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] in [4,6,9,11] and lyst2[2] + amount <= 30:
            lyst2[2] += amount
        for item in lyst2:
            item = str(item)
            if item == '1':
                item = '01'
            elif item == '2':
                item = '02'
            elif item == '3':
                item = '03'
            elif item == '4':
                item = '04'
            elif item == '5':
                item = '05'
            elif item == '6':
                item = '06'
            elif item == '7':
                item = '07'
            elif item == '8':
                item = '08'
            elif item == '9':
                item = '09'
            if counter < 2:
                word += str(item) + '-'
                counter += 1
            else:
                word += str(item)
        return word
    elif unit == 'w':
        amount *= 7
        today = str(date)
        lyst = today.split('-')
        lyst2 = []
        word = ''
        counter = 0
        for item in lyst:
            lyst2.append(int(item))
        if lyst2[1] == 2 and lyst2[1]%4 == 0 and lyst2[2] + amount > 29: # leap year
            lyst2[2] = (lyst2[2] + amount) - 29
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] == 2 and lyst2[1]%4 != 0 and lyst2[2] + amount > 28:
            lyst2[2] = (lyst2[2] + amount) - 28
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] == 2 and lyst2[2] + amount <= 28:
            lyst2[2] += amount
        if lyst2[1] in [1,3,5,7,8,10,12] and lyst2[2] + amount > 31:
            lyst2[2] = (lyst2[2] + amount) - 31
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] in [1,3,5,7,8,10,12] and lyst2[2] + amount <= 31:
            lyst2[2] += amount
        if lyst2[1] in [4,6,9,11] and lyst2[2] + amount > 30:
            lyst2[2] = (lyst2[2] + amount) - 30
            if lyst2[1] + 1 > 12:
                lyst2[0] += 1
                lyst2[1] == 1
            else:
                lyst2[1] += 1
        elif lyst2[1] in [4,6,9,11] and lyst2[2] + amount <= 30:
            lyst2[2] += amount
        for item in lyst2:
            item = str(item)
            if item == '1':
                item = '01'
            elif item == '2':
                item = '02'
            elif item == '3':
                item = '03'
            elif item == '4':
                item = '04'
            elif item == '5':
                item = '05'
            elif item == '6':
                item = '06'
            elif item == '7':
                item = '07'
            elif item == '8':
                item = '08'
            elif item == '9':
                item = '09'
            if counter < 2:
                word += str(item) + '-'
                counter += 1
            else:
                word += str(item)
        return word
    elif unit == 'm':
        today = str(date)
        lyst = today.split('-')
        lyst2 = []
        word = ''
        counter = 0
        for item in lyst:
            lyst2.append(int(item))
        if lyst2[1] + amount > 12:
            lyst2[0] += 1
            lyst2[1] = (lyst2[1] + amount) - 12
        else:
            lyst2[1] += amount
        for item in lyst2:
            item = str(item)
            if item == '1':
                item = '01'
            elif item == '2':
                item = '02'
            elif item == '3':
                item = '03'
            elif item == '4':
                item = '04'
            elif item == '5':
                item = '05'
            elif item == '6':
                item = '06'
            elif item == '7':
                item = '07'
            elif item == '8':
                item = '08'
            elif item == '9':
                item = '09'
            if counter < 2:
                word += str(item) + '-'
                counter += 1
            else:
                word += str(item)
        return word
