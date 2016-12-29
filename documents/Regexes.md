## Regexes

Finding that the SPS format isn't dynamic enough to handle your use case? Simply use a regex.

###Results

You may utilize the result of a regex by specifying r_# where # is the index of the regex within the speech phrase, starting from 0.

###Example

```
this is my /custom[ ]+regex/r;
@results
    r_0 { 'custom regex' }
@
```

- 'this is my custom       regex' ---> 'custom regex'
- 'this is my custom regex' ---> 'custom regex'

The above example demonstrates how to use a custom regex within a speech phrase. This regex will match exactly the specified characters, just as a normal regex does. First, "this is my" will be matched, and then your regex will take effect.

###Specifying Subgroups In Results

You are able to specify groups within your regex, just like normal regexes. These groups can be accessed by stating the index of your regex like so: r_#,

and then specifying your group's name within quotes.

Altogether, it will look like this:

r_0("my_regex_group_name")

###Example

```
/this is/r  my ( /(?<quantifier>(more|less) complex regex/r | /regex/r )
@results
   r_0 { "A regex" }
   r_0, r_1 { "A " r_1('quantifier') " complex regex" }
@
```

*Note:* there is an 'OR' between our final two regexes

Our results:

- 'this is my regex' ---> 'A regex'
- 'this is my more complex regex' ---> 'A more complex regex'
- 'this is my less complex regex' ---> 'A less complex regex'

###Conclusion

Now you know how to match absolutely any type of text possible with regex, and utilize them to build up your results!