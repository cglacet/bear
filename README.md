> :warning: **Make sure to backup your notes before trying this** just in case, you know computer scientist do make mistakes.

# Automatically add back-references to all your Bear notes

![Alt Text](img/what.gif)

Simply run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/cglacet/bear/master/insert_in_links.sh)"
```

**Beginer tip, how to run a bash command on OSX:** bring spotlight search in by hitting ``⌘ + space``, search for _**terminal**_ and validate you search with ``↵ enter``. A terminal will show up, copy paste the previous command in the terminal then hit ``↵ enter`` to run the [bash][bash] script.


## Why

This idea come from this [question][reddit post] on reddit.

## What 

In Bear note it's possible to have hyperlinks to other notes. 
For now in Bear there are no option to display within a note A any other note B that contains a link to A.

After you ran this script, for every such note B, you'll have a link to B within note A:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/cglacet/bear/master/insert_in_links.sh)"
```

## How

Here is what the **bash script** does:

* install all shell dependencies ([Git][Git] and [Python][Python]) using [Homebrew][Homebrew], 
* download the most recent sources from [here][sources],
* run the python script that actually make all the work: 
  * find all outgoing links from existing notes
  * add incoming links to existing notes.

[bash]: https://www.wikiwand.com/en/Bash_(Unix_shell)
[reddit post]: https://www.reddit.com/r/bearapp/comments/gc2ywl/reverselinks_support/
[Homebrew]: https://brew.sh/
[Python]: https://www.python.org/
[Git]: https://git-scm.com/
[sources]: https://github.com/cglacet/bear