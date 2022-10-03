# acronym_generator
This Python code assist the creation of project acronyms.

By default it only matches uppercase letters in the title, although this can be changed with parameter case_sensitive.

The default behaviour allows one to declare what characters/words are relevant by using combinations of uppercase and lowercase 
characters. 

For example, if title is "ACTing for CLIMATE",
no letter from the word "for" needs to be in the acronym and results such as CLIMA (aCting for cLIMAte) will be proposed:
- Loercase parts, as the "ing" ending of word "ACTing" are not selectable for th acronym.
- All words with at least one uppercase letter will contibute to the acronym  with at least one of its uppercase characters.

The code also loads a file with stopwords, that is, words that will be considered optional by default.   



