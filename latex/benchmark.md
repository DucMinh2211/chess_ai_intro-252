## Alpha Beta Benchmark Results
| Game No. | Bot          | Opponent                 | Result | Avg. Time/Move (s) | AI Moves |
| -------- | ------------ | ------------------------ | ------ | ------------------ | -------- |
| 1        | D = 1, Q = 0 | Chess.com AI lv1 (250)   | LOST   | 0.01353            | 35       |
| 2        | D = 3, Q = 0 | Chess.com AI lv1 (250)   | WIN    | 0.70852            | 15       |
| 3        | D = 3, Q = 2 | Chess.com AI (250) lv1   | WIN    | 0.83383            | 13       |
| 4        | D = 3, Q = 0 | Chess.com AI lv2 (400)   | WIN    | 0.60628            | 26       |
| 5        | D = 3, Q = 2 | Chess.com AI lv2 (400)   | WIN    | 0.90193            | 18       |
| 6        | D = 3, Q = 0 | Chess.com AI lv3 (550)   | WIN    | 0.61904            | 27       |
| 7        | D = 3, Q = 0 | Chess.com AI lv4 (700)   | WIN    | 0.79803            | 41       |
| 8        | D = 3, Q = 2 | Chess.com AI lv4 (700)   | WIN    | 0.49739            | 28       |
| 9        | D = 3, Q = 0 | Chess.com AI lv6 (1000)  | WIN    | 0.55618            | 46       |
| 10       | D = 3, Q = 0 | Chess.com AI lv9 (1300)  | LOST   | 0.46624            | 31       |
| 11       | D = 3, Q = 2 | Chess.com AI lv9 (1300)  | WIN    | 0.59392            | 59       |
| 12       | D = 3, Q = 2 | Chess.com AI lv12 (1600) | WIN    | 0.60322            | 46       |
| 13       | D = 3, Q = 2 | Chess.com AI lv14 (1800) | DRAW   | 1.51931            | 9        |
| 14       | D = 3, Q = 2 | Chess.com AI lv14 (1800) | DRAW   | 0.73227            | 9        |
| 15       | D = 3, Q = 4 | Chess.com AI lv14 (1800) | LOST   | 2.63535            | 43       |
| 16       | D = 3, Q = 6 | Chess.com AI lv14 (1800) | LOST   | 2.51426            | 16       |
| 17       | D = 4, Q = 0 | Chess.com AI lv14 (1800) | LOST   | 2.26201            | 94       |
| 18       | D = 4, Q = 3 | Chess.com AI lv14 (1800) | DRAW   | 14.02260           | 71       |
### No 1
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.03"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "1-0"]
[BlackElo "594"]
[WhiteElo "250"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.03"]
[Link "https://www.chess.com/game/computer/1034610857"]

1. e4 Nf6 2. e5 Nc6 3. Be2 Nxe5 4. b4 d5 5. Bb5+ Bd7 6. Bxd7+ Qxd7 7. a3 e6 8. a4 Bxb4 9. Nh3 Qxa4 10. Rxa4 Bxd2+ 11. Nxd2 O-O 12. g3 Ne4 13. Rxe4 dxe4 14. Nxe4 Rfe8 15. Rf1 Rad8 16. Qxd8 Rxd8 17. Bf4 Rd2 18. Nf6+ gxf6 19. Bxd2 f5 20. f4 Kf8 21. Bc1 Ke7 22. fxe5 f4 23. Ba3+ Kd7 24. Rf3 fxg3 25. hxg3 Kc6 26. Nf4 h6 27. Rd3 a6 28. Rd6+ cxd6 29. exd6 e5 30. Ke2 exf4 31. gxf4 Kd5 32. Kd3 h5 33. d7 h4 34. d8=Q+ Ke6 35. Qc8+ Kd5 36. c4# 1-0
```

### No 2
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "250"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1034746199"]

1. e4 Nf6 2. e5 Ne4 3. a4 Nc6 4. Bd3 Nc5 5. a5 d6 6. Bf5 Bxf5 7. c3 Nd3+ 8. Ke2 dxe5 9. g3 Qd5 10. Na3 Qxh1 11. h4 Bg4+ 12. Kxd3 Bxd1 13. b3 Qxg1 14. Ke3 Qe1+ 15. Kd3 Qe2# 0-1
```
Chess.com Score = 78

### No 3
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "250"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1034687203"]

1. e4 Nf6 2. e5 Ne4 3. a4 Nc6 4. Bc4 Nxe5 5. Qe2 d5 6. f4 Nxc4 7. b4 Qd6 8. Ba3 Qxf4 9. Ra2 Bg4 10. d4 Bxe2 11. Nf3 Qe3 12. g4 Nxa3 13. Rxa3 Qf2# 0-1
```

### No 4
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.03"]
[Round "?"]
[White "Komodo2"]
[Black "0GSlay0"]
[Result "0-1"]
[TimeControl "?"]
[WhiteElo "400"]
[BlackElo "594"]
[Termination "0GSlay0 won by checkmate"]
[ECO "A15"]
[EndDate "2026.04.03"]
[Link "https://www.chess.com/game/computer/1034821455"]

1. c4 Nf6 2. g3 Ng4 3. Qb3 Nc6 4. f3 Na5 5. a3 Nxb3 6. Nh3 Ne5 7. Ng5 Nxa1 8. h4
Nb3 9. d4 Nxc4 10. Rh3 Nxc1 11. e4 d5 12. Nd2 Bxh3 13. Nxh3 Nxd2 14. Kxd2 Nb3+ 15. Kd1 Nxd4 16. Bg2 Qd7 17. b3 dxe4 18. fxe4 Nxb3+ 19. Kc2 Nd4+ 20. Kd1 Qg4+ 21. Kc1 Qxg3 22. h5 Qxg2 23. Kb1 Qc2+ 24. Ka1 Rg8 25. Ng1 Rh8 26. Ne2 Nb3# 0-1
```

### No 5
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "400"]
[Termination "by checkmate"]
[ECO "A16"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035106479"]

1. c4 Nf6 2. Nc3 Nc6 3. Qc2 Nd4 4. Qd3 e5 5. g3 d5 6. Kd1 Bf5 7. cxd5 Bxd3 8.
exd3 Nxd5 9. Ne4 Bb4 10. Nd6+ Qxd6 11. g4 Qg6 12. a3 Qxg4+ 13. Ne2 Qf3 14. axb4 Qxh1 15. Nxd4 Qxf1+ 16. Kc2 exd4 17. Kb1 Qxd3+ 18. Ka2 Nxb4# 0-1
```

### No 6
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "550"]
[Termination "by checkmate"]
[ECO "A40"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035180869"]

1. d4 Nc6 2. Nf3 Nf6 3. h3 d5 4. Kd2 Ne4+ 5. Ke1 Be6 6. Rg1 Qd6 7. a4 Qb4+ 8. c3 Qd6 9. Nh2 Qxh2 10. Qd3 Qxg1 11. g4 Qxf2+ 12. Kd1 Qxf1+ 13. Kc2 Nf2 14. Bf4 Nxd3 15. exd3 Qxf4 16. b4 Qf1 17. Kd2 O-O-O 18. Kc2 Kb8 19. Kb2 Rg8 20. Ka3 Qxd3 21. b5 Nxd4 22. Ra2 Qxb1 23. cxd4 Bxg4 24. Rb2 e5+ 25. Kb3 Bd1+ 26. Kc3 Qc1+ 27. Kd3 e4# 0-1
```

### No 7
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "700"]
[Termination "by checkmate"]
[ECO "C25"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035248843"]

1. e4 Nf6 2. Nc3 Nc6 3. g3 e5 4. b3 Bb4 5. Bb2 Nd4 6. Bd3 d5 7. Bb5+ Kf8 8. Nxd5 Nxd5 9. f4 Ne3 10. Bxd4 Qxd4 11. Qc1 Bxd2+ 12. Qxd2 Qxa1+ 13. Ke2 Qf1+ 14. Kxe3 Qxb5 15. h3 Qb6+ 16. Kf3 Be6 17. fxe5 f6 18. exf6 gxf6 19. Qf2 Bg4+ 20. hxg4 Qc6 21. Qf1 Qxc2 22. Qe2 Qc1 23. Rh5 Qxg1 24. Rc5 Qxc5 25. Qf2 Qe7 26. Qd4 c5 27. Qc3 Kg7 28. g5 Rhe8 29. gxf6+ Qxf6+ 30. Qxf6+ Kxf6 31. Kf2 Rxe4 32. a3 Rg8 33. Kg2 Rf4 34. a4 Ke5 35. a5 Rg7 36. a6 bxa6 37. Kh3 Rf2 38. b4 cxb4 39. g4 Kf4 40. g5 Rxg5 41. Kh4 Rh2# 0-1
```

### No 8
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Beginner"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "700"]
[Termination "by checkmate"]
[ECO "A40"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035293017"]

1. d4 Nc6 2. Nf3 Nf6 3. h4 d5 4. Qd2 Bg4 5. Ng5 h6 6. Rh3 hxg5 7. g3 Ne4 8. b4
Nxd2 9. Bxd2 Bxh3 10. Bxh3 gxh4 11. gxh4 Rxh4 12. e3 Rxh3 13. Kf1 e5 14. c3 Bd6 15. c4 dxc4 16. Be1 Rh1+ 17. Ke2 exd4 18. Na3 Bxb4 19. Bxb4 Rxa1 20. Nxc4 d3+ 21. Kd2 Nxb4 22. a3 Nc2 23. Ne5 Rxa3 24. Nc4 Ra2 25. f4 Qd5 26. Na5 Nxe3+ 27. Kc3 c5 28. Nb3 Qc4# 0-1
```

### No 9
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Intermediate"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "1000"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035388483"]

1. e4 Nf6 2. e5 Ne4 3. Na3 Nc6 4. Qg4 d5 5. Qh5 e6 6. f3 g6 7. Qh3 Ng5 8. Qh4
Nxf3+ 9. Nxf3 Qxh4+ 10. Nxh4 g5 11. Nf3 g4 12. Nh4 Be7 13. Ng6 hxg6 14. Nb5 Kd7 15. c3 a6 16. d4 axb5 17. Bxb5 Bh4+ 18. g3 Bxg3+ 19. Ke2 Bxh2 20. Kf1 Bxe5 21. dxe5 Rxh1+ 22. Kg2 Rh8 23. Bd2 Re8 24. Bxc6+ Kxc6 25. Be3 Bd7 26. Rd1 Rxa2 27. Rb1 Rd8 28. Bh6 Rh8 29. Rh1 Rxb2+ 30. Kg3 g5 31. Rh5 Kc5 32. Rxg5 Rxh6 33. Kxg4 Rg2+ 34. Kf4 Rh4+ 35. Rg4 Rhxg4+ 36. Ke3 Re4+ 37. Kf3 Ree2 38. Kf4 Rgf2+ 39. Kg3 Bc6 40. Kg4 Rxe5 41. Kg3 Rc2 42. c4 Rxc4 43. Kf2 Rc3 44. Kg1 Re2 45. Kf1 Bb5 46. Kg1 Rc1# 0-1
```

### No 10
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Intermediate"]
[Black "0GSlay0"]
[Result "1-0"]
[BlackElo "594"]
[WhiteElo "1300"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035435891"]

1. e4 Nf6 2. e5 Ne4 3. Qg4 d5 4. Qd1 Nc6 5. d3 Nc5 6. d4 Ne6 7. Nf3 Nexd4 8.
Nxd4 Nxe5 9. f4 Bg4 10. Be2 Bxe2 11. Qxe2 Nc4 12. Na3 Nd6 13. Nab5 Nc4 14. b3 c5 15. O-O cxd4 16. Nxd4 Nd6 17. Qf3 Qb6 18. Be3 Ne4 19. c4 e5 20. fxe5 Kd8 21. Qxf7 dxc4 22. Ne6+ Qxe6 23. Qxe6 c3 24. Qf7 c2 25. Qxb7 Rc8 26. e6 Rc7 27. Qa8+ Ke7 28. Rf7+ Kxe6 29. Rxc7 Nc5 30. Qf3 Nxb3 31. Qe4+ Kf6 32. Rf1# 1-0
```

### No 11
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Intermediate"]
[Black "0GSlay0"]
[Result "0-1"]
[BlackElo "594"]
[WhiteElo "1300"]
[Termination "by checkmate"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035583599"]

1. e4 Nf6 2. e5 Ne4 3. Qg4 d5 4. Qe2 Nc6 5. d3 Nd4 6. Qd1 Nc5 7. Ne2 Bg4 8. f3 Nxe2 9. Bxe2 Bf5 10. d4 Nd7 11. g4 Bg6 12. O-O c5 13. Nc3 cxd4 14. Nxd5 e6 15. Nf4 Nxe5 16. Bb5+ Ke7 17. c3 dxc3 18. Qb3 Qb6+ 19. Kg2 cxb2 20. Bxb2 Bc2 21. Qa3+ Kd8 22. Rfd1+ Bxd1 23. Rxd1+ Kc8 24. Qb3 Bd6 25. Bd4 Qc7 26. Nxe6 fxe6 27. h3 Qf7 28. Qe3 Qf6 29. Bxa7 Bc7 30. Rc1 Rd8 31. f4 Ng6 32. Kh2 Qb2+ 33. Be2 Rxa7 34. Rc4 Ra6 35. a3 Rd2 36. Re4 Rxa3 37. Qf2 Ra6 38. Qg2 Kb8 39. Qf2 Bb6 40. Qg2 Bc5 41. g5 Rad6 42. f5 Ne7 43. f6 gxf6 44. gxf6 Ng6 45. f7 Nf8 46. Kh1 Qc2 47. Rc4 Qf5 48. Qf1 Rd1 49. Rxc5 Rxf1+ 50. Bxf1 Qxc5 51. h4 Rd7 52. h5 Qxh5+ 53. Kg1 Qc5+ 54. Kg2 Ng6 55. f8=Q+ Nxf8 56. Kg3 Rd2 57. Bg2 Qg5+ 58. Kf3 Ng6 59. Ke4 Qf4# 0-1
```

### No 12
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.03"]
[Round "?"]
[White "Komodo12"]
[Black "0GSlay0"]
[Result "0-1"]
[TimeControl "?"]
[WhiteElo "1600"]
[BlackElo "594"]
[Termination "0GSlay0 won by checkmate"]
[ECO "B02"]
[EndDate "2026.04.03"]
[Link "https://www.chess.com/game/computer/1035636165?move=0"]

1. e4 Nf6 2. e5 Ne4 3. d3 Nc5 4. b4 Ne6 5. d4 d6 6. d5 dxe5 7. c3 Nf4 8. Bxf4
exf4 9. Ne2 e5 10. dxe6 Qxd1+ 11. Kxd1 Bd6 12. Nd4 Bxe6 13. Nd2 Ke7 14. Bc4 Nc6 15. Bxe6 fxe6 16. Re1 Nxd4 17. cxd4 Bxb4 18. Rb1 a5 19. Rc1 Kd6 20. Re4 Ba3 21. Rc3 Bb4 22. Rd3 c5 23. dxc5+ Kc6 24. Rxe6+ Kxc5 25. Rd7 Rhe8 26. Rxe8 Rxe8 27. g4 fxg3 28. hxg3 Rf8 29. f4 Bxd2 30. Kxd2 Rg8 31. Kd3 Kc6 32. Re7 a4 33. Ke3 h6 34. Kd3 Rd8+ 35. Kc4 Rd2 36. f5 b5+ 37. Kb4 Rxa2 38. Re6+ Kd5 39. Re7 Rb2+ 40. Ka5 a3 41. Rf7 a2 42. Rd7+ Kc6 43. Rd1 Rb1 44. Rxb1 axb1=Q 45. g4 Qe4 46. Ka6 Qa4# 0-1
```

### No 13
```pgn
1.Nf3 Nf6

2.g3 Nc6

3.Nc3 e5

4.d4 Bb4

5.dxe5 Ne4

6.Qd3 Nc5

7.Qd2 Ne4

8.Qd3 Nc5

9.Qd2 Ne4
```

### No 14
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Advanced"]
[Black "0GSlay0"]
[Result "1/2-1/2"]
[BlackElo "594"]
[WhiteElo "1800"]
[Termination "by repetition"]
[ECO "B02"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1035685597"]

1. e4 Nf6 2. e5 Ne4 3. Bd3 d5 4. Qf3 Nc6 5. Bxe4 Nd4 6. Qf4 Ne6 7. Qf5 Nd4 8.
Qf4 Ne6 9. Qf5 Nd4 10. Qf4 1/2-1/2
```

### No 15
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Advanced"]
[Black "0GSlay0"]
[Result "1-0"]
[BlackElo "594"]
[WhiteElo "1800"]
[Termination "by checkmate"]
[ECO "A46"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1037854583"]

1. d4 Nf6 2. Nf3 Nc6 3. d5 Nb4 4. c4 e6 5. a3 Na6 6. Nc3 exd5 7. cxd5 Nc5 8. b4 Nce4 9. Nxe4 Nxe4 10. Qd4 Qe7 11. Bf4 d6 12. Rd1 Bg4 13. h3 Bh5 14. g4 Bg6 15. h4 Qd7 16. h5 Qxg4 17. hxg6 f5 18. Rxh7 Rxh7 19. gxh7 Qh5 20. Rc1 Kd8 21. Qc4 Rc8 22. Nd4 Qxh7 23. Ne6+ Ke7 24. a4 c5 25. Qb5 b6 26. Qa6 Re8 27. Bg2 cxb4 28. Bxe4 fxe4 29. Qb5 Qh1+ 30. Kd2 Qh5 31. Qc6 Kf7 32. f3 exf3 33. e4 f2 34. e5 dxe5 35. Be3 Qf5 36. Qb5 Bc5 37. a5 Bxe3+ 38. Kxe3 bxa5 39. Kd2 Re7 40. Qc4 Kg8 41. Qc8+ Re8 42. Qxe8+ Kh7 43. Rh1+ Qh5 44. Rxh5# 1-0
```

### No 16
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Advanced"]
[Black "0GSlay0"]
[Result "1-0"]
[BlackElo "594"]
[WhiteElo "1800"]
[Termination "by checkmate"]
[ECO "A46"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1037888347"]

1. d4 Nf6 2. Nf3 Nc6 3. Bf4 Nd5 4. e3 Nxf4 5. exf4 e6 6. d5 exd5 7. Nc3 Qe7+ 8. Be2 Qb4 9. O-O Qxb2 10. Nxd5 Bd6 11. Bd3 O-O 12. a4 Re8 13. Re1 Rxe1+ 14. Qxe1 Nd4 15. Qe8+ Bf8 16. Ne7+ Kh8 17. Qxf8# 1-0
```

### No 17
```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Advanced"]
[Black "0GSlay0"]
[Result "1-0"]
[BlackElo "594"]
[WhiteElo "1800"]
[Termination "by checkmate"]
[ECO "A40"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1037977823"]

1. d4 Nc6 2. Nf3 Nf6 3. d5 Nb4 4. c4 Na6 5. Bg5 Ne4 6. Nc3 Nxc3 7. bxc3 h6 8.
Be3 c6 9. Qd3 cxd5 10. cxd5 Qc7 11. h3 b5 12. Bd4 Qb7 13. e4 Nc7 14. c4 e6 15. cxb5 Bb4+ 16. Kd1 exd5 17. exd5 Qxd5 18. a3 Bc5 19. Rc1 Bxd4 20. Qxd4 Qb3+ 21. Kd2 Ne6 22. Qe4 d5 23. Qe5 Qxa3 24. Qxd5 Qb4+ 25. Rc3 Qb2+ 26. Rc2 Qb4+ 27. Kc1 Qa3+ 28. Kd1 Qa1+ 29. Rc1 Qa4+ 30. Ke1 Bb7 31. Qxb7 O-O 32. Bc4 Qa3 33. Rb1 Qc3+ 34. Kf1 Qxc4+ 35. Kg1 Rfb8 36. Qxf7+ Kxf7 37. Ne5+ Kf6 38. Nxc4 Kf5 39. Rb3 Rd8 40. Re3 Rd1+ 41. Kh2 Rxh1+ 42. Kxh1 Nd4 43. Re7 Kf6 44. Re5 Rc8 45. b6 Rxc4 46. bxa7 Rc8 47. Rd5 Ne6 48. Rd6 Ra8 49. Rd7 Nf4 50. Kg1 h5 51. g3 Nxh3+ 52. Kf1 Ng5 53. f4 Ne4 54. Kg2 g6 55. Kf3 Nc3 56. Rb7 Ke6 57. Rb3 Na4 58. Rb7 Nc3 59. Rc7
Nd5 60. Rh7 Kd6 61. f5 gxf5 62. Rxh5 Rxa7 63. Rxf5 Re7 64. Rh5 Re8 65. Rh4 Re3+ 66. Kf2 Re7 67. Rh6+ Kc5 68. Kf3 Re5 69. Ra6 Re3+ 70. Kf2 Nc7 71. Rc6+ Kxc6 72. Kxe3 Kd5 73. Ke2 Ke4 74. Ke1 Ke3 75. Kd1 Nd5 76. Kc2 Ke4 77. Kc1 Kd3 78. g4 Ne3 79. Kb2 Nc2 80. Kc1 Nd4 81. g5 Nb3+ 82. Kb2 Na5 83. g6 Nc4+ 84. Ka1 Na5 85. g7 Nc6 86. g8=Q Kd4 87. Qg5 Nb8 88. Qf4+ Kd5 89. Qxb8 Kc5 90. Qe5+ Kc4 91. Kb2 Kd3 92. Qf4 Ke2 93. Kc2 Ke1 94. Kd3 Kd1 95. Qd2# 1-0
```

### No 18

```pgn
[Event "Play vs Bot"]
[Site "Chess.com"]
[Date "2026.04.04"]
[Round "?"]
[White "Advanced"]
[Black "0GSlay0"]
[Result "1/2-1/2"]
[BlackElo "594"]
[WhiteElo "1800"]
[Termination "by repetition"]
[ECO "A50"]
[EndDate "2026.04.04"]
[Link "https://www.chess.com/game/computer/1038330141"]

1. c4 Nf6 2. d4 Nc6 3. Nf3 e6 4. a3 Ne4 5. d5 Ne7 6. Qd4 f5 7. Nc3 Nxc3 8. Qxc3
exd5 9. cxd5 Nxd5 10. Qe5+ Ne7 11. e4 fxe4 12. Qxe4 d5 13. Qe5 Kf7 14. Bd3 Kg8 15. O-O Nc6 16. Qe3 Bd6 17. Re1 Qf8 18. Qg5 Qf7 19. Bd2 Bd7 20. h3 Bxh3 21. gxh3
Qxf3 22. Qe3 Qxe3 23. Bxe3 Ne5 24. Be2 Kf7 25. Rad1 Ke6 26. f4 Ng6 27. Bd3 Kf7 28. f5 Ne5 29. Be2 Rhd8 30. Rxd5 Kf6 31. Red1 Kxf5 32. b4 Ke4 33. Bf2 a6 34. Bh4 Rf8 35. Bg5 Kf5 36. Be3 Rad8 37. Kg2 Ke4 38. Bc1 h6 39. R1d4+ Kf5 40. Bd1 Kf6 41. Bc2 Nc6 42. Rg4 Ne5 43. Bb2 Ke6 44. Rgd4 Nf3 45. Rd1 Ne1+ 46. Rxe1+ Kxd5 47. Be4+ Kc4 48. Bxg7 Rg8 49. Rc1+ Kb5 50. Bd3+ Kb6 51. Bf5 Rxg7+ 52. Bg4 h5 53. Rc4 Rdg8 54. Kf3 Rf8+ 55. Ke2 hxg4 56. Rxg4 Rh7 57. h4 Rf4 58. Rxf4 Bxf4 59. a4 Bd6 60. b5 axb5 61. axb5 Rxh4 62. Kf3 Rb4 63. Ke2 Rb3 64. Kd1 Kxb5 65. Kd2 Kc4 66. Ke1 Rb2 67. Kd1 Be5 68. Ke1 Bf6 69. Kd1 Bg5 70. Ke1 Bf6 71. Kd1 Bg5 72. Ke1 Bf6 1/2-1/2
```
