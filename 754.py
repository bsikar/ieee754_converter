"""
Sign Bit + 8 bits Exponent + 23 bits Mantissa
MSB                                  LSB
"""

from math import log2, floor, ceil


def base10_to_ieee754(number, loud=True):
    number = float(number)
    if loud:
        print("Input number: {}".format(number))

    sign_bit = 0 if number >= 0 else 1
    if loud:
        print("-> 1. Sign bit: {}".format(sign_bit))

    """ START SPECIAL CASE """
    # Special Case 1: Number is 0
    if number == 0:
        if loud:
            print("[Number is 0]")
        # Handle special case for 0
        return "00000000" + "0" * 23

    # Special Case 2: Number is inf
    if number == float("inf"):
        if loud:
            print("[Number is +inf]")
        # Handle special case for +infinity
        return "01111111" + "0" * 23

    # Special Case 3: Number is -inf
    if number == float("-inf"):
        if loud:
            print("[Number is -inf]")
        # Handle special case for -infinity
        return "11111111" + "0" * 23

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
    # Special Case 5: Number is subnormal
    if abs_number < (2**-126):
        if loud:
            print("[Number is subnormal]")
        exponent = 0
        if loud:
            print("-> 3. Exponent: 0")
        mantissa = abs_number * (2 ** (23 + 126))
        if loud:
            print(
                "-> 4. Mantissa: {} * (2^(23 + 126)) = {}".format(abs_number, mantissa)
            )
    # General Case : Normalized
    else:
        if loud:
            print("[Number is normalized]")
        exponent_real = log2(abs_number)
        if loud:
            print("-> 3. Exponent:")
            print("-> 3a. log2({}) = {}".format(abs_number, exponent_real))
        exponent_floor = floor(exponent_real)
        if loud:
            print("-> 3b. floor({}) = {}".format(exponent_real, exponent_floor))
        exponent_127 = 127 + exponent_floor
        if loud:
            print("-> 3c. 127 + {} = {}".format(exponent_floor, exponent_127))
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
        mantissa = round((abs_number / (2**exponent_floor) - 1) * (2**23))
        if loud:
            print(
                "-> 4. Mantissa: round(({} / (2^{}) - 1) * (2^23)) = {}".format(
                    abs_number, exponent_floor, mantissa
                )
            )

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

    # Combine sign bit, exponent, and mantissa to get IEEE 754 representation
    ieee754_binary = "{}{}{}".format(sign_bit, exponent_bin, mantissa_bin)
    if loud:
        print("IEEE754: ", end="")
        for i in range(0, len(ieee754_binary), 4):
            print(ieee754_binary[i : i + 4], end=" ")
        print()

    return ieee754_binary, hex(int(ieee754_binary, 2))


def base16_to_ieee754(hex_num, loud=True):
    decimal_num = float.fromhex(hex_num)
    return base10_to_ieee754(decimal_num, loud)


def base2_to_ieee754(bin_num, loud=True):
    # Split the binary number into the whole and fractional parts
    parts = bin_num.split(".")
    whole_part = int(parts[0], 2) if parts[0] else 0
    fractional_part = 0
    # Convert the fractional part
    if len(parts) > 1:
        for i, digit in enumerate(parts[1]):
            fractional_part += int(digit) * (2 ** (-(i + 1)))
    decimal_num = whole_part + fractional_part
    return base10_to_ieee754(decimal_num, loud)


def ieee754_base16_to_base10(hex_num):
    # example:
    # input: 0x40bc0000
    # output: 5.875
    # Step 1: Convert hex to binary
    binary_num = bin(int(hex_num, 16))[2:].zfill(32)

    # Step 2: Extract components
    sign = int(binary_num[0], 2)
    exponent = int(binary_num[1:9], 2)
    mantissa_bin = binary_num[9:]

    # Step 3: Calculate the sign
    sign_factor = (-1) ** sign

    # Step 4: Adjust the exponent
    exponent_adjusted = exponent - 127

    # Step 5: Calculate the mantissa
    mantissa = 1 + sum(
        int(bit) * 2 ** (-index) for index, bit in enumerate(mantissa_bin, start=1)
    )

    # Step 6: Calculate the decimal number
    decimal_number = sign_factor * (2**exponent_adjusted) * mantissa

    return decimal_number


def ieee754_base2_to_base10(bin_num):
    # example:
    # input: 01000000101111000000000000000000
    # output: 5.875
    # Ensure the binary string is 32 bits for single precision
    bin_num = bin_num.zfill(32)

    # Extract components
    sign = int(bin_num[0], 2)
    exponent = int(bin_num[1:9], 2) - 127
    mantissa_bin = bin_num[9:]

    # Calculate the mantissa
    mantissa = 1 + sum(
        int(bit) * 2 ** (-index) for index, bit in enumerate(mantissa_bin, start=1)
    )

    # Calculate the final number
    decimal_number = ((-1) ** sign) * (2**exponent) * mantissa

    return decimal_number


def ieee754_base16_to_base16(hex_num):
    # example:
    # input:  0x40bc0000
    # output: 0x5.E
    # Convert input hex to binary
    bin_str = bin(int(hex_num, 16))[2:].zfill(32)

    # Decode binary string to float
    sign = 1 if bin_str[0] == "0" else -1
    exponent = int(bin_str[1:9], 2) - 127
    mantissa = int("1" + bin_str[9:], 2) / (2**23)

    # Calculate the floating-point number
    float_val = sign * mantissa * (2**exponent)

    # Convert float to simplified hex
    # This step is non-standard and hypothetical, focusing on the desired output format
    hex_val = hex(int(float_val)).rstrip("L")  # Integer part
    frac_val = float_val - int(float_val)
    frac_hex = ""  # Initialize fractional hex string

    # Convert fractional part to hex (simplified, illustrative example)
    while frac_val > 0 and len(frac_hex) < 2:  # Limiting the length for simplicity
        frac_val *= 16
        frac_hex += hex(int(frac_val))[2:]
        frac_val -= int(frac_val)

    simplified_hex = "{}.{}".format(hex_val, frac_hex.upper()) if frac_hex else hex_val
    return simplified_hex


def _float_to_hex(f):
    # Convert the integer part
    hex_num = hex(int(f))[2:].upper()
    # Process fractional part
    frac, frac_hex = f - int(f), ""
    while frac > 0 and len(frac_hex) < 5:  # Limiting length for simplicity
        frac *= 16
        frac_hex_part = int(frac)
        frac_hex += hex(frac_hex_part)[2:].upper()
        frac -= frac_hex_part
    return "{}.{}".format(hex_num, frac_hex) if frac_hex else hex_num


def ieee754_base2_to_base16(bin_num):
    # example:
    # input:  01000000101111000000000000000000
    # output: 0x5.E
    # Ensure bin_num is 32 bits for single precision
    if len(bin_num) != 32:
        raise ValueError("Input should be a 32-bit binary string")

    # Parse binary string
    sign = (-1) ** int(bin_num[0])
    exponent = int(bin_num[1:9], 2) - 127
    mantissa = 1 + sum(
        int(bit) * 2 ** (-i) for i, bit in enumerate(bin_num[9:], start=1)
    )

    # Calculate the floating-point number
    float_val = sign * (2**exponent) * mantissa

    # Convert to hexadecimal
    hex_val = _float_to_hex(float_val)

    return "0x{}".format(hex_val)


def ieee754_base16_to_base2(hex_num):
    # example:
    # input:   0x40bc0000
    # output: 101.111
    # Convert hex to binary
    bin_num = bin(int(hex_num, 16))[2:].zfill(32)

    # Decode binary to float
    sign_bit = bin_num[0]
    exponent = int(bin_num[1:9], 2) - 127  # Adjust for bias
    mantissa = "1" + bin_num[9:]  # Include the implicit leading 1

    # Calculate the simplified binary representation
    if exponent >= 0:
        # Move the binary point to the right place
        significant_bits = mantissa[: exponent + 1] + "." + mantissa[exponent + 1 :]
    else:
        # If exponent is negative, add leading zeros
        significant_bits = "0." + "0" * (-exponent - 1) + mantissa

    # Remove trailing zeros and the binary point if it's the last character
    simplified_binary = significant_bits.rstrip("0").rstrip(".")

    # Add the sign bit for negative numbers
    if sign_bit == "1":
        simplified_binary = "-" + simplified_binary

    return simplified_binary


def ieee754_base2_to_base2(bin_num):
    # example:
    # input:  01000000101111000000000000000000
    # output: 101.111
    # Decode binary string to float
    sign = (-1) ** int(bin_num[0])
    exponent = int(bin_num[1:9], 2) - 127  # Adjust for the bias
    mantissa = 1 + sum(
        int(bit) * 2 ** (-i) for i, bit in enumerate(bin_num[9:], start=1)
    )

    # Calculate the decimal number
    float_val = sign * (2**exponent) * mantissa

    # Convert decimal number to simplified binary
    int_part = int(float_val)
    frac_part = float_val - int_part

    # Convert integer part to binary
    int_part_bin = bin(int_part).lstrip("-0b")

    # Convert fractional part to binary
    frac_part_bin = ""
    while frac_part > 0 and len(frac_part_bin) < 5:  # Limit the length for simplicity
        frac_part *= 2
        if frac_part >= 1:
            frac_part_bin += "1"
            frac_part -= 1
        else:
            frac_part_bin += "0"

    simplified_bin = "{}.{}".format(int_part_bin, frac_part_bin)
    return simplified_bin


def run():
    while True:
        print("\nMenu (doesn't support 2s complement):")
        print("1. Base10 (simple) to IEEE754")
        print("2. Base16 (simple) to IEEE754")
        print("3. Base2  (simple) to IEEE754")
        print("4. IEEE754 to Base10 (simple)")
        print("5. IEEE754 to Base16 (simple)")
        print("6. IEEE754 to Base2  (simple)")
        print("7. Quit")
        choice = input("Enter your choice: ")

        if choice == "7":
            print("Exiting program.")
            break

        num = input("Enter your number: ").lower()

        if choice == "1":
            binary, hex_repr = base10_to_ieee754(num)
            print("Binary: {}, Base16: {}".format(binary, hex_repr))
        elif choice == "2":
            binary, hex_repr = base16_to_ieee754(num)
            print("Binary: {}, Base16: {}".format(binary, hex_repr))
        elif choice == "3":
            binary, hex_repr = base2_to_ieee754(num)
            print("Binary: {}, Base16: {}".format(binary, hex_repr))
        elif choice == "4":
            if num[:2] == "0x":
                base10 = ieee754_base16_to_base10(num)
            else:
                base10 = ieee754_base2_to_base10(num)
            print("Base10: {}".format(base10))
        elif choice == "5":
            if num[:2] == "0x":
                base16 = ieee754_base16_to_base16(num)
            else:
                base16 = ieee754_base2_to_base16(num)
            print("Base16: {}".format(base16))
        elif choice == "6":
            if num[:2] == "0x":
                base2 = ieee754_base16_to_base2(num)
            else:
                base2 = ieee754_base2_to_base2(num)
            print("Base2: {}".format(base2))
        else:
            print("Invalid choice. Please try again.")


def _test_base10_to_ieee754():
    # base10_to_ieee754
    def base10_to_ieee754_test(number):
        # Convert the number to IEEE 754 binary representation using struct
        ieee754_bytes = struct.pack(">f", number)
        ieee754_bits = "".join(f"{byte:08b}" for byte in ieee754_bytes)

        # Convert the IEEE 754 binary representation to hexadecimal
        ieee754_hex = "".join(f"{byte:02x}" for byte in ieee754_bytes)

        return (ieee754_bits, "0x" + ieee754_hex)

    numbers = np.linspace(-1e10, 1e10, num=int(1e5))
    test_results = list(
        zip(
            numbers,
            [base10_to_ieee754_test(number) for number in numbers],
        )
    )

    fun_results = list(
        zip(
            numbers,
            [base10_to_ieee754(number, False) for number in numbers],
        )
    )

    # Assert and print failed cases
    failed_cases = []
    for test_case, fun_case in zip(test_results, fun_results):
        if test_case[1] != fun_case[1]:
            failed_cases.append((test_case[0], test_case[1], fun_case[1]))

    if failed_cases:
        print("Failed Cases:")
        for case in failed_cases:
            print(f"Number: {case[0]}, Expected: {case[1]}, Got: {case[2]}")


def _test_base16_to_ieee754():
    def base16_to_ieee754_test(hex_value):
        # Convert the simplified floating-point hex to decimal
        decimal_value = float.fromhex(hex_value)

        # Convert the decimal value to IEEE 754 binary representation using struct
        ieee754_bytes = struct.pack(">f", decimal_value)
        ieee754_bits = "".join(f"{byte:08b}" for byte in ieee754_bytes)

        # Convert the IEEE 754 binary representation to hexadecimal
        ieee754_hex = "".join(f"{byte:02x}" for byte in ieee754_bytes)

        return (ieee754_bits, "0x" + ieee754_hex)

    def float_to_custom_hex(value):
        # Split the value into integer and fractional parts
        integer_part, fractional_part = divmod(abs(value), 1)

        # Convert integer part to hexadecimal
        integer_hex = format(int(integer_part), "X")

        # Treat the fractional part by scaling (this is a simplification)
        fractional_hex = format(int(fractional_part * 1e6), "X")

        # Combine with a sign and decimal-like point
        hex_string = f"{'-' if value < 0 else ''}{integer_hex}.{fractional_hex}"

        return hex_string

    values = np.linspace(-1e10, 1e10, num=int(1e5))

    # Convert to custom hex-like strings
    hex_values = [float_to_custom_hex(value) for value in values]

    # Test results using base16_to_ieee754_test
    test_results = [
        (hex_value, base16_to_ieee754_test(hex_value)) for hex_value in hex_values
    ]

    # Test results using base16_to_ieee754
    fun_results = [
        (hex_value, base16_to_ieee754(hex_value, False)) for hex_value in hex_values
    ]

    # Assert and print failed cases
    failed_cases = []
    for test_case, fun_case in zip(test_results, fun_results):
        if test_case[1] != fun_case[1]:
            failed_cases.append((test_case[0], test_case[1], fun_case[1]))

    if failed_cases:
        print("Failed Cases:")
        for case in failed_cases:
            print(
                f"Simplified Hex Value: {case[0]}, Expected: {case[1]}, Got: {case[2]}"
            )


def run_tests():
    _test_base10_to_ieee754()
    _test_base16_to_ieee754()
    # _test_base2_to_ieee754()

    # ieee754_base2_to_base2

    # ieee754_base2_to_base10

    # ieee754_base2_to_base16

    # ieee754_base16_to_base2

    # ieee754_base16_to_base10

    # ieee754_base16_to_base16


if __name__ == "__main__":
    import numpy as np
    import struct

    run_tests()
    run()
