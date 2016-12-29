##Kleene

Kleene operators *in regex* work as so:

```
a+ //this will match 1 or more 'a' characters
(hello)+ //this will match 1 or more 'hello' strings (ex. hellohellohello)

a* //this will match 0 or more 'a' characters (becomes optional)
(hello)* //this will match 0 or more 'hello' strings (becomes optional)
```

SpeakPython uses kleene just like regex. In fact, it does use regex's kleene operators!

Example in SpeakPython:

```
//this is a text-based example because of variable use
give me ($item (and)?)+;
@results
    k_0 { k_0<','>($item) }
@
```

###Labels

k_0 is the first kleene that exists in your rule.
K_1 is the second... etc.

###Results

```
k_0 { k_0<DELIM>(RESULTS) }
```

Inside of the round brackets is where we specify what the kleene will return. If we use variables that exist within the kleene such as (... $item ...)+, then the value of $item will iterate over what was captured in the kleene, changing the value of $item each iteration and appending the results together using the delimiter (described later).

In this example, if we say "give me bananas apples and oranges", our result would be "bananas,apples,oranges". This is because the value of $item changes as it evaluates the result if used in a kleene.
##Variables outside the kleene

We can also use variables that exist outside of the kleene, though their values will not change as the kleene iterates.

Note that if you use a variable that has already been defined outside of the kleene, this variable will be overwritten with the kleene's dynamic (changing) result rather than the result that exists outside of the kleene.

```
k_0, place { k_0<','>($place '...' $item) } //$item will change value while $place stays the same
```

###Delimiter <...>

This is where it gets really interesting! We've specified above that we want to use the result of what the kleene was able to match. Well, in the '<>' we are able to specify the joining delimiter(s) between instances of what appears in the '()'.

Not only can we use a string literal as the delimiter, but we can specify a whole list of results, just like within the '()' of the kleene, or just like any rule result.

Ex. This results in 'chicken Toronto, beef Toronto, Cigars Toronto,'
```
{ k_0<' ' $place ', '>($item) }
```

For more usages see the examples in speakpython/SpeakPython/examples/.
- WithoutSpeechRecognition will include more kleene and variable use.

Well now, wasn't that previous example tedious... We had to keep writing 'restaurant', 'cafe' and 'gas' over and over. Wouldn't it be helpful if we had modularity? Well, we can with aliases!