import re

entrada = None

#cpf
def __validate_formatting_cpf(cpf):
    match = re.search(r"\d\d\d.\d\d\d.\d\d\d-\d\d",cpf)
    if(match != None):
        return True
    else:
        return False

def __validate_numbers_cpf(cpf):
    base_cpf = cpf[0:3] + cpf[4:7] + cpf[8:11]
    digit_1 = int(cpf[12])
    digit_2 = int(cpf[13])

    multiplicator = 10
    acumulator = 0
    for number in base_cpf:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    rest = acumulator % 11

    if(rest < 2):
        expected_digit_1 = 0
    else:
        expected_digit_1 = 11 - rest

    if(expected_digit_1 != digit_1):
        return False

    base_cpf = base_cpf + str(expected_digit_1)

    multiplicator = 11
    acumulator = 0
    for number in base_cpf:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    rest = acumulator % 11

    if(rest < 2):
        expected_digit_2 = 0
    else:
        expected_digit_2 = 11 - rest

    if(expected_digit_2 != digit_2):
        return False

    return True

def validate_cpf(cpf):
    formatted = __validate_formatting_cpf(cpf)
    if(formatted is not True):
        return False

    valid_numbers = __validate_numbers_cpf(cpf)
    if(valid_numbers is not True):
        return False

    return True


#identification
def __validate_formatting_identification(identification):

    is_cpf = __validate_formatting_cpf(identification)

    match = re.search(r"\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d",identification)
    if(match != None):
        is_cnpj = True
    else:
        is_cnpj = False

    if(is_cpf == True or is_cnpj == True):
        if(is_cpf == True):
            return True, "CPF"
        else:
            return True, "CNPJ"
    else:
        return False, ""

def __validate_numbers_identification(identification):
    base_identification = identification[:2] + identification[3:6] + identification[7:10] + identification[11:15]
    digit_1 = int(identification[-2])
    digit_2 = int(identification[-1])

    base_identification_1 = base_identification[:4]
    base_identification_2 = base_identification[4:]

    multiplicator = 5
    acumulator = 0
    for number in base_identification_1:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    multiplicator = 9
    for number in base_identification_2:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    rest = acumulator % 11

    if(rest < 2):
        expected_digit_1 = 0
    else:
        expected_digit_1 = 11 - rest

    if(expected_digit_1 != digit_1):
        return False

    base_identification_1 = base_identification[:5]
    base_identification_2 = base_identification[5:] + str(digit_1)

    multiplicator = 6
    acumulator = 0
    for number in base_identification_1:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    multiplicator = 9
    for number in base_identification_2:
        acumulator += int(number) * multiplicator
        multiplicator -= 1

    rest = acumulator % 11

    if(rest < 2):
        expected_digit_2 = 0
    else:
        expected_digit_2 = 11 - rest

    if(expected_digit_2 != digit_2):
        return False

    return True

def validate_identification(identification):
    is_valid, type_identification = __validate_formatting_identification(identification)

    if(is_valid == False):
        return False

    is_numbers_valid = None
    if(type_identification == "CPF"):
        is_numbers_valid = __validate_numbers_cpf(identification)
    else:
        is_numbers_valid = __validate_numbers_identification(identification)

    return is_numbers_valid


#time
def __validate_formatting_time(time):
    match = re.search(r"\d\d\d\d.\d\d.\d\d",time[0])
    if(match == None):
        return False

    match = re.search(r"\d\d:\d\d:\d\d",time[1])
    if(match == None):
        return False

    return True

def __validate_numbers_time(time):

    hour = int(time[1][:2])
    if(hour < 0 or hour > 23 ):
        return False

    minutes = int(time[1][3:5])
    if(minutes < 0 or minutes > 59):
        return False

    return True

def validate_time(time):
    is_valid = __validate_formatting_time(time)
    if(is_valid == False):
        return False

    if(__validate_numbers_time(time) == False):
        return False

    return True


#prices
def __get_list_of_prices(prices):
    return prices[1:-1].split(",")

def __validate_formatting_prices(prices):
    list_of_prices = __get_list_of_prices(prices)
    for price in list_of_prices:
        match = re.search(r"^[0-9]+.[0-9]{2}$",price)
        if(match == None):
            return False

    return True

def validate_prices(prices):
    return __validate_formatting_prices(prices)

#code
def __validate_formatting_code(code):
    match = re.search(r"[0-9]{9}-[0-9a-z]{5}-[0,2,4,6,8]{3}(-[0,1]{3})?",code)
    if(match == None):
        return False

    return True

def __validate_numbers_code(code):
	second_part = code[10:15]
	for letter in second_part:
		if(second_part.count(letter) > 1):
			return False

	return True

def validate_code(code):
	if(__validate_formatting_code(code) == False):
		return False

	if(__validate_numbers_code(code) == False):
		return False

	return True

#final
def __validate_formatting_expression(expression):
    match = re.search(r"^[0-9\.\-]{14}\s[0-9\.\-\/]{14}([0-9\.\-\/]{4})?\s[0-9\.]{10}\s[0-9\:]{8}\s[\[]([0-9]+.[0-9]{2}(\,)?)+[\]]\s[0-9a-z\-]{19}(\-[0,1]{3})?$",expression)
    if(match == None):
        return False

    return True

def validate_expression(expression):

    if(__validate_formatting_expression(expression) == False):
        return False

    expression = expression.split()

    cpf                     = expression[0]
    identification          = expression[1]
    estampa_tempo           = expression[2:4]
    preco                   = expression[4]
    codigo_transacao        = expression[5]

    if(validate_cpf(cpf) == False):
        return False
    if(validate_identification(identification) == False):
        return False
    if(validate_time(estampa_tempo) == False):
        return False
    if(validate_prices(preco) == False):
        return False
    if(validate_code(codigo_transacao) == False):
        return False

    return True

if __name__ == '__main__':
    entrada = input()

    if(entrada != None):
        print(validate_expression(entrada))
    else:
        print(False)
