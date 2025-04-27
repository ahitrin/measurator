Read file:
```
F,2019-11-13 11:10,2019-11-18 09:00,,Could I fix all failing tests in TASK-13267 until the end of the week? 90%-No
F,2019-11-13 11:10,2019-11-18 09:00,,Could I start to work on NSDPRJ-2313 until the end of the week? 90%-Yes
F,2019-11-14 13:10,2019-12-03 07:00,,Ticket NSDPRD-13339 needs no more than 1d 4h
S,2019-11-14 13:10,2020-01-20 08:00,,Ticket NSDPRD-12928 needs no more than 5d
S,2019-11-17 18:10,2019-11-18 07:00,,Will any test fail in the branch NSDPRD-13267-pre1? 90%-Yes
S,2019-11-18 10:32,2019-11-23 00:00,,Could I move NSDPRD-13267 into review til the end of week? 90%-Yes
F,2019-11-19 14:10,2019-11-26 07:00,,NSDPRD-13445: needs no more than 8h? 90%-Yes
S,2019-11-25 14:50,2019-11-30 07:00,,NSDPRD-13339: could finish it in a week? 90%-Yes
F,2019-11-29 11:49,2019-12-04 08:00,,NSDPRD-13440: could finish in 2d? 90%-Yes
S,2019-12-02 12:58,2019-12-07 08:00,,Will I be able to start Junit5 or PMD tickets til the end of week? 90%-Yes
F,2019-12-05 12:58,2019-12-10 07:00,,NSDPRD-13575: will 4h be enough? 90%-Yes
F,2019-12-09 13:19,2020-01-10 08:00,,NSDPRD-13547: will 12h be enough? 90%-Yes
N,2020-01-14 11:02,2020-03-01 08:00,,NSDPRD-13544: will 13d be enough? 90%-NO
N,2020-01-14 11:02,2020-03-01 08:00,,NSDPRD-13544: will 26d be enough? 90%-YES
```

Current time is 2020-01-31 12:00.

Program output:
> Successful predictions (total time): 41%, not done yet:2

> Successful predictions (half time): 42%, not done yet:2

> Add another prediction? Yes/*No*/List

User input:
> L

Program output:
> 2020-03-01 08:00: NSDPRD-13544: will 13d be enough? 90%-NO

> 2020-03-01 08:00: NSDPRD-13544: will 26d be enough? 90%-YES

File is written:
```
F,2019-11-13 11:10,2019-11-18 09:00,,Could I fix all failing tests in TASK-13267 until the end of the week? 90%-No
F,2019-11-13 11:10,2019-11-18 09:00,,Could I start to work on NSDPRJ-2313 until the end of the week? 90%-Yes
F,2019-11-14 13:10,2019-12-03 07:00,,Ticket NSDPRD-13339 needs no more than 1d 4h
S,2019-11-14 13:10,2020-01-20 08:00,,Ticket NSDPRD-12928 needs no more than 5d
S,2019-11-17 18:10,2019-11-18 07:00,,Will any test fail in the branch NSDPRD-13267-pre1? 90%-Yes
S,2019-11-18 10:32,2019-11-23 00:00,,Could I move NSDPRD-13267 into review til the end of week? 90%-Yes
F,2019-11-19 14:10,2019-11-26 07:00,,NSDPRD-13445: needs no more than 8h? 90%-Yes
S,2019-11-25 14:50,2019-11-30 07:00,,NSDPRD-13339: could finish it in a week? 90%-Yes
F,2019-11-29 11:49,2019-12-04 08:00,,NSDPRD-13440: could finish in 2d? 90%-Yes
S,2019-12-02 12:58,2019-12-07 08:00,,Will I be able to start Junit5 or PMD tickets til the end of week? 90%-Yes
F,2019-12-05 12:58,2019-12-10 07:00,,NSDPRD-13575: will 4h be enough? 90%-Yes
F,2019-12-09 13:19,2020-01-10 08:00,,NSDPRD-13547: will 12h be enough? 90%-Yes
N,2020-01-14 11:02,2020-03-01 08:00,,NSDPRD-13544: will 13d be enough? 90%-NO
N,2020-01-14 11:02,2020-03-01 08:00,,NSDPRD-13544: will 26d be enough? 90%-YES
```
