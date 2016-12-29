#Summary

**Variables are strictly for text-only applications.**

A variable will allow you to match any word you'd like. The default regex for matching words is ```[a-zA-Z\.]+```. This is planned to be changeable in the ```@options``` section, which is not yet functional.

#Anatomy

```
<phrase> $myVar <phrase>;
@results
    <label(s)>, myVar { <results...> $myVar <results...> }
    <label(s)> { <results...> }
    ...
@
```

#Example

```
turn the $colour light on;
@results
    $colour { 'turnOn("' $colour '")' }
@
```

this example will work like this in practice:

**input:** "turn the turqoise light on"

**matches:** {'colour': 'turqoise'}

**result:** turnOn("turqoise")

#Labels

variables can be referenced as labels by stating ```$<variableName>``` or just ```<variableName>``` in the labels section, just as the example above does.

The next step is to learn about [Aliases](Alias.md).