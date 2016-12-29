#Summary

To define a rule for recognition, we simply type a sentence that ends in a semi colon:

This will allow recognition of a simple command, but isn't very useful yet as we have no results being returned from this speech phrase.

#Anatomy

```
<phrase>;
@results
    <label(s)> { <results...> }
    <label(s)> { <results...> }
    ...
@
```

#Example

```
[turn the red light on];
@results
    0 { 'turnOn("red")' }
@
```

This example will contain the label-value pair once recognized:

{'0': 'turn the red light on'}
#Labels

Notice how we add square brackets to our phrase. Square brackets allow capturing sections of the phrase as a numbered group (starting at 0). This will allow us to specify which result we would like to utilize by adding the 0 as a label.
Determined by square brackets [...] within the speech phrase.

NOTE: Labels are always zero-based! Let's face it, we're programmers.

Good! You now have a working simple speech phrase. Let's add some complexity to this phrase: