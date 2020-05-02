# Automatically add back-references to all your Bear notes

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

[reddit post]: https://www.reddit.com/r/bearapp/comments/gc2ywl/reverselinks_support/
[Homebrew]: https://brew.sh/
[Python]: https://www.python.org/
[Git]: https://git-scm.com/
[sources]: https://github.com/cglacet/bear