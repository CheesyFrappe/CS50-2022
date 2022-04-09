from cs50 import get_string

def main():
    text = get_string("Text: \n")

    L = float(count_letters(text) / count_words(text) * 100)
    S = float(count_sentences(text) / count_words(text) * 100)
    index = round((float)(0.0588 * L - 0.296 * S - 15.8))

    get_result(index)

def count_words(text):
    substring = " "

    total = text.count(substring)

    return total + 1

def count_sentences(text):#its okay  cümle kelime harf
    count = 0
    for i in range(0,len(text)):
        if text[i] in (".","?","!"):
            count+=1
    return count

def count_letters(text):
    count = 0
    for char in text:
        if(char.isalpha()):
            count+=1
    return count

def get_result(grade):

    if grade < 1:
            print("Before Grade 1\n")

    elif grade >= 16:
            print("Grade 16+\n")

    else:
            print(f"Grade {grade}")

if __name__ == "__main__":
    main()