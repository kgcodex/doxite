# Doxite Markdown Render Test

This is a normal paragraph with *bold text*, _italic text_, `inline code`, a [link](https://google.com), and an ![image](https://picsum.photos/400).

## Heading Level 2

Another paragraph with mixed inline formatting.

This paragraph contains:
- plain text
- *bold*
- _italic_
- `code`
- [link](https://google.com)
- ![image](https://picsum.photos/400)

### Heading Level 3

> This is a quote block.
>
> It spans multiple lines.
>
> It also contains *bold text*, _italic text_, and `inline code`.

#### Heading Level 4

```python
def greet(name: str) -> None:
    print(f"Hello, {name}")
```

##### Heading Level 5

Unordered list example:

- First item
- Second item
- Third item with *bold*
- Fourth item with _italic_
- Fifth item with `code`
- Sixth item with a [link](https://google.com)
- Seventh item with an ![image](https://picsum.photos/400)

###### Heading Level 6

Ordered list example:

1. First ordered item
2. Second ordered item
3. Third ordered item with *bold*
4. Fourth ordered item with _italic_
5. Fifth ordered item with `code`
6. Sixth ordered item with a [link](https://google.com)
7. Seventh ordered item with an ![image](https://picsum.photos/400)

# Mixed Blocks

This is a paragraph before a quote.

> Quote line 1
> Quote line 2
> Quote line 3 
quote continue

This is a paragraph after a quote.

# Consecutive Paragraphs

First paragraph.

Second paragraph.

Third paragraph with *bold*, _italic_, and `code`.

# Consecutive Lists

- Apple
- Banana
- Orange

- Another list
- With more items
list continue

1. Ordered one
2. Ordered two
3. Ordered three

1. Another ordered list
2. Continued
ordered continue

# Code Block Stress Test

```text
`inline code inside fenced code`
*bold inside fenced code*
_italic inside fenced code_
[link](https://example.com)
![image](img.png)
```


# Weird Inline Cases

This should remain plain text:

`unclosed code

*unclosed bold

_unclosed italic

[broken link](https://google.com

![broken image](https://picsum.photos/400

# Adjacent Inline Formatting

*bold*_italic_`code`[link](https://google.com)![img](https://picsum.photos/400)

# Nested-like Inline Input

This parser does not support nesting, but these are useful tests:

*bold _inside_*

_italic *inside*_

`code *inside* _inside_`

# Long Paragraph

Lorem ipsum dolor sit amet, consectetur adipiscing elit. *Bold text* appears here, followed by _italic text_, then `inline code`, and finally a [link](https://google.com). Another sentence continues the paragraph to test paragraph rendering over larger bodies of text. Here is another ![image](https://picsum.photos/400) included inline.

# Empty Inline Blocks

``

__

**

# End Of File Test

Final paragraph with *bold*, _italic_, `code`, [link](https://google.com), and ![image](https://picsum.photos/400).



