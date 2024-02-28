
"""
Sign Bit + 8 bits Exponent + 23 bits Mantissa
MSB                                  LSB
"""

from math import log2, floor, ceil


def base10_to_ieee754(number):
    # Special Case Number is inf
    if number == "inf":
        print("[Number is +inf]")
        # Handle special case for +infinity
        return "01111111" + "0" * 23

    # Special Case Number is -inf
    if number == "-inf":
        print("[Number is -inf]")
        # Handle special case for -infinity
        return "11111111" + "0" * 23

    number = float(number)
    print("Input number: {}".format(number))

    sign_bit = 0 if number >= 0 else 1
    print("-> 1. Sign bit: {}".format(sign_bit))
    input("Press Enter to continue...")

    """ START SPECIAL CASE """
    # Special Case 1: Number is 0
    if number == 0:
        print("[Number is 0]")
        # Handle special case for 0
        return "00000000" + "0" * 23

    # Special Case 4: Number is NaN
    if number != number:
        print("[Number is NaN]")
        # Handle special case for NaN
        return "01111111" + "1" * 22 + "0"
    """ END SPECIAL CASE """

    abs_number = abs(number)
    print("-> 2. Absolute Value: {}".format(abs_number))
    input("Press Enter to continue...")
    # Special Case 5: Number is subnormal
    if abs_number < (2**-126):
        print("[Number is subnormal]")
        input("Press Enter to continue...")
        exponent = 0
        print("-> 3. Exponent: 0")
        input("Press Enter to continue...")
        mantissa = round(1.0 * abs_number * (2 ** (23 + 126)))
        print("-> 4. Mantissa: round({} * (2^(23 + 126))) = {}".format(abs_number, mantissa))
        input("Press Enter to continue...")
        exponent_bin = "{:08b}".format(exponent).replace("0b", "")
    # General Case : Normalized
    else:
        print("[Number is normalized]")
        input("Press Enter to continue...")
        exponent_real = log2(abs_number)
        print("-> 3. Exponent:")
        print("-> 3a. log2({}) = {}".format(abs_number, exponent_real))
        input("Press Enter to continue...")
        exponent_floor = floor(exponent_real)
        print("-> 3b. floor({}) = {}".format(exponent_real, exponent_floor))
        input("Press Enter to continue...")
        exponent_127 = 127 + exponent_floor
        print("-> 3c. 127 + {} = {}".format(exponent_floor, exponent_127))
        input("Press Enter to continue...")
        exponent_bin = "{:08b}".format(exponent_127).replace("0b", "")
        print(
            "Exponent = {} -> {} -> {} -> {} {}".format(
                exponent_real,
                exponent_floor,
                exponent_127,
                exponent_bin[:4],
                exponent_bin[4:],
            )
        )
        input("Press Enter to continue...")
        mantissa = round((abs_number / (2**exponent_floor) - 1) * (2**23))
        print(
            "-> 4. Mantissa: round(({} / (2^{}) - 1) * (2^23)) = {}".format(
                abs_number, exponent_floor, mantissa
            )
        )
        input("Press Enter to continue...")

    mantissa_bin = "{:023b}".format(int(mantissa))
    print(
        "Mantissa = {} {} {} {} {} {} {} {}".format(
            mantissa_bin[:3],
            mantissa_bin[3:7],
            mantissa_bin[7:11],
            mantissa_bin[11:15],
            mantissa_bin[15:19],
            mantissa_bin[19:23],
            mantissa_bin[23:27],
            mantissa_bin[27:],
        )
    )
    input("Press Enter to continue...")

    # Combine sign bit, exponent, and mantissa to get IEEE 754 representation
    ieee754_binary = "{}{}{}".format(sign_bit, exponent_bin, mantissa_bin)
    print("IEEE754: ", end="")
    for i in range(0, len(ieee754_binary), 4):
        print(ieee754_binary[i : i + 4], end=" ")
    print()
    input("Press Enter to continue...")

    return ieee754_binary, hex(int(ieee754_binary, 2))


def ieee754_to_base10(binary_str):
    print("Input: {}".format(binary_str))
    input("Press Enter to continue...")

    # Special cases handling
    # +Infinity
    if binary_str == "011111111" + "0" * 23:
        print("[Number is +inf]")
        return "+inf"

    # -Infinity
    if binary_str == "111111111" + "0" * 23:
        print("[Number is -inf]")
        return "-inf"

    # Zero
    if binary_str == "00000000" + "0" * 23:
        print("[Number is 0]")
        return "0"

    # NaN
    if binary_str == "011111111" + "1" * 22 + "0":
        print("[Number is NaN]")
        return "NaN"

    sign_bit = int(binary_str[0])
    print("-> 1. Sign bit: {}".format(sign_bit))
    input("Press Enter to continue...")

    exponent = binary_str[1:9]
    mantissa = binary_str[9:]

    exponent_val = int(exponent, 2) - 127
    print(
        "-> 2. Exponent Value: 2^{} - 127 = {}".format(int(exponent, 2), exponent_val)
    )
    input("Press Enter to continue...")

    # Handling subnormal numbers
    if exponent == "00000000":
        print("[Number is subnormal]")
        mantissa_val = int(mantissa, 2) / (2**23)
        base10 = mantissa_val * (2**-126)
    else:
        print("[Number is normalized]")
        mantissa_val = 1 + int(mantissa, 2) / (2**23)
        print(
            "-> 3. Mantissa Value: 1 + int({}) / 2^23 = {}".format(
                mantissa_val, mantissa_val
            )
        )
        input("Press Enter to continue...")
        print("-> 3a. Base 10: {} * 2^{}".format(mantissa_val, exponent_val))
        base10 = mantissa_val * (2**exponent_val)

    if sign_bit == 1:
        base10 = -base10

    print("-> 4. Base10 Value: {}".format(base10))
    input("Press Enter to continue...")

    return base10


def run():
    print("Base10 (simple) to IEEE754")
    print("1. base10 to 754")
    print("2. 754 to base 10")

    choice = input("Enter your choice: ")
    num = input("Enter your number: ").lower()

    if choice == "1":
        binary, hex_repr = base10_to_ieee754(num)
        print("Binary: {}, Base16: {}".format(binary, hex_repr))
    if choice == "2":
        base10 = ieee754_to_base10(num)
        print("Base 10: {}".format(base10))


run()

