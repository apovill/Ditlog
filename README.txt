Ditlog V0.0.1

Author:
Andrew Povill

Hi reader.

This program right now only works with Alexa format metadata (or any .ale format actually), there's probably a module avalible to parse out some of the xml metadata
but the ale tab separated text is much more intuitive to work with and I can't tell an appreciable difference in stored content.

To get it working with a RED camera I believe you're forced to use Redline, which will take some more work to implement, but I believe that redline finally is out for linux.

The filenames are all expected in an Arri Alexa format, so that should be a priority to extend to multiple types of cameras, like Blackmagics or Canons.

It also should make more use of dictionaries and cleaner more 'python' code, especially to search through the metadata stored on each clip.  For example, a lookup method of "findWhiteBalance" should be able to look up the argument 'White_balance' to automatically use that as a key in the corresponding clip metadata.

I make no promises as to the naming style being consistent, but I tried.

The program is useful enough to generate logs for the most common camera type and lets you efficiently lookup metadata in a human readable format for any specific clip,
so that said, it's good enough to call a Version 0.0.1.

It's written with the perspective of a DIT to generate a quick log on set, bookkeeping.

Tested only in Linux.

I'll keep making this more useful for myself, but it should be useful for others.

I'll also do some proper cleanup of the comments so the methods and classes should be easier to follow.

---
Andrew
