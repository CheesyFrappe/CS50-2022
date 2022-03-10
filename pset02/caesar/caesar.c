#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool only_digits(string arg);
string compute_chiper(string plain, int key);

int main(int argc, string argv[])
{
    int key = 0;
    
    if(argc == 1){
        return 1;
    }

    if(only_digits(argv[1]) && argc == 2){

        key = atoi(argv[1]);
        string plainText = get_string("plaintext: ");

        printf("ciphertext: %s\n", compute_chiper(plainText, key));

        return 0;
    } else{
        printf("Usage: ./caesar key\n");
        return 1;
    }


}

string compute_chiper(string plain, int key){
    int length = strlen(plain);
    int ci = 0;


    for(int i = 0; i < length; i++){
        ci = plain[i];
        if(isupper(plain[i])){
            ci -= 65;
            ci = (ci + key) % 26;
            plain[i] = ci + 65;
        } else if(islower(plain[i])){
            ci -= 97;
            ci = (ci + key) % 26;
            plain[i] = ci + 97;
        }
    }
        return plain;
}

bool only_digits(string arg){

    int length = strlen(arg);

    int counter = 0;
    for(int i = 0; i < length; i++){
        if(arg[i] >= '1' && '9' >= arg[i]){
            counter++;
        } else {
            continue;
        }
    }
    if(counter == (length)){
        return true;
    } else{
        return false;
    }

}