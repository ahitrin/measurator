# Measurator

This application is inspired by the book ["How to measure anything"][book] which I've bought several years ago.

It implements following idea from the book: if you want to make good predictions in some field, you need to _calibrate_ yourself regularly.
This simply means following:

* You make predictions/guesses about something
* Then you evaluate your predictions: are they successful or not
* Then you calculate a total percent of your successful predictions.

If this percent is too low, then your next predictions must use wider borders.

## When it could be useful

I use it in my work to calibrate predictions about key points of my tasks.
E.g.: "ticket X will go into code review til the given date".
I run this script during morning routine, and when the specified date occurs, the script asks me whether the key point is reached.

## Usage

Install it from the source:

```shell
$ pip3 install --user .
```

Then, run `measure` script that asks you for the next prediction.

For more examples, please examine `.md` files in the [tests](measurator/tests) directory.

## Aknowledges

Thanks @hgenru who asked me to opensource this simple code!

[book]: https://www.howtomeasureanything.com/3rd-edition/