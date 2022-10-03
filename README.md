# acronym_generator
This Python code assist the creation of project acronyms.

By default it only matches uppercase letters in the title, although this can be changed with parameter case_sensitive.

The default behaviour allows one to declare what characters/words are relevant by using combinations of uppercase and lowercase 
characters. 

For example, if title is "ACT for CLIMATE",
no letter from the word "for" needs to be in the acronym and results such as CLIMA (aCt for cLIMAte) will be proposed. 

A word with at least one uppercase letter will be however necessarily present in the acronym 
(with at least one of its uppercase characters).



