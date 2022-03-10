#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool only_digits(string arg);
string compute_word(string plain, string codex);
bool is_duplicated(string arg);

int main(int argc, string argv[])
{

    if(argc == 1){
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if(is_duplicated(argv[1])){
        return 1;
    }

    if(only_digits(argv[1]) && argc == 2){
        string crypt = argv[1];

        string plainText = get_string("plaintext: ");

        printf("ciphertext: %s\n", compute_word(plainText, crypt));
        return 0;
    } else {
        printf("Usage: ./substitution key\n");
        return 1;
    }

}

string compute_word(string plain, string codex){

    int length = strlen(plain);
    int index = 0;

    for(int i = 0; i < length; i++){
        index = plain[i];

        if(isupper(plain[i])){

            index -= 65;

            if(islower(codex[index])){
                plain[i] = codex[index] - 32;
            } else{
                plain[i] = codex[index];

            }

        } else if (islower(plain[i])){

            index -= 97;

            if(isupper(codex[index])){
                plain[i] = codex[index] + 32;
            } else{
                plain[i] = codex[index];
            }

        }
    }
    return plain;
}

bool only_digits(string arg){
    int length = strlen(arg);

    int counter = 0;
    for(int i = 0; i < length; i++){
        if((arg[i] >= 'a' ||  arg[i] >= 'A') && ('z' >= arg[i] || 'Z' >= arg[i])){
            counter++;
        } else {
            break;
        }
    }

    if(counter == 26){
        return true;
    } else{
        return false;
    }
}

bool is_duplicated(string arg){
    int length = strlen(arg);

    for(int i = 0; i < length; i++) {
        for(int j = i + 1; j < length; j++){
            if(arg[j] == arg[i]){
                return true;
            }
        }
    }
    return false;
}