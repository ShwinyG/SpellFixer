"""
Name: Ashwin Gowda asg7954@rit.edu
Purpose: Main function of Spell Fixer project to create an auto correcter
Class: CS141
"""
import sys

from fixer import *

# Global Variables
LEGAL_WORD_FILE = "american-english.txt"
KEY_ADJACENCY_FILE = "keyboard-letters.txt"
ALPHABET = tuple(chr(code) for code in range(ord('a'), ord('z')+1))

def get_wordlst(file_name):
    """
    Gets all the words and puts them in a dictionary
    :param file_name: the inputted file
    :return: a list of all the words in the file separated
    """
    fd = open(file_name)
    wordlst = []
    for line in fd:
        for word in line.split():
            wordlst.append(word)
    fd.close()
    return wordlst


def get_full_dict():
    """
    Sets up a full dictionary to use
    :return:
    """

    dct = {}
    fd = open(LEGAL_WORD_FILE)
    for line in fd:
        key = line
        dct[key[:-1]] = None
    return dct


def get_key_dict():
    """
    Sets up the key dictionary and its value are all the adjacent keys next to them
    :return: the dictionary of adajcent keys
    """
    dct = {}

    fd = open(KEY_ADJACENCY_FILE)

    for line in fd:
        lst = line.split()
        key = lst[0]
        dct[key] = lst[1:]
    return dct


def words(incorrect_words, corrected_words, unknown_words, key_dct, full_dct, wordlst):
    """
    Words mode where it gives the words before they were corrected and what they were corrected too
    :return:
    """
    final_words = []

    for word in wordlst:
        if is_incorrect(word, full_dct):
            new_word =  remove_incorrect_word(incorrect_words, corrected_words, unknown_words, full_dct, key_dct, word)
            final_words.append(new_word)
            if new_word in full_dct:
                incorrect_words.append(word)
                corrected_words.append(new_word)
        else:
            final_words.append(word)
    return final_words


def print_words(incorrect_words, corrected_words, unknown_words, key_dct, full_dct):
    """
    prints words and what they are corrected too
    :param incorrect_words:  a list of incorrect words
    :param corrected_words:  list of corrected words
    :param unknown_words:  all unknown words
    :param key_dct: full dct of keys
    :param full_dct: full dct of all words
    :return:
    """
    for i in range(0, len(incorrect_words)):
        print(incorrect_words[i], " -> ", corrected_words[i])

def is_incorrect(word, full_dct):
    """
    T/F Boolean to check if word is incorrect
    :param word: word that is being checked
    :param full_dct: full dictionary
    :return:
    """
    if word not in full_dct:
        return True
    else:
        return False




def incorrect(wordlst, full_dct):
    """
    Takes all the words and compares them in the dictionary to see whether they are words or not
    :return: A list of incorrect words
    """
    incorrect_words = []
    for elm in wordlst:
        if elm not in full_dct:
            incorrect_words.append(elm)
    return incorrect_words


####################################################################
# Adjacent Key Spell Checker Part
####################################################################


def adjacent_key(incorrect_words, corrected_words, unknown_words, key_dct, full_dct, word):
    """
    Takes the incorrect words and checks if they were mistakenly spelled by hitting an adjacent key
    :param incorrect_words: lst of incorrect words in the file
    :param key_dct: dictionary of all adjacent keys
    :param full_dct: full dictionary of all values
    :return: The new_word or none and all the lists of corrected words / incorrect
    """
    for i in range(len(word)):
        adjacent_keys = key_dct[word[i]]
        for j in adjacent_keys:
            new_word = check(j, i, word, full_dct)
            if new_word is None:
                pass
            else:
                return new_word, corrected_words, incorrect_words, unknown_words
    return None, corrected_words, incorrect_words, unknown_words




def check(letter, n, word, full_dct):
    """
    Checks to see if creating the new word by replacing the letter with the new letter will allow it to be an actual
    word
    :param letter: The letter that is being changed
    :param n: The position of that letter
    :param word: the original word that is misspelled
    :param full_dct: the dictionary of all actual english words
    :return: the new word that is in the dictionary or none if its not in the dictionary
    """
    new_word = ""
    for g in range(0, len(word)):
        if g == n:
            new_word = new_word + letter
        else:
            new_word = new_word + word[g]

    if new_word in full_dct:
        return new_word
    else:
        return None


####################################################################
# Missing Letter Spell checker by adding letter
####################################################################


def missing_letter(incorrect_words, corrected_words, unknown_words, full_dct, word):
    """
    Missing leter function checks the whole word to see if adding a letter allows it to become a word
    :param incorrect_words: all the incorrect words
    :param corrected_words: all corrected words
    :param unknown_words: all unknown words
    :param full_dct: full dictionary
    :param word: word that is being spell checked
    :return:
    """
    for i in range(0, len(word)):
        for j in ALPHABET:
            new_word = add_letters(j, i, word, full_dct)
            if new_word is None:
                pass
            else:
                return new_word, incorrect_words, corrected_words, unknown_words
    return None, incorrect_words , corrected_words, unknown_words



def add_letters(letter, n, word, full_dct):
    """
    Adds an extra letter in each position of the word to see whether it becomes an actual word or not
    :param letter: the extra letter to add in
    :param n: what position to add in
    :param word:
    :param full_dct:
    :return:
    """
    new_word = ""
    for i in range(0, len(word)):
        if i == n:
            new_word = new_word + letter + word[i]
        else:
            new_word = new_word + word[i]
    if new_word in full_dct:
        return new_word
    else:
        return None


####################################################################
# Extra Key Spell Checker by removing the extra letter
####################################################################

def extra_key(incorrect_words, corrected_words, unknown_words, full_dct, word):
    """
    Extra Key spell checker that checks if the user accidentally typed in extra letter by removing one each
    :param incorrect_words:
    :param corrected_words:
    :param unknown_words:
    :param full_dct:
    :param word:
    :return: new word
    """
    for i in range(0, len(word)):
        new_word = remove_letter(i, word, full_dct)
        if new_word is None:
            pass
        else:
            return new_word, incorrect_words, corrected_words, unknown_words
    return None, incorrect_words, corrected_words, unknown_words


def remove_letter(n, word, full_dct):
    """
    helper function for remove letter to actually remove the letter
    :param n:  the position needed to remove the letter
    :param word: word that is being removed
    :param full_dct:  full dictionary
    :return: the new word or none
    """
    new_word = ""
    for i in range(0, len(word)):
        if i == n:
            pass
        else:
            new_word = new_word + word[i]
    if new_word in full_dct:
        return new_word
    else:
        return None



def capitilization(incorrect_words, corrected_words, unknown_words, full_dct, key_dct, word):
    """
    Capitalizes the word or un capitalizes  it depending on whether it is allready capitlized or not
    :param word: the specific word that it is capitilizing
    :return:  the new capitlized word
    """
    ogword = word
    lst = []
    for elt in word:
        lst.append(elt)
    first = lst[0]
    if first.istitle():
        word = word.lower()
    else:
        word = word.capitalize()
    new_word = remove_incorrect_word(incorrect_words, corrected_words, unknown_words, full_dct, key_dct, word)
    if new_word == word:
        unknown_words.append(ogword)
        return None
    else:
        incorrect_words.append(ogword)
        corrected_words.append(new_word)
        return new_word
####################################################################
# Legit Code

def remove_incorrect_word(incorrect_words, corrected_words, unknown_words, full_dct, key_dct, word):
    """
    Main function that manages all other function in which calls each other function
    :param incorrect_words:  list of incorrect words
    :param corrected_words:  list of corrected words
    :param unknown_words:  list of unknown words
    :param full_dct:  dictionary of all words
    :param key_dct: dictionary of adjacent keys
    :param word: word being spell checked
    :return: the new word or same word depending on if it can be corrected
    """

    new_word, corrected_words, incorrect_words, unknown_words = adjacent_key(incorrect_words, corrected_words,
                                                                             unknown_words, key_dct, full_dct, word)
    if new_word != None:
        return new_word
    else:
        new_word, incorrect_words, corrected_words, unknown_words = missing_letter(incorrect_words, corrected_words, unknown_words, full_dct, word)
        if new_word != None:
            return new_word
        else:
            new_word, corrected_words, incorrect_words, unknown_words = extra_key(incorrect_words, corrected_words, unknown_words,full_dct, word)
            if new_word != None:
                return new_word
            else:
                unknown_words.append(word)
                return word

####################################################################


def main():
    mode = str(input("Enter whether to see only the words or lines: "))
    file_name = input("Enter File Name: ")  # Change to input
    corrected_words = []
    unknown_words = []
    incorrect_words = []
    read_words = get_wordlst(file_name)
    full_dct = get_full_dict()
    key_dct = get_key_dict()
    final_lst = words(incorrect_words, corrected_words, unknown_words, key_dct, full_dct, read_words)
    s = " "
    beginning_lst = s.join(read_words)


    print(beginning_lst)
    if mode == "words":
        print_words(incorrect_words,corrected_words,unknown_words, key_dct, full_dct)
    elif mode == "lines":
        print(s.join(final_lst))
    print(len(read_words), " words read from the file")
    print(len(incorrect_words), "Corrected Words")
    print(incorrect_words)
    print(len(unknown_words), "Unknown Words")
    print(unknown_words)


if __name__ == '__main__':
    main()
