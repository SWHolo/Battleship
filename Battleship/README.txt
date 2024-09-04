INSTRUCTIONS

Source:
https://lukerissacher.com/battleships

This code solves for any configuration where the largest ship is size 4. On the source site, the largest configuration it solves for is 8x8.

The input file has the following format.

The 1st line describes the number of ship pieces in each row as a string of N numbers.
The 2nd line describes the number of ship pieces in each column as a string of N numbers.
The 3rd line describes the number of each type of ship. The numbers represent the number of 1x1, 1x2, 1x3, 1x4 ships, respectively.
The remaining lines represent the board. There are a total of 8 different 
"0" represents no info
"S" represents a 1x1 Submarine
"." represents water
"<" represents the left end of a horizontal ship
">" represents the right end of a horizontal ship
"^" represents the top end of a vertical ship
"v" represents the bottom end of a vertical ship
"M" represents a middle segment of a ship (horizontal or vertical)

Some puzzles are provided in the code.

