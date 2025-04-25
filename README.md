# kitty plotnine (k-nine)
Plot graphs directly in the terminal with shell one-liners.

Use the [grammar of graphics](https://vita.had.co.nz/papers/layered-grammar.pdf) library [plotnine](https://plotnine.org/) from the command-line if your terminal supports kitty's terminal graphics protocol.

# Motivation
You probably don't want to do this. Start up `jupyter`, use `subprocess.check_output` to fetch some data and proceed to do analysis in the normal way in jupyter keeping track of everything your have done and doing a bit of analysis. But isn't that just so much *effort*; doesn't the browser suck with all the clicking; wouldn't you like to see help inline.

If you are are sufficiently lazy to want to make some more work for yourself you can use this library to do your plotting directly in the shell with single commands.

A number of terminals including KDE's Konsole, kitty, wezterm, and  ghostty (you should not use ghostty for a few reasons (*)) now support graphics in the browser. You can use these to create images directly in the terminal. This can be used together with plotnine to plot in the terminal. This has some nice properties, you can read output from shells and scroll back to early graphs.







# Alternatives and prior work
This tool combines three properties. Being able to plot from the terminal with a "one-liner" - a shell expression written in one line; being able to plot in high resolution in the terminal; being trivial to install and use . In this regard, I believe this tool is unique but the components which it comprises of are not.

I could not find any other command-line plotting tools aimed at the graphics terminal protocol. There are many command-line libraries to produce this output. I am using
[matplotlib-backend-kitty](https://github.com/jktr/matplotlib-backend-kitty), [kitcat](https://github.com/mil-ad/kitcat) is an alternative for Python. It would be comparatively simple to produce an image of plot in any language and render it with one of kitty's image programs such as [icat](https://sw.kovidgoyal.net/kitty/kittens/icat/) or [timg](https://github.com/hzeller/timg).

There are other approaches to rendering graphics within the terminal than the graphics terminal protocol, but these are of a lower resolution. These tend to use characters to represent graphical components. One such exapmle is the [sixel](https://github.com/saitoha/libsixel) library.

There are other tools that can be run from the command-line and plot in another window. [gnuplot](https://jasonmurray.org/posts/2020/basicgnuplot/) can plot from the command-line (rendering in an X) but the syntax is not terribly succinct. [sparklines](https://github.com/deeplook/sparklines) with produce a spark-line, these are very succinct plots that are good at showing the rate of change.

# Usage
Make sure your terminal supports the [terminal graphics protocol](https://sw.kovidgoyal.net/kitty/graphics-protocol/). If you are using tmux (and potentially other terminal multiplexers) you need to use a terminal which supports "unicode placeholder characters". At the time of writing the only usable terminal emulator seems to be kitty (ghostty supports this feature - but should not be used). If you are not using a terminal multiplexer and of kitty, wezterm or konsole would work (or ghostty - which you shoiuld not use).

You can test you terminal with the following command (assuming you have `ffmpeg` and `timg` installed):

```
ffmpeg -filter_complex "color=purple, drawtext=text=k-nine:fontsize=h" -frames:v 1 -f apng - | timg -V -pk -


```

k-nine read input from standard in in a number of formats and attempts convert the data into a useable format. It support CSV, space separated numbers and, JSONL formats. The [jq](https://jqlang.org/) or [npcli](https://pypi.org/project/npcli/) tools may be useful for preparing data for input into `k-nine` since `k-nine` has very limited ability to redner data.


The following creates a histogram from the numbers 1 to 100.

```
seq 100 | k-nine 'aes(x="one") + geom_histogram(bins=12)'
```


## Security
Do not use unknown data to generate the expression used in `k-nine`. This expression is evaluated using Python's eval mechanism. Well you can if you like... but people could potentially use an escaping attack to run arbitrary code.


## An introduction to the Graphics of Grammer
This library is a thin wrapper around the python [plotnine](https://plotnine.org/) library. Unfortunately, likely owing to the fact that plotnine is a reimplementation of [ggplot2](https://ggplot2.tidyverse.org/) which is a broadly understood tool, the *introductory* documentation for plotnine is not very complete. So I shall offer a small introduciton here. You may prefer to review the [ggplot2 documentation](https://ggplot2.tidyverse.org/).

The basic idea of the graphics of grammar is to try to produce graphs in a very expressive way. Separate aspects of plotting and represented by different expressions and then these expressions are combined with the `+` symbol.

Properties of plotting are:

* Loading of data (this handled by k-nine)
* The mapping of data to graphical properties such as poistion or color referred to as aes.
* The grouping of data plotted on the same line. Represented by `group` in the `geom_aes` mapping
* The faceting of data to different plots (e.g. `facet_grid`)


## About me
I am @readwithai



## Notes
[*] Unfortunately ghostty seems to be [childishly and poorly managed](https://x.com/readwithai/status/1910398678306865269). If you care about good open and non-authoritarian control of projects you should pick on of the other good terminals.
