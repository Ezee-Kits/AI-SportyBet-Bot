def cal(odd, pba):
    odd = float(odd)
    pba = float(pba)
    # print("Probability:", pba)  # Debugging print
    
    amt = 100
    odd -= 1  # Ensure we don't divide by zero

    proba = round(pba / 100, 4)
    loss = 1 - proba

    if odd == 0:  # Prevent division by zero
        return 0

    f = round((((odd * proba) - (loss)) / odd) * amt)
    return f