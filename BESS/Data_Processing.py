# Pre-processing ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++







# Post-processing ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ------------- Export all values of a variable into a list parameter ------------  
def List_dictionary (Variable):
    all_elements = []
    all_elements = [element for sublist in Variable for element in sublist]

    return all_elements   