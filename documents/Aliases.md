## Aliases

###Example

```
#myAlias() = this is my alias definition;
```

The above alias is simply a reusable name given to a speech phrase. This alias will recognize 'this is my alias definition' wherever we place it within a rule.

Results may be used with aliases to obtain those results in whichever rule is making use of the alias.
This allows some sort of modularity when creating speech phrases.

**DO NOT DEFINE ALIASES RECURSIVELY, OR CIRCULARLY**

- because alias definitions are directly inserted as regex into a rule, a recursive definition will require that an infinite amount of expansions are performed on the regex. Your computer might explode (kidding).

###Example Usage

Our alias:

```
#myAlias() = this is my ([alias] | [function]) definition;
@results
    0 {'it was an alias'}
    1 {'it was a function'}
@
```

This is an example usage of the above alias:

```
they say (that)? #myAlias;
@results
    #myAlias { 'They said ' #myAlias '.' }
@
```

Our results:

- 'they say that this is my alias definition' ---> 'They said it was an alias.'
- 'they say that this is my function definition' ---> 'They said it was a function.'

###Conclusion

Now you know how to make your speech applications conveniently modular!

For more advanced usages that involve recursion, you can learn about using [kleene](https://bitbucket.org/matthew3/speakpython/wiki/Kleene%20(Repetition)%20Rules)