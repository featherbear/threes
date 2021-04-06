# Threes

> Instagram 3 x n Content Spacer 

---

![](https://featherbear.cc/blog/uploads/5.jpg)

## Rationale

So I used to post images as `3 x n` (length x height) tiles on [Instagram](https://www.instagram.com/_andrewjwong/) but I've decided that it's too much effort to do for all my photos - and it probably had stunted my creative willingness.

In the future I'd like to just post single images - however that would cause my old `3 x n` images to be misaligned. Now there _are_ only like 15 or so of those types of images, but I didn't want to delete them.  
Instead I wrote some code to automatically (un)archive some spacer posts in order to maintain the alignment!

---

## Setup

### Installation

I'm using [`poetry`](https://python-poetry.org/) as the Python package manager, so use `poetry install`

### Configuration

1) Copy the `.env.example` file to `.env`  
2) Fill in the required fields

#### Spacer IDs

There are two types of ID that are required by the underlying API wrapper - `short code`, and `media id`.  
The **short code** is the tag that you see at the end of a post if you copy its share link - i.e. the `CNNVgtGn95F` in `https://www.instagram.com/p/CNNVgtGn95F/`.  
The **media id** - uhhhh well I did some snooping to find it.

---

## License

Copyright © 2021 Andrew Wong

This software is licensed under the MIT License.  
You are free to redistribute it and/or modify it under the terms of the license.
