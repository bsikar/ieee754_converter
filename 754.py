"""
Sign Bit + 8 bits Exponent + 23 bits Mantissa
MSB                                  LSB
"""

from math import log2, floor, ceil


def base10_to_ieee754(number, loud=True):
    # Special Case 2: Number is inf
    if number == "inf":
        if loud:
            print("[Number is +inf]")
        # Handle special case for +infinity
        return "01111111" + "0" * 23

    # Special Case 3: Number is -inf
    if number == "-inf":
        if loud:
            print("[Number is -inf]")
        # Handle special case for -infinity
        return "11111111" + "0" * 23

    number = float(number)
    if loud:
        print("Input number: {}".format(number))

    sign_bit = 0 if number >= 0 else 1
    if loud:
        print("-> 1. Sign bit: {}".format(sign_bit))
        input()

    """ START SPECIAL CASE """
    # Special Case 1: Number is 0
    if number == 0:
        if loud:
            print("[Number is 0]")
        # Handle special case for 0
        return "00000000" + "0" * 23

    # Special Case 4: Number is NaN
    if number != number:
        if loud:
            print("[Number is NaN]")
        # Handle special case for NaN
        return "01111111" + "1" * 22 + "0"
    """ END SPECIAL CASE """

    abs_number = abs(number)
    if loud:
        print("-> 2. Absolute Value: {}".format(abs_number))
        input()
    # Special Case 5: Number is subnormal
    if abs_number < (2**-126):
        if loud:
            print("[Number is subnormal]")
            input()
        exponent = 0
        if loud:
            print("-> 3. Exponent: 0")
            input()
        mantissa = abs_number * (2 ** (23 + 126))
        if loud:
            print(
                "-> 4. Mantissa: {} * (2^(23 + 126)) = {}".format(abs_number, mantissa)
            )
            input()
        exponent_bin = "{:08b}".format(exponent).replace("0b", "")
    # General Case : Normalized
    else:
        if loud:
            print("[Number is normalized]")
            input()
        exponent_real = log2(abs_number)
        if loud:
            print("-> 3. Exponent:")
            print("-> 3a. log2({}) = {}".format(abs_number, exponent_real))
            input()
        exponent_floor = floor(exponent_real)
        if loud:
            print("-> 3b. floor({}) = {}".format(exponent_real, exponent_floor))
            input()
        exponent_127 = 127 + exponent_floor
        if loud:
            print("-> 3c. 127 + {} = {}".format(exponent_floor, exponent_127))
            input()
        exponent_bin = "{:08b}".format(exponent_127).replace("0b", "")
        if loud:
            print(
                "Exponent = {} -> {} -> {} -> {} {}".format(
                    exponent_real,
                    exponent_floor,
                    exponent_127,
                    exponent_bin[:4],
                    exponent_bin[4:],
                )
            )
            input()
        mantissa = round((abs_number / (2**exponent_floor) - 1) * (2**23))
        if loud:
            print(
                "-> 4. Mantissa: round(({} / (2^{}) - 1) * (2^23)) = {}".format(
                    abs_number, exponent_floor, mantissa
                )
            )
            input()

    mantissa_bin = "{:023b}".format(int(mantissa))
    if loud:
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
        input()

    # Combine sign bit, exponent, and mantissa to get IEEE 754 representation
    ieee754_binary = "{}{}{}".format(sign_bit, exponent_bin, mantissa_bin)
    if loud:
        print("IEEE754: ", end="")
        for i in range(0, len(ieee754_binary), 4):
            print(ieee754_binary[i : i + 4], end=" ")
        print()
        input()

    return ieee754_binary, hex(int(ieee754_binary, 2))


def run():
    print("Base10 (simple) to IEEE754")

    num = input("Enter your number: ").lower()

    binary, hex_repr = base10_to_ieee754(num)
    print("Binary: {}, Base16: {}".format(binary, hex_repr))


run()
