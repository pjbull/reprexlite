# Test

## Not executed block (normal `python` fence)

```python
def not_executed():
    print('hello')

not_executed()
```

## Executed block (`reprexlite` fence)

```reprexlite
def executed():
    print('hello')

executed()
```


## Reference blocks (`reprexlite` fence)

If the `scope` config variable is set to `"page"` then the `reprexlite` blocks on this page share a namespace
so that variables defined in one block are available to subsequent blocks (much like how a notebook works).

Setup a variables

```reprexlite
a = 1
a
```

See if it can be used in next block.

```reprexlite
a += 1
a
```

If the block above has an error, change the mkdocs.yml config `plugins.reprexlite.scope = page`.

## That's all folks!

Let's make sure all the text is included at the end.


Add the ability to create fenced code blocks that are executed at `mkdocs` build time using [`reprexlite`](https://github.com/jayqi/reprexlite).

![](ss.png)

Features include:
 - `page` scope where all `reprexlite` code blocks are executed in order in a common namespace (i.e., "notebook mode").
 - Stop build if reprexlite block raises an error

# `mkdocs.yml` config example

All of the parameters that [reprexlite supports](https://jayqi.github.io/reprexlite/stable/api-reference/reprex/#reprexlite.reprex.reprex) can be passed through at the config level.

In addition to those options, we add three config settings:
 - `scope` - If `block` all of the `reprexlite` blocks on a page have separate namespaces; if `page` the blocks share a namespace
 - `raise_on_error` - If `True`, the `mkdocs build` step will raise an error if any of the `reprexlite` blocks raises an `Exception`.
 - `reprexlite_regex` - Customize the the regex to look for blocks in the markdown; this regex must have a [named group](https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups) called 'code' to work properly. For example, you may want to change the regex to cover all `python` fenced blocks rather than just ones that are explicitly `reprexlite`.

```yaml
site_name: Test Site

plugins:
    - reprexlite:
        session_info: False     # passed through to reprexlite
        comment: "## >  "       # ...
        scope: page             # 'block' each block is isolated, `page` blocks share a namespace
        raise_on_error: False   # if True, break the `mkdocs build` if a reprexlite block errors
```
