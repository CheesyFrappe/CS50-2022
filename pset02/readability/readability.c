#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string sentence = get_string("Text: \n");

    float grade = 0.0588 * (100 * (float) count_letters(sentence) / (float) count_words(sentence)) - 0.296 * (100 * (float) count_sentences(sentence) / (float) count_words(sentence)) - 15.8;

    if((int) round(grade) < 1){
            printf("Before Grade 1\n");

    } else if ((int) round(grade) >= 16){
            printf("Grade 16+\n");

    } else {
            printf("Grade %i\n", (int) round(grade));
    }
}

int count_letters(string text){

    int letters = 0;
    int length = strlen(text);

    for(int i = 0; i < length; i++){
            if(isupper(text[i]) || islower(text[i])){
                letters++;
            }
    }
    return letters;
}


int count_words(string text){

    int words = 0;
    int length = strlen(text);

    for(int i = 0; i < length; i++){
        if(text[i] == ' '){
            words++;
        }
    }
    return words + 1;
}


int count_sentences(string text){

    int sentences = 0;
    int length = strlen(text);

    for(int i = 0; i < length; i++){
        if(text[i] == '.' || text[i] == '?' || text[i] == '!'){
            sentences++;
        }
    }
    return sentences;
}







