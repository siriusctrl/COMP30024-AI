This a project repo for game chexers which introduced by course COMP30024 Semester 1

## strategy idea summary
1. need to consider all the positions of the pieces, and sum (or mean) of their heuristic
    - Additonal to that, we can somehow implement a harmonic mean to the position of the all the piece, since harmonic mean is really sensative to variance inbetween the number.
2. heuristic for each piece is the distance for it to the
    - closest exit
    - mean of two closest exit
    - mean of four exit
3. 