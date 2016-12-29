# What is SPS?

SPS is an extension that stands for Speech Phrase Specification. Any file named '[appName].sps' will contain all of the phrases you wish your program to recognize, as well as the results upon recognition.

# SPS Format

[Simple SPS Rules](Simple-SPS-Rules.md)

[Variables](Variables.md)

[Aliases / Functions](Aliases.md)

[Kleene (Repetition)](Kleene-Repetition-Rules.md)

## Rule Types Index

Here's a list of rule formats for reference:

```
() #allows anonymous grouping (won't capture)
[] #allows numbered groupings (captures as 0, 1, 2, ..., etc depending on position in phrase)
|  #allows OR-ing between two phrases
(...)+  #allows one or more of the phrase (similar to regex)
(...)*  #allows zero or more of the phrase (kleene star in regex)
(...)?  #allows a phrase to be optional (requires brackets around phrase)

***only text-based***

$var
    #variables - allows the definition of a variable that matches any word **only usable in purely text-based applications**
    #variables are, by default, caught using the regex [a-zA-Z0-9\.]+

/[@#$%^&\*]+/r
    #this is a custom regex and can be used to specify any sort of regex you would like to match.
    #format: /my regex/r

```

**Please note that variable and regex usage are only allowed in purely text-based applications at this time as the speech recognition relies on knowing the speech possibilities as a formal grammar. Future work will include implementing a statistical method of determining recognition for variable instances.**

#Encompassing Example

```
//this is our function for use in the below rule
#placeType() = [restaurant] | [cafe] | [gas station];
@results
    1 { "restaurant" }
    2 { "cafe" }
    3 { "gas" }
@

show me the [nearest | closest] #placeType (to $place)? (that has ($item (and)?)+)?;
@results
    //take note of the usages of double and single quotes. If you need to use a certain type of quote in your result, choose the other kind of quote as your surrounding quotation.
    #placeType { "closest('" #placeType "')" }

    //here, we utilize the variable $place to output whatever may have been said in place ;) of $place
    #placeType place { "closest('" #placeType "', '" $place "')" }
    
    //now let's handle that pesky kleene. How could we possibly do this?
    //k_0 { k_0<','>($item) }
    #placeType, place, k_0 { "closest('" #placeType "', '" $place "', '" k_0<','>($item) "')" }
@
```

Now let's incorporate our SPS into python! Take a look at the [Usage Patterns](Usage-Patterns.md) of SpeakPython. It's really easy!
